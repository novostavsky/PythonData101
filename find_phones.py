#check out task2.py for task

import re
import csv
import argparse

#default options
INPUT = "input.txt"
OUTPUT = "phones.csv"
CELL_CODES = "ua_cell_codes.csv"


#init a list of regex to findphones in text
def get_regex_patterns():
    #just in case you need other reg_ex plz add here other ones
    return [r'0\s?\(?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}']

#read a file and return a list of all recs matching regex list
def get_phones_from_line(line):
    result = []
    all_patterns = get_regex_patterns()
    for reg_ex in all_patterns:
        result.extend(re.findall(reg_ex, line))

    return result

#remove all 'x', ' ', '-', '(', ')' and return stripped phone number
def clean_phone_pattern(line):
    return re.sub(r'[x\ \(\)\-]', '', line)

#read a file and find a dcitionary of codes and operator
def get_operator_dict_from_file(operator_file):
    operator_code_dict = {}
    with open(operator_file, 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            operator_code_dict[clean_phone_pattern(line['number_pattern'])] = line['provider']

    return operator_code_dict

#read a file and retuern a list of all phones matching regex
def get_phones_list_from_file(phone_file):
    phones_list = []
    with open(phone_file, 'r') as phone_file:
        for line in phone_file:
            phones_list.extend(get_phones_from_line(line))

    return phones_list

#check if phone belongs to operator
def is_this_operator(operator_code, phone_number):
    return clean_phone_pattern(phone_number).startswith('0{}'.format(operator_code))

#format phone number like '+380 (50) 123-45-67'
def format_phone(phone_number):
    phone_number = clean_phone_pattern(phone_number)

    return '+38{} ({}) {}-{}-{}'.format(
        phone_number[0:1],
        phone_number[1:3],
        phone_number[3:6],
        phone_number[6:8],
        phone_number[8:]
    )


#get all codes by operator name from a dict
def get_codes_list_by_operator_name(operator_name, operators_dict):
    result = []
    for record in operators_dict:
        if operators_dict[record] == operator_name:
            result.append(record)

    return result

#return result list of string containig formatted phone number and operator
#from a phones list and a single operator name
def get_phones_operator_result_list(operator_name, operators_dict, phones_list):
    result = []
    operator_codes = get_codes_list_by_operator_name(operator_name, operators_dict)
    for phone_num in phones_list:
        for code in operator_codes:
            if is_this_operator(code,phone_num):
                result.append("{}	{}".format(
                    format_phone(phone_num),
                    operator_name))

    return result

#get all results for a list of operators
def get_result_from_operators_list(operators,operators_dict,phones_list):
    result = []
    for operator_name in operators:
        result.extend(get_phones_operator_result_list(operator_name,operators_dict,phones_list))

    return result

#write resulting list into file
def write_output_to_file(out_file, result_list):
    with open(out_file, 'w', encoding='utf8') as out_file:
        for line in result_list:
            out_file.write(line + '\n')

####################################################################
#################### let's roll#####################################
####################################################################

parser = argparse.ArgumentParser(
    description='This is program that seearches for UA phone codes in a text file, '
                'and matches it with operator codes. The program output is another'
                'file with all found phones for given operators.',
)

parser.add_argument('-i', action='store', dest='input_file', default=INPUT)
parser.add_argument('-c', action='store', dest='cell_codes_file', default=CELL_CODES)
parser.add_argument('-p', action='append', dest='operators_list')
parser.add_argument('-o', action='store', dest='output_file', default=OUTPUT)
args = parser.parse_args()


phones_list = get_phones_list_from_file(args.input_file)
operators_dict = get_operator_dict_from_file(args.cell_codes_file)
operators = args.operators_list
write_output_to_file(args.output_file,
                     get_result_from_operators_list(operators, operators_dict, phones_list))
