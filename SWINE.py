############################################################
#
#	Written by Alexander Liptak (Summer Student 2017)
#	Date: August 2017
#	E-Mail: Alexander.Liptak.2015@live.rhul.ac.uk
#	Phone: +44 7901 595107
#
#	Designed to be run on Python 3
#	and tested with McStas 2.4
#
#	IT IS RECOMMENDED TO RUN THIS SCRIPT USING SHELL
#
############################################################

import os
import sys
import multiprocessing
import numpy as np
from sympy import *
import matplotlib.pyplot as plt
from subprocess import Popen, CREATE_NEW_CONSOLE, check_call
from datetime import datetime
import time
from glob import glob
from colorama import init, Fore
import shutil
import pickle

############################################################
# Introdction
############################################################

print("==================================================")
print("                      SWINE                       ")
print("==================================================")
print("  Slit Width Influence on Neutron flux Estimates  ")
print("==================================================")

############################################################
# Load ANSI support for coloured text
#
# Colour meaning:
#	RED - Error
#	YELLOW - Warning
#	GREEN - Success
#	MAGENTA - Input
############################################################

init(autoreset=True)

############################################################
# Make sure I am running in Windows
############################################################

print("Checking OS...")
if os.name != 'nt':
	print(Fore.RED + "This script only works on Windows!")
	print(Fore.RED + "Exitting...")
	sys.exit()
print(Fore.GREEN + "You are running a compaible Windows-based OS")

############################################################
# Make sure I am running in Python 3 or higher
# (no longer necessary as running embedded python)
############################################################

print("Checking Python version...")
if sys.version_info[0] < 3:
	print(Fore.RED + "This script only works on Python 3!")
	print(Fore.RED + "Exitting...")
	sys.exit()
print(Fore.GREEN + "Embedded Python version is compatible")

############################################################
# Checking the amount of cores system has for running
#	multiple simulations without slowing each sim down
############################################################

print("Checking system...")
cores = multiprocessing.cpu_count()
print(Fore.GREEN + "Found [" + str(cores) + "] cores!")

############################################################
# Chekc if mcstas, mcrun and mclib are in their default dir
############################################################

print("Checking McStas...")
try:
	mcrun = glob('C:\\mcstas*\\bin\\mcrun.bat')[0]
	mcstas = glob('C:\\mcstas*\\bin\\mcstas.exe')[0]
	mclib = glob(glob('C:\\mcstas*\\lib')[0]+'\\*')
	gcc =  glob('C:\\mcstas-*\\miniconda*\\Library\\mingw-w64\\bin\\')[0]
except:
	print("McStas is not installed in the default directory!")
	print(Fore.RED + "Exitting...")
	sys.exit()
print(Fore.GREEN + "Using version: " + mcrun.split('\\')[1])

############################################################
# Ask user whether to retrieve interactive plot or run sim
# Included end='' in print statement as a hack for colorama
#	incompatibility with non-ANSI input()
#	GitHub colorama issue #103
############################################################

print("==================================================")
while True:
	print(Fore.MAGENTA + "Would like to load a previous plot (L) or run a simulation (S)? [L/S] ", end='')
	load_or_sim = str(input()).upper()
	if load_or_sim == 'L' or load_or_sim == 'S':
		if load_or_sim == 'L':
			unpickle = True
		if load_or_sim == 'S':
			unpickle = False
		break
	else: 
		print(Fore.YELLOW + "That is not a recongnised option!")

############################################################
# If user decided to load previous plot, begin unpickling
# For some reason, all unpickled figures default to tkagg
#	so used appropriate maximise commands
# Shows plot and exits
############################################################

if unpickle == True:
	print(Fore.MAGENTA + "Drag and drop your .swine file here: ", end='')
	pickledplot = input()
	print("Loading plot...")
	fig = pickle.load(open(pickledplot, 'rb'))
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
	plt.show()
	print("Exitting...")
	sys.exit()

############################################################
# Ask user whether to use the default OffSpec-based .instr
#	file for this simulation or use their own
############################################################

print("==================================================")
while True:
	print(Fore.MAGENTA + "Would like to run from deafult (OffSpec-based) instrument file? [Y/N] ", end='')
	default_instr = str(input()).upper()
	if default_instr == 'Y' or default_instr == 'N':
		break
	else: 
		print(Fore.YELLOW + "That is not a recongnised option!")

