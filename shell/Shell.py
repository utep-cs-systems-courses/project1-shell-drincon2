#!/usr/bin/env python3

# Libraries 
import os
import sys
import re


# Shell process
def shell():
   status = 1
    
   while status == 1:
      # Read user input for commands
      line = input(os.getcwd() + "$ ")       
      # Parse user input
      args = sh_parser(line)
      # Execute commands
      status = sh_exec(args)
       
    
# Shell parser
def sh_parser(line):
   # Parse user input 
   tokens = line.split(" ")
     
   return tokens
  
# Execute commands
def sh_exec(args):
   # Check user input is not empty 
   if not args or '' in args:
      return 1
   
   # Check for built-in commands
   for command in range(len(args)):
      # cd 
      if args[command] == "cd" and args[command + 1] != None:
         # Change to directory specified by user
         try:
            os.chdir(args[command + 1])
            return 1 
         # Prompt error message whenever directory is invalid
         except FileNotFoundError:
            print("bash: cd: "+ args[command + 1] + ": No such file or directory")
            return 1
      # exit
      if args[command] == "exit":
         print("Closing shell ...")
         return 2
         
   print("invalid command...")
   
   return 1

shell() 
