#!/usr/bin/env python3

"""
This script plots data for a given patient
"""

import argparse
import sys
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def main(args):
    with beam.Pipeline() as p:
        patient_data = (
                p
                | beam.io.ReadFromText(args.input_file, skip_header_lines=1)
                | beam.ParDo(

        )
        )

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_folder', default='output')
    sys.exit(main(parser.parse_args()))
