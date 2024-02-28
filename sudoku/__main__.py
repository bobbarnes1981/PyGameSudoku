"""Sudoku solver"""

import argparse
import json
import logging
import solver

if __name__ == '__main__':
    loglevels = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ]

    parser = argparse.ArgumentParser(description='solve sudoku')
    parser.add_argument('file_path')
    parser.add_argument('-d',
                        '--delay',
                        type=float,
                        required=False,
                        default=1.0,
                        dest='delay')
    parser.add_argument('-l',
                        '--logging',
                        type=str,
                        required=False,
                        default='INFO',
                        dest='logging',
                        choices=loglevels)
    parser.add_argument('-e',
                        '--exit',
                        required=False,
                        default=False,
                        dest='exit',
                        action='store_true')
    args = parser.parse_args()

    loglevel = getattr(logging, args.logging, None)
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    with open(args.file_path, 'r') as f:
        content = f.read()
    data = json.loads(content)

    a = solver.App(data, args.delay, args.exit)
    a.on_execute()

    if a.is_complete():
        output_file = "solved-{0}".format(args.file_path)
        with open(output_file, 'w') as f:
            rows = a.get_solution()
            f.write('[\n')
            for r in range(9):
                f.write("    {0}".format(rows[r]))
                if r < 8:
                    f.write(',')
                f.write('\n')
            f.write(']\n')
