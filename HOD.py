import glob
import os
import math
import numpy as np


class Variables:		# Class for storage
	def __init__(self):
		self.frame_no = [] # Variable to store frame no
		self.joint_no = [] # Variable to store joint no
		self.x_coo = []	   # Variable to store x-coordinate
		self.y_coo = []    # Variable to store y-coordinate
		self.z_coo = []    # Variable to store z-coordinate
		self.theta_xy = [] # Variable to store theta in xy plane
		self.theta_yz = [] # Variable to store theta in yz plane
		self.theta_zx = [] # Variable to store theta in zx plane

for loop_count in range(2):
	if loop_count == 1:
		out_file_train = open("hod_d1","w+") 	# Opening files to store the result of train set
	else:
		out_file_test = open("hod_d1.t","w+") 	# Opening files to store the result of test set
	obj = []
	j = -1
	m = 0
	curPath = os.getcwd() # Getting the current working directory
	
	if loop_count == 1:
		req_path = os.path.join(curPath,'dataset/train/*.txt')	# Running the files in the train folder in the first run
	else:
		req_path = os.path.join(curPath,'dataset/test/*.txt')   # Running the files in the test folder in the second run
	
	req_files = glob.glob(req_path)
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
				m = 0
			elif int(split_line[0]) <= j-10: # If statement to find the change in file 
				obj = []
				j = 0		 	 # j value gets reset as its a new file
				m = 0
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

		final_list = []
		for m in range(len(obj[0].joint_no)):
			traj_x = []	# Creating a empty list called traj_x
			traj_y = []	# Creating a empty list called traj_y
			traj_z = []	# Creating a empty list called traj_z
			for i in range(len(obj)):
				traj_x.append(obj[i].x_coo[m]) # Storing the x-coordinate values of all frames for a single joint
				traj_y.append(obj[i].y_coo[m]) # Storing the y-coordinate values of all frames for a single joint
				traj_z.append(obj[i].z_coo[m]) # Storing the z-coordinate values of all frames for a single joint
			theta_xy = []	# Creating a empty list called theta_xy
			theta_yz = []	# Creating a empty list called theta_yz
			theta_zx = []	# Creating a empty list called theta_zx
			for l in range(len(traj_x)-1):
				dist_xy = pow((pow((traj_y[l+1]-traj_y[l]),2)+pow((traj_x[l+1]-traj_x[l]),2)),2)
				dist_yz = pow((pow((traj_z[l+1]-traj_z[l]),2)+pow((traj_y[l+1]-traj_y[l]),2)),2)
				dist_zx = pow((pow((traj_x[l+1]-traj_x[l]),2)+pow((traj_z[l+1]-traj_z[l]),2)),2)
				if (traj_x[l+1]-traj_x[l])==0 and (traj_y[l+1]-traj_y[l])>0:
					theta_xy.append(math.pi/2 * dist_xy)			# Storing pi radians for infinite slope
				elif (traj_x[l+1]-traj_x[l])==0 and (traj_y[l+1]-traj_y[l])<0:
					theta_xy.append(-1*math.pi/2 * dist_xy)			# Storing pi radians for negative infinite slope
				elif (traj_x[l+1]-traj_x[l])==0 and (traj_y[l+1]-traj_y[l])==0:
					theta_xy.append(0)						# Storing 0 radians for 0 slope
				elif (traj_y[l+1]-traj_y[l])==0 and (traj_z[l+1]-traj_z[l])>0:
					theta_yz.append(math.pi/2 * dist_yz)			# Storing pi radians for infinite slope
				elif (traj_y[l+1]-traj_y[l])==0 and (traj_z[l+1]-traj_z[l])<0:
					theta_yz.append(-1*math.pi/2 * dist_yz)			# Storing pi radians for negative infinite slope
				elif (traj_y[l+1]-traj_y[l])==0 and (traj_z[l+1]-traj_z[l])==0:
					theta_yz.append(0)						# Storing 0 radians for 0 slope
				elif (traj_z[l+1]-traj_z[l])==0 and (traj_x[l+1]-traj_x[l])>0:
					theta_zx.append(math.pi/2 * dist_zx)			# Storing pi radians for infinite slope
				elif (traj_z[l+1]-traj_z[l])==0 and (traj_x[l+1]-traj_x[l])<0:
					theta_zx.append(-1*math.pi/2 * dist_zx)			# Storing pi radians for negative infinite slope
				elif (traj_z[l+1]-traj_z[l])==0 and (traj_x[l+1]-traj_x[l])==0:
					theta_zx.append(0)						# Storing 0 radians for 0 slope
				else:
					slope_xy = (traj_y[l+1]-traj_y[l])/(traj_x[l+1]-traj_x[l]) 	# Calculating slope with x-axis
					slope_yz = (traj_z[l+1]-traj_z[l])/(traj_y[l+1]-traj_y[l]) 	# Calculating slope with y-axis
					slope_zx = (traj_x[l+1]-traj_x[l])/(traj_z[l+1]-traj_z[l]) 	# Calculating slope with z-axis
					if (traj_x[l+1]-traj_x[l])>0:
						theta_xy.append((np.arctan(slope_xy)) * dist_xy)				# Calculating theta_xy for positive slope
					else:
						if (traj_y[l+1]-traj_y[l])>=0:
							theta_xy.append((math.pi+np.arctan(slope_xy)) * dist_xy)	   	# Calculating theta_xy for negative slope
						else:
							theta_xy.append(((-1*math.pi)+np.arctan(slope_xy)) * dist_xy)	# Calculating theta_xy for negative slope
					if (traj_y[l+1]-traj_y[l])>0:
						theta_yz.append((np.arctan(slope_yz)) * dist_yz)				# Calculating theta_xy for positive slope
					else:
						if (traj_z[l+1]-traj_z[l])>=0:
							theta_yz.append((math.pi+np.arctan(slope_yz)) * dist_yz)		# Calculating theta_yz for negative slope
						else:
							theta_yz.append(((-1*math.pi)+np.arctan(slope_yz)) * dist_yz)	# Calculating theta_yz for negative slope
					if (traj_z[l+1]-traj_z[l])>0:
						theta_zx.append((np.arctan(slope_zx)) * dist_zx)				# Calculating theta_xy for positive slope
					else:
						if (traj_x[l+1]-traj_x[l])>=0:
							theta_zx.append((math.pi+np.arctan(slope_zx)) * dist_zx)		# Calculating theta_yz for negative slope
						else:
							theta_zx.append(((-1*math.pi)+np.arctan(slope_zx)) * dist_zx)	# Calculating theta_zx for negative slope
			final_list_joint = []
			for x in range(3):
				if x==0:
					for b in range(len(theta_xy)):
						while (theta_xy[b])>2*np.pi: 			# Checking whether the angle is between 0 and 360
							theta_xy[b] = theta_xy[b] - 2*np.pi
						while (theta_xy[b])<0:	 			# Checking whether the angle is between 0 and 360
							theta_xy[b] = theta_xy[b] + 2*np.pi
				elif x==1:
					for b in range(len(theta_yz)):
						while (theta_yz[b])>2*np.pi: 			# Checking whether the angle is between 0 and 360
							theta_yz[b] = theta_yz[b] - 2*np.pi
						while (theta_yz[b])<0:	 			# Checking whether the angle is between 0 and 360
							theta_yz[b] = theta_yz[b] + 2*np.pi				
				else:
					for b in range(len(theta_zx)):
						while (theta_zx[b])>2*np.pi: 			# Checking whether the angle is between 0 and 360
							theta_zx[b] = theta_zx[b] - 2*np.pi
						while (theta_zx[b])<0:	 			# Checking whether the angle is between 0 and 360
							theta_zx[b] = theta_zx[b] + 2*np.pi				
				count_sx = 0
				final_list_pyramid = []
				if x == 0:
					ang = theta_xy
				elif x == 1:
					ang = theta_yz
				else:
					ang = theta_zx
				for sx in range(7):
					count_sx = count_sx+1
					#print(count_sx)
					tot_bins = 8 	# Total Bins
					bins_list = []	
					occ = []
					for div in range(tot_bins+1):
						bins_list.append((2*np.pi/tot_bins)*div)		# Bins gets created like 0,45,90,135,180,225,270,315,360
					if sx==0:
						occ , bin_size = np.histogram(ang,bins_list)	# Histogram
					elif sx<3:
						sx1=sx-1;
						#print(sx1)
						occ , bin_size = np.histogram(ang[sx1*int(len(ang)/2):(sx1+1)*int(len(ang)/2)],bins_list)	# Histogram
					else:
						sx2=sx-3;
						#print(sx2)
						occ , bin_size = np.histogram(ang[sx2*int(len(ang)/4):(sx2+1)*int(len(ang)/4)],bins_list)	# Histogram
					for q1 in range(len(occ)):
						if occ[q1]>len(obj):
							print(occ[q1])
					occ = occ/len(obj)				# Normalizing
					single_list = []
					for q in range(len(occ)):
						#if occ[q]>1:
							#print(occ[q])
						final_list.append(occ[q])		# Creating an elements as [lower bound,value,upper bound]
		if loop_count == 1:
			out_file_train.write("%s " %fi_name[1:3])		# Writing the values required to the hod_d1 file for train set
			for sd in range(len(final_list)):
				out_file_train.write("%s:%s " %(sd+1,final_list[sd]))
			out_file_train.write("\n")
		else:
			out_file_test.write("%s " %fi_name[1:3])		# Writing the values required to the hod_d1 file for train set
			for sd in range(len(final_list)):
				out_file_test.write("%s:%s " %(sd+1,final_list[sd]))
			out_file_test.write("\n")
	if loop_count == 1:
		out_file_train.close()	# Closing file
	else:
		out_file_test.close() 	# Closing file
