# TODO - Figure out how to test this

import sys  # pragma: no cover

current_line = None  # pragma: no cover
current_count = 0  # pragma: no cover
word = None  # pragma: no cover

for line in sys.stdin:  # pragma: no cover
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper by the tab input
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_line == word:
        current_count += count
    else:
        if current_line:
            # write result to STDOUT
            print '%s\t%s' % (current_count, current_line)
        current_count = count
        current_line = word

# do not forget to output the last word if needed!
if current_line == word:  # pragma: no cover
    print '%s\t%s' % (current_line, current_count)