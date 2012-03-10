#####################################################                                    #
# Python script to convert the supplied csv files to
# svm required format for training and test files.
#
# The script takes all the paramesters for samples
# in age range 18-47.
#
# Three files are generated:
# *_train.svm is the file for training.
# *_18to47_ref.svm is the reference file to generate PR
# *_18to47_test.svm is the file used for test
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
    out_filename = raw_name + "_train" + ".svm"
    out_testref = raw_name + "_18o47_ref" + ".svm"
    out_testfile = raw_name + "_18to47_test" + ".svm"

    csv_file = open(csv_filename, 'rb')
except (IndexError, IOError) as e:
    print "csv2svm: invalid file detected..."
    exit(1)

# create new file to write svm format to
try:
    out_file = open(out_filename, 'w')
    out_ref = open(out_testref, 'w')
    out_test = open(out_testfile, 'w')
except IOError as e:
    print "csv2svm: could not create file '" + out_filename + "'"
    exit(1)

# create a new csv_reader object
csv_input = csv.reader(csv_file, delimiter=',', quotechar='|')

# remove the first line (contains field titles anyway)
line = csv_input.next()

first_line = True
j = 1
k = 150000 * 2 / 3

for line in csv_input:
    # pop off the index column (not needed)
    if len(line) <= 1:
        print "csv2svm: encountered malformed line, skipping"
        k -= 1
        continue

    info = "# " + str(line.pop(0))

    try:
        target = line.pop(0)

        # this will be blank for test data
        if target == "0": target = "-1"
        if target == "": target = "0"

        target = str(-1 * int(target)) # so that default is -1, rest are 1
    except TypeError as e:
        print "csv2svm: encountered malformed line, skipping"
        k -= 1 
        continue

    # make sure all of these numbers are ints or floats (handle N/A)
    svm_line = map(lambda x: "0.0" if x == "NA" else str(float(x)), line)

    # add in feature numbers (careful, this assumes all
    # features are present in original file)
    feature_nums = range(1, len(svm_line)+1)
    feature_nums = map(str, feature_nums)
    
    # interleave the two
    feature_list = []
    flag = 0
    for i in range(1, len(svm_line)+1):
        if i == 2:
            age = svm_line.pop(0)
            num = feature_nums.pop(0)
            if (float(age) < 18) or (float(age) > 47):
                flag = 1
                break;
            feature_list.append(num + ":" + age)
        else:
            feature_list.append(feature_nums.pop(0) + ":" + svm_line.pop(0))

    if flag == 1:
        k -= 1
        continue
    
   # format into a string
    svm_string = target + " " + " ".join(feature_list) + " " + info

    # write line to the output file
    if k > 1:
        # write line to the output file
        if not first_line:
            out_file.write("\n\r")
        out_file.write(svm_string)
        first_line = False
        j += 1
        k -= 1
    elif k == 1:
        out_file.write("\n\r")    # must not be the first line here
        out_file.write(svm_string)
        print j
        # prepare for the other output file
        first_line = True        
        j = 1
        k -= 1;
    else:
        # testInput
        test_string = str(0) + " " + " ".join(feature_list) + " " + info
        # write line to the output file
        if not first_line:
            out_test.write("\n\r")
            out_ref.write("\n\r")
        out_test.write(test_string)
        out_ref.write(svm_string)
        first_line = False
        j += 1 

print (j - 1)

# don't forget to close the output file!
out_file.close()
out_test.close()
out_ref.close()

print "done."
