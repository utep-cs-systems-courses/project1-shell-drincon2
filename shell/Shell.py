#!/usr/bin/env python3

# Libraries 
import os
import sys
import re
import gc

# Shell process
def  shell():
   line = {}
   status = None 
   while status:
   	print("$ ")
   	# Read
   	line = sh_reader()
   	# Parse
   	args = sh_parser(line)
   	# Execute
   	status = sh_exec(args)
   	# Free space 
   	gc.collect()
   	
# Reader (this will read the commands written in the shell)
def sh_reader():
   # Line dictionary
   line = sys.argv
   
   return line    	
   
# Parser (this will tokenize the commands from the shell)
def sh_parser(line): 
   #Token dictionary 
   tokens = {}
   
   for arg in line:
      tokens[arg] = re.split(" ", arg)
      
   return token
   
# Execute built_in commands (cd, exit)
def sh_exec(args):
   # Use loop to determine whether execute a shell or built-in command 

# Pipes
def sh_pipes():

# Execute commands
def sh_exec_nativ(args):
   cpid = os.fork()
   # Fork failed
   if cpid < 0:
      os.write(2, ("Fork failed, returning %d\n" % cpid).encode())
      sys.exit(1)
   elif cpid == 0:
      os.write(1, ("I'm child. Pid: %d\n" % (os.getpid())).encode())
   elif cpid > 0:
      os.write(1, ("I am parent. Pid: %d. Child Pid: %d\n" % (os.getpid(),cpid)).encode())

# Main 
def main(argc, argv):
   # Initialize 
   # Interpret 
   # Terminate 
   shell()


