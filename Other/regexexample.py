#!/usr/bin/python

import re

WORDS = ''

with open('sample.txt') as source:
    for line in source:
        text = line.rstrip()
        WORDS += text

PATTERN = re.findall('(\S*abe\S*)', WORDS)
print PATTERN
