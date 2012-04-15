#
# generate 11 files for svm training
# col0.svm has all 11 coloumns
# col#{i}.svm has the ith colomn removoed for i > 0
# Within each file, no entry is missing
#
# bn82, April 7
#

require 'csv'

def write_into_file(flag, row, output)
	for i in 0..(row.length()-1)
		if i != flag or flag == 0
			if i < flag or flag == 0:
				j = i
			else
				j = i -1
			end
			if i == row.length()-1
				msg = "#{j}:" + row[i] + "\n"
			elsif i > 0 
				msg = "#{j}:" + row[i] + " "
			else
				if row[0] == '0' 
					msg = "-1 "
				else
					msg = "1 "
				end
			end
			output[flag].syswrite(msg)
		end
	end
end

reader = CSV.open('cs-training.csv', 'r')
row = reader.shift  # ignore the first row
output = []

for k in 0..10
	output[k] = File.new("col#{k}.svm", "w")
end

count = 0
row = reader.shift
while count < 150000
	miss = 0
	flag = 0
	for i in 0..(row.length()-1)
		if row[i] == 'NA'
			miss += 1
			if miss > 1
				break
			end
			flag = i
		end
	end
	
	if miss > 1 or (miss ==1 and flag == 0)  # more than 1 column missing or y value is missing
		row = reader.shift
		next
	end
	
	if flag > 0
		write_into_file(flag, row, output)
	else # nothing is missing. 
		# flag here indicates which file it is writing in.
		for j in 0..10
			write_into_file(j, row, output)
		end
	end
	row = reader.shift
	count += 1
	if count == 75000
		puts "Half way!"
	end
end

for i in 0..10
	output[i].close()
end

puts "Done"