############################################################
# If user selected using the default instrument file, slit
#	and sample parameter names are set automatically, and
#	the user is given choice whether to use the default
#	positions or set their own. Then the values for slit and
#	sample postions are entered, or defaults are used.
# If the user wants to use their own instrument file, the
#	parameters that control McStas slit and sample widths
#	and positions need to be entered manually, as do their
#	values.
############################################################

cwd = os.getcwd()
if default_instr == "Y":
	instr = cwd+'\\resources\\default.instr'
	
	s1w_param = 'slit1_width'
	s2w_param = 'slit2_width'
	s1p_param = 'slit1_pos'
	s2p_param = 'slit2_pos'
	sap_param = 'sample_pos'
	out_param = 'sample_psd'
	
	print("Enter slit and sample positons after bender (leave empty for default):")
	print(Fore.MAGENTA + "McStas position of slit 1 [8.58](m): ", end='')
	slit1Pos = float(input() or (8.58))
	print(Fore.MAGENTA + "McStas position of slit 2 [13.63](m): ", end='')
	slit2Pos = float(input() or (13.63))
	print(Fore.MAGENTA + "McStas position of sample [14.03](m): ", end='')
	sampPos	= float(input() or (14.03))

if default_instr == "N":
	print("Make sure your .instr file is formatted as set out in the README!")
	print(Fore.MAGENTA + "Drag and drop your .instr file here: ", end='')
	instr = input()
	
	print(Fore.MAGENTA + "Enter McStas parameter that controls slit 1 width: ", end='')
	s1w_param = str(input())
	print(Fore.MAGENTA + "Enter McStas parameter that controls slit 2 width: ", end='')
	s2w_param = str(input())
	print(Fore.MAGENTA + "Enter McStas parameter that controls slit 1 position: ", end='')
	s1p_param = str(input())
	print(Fore.MAGENTA + "Enter McStas parameter that controls slit 2 position: ", end='')
	s2p_param = str(input())
	print(Fore.MAGENTA + "Enter McStas parameter that controls sample position: ", end='')
	sap_param = str(input())
	print(Fore.MAGENTA + "Enter McStas component name of your PSD_monitor: ", end='')
	out_param = str(input())
	
	while True:
		try:
			print("Enter slit and sample positons for your McStas instrument:")
			print(Fore.MAGENTA + "McStas position of slit 1 (m): ", end='')
			slit1Pos = float(input())
			print(Fore.MAGENTA + "McStas position of slit 2 (m): ", end='')
			slit2Pos = float(input())
			print(Fore.MAGENTA + "McStas position of sample (m): ", end='')
			sampPos	= float(input())
			break
		except:
			print(Fore.YELLOW + "Blank and non-numeric input is not allowed, try again!")

############################################################
# Only if using custom instrument file, checks whether
#	specified parameters that were entered actually exist
#	in the file
############################################################

if default_instr == "N":
	if (s1w_param not in open(instr).read() or s1w_param == ''
	 or s2w_param not in open(instr).read() or s2w_param == ''
	 or s1p_param not in open(instr).read() or s1p_param == ''
	 or s2p_param not in open(instr).read() or s2p_param == ''
	 or sap_param not in open(instr).read() or sap_param == ''
	 or out_param not in open(instr).read() or out_param == ''):
		print(Fore.RED + "The selected instrument file does not use these parameters!")
		print(Fore.RED + "Edit your instrument file or re-run this script and try again.")
		print(Fore.RED + "Exitting...")
		sys.exit()

############################################################
# Compile instrument into C using McStas
# Requred to CD to the folder containing the instrument file
#	to get around McStas GitHub Issue #532
############################################################

print("==================================================")
print("Compiling instrument file into C...")
INSTRtoC = mcstas, '-I', ' -I '.join(mclib), '-t', os.path.split(instr)[1]
try:
	os.chdir(os.path.split(instr)[0])
	check_call(' '.join(INSTRtoC), creationflags=CREATE_NEW_CONSOLE)
	os.chdir(cwd)
except:
	print(Fore.RED + "An unknown error has occured while compiling to C...")
	print(Fore.RED + "Exitting...")
	sys.exit()
print(Fore.GREEN + "Compiled to C successfully!")

############################################################
# Compile C code into binary
############################################################

print("Compiling C file into binary...")
CtoEXE = 'gcc', '-o', os.path.splitext(instr)[0]+'.exe', os.path.splitext(instr)[0]+'.c', '-g', '-O2','-lm'

try:
	CtoEXEbatch = open('gcc_temp.bat', 'w')
	
	CtoEXEbatch.write("setlocal\n")
	CtoEXEbatch.write("set PATH="+gcc+"\n")
	CtoEXEbatch.write(' '.join(CtoEXE))
	
	CtoEXEbatch.close()
