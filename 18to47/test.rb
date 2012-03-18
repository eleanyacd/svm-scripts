# Automate svm on age range 18 to 47
# Output is in 18to47_results.txt
# Each line in the file is in the following format
# "recall value, corresponidng module file name"
# Lines in the output file is sorted by increasing recall value
#
# bn82

R = []

# run svm
def f_svm(k, cval, jval, model_name, predict_file, pr_file)
	system "./svm_learn -t #{k} -c #{cval} -j #{jval} cs-training_18to47_train.svm #{model_name}"
	system "./svm_classify cs-training_18to47_test.svm #{model_name} #{predict_file}"
	system "python PR.py cs-training_18to47_ref.svm #{predict_file} #{pr_file}"
	# get recall
	file = File.open(pr_file, "r")
	line = file.gets #ignore first line
	line = file.gets
	result_R  = line.split(" ")[1].to_f
	file.close
	return result_R
end

for t in 0..4
	for p in 1..10
		cval = 10 ** (-p)
		for q in 1..10
			jval = 10 ** (-q)
			model_name = "model_#{t}_#{cval}_#{jval}"
			predict_file = "result_#{t}_#{cval}_#{jval}.txt"
			pr_file = "PR_#{t}_#{cval}_#{jval}.txt"
			result_R = f_svm(t, cval, jval, model_name, predict_file, pr_file)
			R.push([result_R,model_name])
		end
	end
end

# sort by increasing R value
R_sort = R.sort {|a, b| a[0] <=> b[0]}

outfile = File.new("18to47_results.txt", "w")
R_sort.each do |elem|
	elem.each do |thing|
		outfile.syswrite(thing)
		outfile.syswrite(" ")
	end
	outfile.syswrite("\n")
end
outfile.close()


