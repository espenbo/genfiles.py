#!/usr/bin/env python

import os
from datetime import datetime, time

input_dir = None 	# 'PLS1/' 	Where the inputfiles are'
output_dir = 'dir/' #None		Where to put the output files

klokke_start = time(hour=8, minute=0, second=0) 	# Don't get data from. Start
klokke_end = time(hour=16, minute=0, second=0)  	# Don't get data from. Stop
#klokke_start = None                            	# If all data should be included
#klokke_end = None                              	# If all data should be included

if input_dir and not input_dir.endswith('/'):       
    input_dir = input_dir + '/'                     # puts on / if it's not in varibel
if output_dir and not output_dir.endswith('/'):     
    output_dir = output_dir + '/'                   # puts on / if it's not in varibel
if not input_dir:                                   
    input_dir = './'                                # puts on ./ if it's not in varibel

header_included = False

class Handler(object):
    def __init__(self, name, indexes):
        self.name = name
        self.indexes = indexes
        if output_dir:
            self.f = open(output_dir + name, 'w')	# Writes the output tables to files
        else:
            self.f = open(name, 'w')

    def handle(self, values):
        store = []
        for i in self.indexes:
            store.append(values[i])
        self.f.write(';'.join(store) + '\n')

handlers = [
    Handler('AllRoomINFO_1006_1010_1054.csv', [ 0, 1, 2, 3, 4, 37, 38, 5, 6 ]),	# Makes the the new files, gets tab 0, 1, 2, 3, 4, 37, 38, 5, 6
    Handler('1006_Heatflux_In_Out_fuktighet.csv', [ 0, 7, 8, 9, 10, 5, 6 ]),	# Makes the the new files, gets tab 0, 7, 8, 9, 10, 5, 6
    Handler('1010_Heatflux_In_Out_fuktighet.csv', [ 0, 11, 12, 13, 14, 5, 6 ]),	# Makes the the new files, gets tab 0, 11, 12, 13, 14, 5, 6
    Handler('1054_Heatflux_In_Out_fuktighet.csv', [ 0, 45, 46, 47, 48, 5, 6 ]),	# Makes the the new files, gets tab
	Handler('Termisk_energi_360_01.csv', [ 0, 23, 24 ]),						# Makes the the new files, gets tab
    Handler('Termisk_energi_Radiator.csv', [ 0, 25, 57 ]),						# Makes the the new files, gets tab
    Handler('Elektrisk_energi_433_01.csv', [ 0, 26, 27 ]),						# Makes the the new files, gets tab
    Handler('Elektrisk_energi_433_09.csv', [ 0, 28, 29 ]),						# Makes the the new files, gets tab	
    Handler('Elektrisk_energi_434_01_Q15.csv', [ 0, 30, 31 ]),					# Makes the the new files, gets tab	
    Handler('Elektrisk_energi_434_01_Q01.csv', [ 0, 32, 33 ]),					# Makes the the new files, gets tab	
  
]

pls_files = [ input_dir + x for x in os.listdir(input_dir) if '.csv' in x ]     # Gets all the input files in the input directory
pls_files.sort()                                                                # Sorts input files
for f in pls_files:                                                             
    for line in open(f, 'r').readlines():                                       
        values = [ x.replace('.', ',') for x in line.split(',') ]               # replaces all the '.' with ','
        try:                                                                    
            d = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S')               # if we have year monthe daye osv we don't have a header
        except ValueError:                                                      
            if not header_included:                                             
                for h in handlers:                                              
                    h.handle(values)                                            
                header_included = True                                          # if we have other values in first line we have header. save the first.
                print 'included header'
            continue
        except TypeError:
            continue

        if (klokke_start and d.time() >= klokke_start) and (not klokke_end or d.time() < klokke_end):	# what times we are logging
            continue

        for h in handlers:
            h.handle(values)