except:
	print(Fore.RED + "You do not appear to have write permission in this folder!")
	print(Fore.RED + "Exitting...")
	sys.exit()
	
try:
	check_call('gcc_temp.bat', creationflags=CREATE_NEW_CONSOLE)
except:
	print(Fore.RED + "An unknown error has occured while compiling to binary...")
	print(Fore.RED + "Exitting...")
	sys.exit()

os.remove('gcc_temp.bat')
print(Fore.GREEN + "Compiled to binary successfully!")

############################################################
# Data collection that supports default values
############################################################

print("==================================================")
print("Please input the required values or press the return key for defaults.")
print("Default values are in square brackets and required units are in parentheses.")

print(Fore.MAGENTA + "Angle of sample [1.2](degrees): ", end='')
angle = np.deg2rad(float(input() or (1.2)))
print(Fore.MAGENTA + "Maximum allowed penumbra [80](mm): ", end='')
maxPenumbra = float(input() or (80))
print(Fore.MAGENTA + "Number of steps per slit (higer-finer, lower-faster) [50]: ", end='')
steps1 = int(input() or (50))
print(Fore.MAGENTA + "Number of steps per resolution (higer-finer, lower-faster) [50]: ", end='')
steps2 = int(input() or (50))
print(Fore.MAGENTA + "No of neutrons per simulation [1000000]: ", end='')
neutrons = int(input() or (1000000))
print(Fore.MAGENTA + "Plot description (appended to graph title): ", end='')
description = str(input() or (''))

############################################################
# Define necessary values, variables  and equations that
#	will have to be solved later
# Make sure all distances are in mm
# penumbra is the sympy equation for calulcating the
#	penumbra of the footprint with respect to slit widths
#	and their separation, as well as the angle of the
#	sample
# dQQ is a sympy formula that calculates the resolution
#	from slit widths, their positions, and the angle of
#	the sample
############################################################

s1s2Sep = (slit2Pos-slit1Pos)*1000
s2SampSep = (sampPos-slit2Pos)*1000
s1 = symbols('s1')
s2 = symbols('s2')
penumbra = (2*((((s1s2Sep+s2SampSep)*(s1+s2))/(2*s1s2Sep))-(s1/2)))/(sin(angle))
dQQ = ((atan((s1+s2)/(s1s2Sep)))/(2*tan(angle)))*100

############################################################
# Set both slit minima to 0, solve penumbra equation for
#	maximum allowed slit opening
############################################################

slit1min = 0.0
slit2min = 0.0

slit1max = float(next(iter(solveset(Eq(penumbra.subs(s2,0),maxPenumbra),s1))))
slit2max = float(next(iter(solveset(Eq(penumbra.subs(s1,0),maxPenumbra),s2))))

############################################################
# Create and fill array with all the slit width values
#	that will be tested (Simulation 1 only)
############################################################

slit1vals = np.array([])
slit2vals = np.array([])

for i in range(steps1+1):
	slit1vals = np.append(slit1vals, slit1min+(i*((slit1max - slit1min)/steps1)))
	slit2vals = np.append(slit2vals, slit2min+(i*((slit2max - slit2min)/steps1)))

############################################################
# Create two arrays, correctly sized and filled with
#	zeros
# Later, the values that satisfy the constraints will be
#	tested and their results will be added to this array
#	while those values that do not satisfy the constrains
#	will remain as zero
############################################################

intensity = np.zeros((steps1+1,steps1+1))
quality = np.zeros((steps1+1,steps1+1))

############################################################
# Create output directory, if there is some error, closes
############################################################

swinedir = 'SWINE{:[%Y-%m-%d][%H-%M-%S]}'.format(datetime.now())
try:
	os.mkdir(swinedir)
except:
	print(Fore.RED + "You do not appear to have write permission in this folder!")
	print(Fore.RED + "Exitting...")
	sys.exit()

############################################################
# Everything ready to start, give user final instructions
############################################################

print("==================================================")
print("The script is now ready to run!")
print("Depending on your settings, this may take over a few hours to complete.")
print("It is recommended to not use the computer while this script is running.")
print(Fore.MAGENTA + "Press any key to continue...", end='')
input()
print("==================================================")

