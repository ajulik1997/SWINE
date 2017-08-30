##################################################
				SWINE - README
##################################################

					ABOUT

SWINE stands for "Slit Width Influence on Neutron
	flux Estimates". It was originally designed to
	see the effect of varying slit widths on the
	flux intensity and resolution. Since then, it
	has acquired many more features, which will be
	detailed below.

Created by Alexander Liptak (Summer Student 2017)
E-Mail: Alexander.Liptak.2015@live.rhul.ac.uk
Phone: +44 (0) 7901 5959107

GitHub: https://github.com/ajulik1997/SWINE

This README was written and designed to be opened
	using Notepad++ (formatting on other viewers
	may vary)

##################################################

				MAJOR FEATURES

- Creates a heatmap of neutron intensity with
	resolution contours for the full range of
	slit 1 and slit 2 widths
- Creates a graph of intensity vs slit 2 widths
	for every resolution
- Supports saving interactive graphs and loading
	them later
- Multicore support, simulations are spread over
	available cores to reduce simulation time
- Sample instrument file is included, but usage
	of your own McStas instrument file is supported
- Slits and sample repositioning is supported
- Recompiles every instrument file automatically
	using McStas compiler and GCC
- Setting a fixed maximum penumbra is supported
- Changing angle of sample is supported
- For most options, default values are available
	for faster entry
- ANSI support for coloured output
- Does not require Python to be installed to run

##################################################

					USAGE

00	Script checks whether you are running under
	Windows, if not, it throws and error.
	PLEASE RUN THIS SCRIPT UNDER WINDOWS ONLY

01	Script checks how many cores are on the system
	MORE CORES -> FASTER RESULTS

02	Script checks whether McStas is installed in
	the default path C:\mcstas-##
	PLEASE MAKE SURE MCSTAS 2.4+ IS INSTALLED

03	You will be asked whether to load a previously
	generated interactive plot, or to run a
	simualtion to generate a new one.
	
	Press "L" to load a plot, select this option
	only if you have a ".swine" file to use,
	otherwise press "S"

04	You will be asked whether you want to use the
	default instrument or use your own
	
	For most cases, using the default instrument
	would give sufficient results. The instrument
	is based on ISIS OffSpec. To select this
	option, hit "Y".
	
	If you would like to use your own instrument
	file, please make sure that it contains the
	following:
	
	- a parameter that controls the widths of
		slit 1 and slit 2
	- a parameter that controls the position of
		slit 1, slit 2, and sample
	- a PSD monitor placed at sample position#
	
	If you would like to use this option, select
	"N"

05a	If you have selected to use the default
	instrument, the only options you will need to
	enter are the positions of slit 1, slit 2 and
	sample. If you wish to use defaults, you may
	simply press enter without any input
	
05b	If you have selected to use your own instrument
	file, you will need to drag and drop your file
	into the script and hit enter. As my script
	does not know this file, you will need to enter
	the names of the McStas parameters that
	controll the positions of slit 1, slit 2 and
	sample, widths of slit 1 and slit 2, and the
	name of your PSD monitor.
	
	After this entry is done, you will need to
	enter the actual positons of slit 1, slit 2
	and sample. Default values are not supported.
	
	Finally, the script checks whether the names
	you entered exist withing the instrument file,
	and throw an error if they don't. (This is
	mostly here just to catch out spelling errors,
	if I didn't do this check the simulation would
	fail later on an waste a lot of your time)

06	The script now starts compiling the chosen
	instrument file into C code, and then into
	binary. The script checks whether the
	compilation succeeded, if it did not, check
	if your GCC compiler is installed properly.
	
