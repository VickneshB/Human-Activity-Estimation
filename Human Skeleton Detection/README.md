Project 2
Deliverable 2
Vicknesh Balabaskaran


Dependencies:
scipy
numpy
os
sys
libsvm3
gmuplot
math
glob

#coded in such a way that most of the dependencies are automatically installed and imported


PATH TO CODE:
STEP 1: Go to Home.
STEP 2: Open "T2_Vicknesh_Balabaskaran" folder
STEP 3: Open "src" folder
STEP 4: Open Main.py for Accuracy/SVM code
STEP 5: Open RAD.py for RAD code
STEP 6: Open HJPD.py for HJPD code
STEP 7: Open HOD.py for HOD code


COMPILATION INSTRUCTIONS:

Open new Terminal and type the following commands

$ cd T2_Vicknesh_Balabaskaran/

~/T2_Vicknesh_Balabaskaran$ python3 Main.py RAD no_of_bins

~/T2_Vicknesh_Balabaskaran$ python3 Main.py HJPD no_of_bins

~/T2_Vicknesh_Balabaskaran$ python3 Main.py HOD


Main.py RAD Compilation DETAILS:
1. The best value for C and gamma were found to be, C = 2 and gamma = 0.25
2. The best accuracy was found when number of bins = 15 and the accuracy was 81.25%
3. n value was set to 5 

Main.py HJPD Compilation DETAILS:
1. The best value for C and gamma were found to be, C = 1 and gamma = 0.125
2. The best accuracy was found when number of bins = 15 and the accuracy was 85.4167%
3. n value was set to 5

Main.py HOD Compilation DETAILS:
1. The best value for C and gamma were found to be, C = 1 and gamma = 0.25
2. Number of bins was set 8 as default and the accuracy was 87.5%
3. n value was set to 5

PLOTS:
1. The bins vs accuracy plot for RAD can be found in the T2_Vicknesh_Balabaskaran folder under the name of RAD Bins vs Accuracy.png
2. The bins vs accuracy plot for HJPD can be found in the T2_Vicknesh_Balabaskaran folder under the name of HJPD Bins vs Accuracy.png
3. The Gnuplot plot for RAD can be found in the T2_Vicknesh_Balabaskaran folder under the name of rad_d1.png
4. The Gnuplot plot for HJPD can be found in the T2_Vicknesh_Balabaskaran folder under the name of hjpd_d1.png
5. The Gnuplot plot for HOD can be found in the T2_Vicknesh_Balabaskaran folder under the name of hod_d1.png