############################################################
# Simulation 1
# Create an empty list that will contain every call to be
#	made to McStas
# Create an emty list that will contain debugging
#	information
# Solve the penumbra and resolution equations for the
#	current combination of slits, and if satisfies the
#	constraints, call and debug info are appended to their
#	respective lists
# Zero slit width simulations are also skipped due to
#	an issue with the definition of a slit in McStas
#	(GitHub Issue #522 in McCode)
############################################################

calls1 = []
debug1 = []

for index1, item1 in enumerate(slit1vals):
	for index2, item2 in enumerate(slit2vals):
		
		penumbraCurrent = penumbra.subs([(s1,item1),(s2,item2)])
		qualityCurrent = dQQ.subs([(s1,item1),(s2,item2)])
		quality[index1,index2] = qualityCurrent
	
		if ((penumbraCurrent <= maxPenumbra) \
		and (item1 != 0.0 and item2 != 0.0)):
		
			calls1.append([mcrun, instr,
			'-d', swinedir+'/A['+str(index1)+']['+str(index2)+']',
			'-n', str(neutrons),
			s1p_param+'='+str(slit1Pos), s2p_param+'='+str(slit2Pos),
			sap_param+'='+str(sampPos),
			s1w_param+'='+str(item1/1000), s2w_param+'='+str(item2/1000)])
			
			debug1.append([item1, item2, penumbraCurrent, qualityCurrent])
			
############################################################
# Simulation 2
# Like previously, two lists are created that will contain
#	the calls and debugging information
# The values for minimum and maximum resolution are obtained
#	by taking the ceiling and floor functions of the minimum
#	and maximum possible resolutions from the previous
#	simulations, plus or minus one (respectively)
# For every resolution to be found, the range of s2 values
#	that satisfy the maximum penumbra are found, as well as
#	the correcponding s1 values. A check is made if either
#	of these values are not negative, and a call list is
#	generated, along with debugging information
# The final data matrix should be of the format:
#	[resolution, [slit 2 widths], [intensities]]
#	where the data for the intensity sublist will be
#	collected after the simulations complete
############################################################

calls2 = []
debug2 = []

minQ = int(np.ceil(np.amin(quality)))+1
maxQ = int(np.floor(np.amax(quality)))-1

data2 = []

for index, item in enumerate(list(range(minQ, maxQ+1))):
	data2.append([])
	data2[index].append(item)

	s2range =  np.delete(np.linspace(0, float(next(iter(solveset(Eq(solveset(Eq(penumbra,maxPenumbra), symbol=s1),solveset(Eq(dQQ,item), symbol=s1)),symbol=s2)))), steps2), 0)
	s1range = [float(next(iter(solveset(Eq(dQQ,item), symbol=s1).subs(s2, item)))) for element in s2range]

	templist = []
	
	for index2, item2 in enumerate(s2range):
		if float(s2range[index2]) > 0 and float(s1range[index2]) > 0:
			
			calls2.append([mcrun, instr,
			'-d', swinedir+'/B['+str(item)+']['+str(item2)+']',
			'-n', str(neutrons*10),
			s1p_param+'='+str(slit1Pos), s2p_param+'='+str(slit2Pos),
			sap_param+'='+str(sampPos),
			s1w_param+'='+str(s1range[index2]/1000), s2w_param+'='+str(s2range[index2]/1000)])
			
			debug2.append([item, s1range[index2], item2])
			
			templist.append(s2range[index2])
	
	data2[index].append(templist)
	data2[index].append([])
	
############################################################
# Simulation 1
# Runs as many simulations at a time as there are cores
# Keeps count of how manu calls have been made so that
#	we run them all and none are missed
# Print debugging information
############################################################

calls1_done = 0

while calls1_done < len(calls1):
	running_calls = []
	for core in range(0, cores):	
		if calls1_done < len(calls1):

			print('| Sim1',
			'|',format(int((calls1_done+1)/len(calls1)*100), '03.0f')+'%',
			'| Core:',str(core),
			'| S1W:',format(debug1[calls1_done][0], '03.2f'),
			'| S2W:',format(debug1[calls1_done][1], '03.2f'),
			'| PU:',format(float(debug1[calls1_done][2]), '03.2f'),
			'| Res:',format(float(debug1[calls1_done][3]), '03.2f'), '|')
			
			sim = Popen(calls1[calls1_done], creationflags=CREATE_NEW_CONSOLE)
			running_calls.append(sim)
			calls1_done = calls1_done + 1
			
	print("--------------------------------------------------")	
	
	for call in running_calls:
		sim.wait()

	time.sleep(cores)

############################################################
# Same thing as above but for second set of simulations
############################################################

calls2_done = 0

