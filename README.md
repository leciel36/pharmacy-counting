## Overview

The code in this repo solves for the case where, given a large number of pharmacy records, we would like to generate a list of drug names ordered by total cost in descending order. If there is a tie, we would then order the results by drug name in ascending order.

To run the code, simply use the following command from the project root directory and the results will be written to the output directory.

```
$ ./run.sh
```


## Key Components

The solution can be broken down into three parts: `PharmacyRecordParser`, `DrugInfoAggregator`, and a script `pharmacy_counting.py` that is responsible for routing parsed entries to the right computer to aggregate results. Let's look at each of them in more detail.


### PharmacyRecordParser

This class is responsible for reading pharmacy records from an input file, parsing them, and putting them in the desired format so that it can be used by the rest of the system. It does so by opening a file object, and reading one line at a time, on demand, to avoid loading the entire file into memory when we don't need them yet. Each entry this parser emits takes the following format

	[
		prescriber_id,
		prescriber_last_name,
		prescriber_first_name,
		drug_name,
		drug_cost,
	]

### DrugInfoAggregator

This class is to aggregate the prescriber and cost information for the drugs that appear in the pharmacy records. Internally, it keeps a data structure that is in the following format

	{
		'drug_name_1': {
			'prescribers': set([('Chef', 'Curry'), ('King', 'James')]),
			'total_cost': 100.0,
		},
		'drug_name_2': {
			'prescribers': set([('Klay', 'Thompson')]),
			'total_cost': 57.5,
		},
	}

This dictionary allows us to compute the number of unique prescribers and aggregate the total cost on a per-drug basis.

### pharmacy_counting.py

This is where we read the records from the input file and delegate that to an `DrugInfoAggregator` instance. This file is also the entry point of our solution to the pharmacy counting problem.

## Scaling Up

Now we have a working solution for cases where we do not have too many records. We would like to apply it to problems at a larger scale. To do that, we have to address certain limitations in our system.

### Aggregator Memory Limit

In the previous section we saw that we use a dictionary to keep track of unique prescribers and total cost. As the number of pharmacy records increases, we may not be able to allocate enough memory for an aggregator.

A potential solution is to use multiple machines, each responsible for aggregating a smaller set of pharmacy records. For example, we can have 27 machines running such aggregators; the first 26 aggregators handle drug names starting with A to Z while the 27th aggregator handles everything else. We route the drug prescription records to the corresponding aggregators and get 27 output files. These files contains the sorted drug cost information, we can then combine these files by applying the merge-sort algorithm and output a single sorted list in a new file.

### Input Parsing Bottleneck

So far we have only been using a single input parser. This can become a performance bottleneck when we have a huge amount of records to process. To overcome this, we can have multiple machines, each running a parser that processes a section of the input file. These parsers look at the drag name, and route the records to the right aggregators. In this case, the parsing can be done parallelly and in turn improve the performance.