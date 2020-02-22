import os
os.system("sudo apt install gnuplot")
os.system("sudo apt install python3-scipy")
os.system("sudo apt install libsvm3")
import sys
curPath = os.getcwd()
sys.path.insert(0,curPath+'/libsvm-3.23/tools')
import grid
from grid import *
sys.path.insert(0,curPath+'/libsvm-3.23/python')
import svmutil
import scipy
from svmutil import *
sys.path.insert(0,curPath)
import numpy as np

file_arg = sys.argv


rep = file_arg[1]
if rep != 'HOD':
	bins = file_arg[2]
else:
	print("Taking Default number of bins = 8")


if rep == 'RAD':
	os.system('python3 RAD.py %s' %bins)
	dataset_train = curPath+'/rad_d1'
	dataset_test = curPath+'/rad_d1.t'
elif rep == 'HJPD':
	os.system('python3 HJPD.py %s' %bins)
	dataset_train = curPath+'/hjpd_d1'
	dataset_test = curPath+'/hjpd_d1.t'
else:
	os.system('python3 HOD.py')
	dataset_train = curPath+'/hod_d1'
	dataset_test = curPath+'/hod_d1.t'

svmoptions = '-s 0 -t 2'
y,x = svm_read_problem(dataset_train)
svmtrain_path = curPath+'/libsvm-3.23/svm-train'
gnuplot_path = '/usr/bin/gnuplot'
n = 5
options = ('-log2c %d,%d,%d -log2g %d,%d,%d -svmtrain %s %s -gnuplot %s -v %s' %(-5,5,1,-5,5,1,svmtrain_path,svmoptions,gnuplot_path,n))
rate, param = find_parameters(dataset_train,options)	
svmoptions = '-s 0 -t 2 -c %f -g %f' %(param['c'],param['g'])
m = svm_train(y,x,svmoptions)
svm_save_model('Model',m)

y,x = svm_read_problem(dataset_test)
n = svm_load_model('Model')
p_label, p_acc, p_vals = svm_predict(y,x,m)
ACC, MS, SCC = evaluations(y,p_label)
si =(6,6)
mat = np.zeros(si)
vec = [8,10,12,13,15,16]
for s in range(len(y)):
	for i in range(len(vec)):
		if y[s] == vec[i]:
			for j in range(len(vec)):
				if p_label[s] == vec[j]:
					mat[i][j] = mat[i][j]+1
print(mat)
