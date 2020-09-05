#!/usr/bin/env python3

#Libraries 
import os
import sys
import re
import gc

#Shell process
def  shell():
   line = {}
   status = None 
   while status:
   	print("$ ")
   	#Read
   	line = sh_reader()
   	#Parse
   	args = sh_parser(line)
   	#Execute
   	status = sh_exec(args)
   	#Free space 
   	gc.collect()
   	
#Make reader (this will read the commands written in the shell)
def sh_reader():
   
#Make parser (this will execute the commands from the tokenizer)
def sh_parser(line): 

#Make exec for built_in commands (cd, exit)
def sh_exec(args):

#Make pipes
def sh_pipes():

#Make exec for commands
def sh_exec_nativ(args):
   cpid = os.fork()
   #Fork failed
   if cpid < 0:
      os.write(2, ("Fork failed, returning %d\n" % cpid).encode())
      sys.exit(1)
   elif cpid == 0:
      os.write(1, ("I'm child. Pid: %d\n" % (os.getpid())).encode())
   elif cpid > 0:
      os.write(1, ("I am parent. Pid: %d. Child Pid: %d\n" % (os.getpid(),cpid)).encode())

#Main 
def main(argc, argv):
   #Initialize 
   #Interpret 
   #Terminate 
   shell()


