######################################################                                        
# Python script to convert the supplied csv files to 
# svm required format for training and test files.
#
# This script get age as the only parameter for training
# output three files:
# *_age_only_train.svm is the file for training
# *_age_only_ref.svm is the reference file to generare PR
# *_age_only_test.svm is the file used for test
#                                                    
# bn82, 2012                                        
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
    raw_name = out_filename.pop(0)
    out_filename = raw_name + "_age_only_train" + ".svm"
    out_testref = raw_name + "_age_only_ref" + ".svm"
    out_testfile = raw_name + "_age_only_test" + ".svm"

    csv_file = open(csv_filename, 'rb')
except (IndexError, IOError) as e:
    print "csv2svm: invalid file detected..."
    exit(1)

# create new file to write svm format to
try:
    out_file = open(out_filename, 'w')
    out_ref = open(out_testref, 'w')
    out_test = open(out_testfile,'w')
except IOError as e:
    print "csv2svm: could not create file '" + out_filename + "'"
    exit(1)

# create a new csv_reader object
csv_input = csv.reader(csv_file, delimiter=',', quotechar='|')

# remove the first line (contains field titles anyway)
line = csv_input.next()

first_line = True
i = 1
j = 150000 * 2 / 3

for line in csv_input:
    # pop off the index column (not needed)
    if len(line) <= 1:
        print "csv2svm: encountered malformed line, skipping"
        j -= 1
        continue

    info = "# " + str(i)

    try:
        target = line.pop(1)
        # this will be blank for test data
        if target == "0":
            target = "-1"
        elif (target == ""): 
            target = "0"

        target = str(-1 * int(target)) # so that default is -1, rest are 1
    except TypeError as e:
        print "csv2svm: encountered malformed line, skipping"
        j -= 1
        continue

    age = str(float(line.pop(2))) # get the age
    
    
    feature = str(1) + ":" + age

    # format into a string
    svm_string = target + " " + feature + " " + info

    if j > 1:
        # write line to the output file
        if not first_line:
            out_file.write("\n\r")
        out_file.write(svm_string)
        first_line = False
        i += 1
        j -= 1
    elif j == 1:
        out_file.write("\n\r")    # must not be the first line here
        out_file.write(svm_string)
        print i
        # prepare for the other output file
        first_line = True        
        i = 1
        j -= 1;
    else:
        # testInput
        test_string = str(0) + " " + feature + " " + info
        # write line to the output file
        if not first_line:
            out_test.write("\n\r")
            out_ref.write("\n\r")
        out_test.write(test_string)
        out_ref.write(svm_string)
        first_line = False
        i += 1  

print (i-1)        

# don't forget to close the output file!
out_file.close()
out_test.close()
out_ref.close()

print "done."

