##
# compute P and R value for estimated result using
# reference file
# output P = -1 if estimated default number is 0
# output R = -1 if actaul default number is 0
##

import sys

ref_name = sys.argv[1]
res_name = sys.argv[2]
out_name = sys.argv[3]
try:
	#open two source files
	ref_file = open(ref_name,'r')
	res_file = open(res_name, 'r')

except (IndexError, IOError) as e:
        print "error in getting source file"
        exit(1)

try:
        out_file = open(out_name,'w')      
except IOError as e:
        print "Error in create a output file"
        exit(1)

# initialize vareiables
ref_default = 0
res_default = 0
catch = 0  # catch = (ref_default ^ res_default)
# R = (num of (ref_default ^ res_default))/ref_default
# P = (num of (ref_default ^ res_default))/res_default
i = 0
for ref_line in ref_file:
        res_line = res_file.readline()
        res_val = float(res_line.strip().split(' ')[0])
        ref_val = float(ref_line.strip().split(' ')[0])

        if (res_val < 0 and ref_val < 0):
                ref_default += 1
                res_default += 1
                catch += 1
        elif (res_val < 0):
                res_default += 1
        elif (ref_val < 0):
                ref_default += 1
        i += 1

sample_string = "smample_size: " + str(i) + "\n\r"

if ref_default == 0: R = -1
else: R = float(catch) / float(ref_default)

if res_default == 0: P = -1
else: P = float(catch) / float(res_default)

P_string = "P: " + str(P) + "\n\r"
R_string = "R: " + str(R) + "\n\r"
ref_string = "Actual_defaults: " + str(ref_default) + "\n\r"
res_string = "Estimated_defaults: " + str(res_default) + "\n\r"

out_file.write(P_string)
out_file.write(R_string)
out_file.write(ref_string)
out_file.write(res_string)
out_file.write(sample_string)

out_file.close()
res_file.close()
ref_file.close()


