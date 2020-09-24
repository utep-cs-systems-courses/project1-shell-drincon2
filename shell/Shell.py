#!/usr/bin/env python3

# Modules
import os
import sys
import re


# Shell process
def shell():
   status = 1
   sh_prompt = "$ " 
   while status == 1:
      # Check for environmental variable PS1
      if "PS1" in os.environ:
         sh_prompt = os.environ["PS1"]
      # Read user input for commands
      line = input(sh_prompt)       
      # Parse user input
      args = line.split(" ")
      # Execute commands
      status = sh_exec(args)
           
  
# Execute built-in shell commands
def sh_exec(args):
   # Check user input is not empty 
   if not args or '' in args:
      return 1
   
   # cd 
   if "cd" in args and len(args) == 2:
      # Change to directory specified by user
      try:
         os.chdir(args[1])
         return 1 
      # Prompt error message whenever directory is invalid
      except FileNotFoundError:
         os.write(2, ("bash: cd: "+ args[1] + ": No such file or directory\n").encode())
         return 1
   # exit
   elif "exit" in args:
      os.write(2, ("Closing shell ...\n").encode())
      return 2
         
   # Redirection of input
   elif "<" in args:
      try:
         sh_redirect_in(args)
         return 1
      except:
         os.write(2, ("directory not found or invalid\n").encode())
      
   # Redirection of output
   elif ">" in args:
      try:
         sh_redirect_out(args)
         return 1
      except:
         os.write(2, ("directory not found or invalid\n").encode())
            
   # Pipes
   elif "|" in args:
      try: 
         sh_pipes(args)
         return 1
      except (EOFError):
         os.write(2, ("Pipe failed, closing shell...\n").encode())
         return 2
             
   
   # Look for shell commands and execute them 
   else:
      try:
         sh_exec_nativ(args)
      except:      
         os.write(2, (args[0] + ": command not found\n").encode())
   
   return 1


# Redirection of input 
def sh_redirect_in(args):
   # Check 'cat' command in args
   if "cat" in args:
      with open (args[-1], 'r') as input_file:
         for line in input_file:
            os.write(2, line.encode())
         input_file.close()
 
# Redirection of output
def sh_redirect_out(args):
   
   # output redirection for ls command 
   if "cat" in args:
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
      os.write(2, ("Fork failed\n").encode())
      sys.exit(-1)
   # Parent process
   elif pid > 0: 
      status = os.wait()
      os.close(w)
      r = os.fdopen(r)
      cstr = r.read()
      os.write(2, cstr.encode())
      
   # Child process
   else:
      os.close(r)
      w = os.fdopen(w, 'w')
      
      # Flag -r for command ls | sort
      if args[0] == "ls" and args[-1] == "-r":
         dir_list = os.listdir()
         for file in sorted(dir_list, key = str.lower, reverse = True):
            w.write(file + "\n")
         w.close()
         sys.exit(0)

         
# Execute shell commands
def sh_exec_nativ(args):
   cpid = os.fork()
   
   if cpid < 0:
      os.write(2, ("Fork failed\n").encode())
      sys.exit(-1)
   
   # Child process 
   elif cpid == 0:
     for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
      
        try:
           os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
           pass                              # ...fail quietly
           
     # Error ocurred
     os.write(2, ("This should not print\n").encode())
     sys.exit(-1)
   
   # Parent process
   else:
      status = os.wait()
   
shell() 
