# create testing file and training file for svm
# get 1/5 of the data in original file as testing data
# get 4/5 of the data in the orginal file as training data
#
# bn82, Apr,14,2012
#

filename = "col0.svm"
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
	tmp = File.new("tmp#{i}","w")
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
			tmp = File.open("tmp#{i}", "r")
			line = tmp.gets
			while line != nil
				row = line.split(" ")
				if row[0] = '0'
					row[0] = '1'
				else
					row[0] = '-1'
				end
				for j in 0..(row.length()-1)
					train.syswrite(row[j]+" ")
				end
				train.syswrite("\n")
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
	tmp = File.open("tmp#{i}", "r")
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
	File.delete("tmp#{i}")
end