07	You will now need to enter a few more things.
	With every option, press enter without any
	input for defaults.

	- The angle of the sample. This is 1.2 degrees
		by default.
	
	- The maximum allowed penumbra. This is 80mm
		default. Even if your simulation requires a
		smaller penumbra, it is a good idea to set
		this value slightly higher for clarity of the
		plot (any penumbra values larger than the
		maximum are trimmed from the plot)
	
	- The number of steps for slit. This is 50 by
		default. For this setting, a grid of 50 by 50
		different slit positons will be generated.
		Higher numbers will create a finer, more 
		detailed plot, but will take much longer
	
	- The number of slits per simulation. This
		setting	is for the second simulation,
		and also deafults to 50. For this value,
		50 points will be drawn for every possible
		resolution line
	
	- Number of neutrons per simulation. This
		defaults to 1e6 for the first part of
		the simulation (and 1e7 for the second
		simulation, to avoid line jitter)
	
	- Plot description. This is empty by default.
		Any text here will be inserted into the
		plot title, so it can be identified when
		saved as an image

08	A working directory will be created to store
	temporary files created by McRun. These will
	be later deleted. This process will give an
	error if you do not have write perimission
	in this folder.
	MAKE SURE YOU HAVE WRITE PERMISSIONS

09	The script will now warn you that everything
	is ready and the simulation will begin.
	Press any key to start running simulations.
	This process can take over a few hours and
	it is recommended you do not use your PC
	during this time, as the simulations will
	take 100% of your CPU and are also memory
	intensive

10	After the simulations are finished, a few
	backgroung tasks are performed, such as
	collecting data for plotting, cleaning up,
	and drawing the figure. Should the figure
	fail to maximise automatically, please do
	this manually to increase the clarity of
	the plots.

11	Once the figure is opened up, you may view
	it and interact with it. When interacting with
	the plot on the right, tracing a line will
	give you the slit 2 position and intensity
	for in the bottom corner. When doing the
	same with the left plot, intensity will be
	shown but slit 1 and slit 2 widths will not
	(known bug).

12	Figure is finally saved via pickling to
	preserve the interactivity. This is still
	and experimental feature and may have bugs
	in it. The saved file will be a ".swine"
	file with its name being the timestamp
	of when it was created. You may rename this
	file should you wish to.
	
##################################################

				TROUBLESHOOTING

If you are having trouble launching the app:
- Make sure you have at least 1GB of memory
	free
- Try running the app as administrator

If you are seeing the "This script only works
on Windows" error:
- Make sure you are not running this script
	on any Linux based OS, Mini-Windows,
	portable Windows (should be supported
	but not recommended), and that your
	Windows is XP or higher (pre-XP may
	still be supported)
- If you are running the script on a virtual
	machine, try running it elsewhere

If you are seeing the "This script onlt works
on Python 3" error:
- Ever since using embedded Python, this error
	should no longer be possible. If you get it,
	please contact me

If you are seeing the "McStas is not installed
in the default directory" error:
- Please make sure that McStas is version 2.4
	or higher and in the C:\mcstas-## directory
- Please make sure you have read access to this
	directory

If you are seeing the "The selected instrument 
file does not use these parameters" error:
- You may have made a spelling mistake when
	typing the parameter names (or PSD monitor
	name)
- Make sure your McStas instrument file has
	all of the paramters necessary (described
	above)

If you are seeing the "An unknown error has 
occured while compiling to C" error:
- Maker sure McStas is in the /bin directory
	and you have access to it
- If you are using a custom instument, make
	sure that every coponent is somewhere in
	/lib before trying to compiler

If you are seeing the "An unknown error has 
occured while compiling to binary" error:
- make sure you have GCC and Strawberry Perl
	installed and accessible
- this is a GCC error with no obvous fixed,
	please contact me to resolve this issue

If you are seeing the "You do not appear to
have write permission in this folder" error:
- Make sure that you have write permissions
	in the directory where SWINE is installed
	and in the directory where your instrument
	is
- Try running as administrator

If you are seeing the "Error maximising window"
error:
- This is because you are using an unsupported
	backend, ignore the error and maximise the
	window manually should you need to
- Since upgrading to embedded Python, this
	error should no longer be possible, if
	convenient please contact me when you see
	this error

If you are seeing an empty figure:
- this may be due to various reasons, try running
	a single McStas simulation with the parameters
	you specified and see if it completes
	successfully
- if you can't find a solution, please contact me

If you get a runtime error or the application ends
unexpectedly:
- please contact me via any of the means above,
	sending me a screenshot of the error and
	resulting output