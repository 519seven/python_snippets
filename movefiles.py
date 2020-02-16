#!/usr/bin/env python3

import argparse

'''
'''

def get_args():
    parser = argparse.ArgumentParser(
                        description="examine files in source-dir and           \
                        relocate them within the wp-uploads directory")
    parser.add_argument("-d", "--debug",
                        help="enable verbose output",
                        required=False,
                        action="store_true")
    parser.add_argument("-s", "--source-dir",
                        help="source directory for documents",
                        type=str,
                        required=True,
                        default="/home/ithelper/Site_Files")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
