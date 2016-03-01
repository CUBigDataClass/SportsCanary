# TODO - Figure out how to test this

import sys  # pragma: no cover

for line in sys.stdin:  # pragma: no cover
    # remove leading and trailing whitespace
    line = line.strip()
    print '%s\t%s' % (line, 1)
