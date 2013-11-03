Tessera
=======

Front-end wrapper and system profile package for The Volatility Framework.

This tool acts as an interactive, easier-to-use wrapper around the already popular Volatility framework. Currently the tool is written in python and imports Volatility as a library. This may change to exec calls (ew, I know) in the event that the library imports for plugins becomes too heavily and/or cumbersome. 

Usage
------
Call/Run program using:i<br />
<code>./tessera</code> <br />

After booting, Tessera will ask for a case name. Takes a string for input. <br />
<code>	Enter case name: 		Case#067 - Mark Phillips<br /><br />
</code>
Tessera will then ask for a list of investigator names. Terminate the list by entering a "." <br />
<code>	Enter investigator names: 	John Doe</code><br /> 
				 	<code>Mary Sue</code><br /> 
					<code>.</code><br />	 
</code>
The next portion asked for is the location of the memory dump that is being analyzed; this location is verified by Tessera, so if Tessera can't find the image, it will ask for a new location.<br />
<code>	Enter full path to image: 	/home/john/forensics/mark.img</code><br /><br />

Tessera then takes the image and runs imageinfo on it to get a list of profiles. It automatically lists these and then asks you to choose a number. If no number is specified (you just hit enter), it will grab the first option. If you choose OTHER, it will prompt for a profile name. This must be a valid profile that Volatility knows about. <br />
<code>	Profile appears to be: \n
		1. WIN7SP0x64 \n
		2. WIN7SP1x64 \n
		3. OTHER
	Choose profile:		 	3
	Enter profile:			WIN2008R2SP0x64
</code>
Tessera will then attempt to built the case with the information that you have given it. If the case was successfully built and Tessera runs into no problems, it will inform the user of its success. Otherwise it will (hopefully) exit gracefully.<br />
<code>	Case successfully built.</code><br />

From here on out, Tessera will ask questions about what type of information you want to get from the image. List of supported options are: <br />
* Processes
* Open Files and Registry Handles
* Network Information
* Passwords and Cryptographic Keys
From here on out, Tessera will guide further down in and ask the user what type of information it's interested, and drill down to whatever specified granularity. Information gathered will be found in a directory located in the CWD where the image file sits in this format:<br />
<t> /IMAGE_LOCATION/Tessera/data_type/drill/down/output
					 		

Future Additions
----------------
1. Create log of volatility commands utilized on backend
2. Create base Tessera config file to store commonly chosen items (investigator names, etc.) 
3. Generate LaTeX-built Forensic Reports of Collected Information and Commands Issued
4. Rebuild in C++ for Speed and easier transport
