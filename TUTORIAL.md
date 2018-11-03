# Tutorial: step-by-step through configuration & program execution

# Table of contents:
1. [First observations](#first-observations)
2. [First step: Configme.py module](#configme-module)
3. [Moving on: creating an input file](#creating-an-input-file)
4. [And, finally: running input file](#running-input-file)

## First observations
<a name="first-observations"></a>
Please check out the README file for deeper details about anything in this tutorial. The purpose of this file is to help new users to get a quick idea of how to use the core elements of this script.

## First step: Configme.py module
<a name="configme-module"></a>
The first thing you need is to configure the computer architecture that you want to simulate. All configurable aspects supported by this program are, with no exception, inside the "Configme.py" module. You may use any text editor to do the job.

(...)

when finished with all the configuration, save and exit.

## Moving on: creating an input file
<a name="creating-an-input-file"></a>
The next thing to do is to create an input file. As you can see already in the samples inside ./test-cases/ subdirectory, there's no mistery to anyone already familiar to assembly or, even more, MIPS assembly. The rules are simple and clean:
- Currently only type R and type I (of all variations) MIPS instruction formats.
- One instruction per line.
- Commentaries (# like this) are allowed, either proceeding an instruction or at a separated empty line.
- No jump labels.
- Only instructions specified previously in the configuration step.
- You need to use the specified registers in architecture register bank only if "--checkreg" flag is used during program execution.
- The local you put your input file does not matter.

You can use any instruction and registers that you already specified in the previous step, while you're configurating the architecture. Remember that this program does not care about register values nor support branching (neither conditional nor unconditional), so instructions like "beq" or "blt" will be executed as an generic type I instruction (i.e. the branch will never be taken).

Example of input file:
```
LW $1, 0($sp)
LW $2, 4($sp)
ADDI $1, $1, 4
SUB $3, $1, $2
SW $3, 0($sp)
SW $1, 4($sp)
BEQ # Will not be taken! (never!)
```

## And, finally: running input file
<a name="running-input-file"></a>
The last step is the easiest one. The door for using the program is the "run.py" module. The basic usage is

```
	# Remember that python 3.x is needed!
	# Check out your python version with
	python --version
	
	# Basic output version
	python run.py <input_filepath> [optional flags and arguments*]

	# Complete output version
	python run.py <input_filepath> --complete [more optional flags and arguments*]

	# Step-by-step complete output version - you may specify a bigger
	# clockstep to speed up the step size between each screen print of
	# the complete solution
	python run.py <input_filepath> --complete --clockstep 1 [more optional flags and arguments*]


	# *Check README for more information
```

If you need more help about the program usage, just run "run.py" without specifing any additional arguments, or use "-h" or "--help" flags.
```
	# All execution lines below are equivalent
	python run.py
	python run.py -h
	python run.py --help
```
