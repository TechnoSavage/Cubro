import re

words = ''

with open('sample.txt') as source:
    for line in source:
        text = line.rstrip()
        words += text

pattern = re.findall('(.abe\S+)', words)
print pattern
