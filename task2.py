#There are two files attached.
#ua_cell_codes.csv contains cell phone codes for different providers
#input.txt contains some text with phone numbers that might be in different formats.
#
#You need to create a tool that works in the following way:
#
#python find_phones.py -i input.txt -c ua_cell_codes.csv -p "Vodafone Україна" -p lifecell -o phones.csv
#
#It has to look for all the phone numbers in the input.txt, find in the text the numbers that correspond
# to the providers that were specified as command line arguments and create an output CSV file phones.csv
# with the table like
#
#phone	provider
#+380 (66) 112-51-15	Vodafone Україна
#...	...
#
#For command line arguments, use argparse module. For phone matching, use regular expressions. It may be
# not trivial to find the pattern that matches all the potential phone formats. If this is too hard,
# please handle at least the most common format and check the video links that I added in presentation
# related to regexps, they should be helpful for the task.

INPUT = "input.txt"
OUTPUT = "phones.csv"
CELL_CODES = "ua_cell_codes.csv"

####################################################################
#check out find_phones.py for solution