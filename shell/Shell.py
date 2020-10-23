#!/usr/bin/env python3

# Modules
import os
import sys
import re
import time

# Shell process
def shell():
   # Infinite loop parameter
   status = 1
   # Shell prompt
   sh_prompt = "$ "
   # Infinite loop
   while status == 1:
       # Check for environment variable PS1
       if "PS1" in os.environ:
          sh_prompt = os.environ["PS1"]
       # Display prompt in shell
       os.write(1, sh_prompt.encode())
       # Get user input for commands
       line = os.read(0, 256)
       # Break loop if user input could not be read
       if line is None or len(line) == 0:
          break
       # Split user commands in new lines
       args = line.decode().split("\n")
       # Execute commands
       for command in args:
          status = sh_execute(command.split())
       
       
# Execute built-in shell commands   
def sh_execute(args):
   # Check user input is not empty 
   if not args:
      return 1
   
   elif "exit" in args:
      sys.exit(0)
   elif "cd" in args and len(args) == 2:
      try: 
         os.chdir(args[1])
      except FileNotFoundError:
         os.write(2, ("bash: cd: "+ args[1] + ": No such file or directory\n").encode())
   elif "|" in args:
      try:
         sh_pipes(args)
      except:
         os.write(2, ("Pipe failed, closing shell...\n").encode())
   elif "<" in args:
      try:
         sh_redirect_in(args)
      except:
         os.write(2, ("directory not found or invalid\n").encode())
   elif ">" in args:
      try:
         sh_redirect_out(args)
      except:
         os.write(2, ("directory not found or invalid\n").encode())
   else:
      try:
         sh_exec_nativ(args)
      except:      
         os.write(2, (args[0] + ": command not found\n").encode())

   return 1


# Pipes    
def sh_pipes(args):
   pipe_left = args[0:args.index("|")]
   pipe_right = args[args.index("|") + 1:]

   pr,pw = os.pipe()
   rc = os.fork()
   
   # Fork failed
   if rc < 0:
      os.write(2, ("Fork failed\n").encode())
      sys.exit(1)
   # Child
   elif rc == 0:
      # Redirect child's stdout
      os.close(1)
      # Duplicate writing pipe
      os.dup(pw)
      os.set_inheritable(1, True)
      for fd in (pr, pw):
         os.close(fd)
      # Execute commands in left pipe
      for dir in re.split(":", os.environ['PATH']): # try each directory in the path
         program = "%s/%s" % (dir, pipe_left[0])
         try:
            os.execve(program, pipe_left, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly     
      # Error ocurred
      os.write(2, ("This should not print\n").encode())
      sys.exit(1)
   # Parent          
   else:
      # Redirect parent's stdin
      os.close(0)
      # Duplicate reading pipe
      os.dup(pr)
      os.set_inheritable(0, True)
      for fd in (pw, pr):
          os.close(fd)
      if "|" in pipe_right:
         sh_pipes(pipe_right)
      # Execute commands in right pipe
      for dir in re.split(":", os.environ['PATH']): # try each directory in the path
         program = "%s/%s" % (dir, pipe_right[0])
         try:
            os.execve(program, pipe_right, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly
      # Error ocurred
      os.write(2, ("This should not print\n").encode())
      sys.exit(1)


# Redirect input
def sh_redirect_in(args):
   rc = os.fork()

   if rc < 0:
      os.write(2, ("Fork failed\n").encode())
      sys.exit(1)

   elif rc == 0:
      os.open(args[args.index("<") + 1], os.O_RONLY)
      args.remove(args[args.index("<") + 1])
      args.remove('<')

      for dir in re.split(":", os.environ['PATH']): # try each directory in path
         program = "%s/%s" % (dir, args[0])
         try:
            os.execve(program, args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 

      # Error ocurred
      os.write(2, ("This should not print\n").encode())
      sys.exit(1)

   else:
      childPidCode = os.wait()


# Redirect output
def sh_redirect_out(args):
   rc = os.fork()

   if rc < 0:
      os.write(2, ("Fork failed\n").encode())
      sys.exit(1)

   elif rc == 0:
      os.close(1)
      os.open(args[args.index(">") + 1], os.O_CREAT | os.O_WRONLY);
      os.set_inheritable(1, True)
      args.remove(args[args.index(">") + 1])
      args.remove('>')

      for dir in re.split(":", os.environ['PATH']): # try each directory in path
         program = "%s/%s" % (dir, args[0])
         try:
            os.execve(program, args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 

      # Error ocurred
      os.write(2, ("This should not print\n").encode())
      sys.exit(1)

   else:
      childPidCode = os.wait()
      
         
# Execute commands         
def sh_exec_nativ(args):
   cpid = os.fork()
   
   if cpid < 0:
      os.write(2, ("Fork failed\n").encode())
      sys.exit(1)
   
   # Child process 
   elif cpid == 0:
      if "/" in args[0]:
         program = args[0]
         try:
            os.execve(program, args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly
      else:
         for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
               os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
               pass                              # ...fail quietly
           
      # Error ocurred
      os.write(2, ("This should not print\n").encode())
      sys.exit(1)
   
   # Parent process
   else:
      status = os.wait()         


shell()
