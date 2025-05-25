#!/usr/bin/python3
from itertools import islice
batch_processing = __import__('1-batch_processing').batch_processing

# iterate over the generator function and print only the first 6 rows
for user in islice(batch_processing(10), 6):
    print(user)