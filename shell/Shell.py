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
  # Tokens 
  tokens = {}
  
  # Parse user input
  for arg in line.split(" "):
     tokens[arg] = arg
     
  return tokens
  
# Execute commands
def sh_exec(args):
   # Check user input is not empty 
   if not args or '' in args:
      return 1
   
   # Check for built-in commands
   for command in args:
      # cd 
      if args[command] == "cd":
         os.execve(str(os.getcwd), args, os.environ)
      # exit
      if args[command] == "exit":
         print("Closing shell ...")
         return 2
   
   return 1

shell() 
