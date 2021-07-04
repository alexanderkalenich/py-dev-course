# -*- coding: utf-8 -*-

from result_calc import ProcessingResults
import argparse

parser = argparse.ArgumentParser(description='Tournament')
parser.add_argument(
    'input',
    type=str, help='Enter tournament log file'
)

parser.add_argument(
    'output',
    type=str, help='Enter tournament result file name'
)
parser.add_argument(
    'rules',
    type=int, help='Enter rules type of calculating the number of points: "0" - simplified way, '
                   '"1" - according to the requirements of the foreign market'
)
args = parser.parse_args()

processing_results = ProcessingResults()
processing_results.files_processing(args.input, args.output, args.rules)

