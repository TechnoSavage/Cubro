import re

words = ''

with open('sample.txt') as source:
    for line in source:
        text = line.rstrip()
        words += text

pattern = re.findall('(\S+abe.\s)', words)
print pattern
