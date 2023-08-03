#!/usr/bin/env python3

import argparse
import yaml
import weeklies

def parse_args():
    parser = argparse.ArgumentParser()
    # one or more
    parser.add_argument('-f', '--filename', help="Name of weekly report")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    weekly = weeklies.Weekly()
    # weekly yaml
    w_yaml = weekly.get_yaml_obj()
    print(w_yaml)


if __name__ == "__main__":
