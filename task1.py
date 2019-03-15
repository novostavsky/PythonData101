# 3/15/2019 novostavskyyv
# Task 1
# IP_ADDRESS [TIMESTAMP] DOWNLOAD_FILE_SIZE
#
# You need to compute the following:
# 1.	For each date, print the IP address of the top downloader (having the highest sum of download file sizes)
#   for the given day
# The output should look like:
# 05/Mar/2019 - 88.11.33.44
# 06/Mar/2019 - 22.77.11.99
# …
# 2.	Print the least busy hour – the hour that has the least number of requests (each log line represents
#   a separate request, you do not need to account for the file size here).

FILE_NAME = "log_data.txt"

#split given line - IP_ADDRESS [TIMESTAMP] DOWNLOAD_FILE_SIZE
#get 3 tokens (stripped/cleaned)
def split_file_row(line):
    return line.replace('[', '').replace(']', '').split(" ")

#get date/day from stripped line
def get_date(record):
    return (record[1].split(":"))[0]

#get hour from stripped line
def get_hour(record):
    return (record[1].split(":"))[1]

#get ip from stripped line
def get_ip(record):
    return record[0]

#get download size from stripped line
def get_size(record):
    return int(record[2])

#get a dictonary day+ip : total download size from the file
def get_dayip_size_dictionary(file_name):
    dayip_size_dictionary = {}
    file = open(file_name, "r")

    for line in file:
        record = split_file_row(line)
        size = get_size(record)
        dayip = "{} - {}".format(get_date(record), get_ip(record))
        dayip_size_dictionary[dayip] = dayip_size_dictionary.get(dayip,
                                                                 0) + size

    return dayip_size_dictionary

#get a dictonary day : ip of the biggest downloader from the file
def get_max_downloader_per_day(dayip_size_dictionary):
    day_ip_dictionary = {}
    day_size_dictionary = {}
    for rec in dayip_size_dictionary:
        date = rec.split(" - ")[0]
        ip = rec.split(" - ")[1]
        if date in day_size_dictionary:
            if day_size_dictionary[date] < dayip_size_dictionary[rec]:
                day_size_dictionary[date] = dayip_size_dictionary[rec]
                day_ip_dictionary[date] = ip
        else:
            day_size_dictionary[date] = dayip_size_dictionary[rec]
            day_ip_dictionary[date] = ip

    return day_ip_dictionary

#get a dictonary hour : number of requests from the file
def get_hour_reqnum_dictionary(file_name):
    hour_reqnum_dictionary = {}
    file = open(file_name, "r")

    for line in file:
        record = split_file_row(line)
        hour = get_hour(record)
        hour_reqnum_dictionary[hour] = hour_reqnum_dictionary.get(hour, 0) + 1

    return hour_reqnum_dictionary

#get the least busy hour (hour with min number of requersts disregarding download size)
def get_least_busy_hour(hour_reqnum_dictionary):
    min_hour = '00'
    min_req = hour_reqnum_dictionary[min_hour]
    # what to do if we have ">1" least busy hours?
    for rec in hour_reqnum_dictionary:
        if min_req > hour_reqnum_dictionary[rec]:
            min_hour = rec
            min_req = hour_reqnum_dictionary[rec]

    return min_hour

####################################################################
#################### let's roll#####################################
####################################################################
# 1
print("#1")
max_downloader_per_day = get_max_downloader_per_day(
    get_dayip_size_dictionary(FILE_NAME))
for rec in max_downloader_per_day:
    print("{} - {}".format(rec, max_downloader_per_day[rec]))
# 2
print("#2")
least_busy_hour = get_least_busy_hour(get_hour_reqnum_dictionary(FILE_NAME))
print(
    "The least busy hour is {} (Please note that if there's 2 or more 'least busy' hours only one is printed.)"
    .format(least_busy_hour))
