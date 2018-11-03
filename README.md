# Scoreboarding for Dynamic Instruction Scheduling Simulator
This python script implement a simulator of the scoreboarding technique for dynamic instruction scheduling (out-of-order instruction execution in execution time by the computer architecture itself). An architecture with scoreboarding has replicas of some functional units for the EXECUTION PHASE of the instructions, meaning it can execute several instructions at the same clock cycle. Please note that this is *NOT* a superscalar architecture, which is a very similar concept also connected with dynamic instruction scheduling. The main reason is because this program only support a single instruction dispatch at a given clock cycle.

Note that both techniques may execute instructions out-of-order (whenever false dependencies in the code are not an constraint), but the COMMIT/WRITE BACK phase (the last phase of every instruction) must happen strictly in the same order wrote in the program code.

# Table of Contents
0. [Python-related information](#Python-related-information)
    1. [Python version](#Python-version)
    2. [Used packages](#Used-packages)
1. [Usage](#Usage)
    1. [How to run](#How-to-run)
    2. [Command line Flags](#Command-line-flags)
    3. [Command line Arguments](#Command-line-arguments)
    4. [Input file format](#Input-file-format)
    5. [Supported instructions](#Supported-instructions)
2. [Configuration](#Configuration)
    1. [The Configme.py Module](#The-configme-module)
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
- **source**\_**code**\_**filepath:** input filepath for a pseudo-MIPS assembly code. The format demanded by the input source code is explained [here](#Input-file-format) and information about supported MIPS instructions you may found [here](#Supported-instructions).
- **flags:** program flags are explained in deeper details [here](#Command-line-flags). You may check out the program built-in help system using the flag "-help" or just running the program without specifying the "source\_code\_filepath" program argument.

## Command line flags
<a name="Command-line-flags"></a>
Just like in the built-in help system:

| Flag          | Description														|
| ------------- | --------------------------------------------------------------------------------------------------------------------- |
|--checkreg	| accepts only registers declared in architecture defined in Configme.py module.					|
|--nogui	| (currently useless) disable graphical interface.									|
|--complete:	| produce step-by-step output for Instruction, Functional Units and Register status tables.				|
|--nocolor:	| produce all output with just standard terminal color. Makes sense only if used together with "--complete" flag.	|
|--noufstage:	| disable the "update\_flags" pipeline stage, used to prevent deadlocks in RAW dependencies if two instructions in the ("write\_result", "read\_operands") pipeline stages pair matches in the same clock cycle while the first one write in a register and the second one read from it. If this flag is enabled, the functional unit flag updating  will be done in the "write\_result" pipeline stage instead.|

## Command line arguments
<a name="Command-line-arguments"></a>
User may specify the following optional arguments:
| Argument 	| Type			| Description 											|
| ------------- | --------------------- |---------------------------------------------------------------------------------------------- |
|--clockstep	| Positive integer	| specify how many clock cycles must be shown each iteration. If ommited, then all cycles will be printed by default. This argument only makes sense if used together with "--complete" flag. |

## Input file format
<a name="Input-file-format"></a>
The input file format is a simplified version of a MIPS assembly code. 

- You must give a single instruction per line;
- Supported instructions information can be found [here](#Supported-instructions);
- Commentaries are allowed both in the same line of a instruction or in a empty line, if followed by a "#" symbol. Check out the [examples](#Input-file-example-1) given below in inside this subsection.
- The used registers can have (almost) any label (you can't use whitespaces nor ",", "(" and ")" symbols) if "--checkreg" flag is disabled. Otherwise, only registers declared in architecture defined inside "Configme.py" are accepted. More information about "Configme.py" module can be found [here](#The-configme-module).
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
This program supports almost any MIPS non-branch instructions (neither conditional and unconditional branches are supported). The supported MIPS instruction formats are defined as below.

| Supported 	| type	| Instruction classification 	| Instruction format								|
| ------------- | ----- | ----------------------------- | ----------------------------------------------------------------------------- |
| Yes		| R	| Common			| instruction\_label destiny\_reg, reg\_operand\_a, reg\_operand\_b		|
| Yes		| I	| Common			| instruction\_label distiny\_reg, reg\_operand, \[+-\]immediate		|
| Yes		| I	| Load Word			| instruction\_label destiny\_reg, \[+-\]immediate\_value(operand\_reg)		|
| Yes		| I	| Store Word 			| instruction\_label operand\_reg\_b, \[+-\]immediate\_value(operand\_reg\_a)	|
| \*No		| I	| Binary Conditional Branch	| instruction\_label operand\_reg\_a, operand\_reg\_b, jump\_label		|
| \*No		| I	| Unary Conditional Branch 	| instruction\_label operand\_reg, jump\_label					|
| No		| J	| Unconditional Branch		| instruction\_label jump\_label						|

\*You may still use conditional branches in the input code, but they will have no "branching effect" (i.e. the PC will not be moved), so they will be executed just like any other generic instruction.

# Configuration
<a name="Configuration"></a>
All program configuration must be defined in the "configme.py" module, which will be deeper explained in this section.

## The Configme module
<a name="the-configme-module"></a>
The "configme.py" module is dedicated to keep all necessary configuration of the script. It defines all the computer architecture which will used during simulations of the scoreboarding technique. I've loaded it with some general-purpose initial configuration and added a heavy user-oriented commentary inside the module to help during the configuration process.

## Configurable fields
<a name="Configurable-fields"></a>
Inside "configme.py" module you can find a class named "Config" which keeps every aspect of the represented computer architecture that the user may modify as it pleases. These fields are described as below.

| Field					| Python data type	| Description									|
| ------------------------------------- | --------------------- | -----------------------------------------------------------------------------	|
| functional\_units 			| Dict			| Specify available functional units, replicas quantity and clock delay of every functional unit		|
| instruction\_list 			| Dict			| List all supported instructions alongside its type and used functional unit	|
| store\_instruction\_set 		| Set			| List instructions that access primary memory to **store** (not *read*) words	|
| stage\_delay 				| Dict			| Clock delay for pipeline stages other than "execution" (which uses functional units)|
| custom\_inst\_additional\_delay 	| Dict			| Add additional delay for specify instructions (e.g. Load/Store operations)	|
| WORD\_SIZE 				| int			| Specify, in Bytes, the size of a single word of the architecture		|
| architecture\_register\_set 		| Set			| Specify all available registers in the architecture.				|

Each Dict format is better explained in the commentaries within the "configme.py" module source code. If needed, follow up the pre-configuration model.

# Output details
<a name="Output-details"></a>
User has two options for the program output: simplified and complete. In the simplified version only the final Instruction State table configuration will be printed, just like the exemple below:
```
----------------------------------------------------------------
PC :    issue     |read_operands |  execution   | write_result |
----------------------------------------------------------------
0  :      1       |      2       |      4       |      5       |
4  :      6       |      7       |      8       |      9       |
8  :      7       |      8       |      10      |      11      |
12 :      12      |      13      |      14      |      15      |
16 :      13      |      16      |      17      |      18      |
20 :      14      |      19      |      21      |      22      |
24 :      17      |      18      |      19      |      20      |
----------------------------------------------------------------
```
The complete mode can be enabled with the "--complete" flag. In this case, the program will print a step-by-step solution of three bookkeeping-purpose tables: Instruction, Functional Unit and Destiny Registers state tables. If "--nocolor" flag is disabled, then, in every step, the table fields will be colored in a red-green schema, highlighting (with green color) all fields which are changed in the correspondent clock cycle to help user follow up with the solution. An iteration of the complete output would be:
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clock timer = 16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 -> Instruction status table:
----------------------------------------------------------------
PC :    issue     |read_operands |  execution   | write_result |
----------------------------------------------------------------
0  :      1       |      2       |      4       |      5       |
4  :      6       |      7       |      8       |      9       |
8  :      7       |      8       |      10      |      11      |
12 :      12      |      13      |      14      |      15      |
16 :      13      |      16      |              |              |
20 :      14      |              |              |              |
24 :              |              |              |              |
----------------------------------------------------------------

 -> Functional Unit status table:
-----------------------------------------------------------------------------------------------------
Functional unit :  busy |  op  | f_i  | f_j  | f_k  |      q_j       |      q_k       | r_j  | r_k  |
-----------------------------------------------------------------------------------------------------
load_store_0    :  True |  20  |  -   |  -   |  -   |       0        | integer_alu_1  | True |False |
load_store_1    : False |  -1  |  -   |  -   |  -   |       -        |       -        | True | True |
integer_alu_0   : False |  12  |  $3  |  $3  |  -   |       0        |       0        |False |False |
integer_alu_1   :  True |  16  |  $5  |  $2  |  $3  |       0        |       0        |False |False |
float_mult_0    : False |  -1  |  -   |  -   |  -   |       -        |       -        | True | True |
float_mult_1    : False |  -1  |  -   |  -   |  -   |       -        |       -        | True | True |
float_div_0     : False |  -1  |  -   |  -   |  -   |       -        |       -        | True | True |
float_add_sub_0 : False |  -1  |  -   |  -   |  -   |       -        |       -        | True | True |
-----------------------------------------------------------------------------------------------------

 -> Destiny Register status table:
$2 : [ 0 ] $4 : [ 0 ] $5 : [ integer_alu_1 ] $3 : [ 0 ] [...] (More 60 ommited registers)
```
