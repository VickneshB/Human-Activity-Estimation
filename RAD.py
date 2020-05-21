import glob
import os
import math
import numpy as np
import sys
bins_arg = sys.argv

class Variables:
	def __init__(self):
		self.frame_no = [] # Variable to store frame no
		self.joint_no = [] # Variable to store joint no
		self.x_coo = []	   # Variable to store x-coordinate
		self.y_coo = []	   # Variable to store y-coordinate
		self.z_coo = []	   # Variable to store z-coordinate
		self.dist = []	   # Variable to store distance
		self.angle = []	   # Variable to store angle

for loop_count in range(2):
	if loop_count == 1:
		out_file_train = open("rad_d1","w+") 	# Opening files to store the result of train set
	else:
		out_file_test = open("rad_d1.t","w+") 	# Opening files to store the result of test set
	obj = []
	j=-1
	joint_req = [1,4,8,12,16,20]
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
			if int(split_line[1]) in joint_req:
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
				if float(split_line[1]) == joint_req[0]:
					x1 = obj[j].x_coo[-1]	# Storing the x-coordinate of joint 1
					y1 = obj[j].y_coo[-1]	# Storing the y-coordinate of joint 1
					z1 = obj[j].z_coo[-1]	# Storing the z-coordinate of joint 1
				else:
					x2 = obj[j].x_coo[-1]	# Storing the x-coordinate of current joint
					y2 = obj[j].y_coo[-1]	# Storing the y-coordinate of current joint
					z2 = obj[j].z_coo[-1]	# Storing the z-coordinate of current joint
					distance = math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2)+math.pow(z2-z1,2))	# Finding the distance between current joint and joint 1
					obj[j].dist.append(float(distance))   # Storing the displacement
		for k in range(len(obj)):
			a = []
			b = []
			c = []
			for l in range(len(obj[k].joint_no)-1):
				z=l+1
				a=[]
				b=[]
				c=[]
				a.append(obj[k].x_coo[z])		# Storing x-coordinate of one extreme joint
				a.append(obj[k].y_coo[z])		# Storing y-coordinate of one extreme joint
				a.append(obj[k].z_coo[z])		# Storing z-coordinate of one extreme joint
				b.append(obj[k].x_coo[0])		# Storing x-coordinate of joint 1
				b.append(obj[k].y_coo[0])		# Storing y-coordinate of joint 1
				b.append(obj[k].z_coo[0])		# Storing z-coordinate of joint 1
				if z==1:
					c.append(obj[k].x_coo[2])	# Storing x-coordinate of adjacent extreme joint
					c.append(obj[k].y_coo[2])	# Storing y-coordinate of adjacent extreme joint
					c.append(obj[k].z_coo[2])	# Storing z-coordinate of adjacent extreme joint
				elif z==2:
					c.append(obj[k].x_coo[4])	# Storing x-coordinate of adjacent extreme joint
					c.append(obj[k].y_coo[4])	# Storing y-coordinate of adjacent extreme joint
					c.append(obj[k].z_coo[4])	# Storing z-coordinate of adjacent extreme joint
				elif z==4:
					c.append(obj[k].x_coo[5])	# Storing x-coordinate of adjacent extreme joint
					c.append(obj[k].y_coo[5])	# Storing y-coordinate of adjacent extreme joint
					c.append(obj[k].z_coo[5])	# Storing z-coordinate of adjacent extreme joint
				elif z==5:
					c.append(obj[k].x_coo[3])	# Storing x-coordinate of adjacent extreme joint
					c.append(obj[k].y_coo[3])	# Storing y-coordinate of adjacent extreme joint
					c.append(obj[k].z_coo[3])	# Storing z-coordinate of adjacent extreme joint
				else:
					c.append(obj[k].x_coo[1])	# Storing x-coordinate of adjacent extreme joint
					c.append(obj[k].y_coo[1])	# Storing y-coordinate of adjacent extreme joint
					c.append(obj[k].z_coo[1])	# Storing z-coordinate of adjacent extreme joint
				ba = [b[0]-a[0],b[1]-a[1],b[2]-a[2]]	# Finding the displacement between b and a
				bc = [b[0]-c[0],b[1]-c[1],b[2]-c[2]]	# Finding the displacement between b and c
				norm_ba = np.linalg.norm(ba)
				if norm_ba!=0:
					ba = ba/np.linalg.norm(ba)
				norm_bc = np.linalg.norm(bc)
				if norm_bc!=0:
					bc = bc/np.linalg.norm(bc)
				cosine_angle = np.clip(np.dot(ba,bc),-1.0,1.0)	# Finding corresponding cosine angle
				sine_angle = np.cross(ba,bc)
				angle1 = np.arctan2(sine_angle,cosine_angle)		# Finding the angle
				obj[k].angle.append(angle1)			# Storing the angle
		final_list = []
		bins = int(bins_arg[1])
		for x in range(len(obj[0].dist)):
			dis = []
			for p in range(len(obj)):
				dis.append(obj[p].dist[x])	# Storing the distance of all frame in each file to one list
			occ_dis , dis_bin_size = np.histogram(dis,bins)	# Histogram
			occ_dis = occ_dis/len(obj)				# Normalizing
			for h in range(len(occ_dis)):
				final_list.append(occ_dis[h])		# Creating an elements as [lower bound,value,upper bound] 
		for x in range(len(obj[0].angle)):
			ang = []
			for d in range(len(obj)):
				ang.append(obj[d].angle[x])	# Storing the angle of all frame in each file to one list
			occ_ang , ang_bin_size = np.histogram(ang,bins)	# Histogram
			occ_ang = occ_ang/len(obj)				# Normalizing
			for q in range(len(occ_ang)):
				final_list.append(occ_ang[q])		# Creating an elements as [lower bound,value,upper bound] 

		if loop_count == 1:
			out_file_train.write("%s " %str(fi_name[1:3]))	# Writing the values required to the rad_d1 file for train set
			for sd in range(len(final_list)):
				out_file_train.write("%s:%s " %(sd+1, final_list[sd]))
			out_file_train.write("\n")
		else:
			out_file_test.write("%s " %str(fi_name[1:3]))	# Writing the values required to the rad_d1 file for train set
			for sd in range(len(final_list)):
				out_file_test.write("%s:%s " %(sd+1, final_list[sd]))
			out_file_test.write("\n")
	if loop_count == 1:
		out_file_train.close()	# Closing file
	else:
		out_file_test.close() 	# Closing file
