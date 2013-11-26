#!/bin/python
# Uses Python 2.7 Libraries

# Code and current implementation of Tessera Wrapper
# Notes: Future Implementations will probably run in C++ for speed reasons
# Proof of concept for this is going to be done in python since that's what Volatility uses. 

# In order to use this tool, volatility must be in the path as 'vol'; not vol.exe or vol.py. Make a sym link to vol.py labeled vol and add it to your path to get this tool to work. 
   
import os
import re
import hashlib
from subprocess import *
import datetime

def main():
	# Start program header
	print "====================================="
	print " _____"
	print "|_   _|"
	print "  | | ___  ___ ___  ___ _ __ __ _"
	print "  | |/ _ \/ __/ __|/ _ \ '__/ _` |"
	print "  | |  __/\__ \__ \  __/ | | (_| |"
	print "  \_/\___||___/___/\___|_|  \__,_|"
	print "=====================================\n"

	case = raw_input ('\nWould you like to make a case? (y/n) : ')

	# Getting Case Information
	# Will be used to write a file with case information
	if case == 'y':
		# Name the case; similar to Autopsy
		caseName = raw_input('Enter case name: ')
		# Get the Investigators' names and put them on a list; May use this for report generation
		invGtrs = []
		name = ''
		# Stop entering investigator names by entering a single '.' on a line
		print 'Enter investigator names: '
		while (name != '.'):
			name = raw_input()
			if (name != '.'):
				invGtrs.append(name)
		current = datetime.datetime.now()
		
		# Create a directory to store case information in
		cwd = os.getcwd()
		caseDir = cwd+'/'+caseName
		# Check first to see if the directory already exists
		if (not os.path.isdir(caseDir)):
			os.mkdir(caseDir)
		print 'Case will be stored in '+caseDir+'\n'
		# Create the case info file if it doesn't already exist
		if (not os.path.isfile(caseDir+'/case_info')):
			touch (caseDir+'/case_info')
	else:
		# If no case is created, case information gets stored in CWD
		caseDir = os.getcwd()

	# Create an array to store the list of volatility commands used in the case
	commands = []

	# Get full path to image
	image = raw_input('Enter full path to image: ')

	# Check if the image exists
	exist = os.path.isfile(image)

	# If the image can't be found, ask for a new full path
	if (exist != True):
		image = raw_input('Image location DNE.\nEnter full path to image: ')
		exist = os.path.isfile(image)

	# Get the SHA-1 Hash for the image
	print '\nChecking hash of image...\n'
	sha = hashit(image)
	print 'SHA-1 hash is: '+sha+'\n'

	# Get the profile for the image
	print 'Processing to discover profile...'
	profile = profile_finder(image)

	# Add volatility command to get profile to command list
	commands.append('vol -f '+image+' imageinfo')

	######################### TO DO: determine if the profile chosen is legit

	# Build the list of supported plugins from the plugins.txt list
	plugins = pluginBuilder()

	# Choose whether or not to write results to a file
	write = raw_input('\nWrite plugin results to file? (y/n) : ')
	if (write == 'y'):
		write = True
	else:
		write = False

	# All info is loaded for case
	print '\nCase successfully built.'

	running = True

	# Now we're ready for interactive mode!
	while (running):
		entry = raw_input('Choose a plugin (Type exit to quit): ')
		if (entry in plugins):
			commands.append('vol -f '+image+' '+entry+' --profile='+profile)
			if (write):
				output = Popen(['vol', '-f', image, entry, '--profile='+profile], stdout=PIPE, stderr=PIPE)
				out, err = output.communicate()
				print out
				f = open(caseDir+'/'+entry, 'w')
				f.write(out)
				f.close()
			else: 
				call(['vol', '-f', image, entry, '--profile='+profile])
		if (entry == 'exit'):
			# Write the case info file if a case was built
			if (case == 'y'):
				caseInfo(caseName, caseDir, current, invGtrs, sha, commands, image)
			# Exit the program gracefully
			running = False
			print '\n'

##################################################
# FUNCTIONS USED IN MAIN
##################################################
# Touch Function: simple way to make a file (taken from a stack overflow example found here: http://stackoverflow.com/questions/1158076/implement-touch-using-python)
def touch(fname, times=None):
    fhandle = file(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

# Case File Write Function
# caseName = string
# invGtrs = array of investigator names
# hash = sha-1 hash of file (string)
# commands = array of commands
# image = location of image (string)
def caseInfo(caseName, caseDir, timestamp, invGtrs, hash, commands, image):
	current = timestamp.strftime("%A, %B %Y %I:%M %p")
	f = open(caseDir+'/case_info','w')
	f.write('Case Name: '+caseName+'\n')
	f.write('Case Directory: '+caseDir+'\n')
	f.write('Time of Investigation: '+current+'\n')
	f.write('Image: '+image+'\n')
	f.write('SHA-1 Image Hash: '+hash+'\n')
	f.write('-------------------------\nList of Investigators:\n')
	for name in invGtrs:
		f.write('\t'+name+'\n')
	f.write('-------------------------\nList of volatility commands used:\n')
	for command in commands:
		f.write('\t'+command+'\n')
	f.close()
		

# SHA-1 Hash creationf unction
# Gets the SHA-1 Hash for the image
# Takes in a filename
def hashit(image):
	f = open(image)
	L = 128
	m = hashlib.sha1()
	while L == 128:
        	block = f.read(128)
	        m.update(block)
        	L = len(block)
	sha = m.hexdigest()
	f.close()
	return sha

# Profile Guessing function
# uses volatility imageinfo plugin  to try to guess the profile of the image
# Returns a string with the profile name
def profile_finder(image):
	# Get the profile for the image
	profile = Popen(['vol', '-f', image, 'imageinfo'], stdout=PIPE, stderr=PIPE)
	out, err = profile.communicate()

	# Make a regex to pull out the suggested profiles
	out = re.search("Suggested Profile\(s\) : .*\n", out).group(0)
	out = out[23:-1]
	profile = out.split(', ')

	# Choose an image from either the guessed setup, or use "other" image and enter your own
	print '\nChoose an image profile: '
	i = 1
	for each in profile:
		print str(i)+'. '+each
		i+=1
	print str(i)+'. Other'

	# User makes Choice
	prof = raw_input('Choice: ')

	# Error Checking
	while (not prof.isdigit()):
		prof = raw_input('Please choose a number: ')
	# If 'other' was selected, have the user enter their own profile. This HAS to be correct; if they goof up the syntax, it's going to throw errors later
	if (int(prof) == i):
		profile = raw_input('Enter profile: ')
		return profile
	else:
		prof=int(prof)-1
		profile = profile[prof]
		return profile

def pluginBuilder():
	cwd = os.getcwd()
	f = open(cwd+'/plugins.txt')
	plugins = f.readlines()
	plugins = [line.strip() for line in plugins]
	f.close()
	return plugins

# Calling Main Function
main()
