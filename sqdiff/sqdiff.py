import sqlparse
import sys
import tempfile
import icdiff
from optparse import OptionParser

""" sqdiff.py

Author: Inigo Mediavilla Saiz, derived from icdiff

License: This code is usable under the same open terms as the rest of
         python.  See: http://www.python.org/psf/license/

Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006 Python Software Foundation;
All Rights Reserved

Based on Python's icdiff, it displays the diff between two SQL queries.
"""

__version__ = "0.0.1"

# Exit code constants
EXIT_CODE_SUCCESS = 0
EXIT_CODE_DIFF = 1
EXIT_CODE_ERROR = 2


def parse(fpath):
    with open(fpath) as f_in:
        return sqlparse.split("\n".join(f_in.readlines()))

def pretty_print(parsed_queries):
    return "\n".join([sqlparse.format(parsed_query, reindent=True, keyword_case='upper') for parsed_query in parsed_queries])

def write_to_temp(pretty_query, path):
    with open(path, 'w') as f:
        f.write(pretty_query)

def run_diff(options, path1, path2):
    icdiff.diff(options, *[path1, path2])

def validate_has_two_arguments(parser, args):
    if len(args) != 2:
        parser.print_help()
        sys.exit(EXIT_CODE_DIFF)

def update_parser(parser):
    parser.usage = "usage: %prog left_file right_file"
    parser.version = f"sqdiff {__version__}"
    parser.description = "Show differences between two SQL queries in a two column view."

def start():
    parser = icdiff.create_option_parser()
    update_parser(parser)
    options, args = parser.parse_args()
    icdiff.set_cols_option(options)
    validate_has_two_arguments(parser, args)
    fpath1 = args[0]
    fpath2 = args[1]

    with tempfile.NamedTemporaryFile() as tmp1, tempfile.NamedTemporaryFile() as tmp2:
        write_to_temp(pretty_print(parse(fpath1)), tmp1.name)
        write_to_temp(pretty_print(parse(fpath2)), tmp2.name)
        run_diff(options, tmp1.name, tmp2.name)

if __name__ == '__main__':
    start()
