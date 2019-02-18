import os


class DrugInfoAggregator(object):
    '''An object of this class takes in pharmacy records and
    compute the total cost for each drug.

    Parameters
    ----------
    file_path: str
        The path to the file where we want the result to be written.

    Members
    -------
    drugs: dict
        A dictionary that keeps the aggregated results of prescribers
        and cost. Keyed by drug name.
    '''

    PRESCRIBERS = 'prescribers'
    TOTAL_COST = 'total_cost'

    def __init__(self, file_path):
        self.file_path = file_path
        self.drugs = {}

    def ingest(self, record):
        '''Takes a pharmacy record and aggregates the results.

        Arguments
        ---------
        record:
            A records spit out by a `PharmacyRecordParser` object.
        '''
        (
            prescriber_id,
            prescriber_last_name,
            prescriber_first_name,
            drug_name,
            drug_cost,
        ) = record
        if drug_name not in self.drugs:
            self.drugs[drug_name] = {
                DrugInfoAggregator.PRESCRIBERS: set([]),
                DrugInfoAggregator.TOTAL_COST: 0.0
                }
        self.drugs[drug_name][DrugInfoAggregator.PRESCRIBERS].add(
            (prescriber_first_name, prescriber_last_name),
        )
        self.drugs[drug_name][DrugInfoAggregator.TOTAL_COST] += float(drug_cost)

    def _format_number(self, number):
        # Take care of the printout format for numbers. For numbers without
        # fraction, we don't print any thing after the decimal point.

        # Examples:
        # 
        # | number | printout |
        # |.   3.0 |        3.|
        # |    3.2 |.     3.2 |
        int_number = int(number)
        if number - int_number > 0:
            return str(number)
        return str(int_number)

    def output(self):
        '''This method writes the computed results to a file. The results
        are sorted by total cost and drug name, in decending and ascending
        order respectively.
        '''
        sorted_drug_names = sorted(
            self.drugs.keys(),
            key=lambda d: (-self.drugs[d][DrugInfoAggregator.TOTAL_COST], d),
        )

        fh = open(self.file_path, 'w')
        fh.write('drug_name,num_prescriber,total_cost\n')
        for d in sorted_drug_names:
            fh.write(
                '{},{},{}\n'.format(
                    d,
                    len(self.drugs[d][DrugInfoAggregator.PRESCRIBERS]),
                    self._format_number(
                        self.drugs[d][DrugInfoAggregator.TOTAL_COST],
                    ),
                ),
            )
        fh.close()
