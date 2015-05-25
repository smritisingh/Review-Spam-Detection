#-------------------------------------------------------------------------------
# Name:        test.py
# Purpose:	   test program to calculate linguistic features of sample.txt sentences
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

# count lines, sentences, and words of a text file


# set all the counters to zero

lines, blanklines, sentences, words = 0, 0, 0, 0

print '-' * 50

try:
  # use a text file you have, or google for this one ...

  filename = 'sample.txt'
  textf = open(filename, 'r')
except IOError:
  print 'Cannot open file %s for reading' % filename
  import sys
  sys.exit(0)

# reads one line at a time

for line in textf:
  print line,   # test

  lines += 1

  if line.startswith('\n'):
    blanklines += 1
  else:
    # assume that each sentence ends with . or ! or ?

    # so simply count these characters

    sentences += line.count('.') + line.count('!') + line.count('?')

    # create a list of words

    # use None to split at any whitespace regardless of length

    # so for instance double space counts as one space

    tempwords = line.split(None)
    print tempwords  # test


    # word total count

    words += len(tempwords)


textf.close()

print '-' * 50
print "Lines      : ", lines
print "Blank lines: ", blanklines
print "Sentences  : ", sentences
print "Words      : ", words

# optional console wait for keypress

from msvcrt import getch
getch()