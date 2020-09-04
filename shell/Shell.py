#!/usr/bin/env python3

#Libraries 
import os
import sys
import re

#Make tokenizer (this will read the commands written in the shell)

#Make fork (This will take the tokenizer and send it to the parser to execute the commands)
def fork_process():
   cpid = os.fork()
   #Fork failed
   if cpid < 0:
      os.write(2, ("Fork failed, returning %d\n" % cpid).encode())
      sys.exit(1)
   elif cpid == 0:
      os.write(1, ("I'm child. Pid: %d\n" % (os.getpid())).encode())
   elif cpid > 0:
      os.write(1, ("I am parent. Pid: %d. Child Pid: %d\n" % (os.getpid(),cpid)).encode())
   
fork_process()      
   
#Make parser (this will execute the commands from the tokenizer)


