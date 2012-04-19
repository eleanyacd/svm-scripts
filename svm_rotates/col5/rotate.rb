# create testing file, reference file and training file for svm
# get 1/5 of the data in original file as testing data
# get 4/5 of the data in the orginal file as training data
#
# bn82, Apr,14,2012
#

filename = ARGV[0]
partition = 5

input = File.open(filename, "r")

counts = 0

line = input.gets
while line != nil
	counts += 1
	line = input.gets
end
input.close

counts  = counts/partition

input = File.open(filename, "r")

for i in 1..partition
	tmp = File.new("ref#{i}.svm","w")
	for j in 1..counts
		line = input.gets
		tmp.syswrite(line)
	end
	if i == partition
		line = input.gets
		while line != nil
			tmp.syswrite(line)
			line = input.gets
		end
	end
	tmp.close()
end

def combine(ignore,partition)
	train = File.new("train#{ignore}.svm","w")
	for i in 1..partition
		if i != ignore
			tmp = File.open("ref#{i}.svm", "r")
			line = tmp.gets
			while line != nil
				train.syswrite(line)
				line = tmp.gets
			end
			tmp.close()
		end
	end
	train.close()
end

# build the files for training
for i in 1..partition
	combine(i,partition)
end

# build files for testing
for i in 1..partition
	test = File.new("test#{i}.svm", "w")
	tmp = File.open("ref#{i}.svm", "r")
	line = tmp.gets
	while line != nil
		row = line.split(" ")
		row[0] = '0'
		for j in 0..(row.length()-1)
			test.syswrite(row[j]+" ")
		end
		test.syswrite("\n")
		line = tmp.gets
	end
	test.close()
	tmp.close()
end
