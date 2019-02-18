import csv
import os


class PharmacyRecordParser(object):
    '''An object of this class is responsible for parsing and input
    pharmacy record file.

    Parameters
    ----------
    file_path: str
        The path to the input file.
    '''

    DELIMITER = ','
    QUOTE_CHAR = '"'

    def __init__(self, file_path):
        if not os.path.isfile(file_path):
            raise Exception(
                '{} is not a valid file path'.format(file_path),
            )
        self._file_handle = open(file_path, 'rU')
        self._reader = csv.reader(
            self._file_handle,
            delimiter=PharmacyRecordParser.DELIMITER,
            quotechar=PharmacyRecordParser.QUOTE_CHAR,
        )
        _header = self._file_handle.readline()


    def gen_entries(self):
        '''This method generates parsed pharmacy record entries.
        The entries are in the following format:

        [
            prescriber_id: str,
            prescriber_last_name: str,
            prescriber_first_name: str,
            drug_name: str,
            drug_cost: str,
        ]
        '''
        for record in self._reader:
            yield record
        self.close()

    def close(self):
        '''A method that can be used to manually close the file should
        any error happen when processing the entries and we'd like to
        close the file after handling that error.
        '''
        if not self._file_handle.closed:
            self._file_handle.close()
