%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pv_svm_gen.m                                                        %
% reads in the results from the SVM classifier and generates a PV-    %
% curve from it.                                                      %
%                                                                     %
% mjz48, 2012                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all; clear all; clc;
format compact;

% prompt for results filename
filename = input('SVM Results filename: ', 's');

% read in the results
data = importdata(filename);

num_one = sum(data >= 0.5);
num_zero = sum(data <= 0.5);

% initialize variables and settings
r_min = 1;
r_max = size(data, 1);
step = 0.01;

R = zeros(size(0:step:1));
P = zeros(size(0:step:1));

% iterate through thresholds to get points on PV curve
i = 1;
for threshold = 0:step:1
    edr = abs(data(r_min:r_max) > threshold);
    
    R(i) = sum(edr .* data(r_min:r_max)) / sum(data(r_min:r_max));
    R(i) = sum(edr .* data(r_min:r_max)) / sum(edr);
    
    i = i + 1;
end

% plot the PR curve
plot(R, P);
title('PR curve for MATLAB SVM predictions');
xlabel('Recall');
ylabel('Precision');