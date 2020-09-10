#!/usr/bin/env python3

# Modules
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
      elif args[command] == "exit":
         print("Closing shell ...")
         return 2
         
      # Redirection of i/o
      elif args[command] == ">":
         try:
            sh_redirect_io(args)
            return 1
         except:
            print("directory not found or invalid")
            
      # Pipes
      elif args[command] == "|":
         try: 
            sh_pipes(args)
            return 1
         except (EOFError):
            print("Pipe failed, closing shell...")
            return 2
         
   print(args[0] + ": command not found")
   
   return 1
   
 
# Redirection of i/o
def sh_redirect_io(args):
   # List of files in directory
   dir_files = os.listdir()
   
   # Write file in specified directory
   with open(args[-1], 'w') as output_file:
      for file in sorted(dir_files, key = str.lower):
         output_file.write(file + "\n")
         
      output_file.close()
   
   
# Pipes
def sh_pipes(args):
   
   # Read and write pipes
   r, w = os.pipe()
   
   # Fork
   pid = os.fork()
   
   if pid < 0:
      print("Fork failed")
      sys.exit(-1)
   # Parent process
   elif pid > 0: 
      status = os.wait()
      os.close(w)
      r = os.fdopen(r)
      cstr = r.read()
      print(cstr)
      
   # Child process
   else:
      os.close(r)
      w = os.fdopen(w, 'w')
      
      # Flag -r for command ls | sort
      if args[-1] == "-r":
         dir_list = os.listdir()
         for file in sorted(dir_list, key = str.lower, reverse = True):
            w.write(file + "\n")
         w.close()
         sys.exit(0)
   

shell() 