while calls2_done < len(calls2):
	running_calls = []
	for core in range(0, cores):	
		if calls2_done < len(calls2):

			print('| Sim2',
			'|',format(int((calls2_done+1)/len(calls2)*100), '03.0f')+'%',
			'| Core:',str(core),
			'| Res:',str(int(debug2[calls2_done][0])),
			'| S1W:',format(debug2[calls2_done][1], '03.2f'),
			'| S2W:',format(debug2[calls2_done][2], '03.2f'), '|')
			
			sim = Popen(calls2[calls2_done], creationflags=CREATE_NEW_CONSOLE)
			running_calls.append(sim)
			calls2_done = calls2_done + 1
			
	print("--------------------------------------------------")	

	for call in running_calls:
		sim.wait()

	time.sleep(cores)

############################################################
# Reads the specified McRun output file from every subfolder
# If the subfolder is labeled A (sim 1), then the intensity
#	scraped from this file is used to update the intensity
#	matrix
# If the subfolder is labeled B (sim 2), then the value is
#	appended to the correct sublist in the data matrix
############################################################		

print("Collecting data...")
os.chdir(swinedir)
for	folder in os.listdir():
	dim1 = str(folder).split('][')[0][2:]
	dim2 = str(folder).split('][')[1][:-1]
	with open(str(folder)+'/'+str(out_param)+'.dat', 'r') as file:
		for line in file:
			if 'values:' in line:
				if str(folder)[0] == 'A':
					intensity[int(dim1), int(dim2)] = line.split(' ')[2]
				if str(folder)[0] == 'B':
					for item in data2:
						if int(dim1) == item[0]:
							item[2].append(line.split(' ')[2])
				break	

############################################################
# Deleted the swinedir folder to save space, all needed data
#	has been collected already
############################################################

print("Cleaning up...")
os.chdir(cwd)
shutil.rmtree(swinedir)
os.remove(os.path.basename(instr))

############################################################
# Cretes a blank figure that will hold two subplots
# Subplot 1 is created, and on it is plotted the heatmap
#	generated from the intensity matrix. A colourbar for
#	this data is also generated. Resolution contour lines
#	are then obtained from the resolution matrix and plotted
#	on the same subplot. The title and axis labels are made
#	and the tick values are regenerated.
# Subplot 2 is created, and the data matrix is looped over
#	so that a line for every resolution is drawn.
#	The legend, title and axis lables are also drawn.
############################################################				

print("Plotting data...")
fig = plt.figure()

plt.subplot(121)
heatmap = plt.imshow(intensity, cmap='hot', interpolation='nearest')
contour = plt.contour(quality, antialiased=True)
plt.clabel(contour, inline=1, fontsize=10)
plt.colorbar(heatmap)
plt.title('Neutron intensity at varying slit widths | '+description)
plt.xlabel('Slit 2 width (mm)')
plt.ylabel('Slit 1 width (mm)')
plt.xticks(np.linspace(0, len(slit2vals)-1, num=6), np.linspace(round(slit2min, 2), round(slit2max, 2), num=6))
plt.yticks(np.linspace(0, len(slit1vals)-1, num=6), np.linspace(round(slit1min, 2), round(slit1max, 2), num=6))


plt.subplot(122)
for item in data2:
	plt.plot(item[1], item[2], '-', label='dQ/Q = '+str(item[0]))
plt.legend()
plt.title('Intensity against slit 2 width at constant resolution | '+description)
plt.xlabel('Slit 2 width (mm)')
plt.ylabel('Intensity')


############################################################
# The window needs to be maximised as the default view
#	makes reading the plots impossible.
# Almost all the time, pyplot will use the qt4agg / qt5agg
#	backend, but just in case another backend needs to be
#	used, maximise commands are included for three most
#	used backends
############################################################

if (str(plt.get_backend()).lower() == 'qt4agg'
 or str(plt.get_backend()).lower() == 'qt5agg'):
	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()
elif str(plt.get_backend()).lower() == 'tkagg':
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
elif str(plt.get_backend()).lower() == 'wxagg':
	mng = plt.get_current_fig_manager()
	mng.frame.Maximize(True)
else:
	print(Fore.YELLOW + "Error maximising window, please maximise windows manually!")

############################################################
# Experimental pickle support means it is possible to store
#	entire plot in a file and recover it later, intreactive
# Also ahow figure and exit
############################################################

print("Saving figure...")
pickle.dump(fig, open(swinedir+'.swine', 'wb'))

print("Opening plot...")
plt.show()

print("Exitting...")
sys.exit()