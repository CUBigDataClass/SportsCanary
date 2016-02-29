import sys

current_line = None
current_count = 0
word = None

for line in sys.stdin:
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
if current_line == word:
    print '%s\t%s' % (current_line, current_count)