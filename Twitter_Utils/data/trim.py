#! /usr/bin/env python

import csv

# the number of tweets to add to the trimmed set.
# set at 800000 for all tweets, lower if you want
# a smaller set for faster training
LIMIT = 800000
INFILE = 'training_set.csv'

print('Reducing data. This may take a long time.')

posCount = 0
negCount = 0

outfile = open('trimmed.csv', 'w')
with open(INFILE, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[0] == '0' and negCount < LIMIT:
            negCount += 1
            outfile.write("\"{0}\",\"{1}\"\n".format(row[0], row[5]))
        elif row[0] == '4' and posCount < LIMIT:
            posCount += 1
            outfile.write("\"{0}\",\"{1}\"\n".format(row[0], row[5]))

outfile.close()

print('\nData saved to trimmed.csv\n')
print('Stats:')
print('{0} positive tags'.format(posCount))
print('{0} negative tags'.format(negCount))
