# Scoreboarding for Dynamic Instruction Scheduling Simulator
This python script implement a simulator of the scoreboarding technique 
for dynamic instruction scheduling (out-of-order instruction execution
in execution time by the computer architecture itself). An architecture 
with scoreboarding has replicas of some functional units for the EXECU-
TION PHASE of the instructions, meaning it can execute several instruc-
tions at the same clock cycle. Please note that this is *NOT* a super-
scalar architecture, which is a very similar concept also connected with 
dynamic instruction scheduling. The main reason is because this program 
only support a single instruction dispatch at a given clock cycle.

Note that both techniques may execute instructions out-of-order
(whenever false dependencies in the code are not an constraint),
but the COMMIT/WRITE BACK phase (the last phase of every instruction) 
must happen strictly in the same order wrote in the program code.

# Table of Contents
0. [Python-related information](#Python-related-information)
    1. [Python version](#Python-version)
    2. [Used packages](#Used-packages)
1. [Usage](#Usage)
    1. [How to run](#How-to-run)
    2. [Command line Flags](#Flags)
    3. [Input file format](#Input-file-format)
    4. [Supported instructions](#Supported-instructions)
2. [Configuration](#Configuration)
    1. [The Configme.py Module](#Configme-module)
    2. [Configurable fields](#Configurable-fields)
3. [Output details](#Output-details)

# Python-related Information
<a name="Python-related-information"></a>

## Python version
<a name="Python-version"></a>
This script was made using Python 3.
Tested with Python 3.5.2 version.

## Used packages
<a name="Used-packages"></a>
This script uses the following Python 3 package, which can be obtained via pip3 (pip3 install package\_name).
- colorama

# Usage
<a name="Usage"></a>

## How to run
<a name="How-to-run"></a>
The basic program usage is defined as follows:
```
python3 run.py <source_code_filepath> [flags]
```
Where:
- source\_code\_filepath: input filepath for a pseudo-MIPS assembly code. The format demanded by the input source code is explained [here](#Input-file-format) and information about supported MIPS instructions you may found [here](#Supported-instructions).
- flags: program flags are explained in deeper details [here](#Flags). You may check out the program built-in help system using the flag "-help" or just running the program without specifying the "source\_code\_filepath" program argument.

## Command line flags
<a name="Flags"></a>
Just like in the built-in help system:

| Flag          | Description														|
| ------------- | --------------------------------------------------------------------------------------------------------------------- |
|--checkreg	| accepts only registers declared in architecture defined in Configme.py module.					|
|--nogui	| disable graphical interface.												|
|--complete:	| produce step-by-step output for Instruction, Functional Units and Register status tables.				|
|--nocolor:	| produce all output with just standard terminal color. Makes sense only if used together with "--complete" flag.	|

## Input file format
<a name="Input-file-format"></a>
The input file format is a simplified version of a MIPS assembly code. 

- You must give a single instruction per line;
- Supported instructions information can be found [here](#Supported-instructions);
- Commentaries are allowed both in the same line of a instruction or in a empty line, if followed by a "#" symbol. Check out the [examples](#Input-file-example-2) given below in inside this subsection.
- The used registers can have (almost) any label (you can't use whitespaces nor ",", "(" and ")" symbols) if "--checkreg" flag is disabled. Otherwise, only registers declared in architecture defined inside "Configme.py" are accepted. More information about "Configme.py" module can be found [here](#Configme-module).
- You can check out some input file examples in the "./test-cases/" subdirectory.

### Input file example 1:
<a name="Input-file-example-1"></a>
```
# Don't forget customize your configuration at "configme.py" module!
L.D F6,34(R2) # MIPS standard type "I" instruction format
L.D F2,45(R3)
MUL.D F0, F2, F4 # MIPS standard type "R" instruction format
SUB.D F8, F6, F2
DIV.D F10, F0, F6
ADD.D F6, F8, F2
```

### Input file example 2:
<a name="Input-file-example-2"></a>
```
LW $2, 0($4)
ADDI $2, $2, 10
LW $3, 4($4)
ADDI $3, $3, 20
ADD $5, $2, $3
SW $5, 8($4)
ADDI $4, $4, 4
```

## Supported instructions
<a name="Supported-instructions"></a>
This program supports almost any MIPS non-branch instructions (neither conditional and unconditional branches are supported). You may still use branches in the input code, but they will have no "branching effect" (i.e. the PC will not be moved), so they will be executed just like any other generic instruction.

The MIPS instruction supported formats are defined as below.

| Support 	| type	| Instruction classification 	| Instruction format								|
| ------------- | ----- | ----------------------------- | ----------------------------------------------------------------------------- |
| Yes		| R	| Common			| instruction\_label destiny\_reg, reg\_operand\_a, reg\_operand\_b		|
| Yes		| I	| Common			| instruction\_label distiny\_reg, reg\_operand, \[+-\]immediate		|
| Yes		| I	| Load Word			| instruction\_label destiny\_reg, \[+-\]immediate\_value(operand\_reg)		|
| Yes		| I	| Store Word 			| instruction\_label operand\_reg\_b, \[+-\]immediate\_value(operand\_reg\_a)	|
| No		| I	| Binary Conditional Branch	| instruction\_label operand\_reg\_a, operand\_reg\_b, jump\_label		|
| No		| I	| Unary Conditional Branch 	| instruction\_label operand\_reg, jump\_label					|
| No		| J	| Conditional Branch		| instruction\_label jump\_label						|

# Configuration
<a name="Configuration"></a>
All program configuration must be defined in the "configme.py" module, which will be deeper explained in this section.

## The Configme.py module
<a name="Configme-module"></a>

## Configurable fields
<a name="Configurable-fields"></a>

# Output details
<a name="Output-details"></a>
