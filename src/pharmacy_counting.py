import sys
import time
from aggregator import DrugInfoAggregator
from record_parser import PharmacyRecordParser


if __name__ == '__main__':
    computer = DrugInfoAggregator(sys.argv[2])
    parser = PharmacyRecordParser(sys.argv[1])
    for entry in parser.gen_entries():
        computer.ingest(entry)
    computer.output()
