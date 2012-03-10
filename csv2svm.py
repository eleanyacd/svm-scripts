######################################################
# csv2svm.py                                         #
# Python script to convert the supplied csv files to #
# svm required format for training and test files.   #
#                                                    #
# mjz48, 2012                                        #
######################################################

import csv
import itertools

print "=========="
print "csv2svm.py"
print "=========="

try:
    # user enters in the filename of the csv file to convert
    csv_filename = raw_input('Enter in csv filename: ')
    out_filename = csv_filename.split('.')
    out_filename = out_filename.pop(0) + ".svm"

    csv_file = open(csv_filename, 'rb')
except (IndexError, IOError) as e:
    print "csv2svm: invalid file detected..."
    exit(1)

# create new file to write svm format to
try:
    out_file = open(out_filename, 'w')
except IOError as e:
    print "csv2svm: could not create file '" + out_filename + "'"
    exit(1)

# create a new csv_reader object
csv_input = csv.reader(csv_file, delimiter=',', quotechar='|')

# remove the first line (contains field titles anyway)
line = csv_input.next()

first_line = True

for line in csv_input:
    # pop off the index column (not needed)
    if len(line) <= 1:
        print "csv2svm: encountered malformed line, skipping"
        continue

    info = "# " + str(line.pop(0))

    try:
        target = line.pop(0)

        # this will be blank for test data
        if target == "0": target = "-1"
        if target == "": target = "0"

        target = str(-1 * int(target))
    except TypeError as e:
        print "csv2svm: encountered malformed line, skipping"
        continue

    # make sure all of these numbers are ints or floats (handle N/A)
    svm_line = map(lambda x: "0.0" if x == "NA" else x, line)

    # add in feature numbers (careful, this assumes all
    # features are present in original file)
    feature_nums = range(1, len(svm_line))
    feature_nums = map(str, feature_nums)
    
    # interleave the two
    feature_list = []
    for i in range(1, len(svm_line)):
        feature_list.append(feature_nums.pop(0) + ":" + svm_line.pop(0))

    # format into a string
    svm_string = target + " " + " ".join(feature_list) + " " + info

    # write line to the output file
    if not first_line:
        out_file.write("\n\r")

    out_file.write(svm_string)
    first_line = False

# don't forget to close the output file!
out_file.close()

print "done."
