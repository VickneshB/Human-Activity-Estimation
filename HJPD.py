import glob
import os
import math
import numpy as np
import sys
bins_arg = sys.argv

class Variables:		# Class for storage
	def __init__(self):
		self.frame_no = [] # Variable to store frame no
		self.joint_no = [] # Variable to store joint no
		self.x_coo = []	   # Variable to store x-coordinate
		self.y_coo = []	   # Variable to store y-coordinate
		self.z_coo = []	   # Variable to store z-coordinate
		self.dist_x = []	   # Variable to store distance
		self.dist_y = []
		self.dist_z = []

for loop_count in range(2):
	if loop_count == 1:
		out_file_train = open("hjpd_d1","w+") 	# Opening files to store the result of train set
	else:
		out_file_test = open("hjpd_d1.t","w+") 	# Opening files to store the result of test set
	obj = []
	j=-1
	curPath = os.getcwd() # Getting the current working directory
	if loop_count == 1:
		req_path = os.path.join(curPath,'dataset/train/*.txt')	# Running the files in the train folder in the first run
	else:
		req_path = os.path.join(curPath,'dataset/test/*.txt')   # Running the files in the test folder in the second run
	req_files = glob.glob(req_path)
	count_files = 0;
	for fi in req_files:
		f = open(fi,'r')
		fi_name = fi[len(req_path)-5:len(req_path)-2]
		content = f.readlines()	# Reading the lines of the file opened
		count = len(content)
		for i in range(count):
			split_line = content[i].split()
			if int(split_line[0]) == j+2:	 # If statement to find the change in Frame no in a single file
				obj.append(Variables())
				j = j+1		       	 # j increaments as frame no is incremented
			elif int(split_line[0]) <= j-10:
				obj = []
				j=0		 	 # j value gets reset as its a new file
				obj.append(Variables())

			obj[j].frame_no.append(float(split_line[0]))	  # Storing the frame no
			obj[j].joint_no.append(float(split_line[1]))	  # Storing the joint no
			if math.isnan(float(split_line[2])):
				obj[j].x_coo.append(0.00)		  # Storing zero as x-coordinate if the x_coo is stored as NAN
			else:
				obj[j].x_coo.append(float(split_line[2])) # Storing x-coordinate
			if math.isnan(float(split_line[3])):
				obj[j].y_coo.append(0.00)		  # Storing zero as y-coordinate if the value is stored as NAN
			else:
				obj[j].y_coo.append(float(split_line[3])) # Storing y-coordinate
			if math.isnan(float(split_line[4])):
				obj[j].z_coo.append(0.00)		  # Storing zero as z-coordinate if the value is stored as NAN
			else:
				obj[j].z_coo.append(float(split_line[4])) # Storing z-coordinate
			if float(split_line[1]) == 1:
				x1 = obj[j].x_coo[-1]	# Storing the x-coordinate of joint 1
				y1 = obj[j].y_coo[-1]	# Storing the y-coordinate of joint 1
				z1 = obj[j].z_coo[-1]	# Storing the z-coordinate of joint 1
			else:
				displacement = []
				x2 = obj[j].x_coo[-1]	# Storing the x-coordinate of current joint
				y2 = obj[j].y_coo[-1]	# Storing the y-coordinate of current joint
				z2 = obj[j].z_coo[-1]	# Storing the z-coordinate of current joint
				displacement = [x2-x1,y2-y1,z2-z1] # Finding displacement between the current joint and joint 1
				obj[j].dist_x.append(displacement[0])   # Storing the displacement
				obj[j].dist_y.append(displacement[1])
				obj[j].dist_z.append(displacement[2])
		bins = int(bins_arg[1])
		final_list = []
		for co in range(3):
			for x in range(len(obj[0].dist_x)):
				dis = []
				for p in range(len(obj)):
					if co == 0:
						dis.append(obj[p].dist_x[x]) 			# Storing the displacement of all frame in each file to one list
					elif co == 1:
						dis.append(obj[p].dist_y[x]) 			# Storing the displacement of all frame in each file to one list
					else:
						dis.append(obj[p].dist_z[x]) 			# Storing the displacement of all frame in each file to one list
				occ_dis , dis_bin_size = np.histogram(dis,bins)	# Histogram
				occ_dis = occ_dis/len(obj)				# Normalizing
				for h in range(len(occ_dis)):
					final_list.append(occ_dis[h])		# Creating an elements as [lower bound,value,upper bound]
		if loop_count == 1:
			out_file_train.write("%s " %str(fi_name[1:3]))	# Writing the values required to the hjpd_d1 file for train set
			for sd in range(len(final_list)):
				out_file_train.write("%s:%s " %(sd+1, final_list[sd]))
			out_file_train.write("\n")
		else:
			out_file_test.write("%s " %str(fi_name[1:3]))	# Writing the values required to the hjpd_d1 file for test set
			for sd in range(len(final_list)):
				out_file_test.write("%s:%s " %(sd+1, final_list[sd]))
			out_file_test.write("\n")
	if loop_count == 1:
		out_file_train.close()	# Closing file
	else:
		out_file_test.close() 	# Closing file
