SVM Classifier for NeuralCash sample data

mjz48, 2012

Included are the executables svm_learn and svm_classify from Professor Joachims' SVM project. In order to get our data to work with it, I needed to write a python script that converts the csv file into the desired example file format. This script is called "csv2svm.py". For those of you who don't have python installed, I included two files (cs_training.svm and cs_test.svm) that I converted using the script. Lastly, I included a matlab script called "pv_svm_gen.m" that takes the results of the classification and generates the PV curve.

Run instructions:

1) To convert the csv files, open the Windows command prompt or Mac Terminal and browse to the folder containing these files. Use python to run the script by typing in "python csv2svm.py" in the terminal (of course, this requires that you first install python). The script will prompt you for the filename of the csv file to convert and output a similarly named file with the ".svm" extension instead of the ".csv" extension. If you already have the two .svm files, you can skip this step.

2) The SVM needs to be trained on the cs_training.svm data. This is done using the SVM_learn utility. Type in "svm_learn -t 1 cs_training.svm svm_classifier_model" into the terminal and run it. The -t flag specifies the kernel option. If -t is 0, that is linear model, 1 is polynomial, 2 is radial basis function, and 3 is sigmoid tanh.I think the linear model is probably too simple for this data since I couldn't get it to converge with the default step size. The polynomial model converges immediately, and the sigmoid model takes a few minutes but eventually converges. I don't know if the Sigmoid model gives us that much of an advantage. I can't be sure. (Actually if you're interested in this stuff, you could probably ask Ashutosh about it during the meeting.)

**NOTE: The model is outputted to a file called svm_classifier_model specified in the previous command.

3) Now we can classify the test data! This is done with the SVM_classify utility. Type in "svm_classify cs_test.svm svm_classifier_model results.txt". The results of the classification will be stored in a file called "results.txt".

4) If you want to generate the pv curve, you need to take the results and read them into MATLAB and do what the previous script does. I included the "pv_svm_gen.m" script that does this.