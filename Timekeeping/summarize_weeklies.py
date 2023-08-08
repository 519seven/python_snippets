#!/usr/bin/env python3

import argparse
import yaml
import os
import sys
import weeklies.weeklies
import pprint

DEBUG = os.getenv("DEBUG", False)

def parse_args():
    parser = argparse.ArgumentParser()
    # one or more
    parser.add_argument('-f',
                        '--filename',
                        required=True,
                        help="Name of weekly report")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print(f"Path {args.filename} does not exist")
        sys.exit(1)
    return args


def yaml_as_python(val):
    """Convert YAML to dict"""

    try:
        return yaml.load_all(val, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        return exc


def get_list(s_file):
    with open(s_file, "r", encoding="utf-8") as input_file:
        results = yaml_as_python(input_file)
        return list(results)


def main():
    args = parse_args()

    print(f"Debug: {DEBUG}")
    weekly = weeklies.weeklies.Weekly(args.filename, DEBUG)
    # get a list of days from YAML
    weekly.docs = get_list(weekly.source_file)
    weekly.data_parser()
    return 0

if __name__ == "__main__":
    sys.exit(main())