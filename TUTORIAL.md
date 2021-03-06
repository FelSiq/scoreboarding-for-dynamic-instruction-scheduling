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

There are **seven** fields that we will need to check out in order to everything work as you expect. If needed, use your text editor search system and search exactly the field names I will list immediately below to easily find each field.
1. **functional**\_**units:** python dictionary that holds every functional unit of the computer architecture. The keys are the functional unit identifier, and the values are dictionary containing both "quantity" (the number of replicas of that functional unit) and "clock_cycles" (the total clock delay necessary to a single execution in that functional unit). The default configuration, as you may see immediately below, has five types of functional units for different purposes, and a total of seven replicas. You can give any name to your functional unit, and any **positive integer** quantity and clock cycle costs.
```
        functional_units = {
                "integer_alu" : {"quantity" : 1, "clock_cycles" : 1},
                "load_store" : {"quantity" : 2, "clock_cycles" : 2},
                "float_add_sub" : {"quantity" : 1, "clock_cycles" : 2},
                "float_mult" : {"quantity" : 2, "clock_cycles" : 10},
                "float_div" : {"quantity" : 1, "clock_cycles" : 40},
        }
```
2. **instruction**\_**list:** here you must list all instructions used in your input files (as we will see in the next step), alongside the correspondent functional unit they use (remembering that the used functional units must be declared in the previous field) and it's correspondent instruction type. Remember that the instruction type must be either "R" or "I" (with CAPITAL LETTER). "J" instructions are not supported, so the use of it leads to undefined behavior. Use the predefined instructions (some examples are given below) as models to learn the correct instruction specification format.

```
        instruction_list = {
                "L.D" : {
                        "functional_unit" : "integer_alu",
                        "instruction_type" : "I",
                },

                "LW" : {
                        "functional_unit" : "load_store",
                        "instruction_type" : "I",
                },

                "MUL.D" : {
                        "functional_unit" : "float_mult",
                        "instruction_type" : "R",
                },
		
		# (...) Much more instructions defined!
		# Check out inside Configme.py module to
		# see more.
	}
```

3. **store**\_**instruction**\_**set:** here you must specify all instructions that access the primary memory for **STORE PURPOSE ONLY** (i.e. all type of "store word" operations). This is due to the fact that is impossible to differentiate a Store Word and Load Word operation using MIPS instruction format assembly with a generic method, as they looks exactly the same but the semathics behind are completely different.
```
	# Don't put Load Word operations here!
	store_instruction_set = {"SW", "SW.D", "..."}
```
4. **stage**\_**delay:** here you can specify all pipeline stage delays, in clock cycles (so it must be a positive integer value - you can't use floating point values here) that are **independent** from the functional units (avoid specifying the "execution" stage here! Remember that every execution unit already has it's custom delay, specified in the "functional\_units" field already seen).
```
        stage_delay = {
                "issue" : 1,
                "read_operands" : 1,
                "write_result" : 1,
                "update_flags" : 1,
        }
```

5. **custom**\_**inst**\_**additional**\_**delay:** this special field let you apply additional delay to specific instructions into its pipeline "execution" stage. For example, if you want your "LW" ("Load Word") instruction to have an additional cost of 2 clock cycles, even if it uses the same functional unit of, say, "SW" ("Store Word") instruction even if they both uses the same functional unit, then you can just input a entry in this field, just like seen below, in order to guarantee that behavior during program execution.
```
	# All "LW" instructions will now cost functional_unit_cost(LW) + 2
	# clock cycles to complete its "execution" pipeline stage phase.
        custom_inst_additional_delay = {
                "LW" : 2,
        }

```

6. **WORD**\_**SIZE:**: size of a single architecture word, in bytes. Used mainly for interface purposes, as the PC is used to reference all instructions in the program output.

```
	# Only positive integer values are allowed.
	WORD_SIZE = 4
```

7. **architecture**\_**register**\_**set:** register bank of the computer architecture. Just like the functional unit names, the exactly register name is unimportant to the program execution, as long you match they in the input code. You don't need to be bothered modifying these now if you don't plan to use the "--checkreg" flag during the program execution. That flag is made solely for making sure that the registers used in the input code are consistent to the architecture specified. If you don't plan to make that verification, then you can just skip this configuration, as the program will automatically insert unseen registers into the computer architecture register bank while reading the input file if the user permits so (by just not enabling "--checkreg" flag during program execution).
```
	# Simulate general-purpose registers. The semantic behind
	# every register must be guaranteed by the user, as the program
	# does not care about special registers neither the values they
	# may keep at any stage of the program execution.
	architecture_register_set = {
		"$" + str(i) for i in range(32)
	}.union({"$f" + str(i) for i in range(32)})

	# In this example, the computer architecture will habe 64 registers,
	# "$0" to "$31" and "$f0" to "$f31".

```

When you finish all your custom configuration, just save the modifications and exit.

