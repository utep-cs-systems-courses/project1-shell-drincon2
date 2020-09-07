#!/usr/bin/env python3

# Libraries 
import os
import sys
import re
import gc


# Shell process
def shell():
    line = {}
    status = 1
    while status:
        print(os.environ['PATH'] + "$ ")
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
    # Token dictionary
    tokens = {}

    # Parse line dictionary
    for arg in line:
        tokens[arg] = re.split(" ", arg)

    return tokens


# Execute built_in commands (cd, exit)
def sh_exec(args):
    # Line with arguments is empty
    if args[0] is None:
        return 1

    # Built-in commands
    builtin_commands = ["cd", "exit"]
    # Use loop to determine whether execute a shell or built-in command
    for command in builtin_commands:
        if builtin_commands[command] == args[command]:
            # Run built-in command
            # cd
            if args[command] == "cd":
                os.chdir(os.environ['PATH'] + args[command])
            # exit
            elif args[command] == "exit":
                print("Closing shell...")
                return 0

    # Run shell commands
    return sh_exec_nativ(args)


# Pipes
def sh_pipes():
    print("Initializing Pipe...")


# Redirection of input output
def sh_redirect_inout():
    print("Redirecting input ...")


# Execute commands
def sh_exec_nativ(args):
    # Shell home directory
    initial_path = os.environ['PATH']
    cpid = os.fork()

    # Fork failed
    if cpid < 0:
        print("Fork failed, returning %d\n" % cpid)
        sys.exit(1)
    # Child process
    elif cpid == 0:
        print("I'm child. PID: %d\n" % (os.getpid()))
        # Attempt executing shell command
        try:
            os.execve(initial_path, args, os.environ)
        except FileNotFoundError:
            sys.exit(1)
    # Parent process
    elif cpid > 0:
        print("I am parent. PID: %d. Child PID: %d\n" % (os.getpid(), cpid))
        wpid = os.wait()
        print("Child %d terminated with exit code %d\n" % wpid)

    return 1


# Main
def main(argc, argv):
    # Initialize
    # Interpret
    # Terminate
    shell()
