#command: ruby test.rb threshold
# bn82
#

def f_svm_param(k, cval, jval, model_name, predict_file, threshold)
	system "./svm_learn -v 0 -t #{k} -c #{cval} -j #{jval} train1.svm #{model_name}"
	system "./svm_classify -v 0 test1.svm #{model_name} #{predict_file}"
	system "Python paramPR.py #{predict_file} PR_#{k}_#{cval}_#{jval}.txt #{threshold}"
	file = File.open(predict_file, "r")
	line = file.gets
	p = line.split(" ")[1].to_f
	line = file.gets
	r  = line.split(" ")[1].to_f
	file.close
	File.delete(predict_file)
	File.delete(model_name)
	File.delete("PR_#{k}_#{cval}_#{jval}.txt")
	return [p,r]
end

def getParam(threshold)
p = -1
r = -1
model = []
k = 2
while k < 5
for c in 1..6
	for j in 1..6
		cval = 10 ** (-c)
		jval = 10 ** (-j)
		model_name = "model#{k}_#{cval}_#{jval}"
		File.new(model_name, "w")
		predict_file = "result#{k}_#{cval}_#{jval}.txt"
		result = f_svm_param(k, cval, jval, model_name, predict_file, threshold)
		if result[1] > r
			r = result[1]
			p = result[0]
			model[0] = k
			model[1] = cval
			model[2] = jval
		elsif result[1] == r and result[0] > p
			r = result[1]
			p = result[0]
			model[0] = k
			model[1] = cval
			model[2] = jval
		end
	end
end
k += 2
end
return model
end

# run svm
def f_svm(k, cval, jval, model_name, predict_file,i)
	puts "train on #{i}"
	system "./svm_learn -v 0 -t #{k} -c #{cval} -j #{jval} train#{i}.svm #{model_name}"
	puts "test on #{i}"
	system "./svm_classify -v 0 test#{i}.svm #{model_name} #{predict_file}"
end

puts"Start..."

threshold = ARGV[0]

puts threshold

param = getParam(threshold)

puts param

for i in 1..5
	k = param[0]
	cval = param[1]
	jval = param[2]
	model_name = "model#{i}"
	File.new(model_name, "w")
	predict_file = "result#{i}.txt"
	f_svm(k, cval, jval, model_name, predict_file, i)
end


system "Python PR.py #{threshold}"

puts "DONE!"