## Moving on: creating an input file
<a name="creating-an-input-file"></a>
The next thing to do is to create an input file. As you can see already in the samples inside ./test-cases/ subdirectory, there's no mistery about the format to anyone with some familiarity with basic assembly or, even better, MIPS assembly. The rules are simple and clean:
- Currently you may use only type R and type I (of all variations) MIPS instruction formats.
- One instruction per line.
- Commentaries (# like this) are allowed, either proceeding an instruction or at a separated empty line.
- No jump labels are allowed.
- Use only instructions specified previously in the configuration step. If you miss it, check out step 1 of this tutorial.
- You need to use the specified registers in architecture register bank only if "--checkreg" flag is used during program execution. Otherwise, any register label can be used as it will automatically be inserted in the computer architecture if they're not in it already.
- The file local where you plan to keep your input files is unimportant.

You can use any instruction and registers that you already specified in the previous step, while you're configurating the architecture. Remember that this program does not care about register values nor support branching (neither conditional nor unconditional), so instructions like "beq" or "blt" will be executed as an generic type I instruction (i.e. the branch will never be taken).

Example of input file:
```
# Don't forget to make sure that all instructions
# are specified at Configme.py module, in the
# "instruction_list" field! The registers must be
# specified in the Configme.py module only if you
# plan to use the "--checkreg" flag during program
# execution.
LW $1, 0($sp)
LW $2, 4($sp)
ADDI $1, $1, 4
SUB $3, $1, $2
SW $3, 0($sp)
SW $1, 4($sp)
BEQ $1, $2, -48 # This branch will not be taken! (never!)
```

## And, finally: running input file
<a name="running-input-file"></a>
The last step is the easiest one. The door for using the program is the "run.py" module. The basic usage is

```
	# Remember that python 3.x is needed!
	# Check out your python version with
	python --version
	
	# Basic output version - only final state of the instruction
	# state table will show up
	python run.py <input_filepath> [optional flags and arguments*]

	# Complete output version - all tables (instruction, functional units and
	# registers states), all steps (clock by clock, omitting the ones that does
	# not have any difference from the previous clock cycle)
	python run.py <input_filepath> --complete [more optional flags and arguments*]

	# Step-by-step complete output version - you may specify a bigger
	# "clockstep" to speed up the step size between each screen print of
	# the complete solution
	python run.py <input_filepath> --complete --clockstep 1 [more optional flags*]

	# If colors bothers you, just disable they
	python run.py <input_filepath> --complete --nocolor [more optional flags and arguments*]

	# In case your terminal does not like to cooperate with you,
	# try generating a text output file and analyze it with your
	# text editor
	python run.py <input_filepath> --complete --nocolor > output_file.txt

	# *Check README for more information
```

If you need more help about the program usage, just run "run.py" without specifing any additional arguments, or use "-h" or "--help" flags.
```
	# All execution lines below are equivalent
	python run.py
	python run.py -h
	python run.py --help
```

## Output interpretation
If you run the program without the "--complete" flag, then your program output will be likely something similar to
```
-------------------------------------------------------------------------------
PC :    issue     |read_operands |  execution   | write_result | update_flags |
-------------------------------------------------------------------------------
0  :      1       |      2       |      4       |      5       |      6       |
4  :      2       |      3       |      5       |      6       |      7       |
8  :      6       |      7       |      8       |      9       |      10      |
12 :      10      |      11      |      12      |      13      |      14      |
16 :      11      |      15      |      17      |      18      |      19      |
20 :      12      |      13      |      15      |      16      |      17      |
24 :      14      |      15      |      16      |      17      |      18      |
-------------------------------------------------------------------------------
```
This is the "Instruction Status table". The values shown inside it (other than the PC values at the leftmost column) are the clock cycles that the correspondent pipeline stage of the corresponding instruction ended.

If you use the "--complete" flag, then a full relatory of Instruction Status, Functional Unit and Destiny Register Tables (in exactly this order) for all clock cycles (omitting the ones that does not differ from the previous one) will be outputted. In this case, the default behavior of the script is to color encode the tables each step with a "red-green" schema, where green color represent all the fields changed in the corresponding clock cycle. 

If you run the ./test-cases/2.in (python run.py ./test-cases/2.in --complete) input file, the final state of the output would be:

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Final state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 -> Instruction status table:
-------------------------------------------------------------------------------
PC :    issue     |read_operands |  execution   | write_result | update_flags |
-------------------------------------------------------------------------------
0  :      1       |      2       |      4       |      5       |      6       |
4  :      2       |      3       |      5       |      6       |      7       |
8  :      6       |      7       |      8       |      9       |      10      |
12 :      10      |      11      |      12      |      13      |      14      |
16 :      11      |      15      |      17      |      18      |      19      |
20 :      12      |      13      |      15      |      16      |      17      |
24 :      14      |      15      |      16      |      17      |      18      |
-------------------------------------------------------------------------------

 -> Functional Unit status table:
-----------------------------------------------------------------------------------------------------
Functional unit :  busy |  op  | f_i  | f_j  | f_k  |      q_j       |      q_k       | r_j  | r_k  |
-----------------------------------------------------------------------------------------------------
float_div_0     : False |  -   |  -   |  -   |  -   |       -        |       -        | True | True |
load_store_0    : False |  16  |  -   | $sp  |  $3  |       0        |       0        |False |False |
load_store_1    : False |  20  |  -   | $sp  |  $1  |       0        |       0        |False |False |
float_mult_0    : False |  -   |  -   |  -   |  -   |       -        |       -        | True | True |
float_mult_1    : False |  -   |  -   |  -   |  -   |       -        |       -        | True | True |
float_add_sub_0 : False |  -   |  -   |  -   |  -   |       -        |       -        | True | True |
integer_alu_0   : False |  24  |  $1  |  $2  |  -   |       0        |       0        |False |False |
-----------------------------------------------------------------------------------------------------

 -> Destiny Register status table:
$3 : [ 0 ] $1 : [ 0 ] $2 : [ 0 ] [...] (More 62 omitted registers)
```

If you want a more interative step-by-step solution, then you can just use the "--clockstep n" program argument, where "n" is the number of clock cycles that must be outputed before program execution is prompted and asking user to press "ENTER" key in order to proceed. The purpose of this feature is to make easier the user follow up with the scoreboarding execution process.
