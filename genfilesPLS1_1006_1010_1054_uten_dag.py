#!/usr/bin/env python

import os
from datetime import datetime, time


input_dir = 'csv_filer/PLS1/'
output_dir = 'csv_rom_1006_og_1010_uten_dag/'

klokke_start = time(hour=8, minute=0, second=0)
klokke_end = time(hour=16, minute=0, second=0)
#klokke_start = None
#klokke_end = None

if input_dir and not input_dir.endswith('/'):
    input_dir = input_dir + '/'
if output_dir and not output_dir.endswith('/'):
    output_dir = output_dir + '/'
if not input_dir:
    input_dir = './'

header_included = False

class Handler(object):
    def __init__(self, name, indexes):
        self.name = name
        self.indexes = indexes
        if output_dir:
            self.f = open(output_dir + name, 'w')
        else:
            self.f = open(name, 'w')

    def handle(self, values):
        store = []
        for i in self.indexes:
            store.append(values[i])
        self.f.write(';'.join(store) + '\n')

handlers = [
#Rom 1006 splitting av data til små filer
    Handler('rom1006-temp.csv', [ 0, 5, 1, 7, 9, 8, 10 ]),
    Handler('rom1006-fuktighet.csv', [ 0, 2, 6 ]),
    Handler('rom1006-flux.csv', [ 0, 15, 17, 16, 18 ]),
    Handler('rom1006-u_verdi-matte.csv', [ 0, 15, 7, 9, 17, 7, 9, 16, 8, 10, 18, 8, 10 ]),
#Rom 1010 splitting av data til små filer
    Handler('rom1010-temp.csv', [ 0, 5, 3, 11, 13, 12, 14 ]),
    Handler('rom1010-fuktighet.csv', [ 0, 4, 6 ]),
    Handler('rom1010-flux.csv', [ 0, 19, 21, 20, 22 ]),
    Handler('rom1010-u_verdi-matte.csv', [ 0, 19, 11, 13, 21, 11, 13, 20, 12, 14, 22, 12, 14 ]),
#Rom 1054 splitting av data til små filer
    Handler('rom1054-temp.csv', [ 0, 5, 37, 49, 51, 50, 52 ]),
    Handler('rom1054-fuktighet.csv', [ 0, 38, 6 ]),
    Handler('rom1054-flux.csv', [ 0, 45, 47, 46, 48 ]),
    Handler('rom1054-u_verdi-matte.csv', [ 0, 45, 49, 51, 47, 49, 51, 46, 50, 52, 46, 50, 52 ]),
    
]

pls_files = [ input_dir + x for x in os.listdir(input_dir) if '.csv' in x ]
pls_files.sort()
for f in pls_files:
    for line in open(f, 'r').readlines():
        values = [ x.replace('.', ',') for x in line.split(',') ]
        try:
            d = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            if not header_included:
                for h in handlers:
                    h.handle(values)
                header_included = True
                print 'included header'
            continue
        except TypeError:
            continue

        if (klokke_start and d.time() >= klokke_start) and (not klokke_end or d.time() < klokke_end):
            continue

        for h in handlers:
            h.handle(values)
