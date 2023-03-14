import argparse
import json
import logging
import solver
from pygame.locals import *

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
    parser.add_argument('-d', '--delay', type=float, required=False, default=1.0, dest='delay')
    parser.add_argument('-l', '--logging', type=str, required=False, default='INFO', dest='logging', choices=loglevels)
    args = parser.parse_args()
    
    loglevel = getattr(logging, args.logging, None)
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    with open(args.file_path, 'r') as f:
        content = f.read()
    data = json.loads(content)
    
    a = solver.App(data, args.delay)
    a.on_execute()
