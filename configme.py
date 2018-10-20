"""
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	MODULE SYNTHESIS:
	This module is meant to just keep all necessary 
	configuration for the main script.

	All implementation details focus always on the
	code readability and try to be as user-friendly
	as possible, and therefore may not follow the 
	some optimized way. 
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Config:
	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		In the dictionary below you must declare all 
		functional units implemented in the archi-
		tecture. 

		The "key" value must be a string-type whose
		value is any custom functional unit name.

		The "value" must be a dictionary-type with
		the keys "quantity", a integer-type variable 
		which tells how many of the corresponding
		unit is available in the given architecture,
		and "clock_cycles", another integer-type var-
		iable which express how many computer clock
		cycles must be used to the corresponding fun-
		ctional unit to complet it's operation for
		any instruction that uses it.

		Model:
		"functional-unit-name" : {
				"quantity" : int("how-many"),
				"clock_cycles" : int("how-many-delay-clocks"),
		}

		Check predefined examples below for more
		details.
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""

	functional_units = {
		"integer_alu" : {"quantity" : 1, "clock_cycles" : 1},
		"float_add_sub" : {"quantity" : 1, "clock_cycles" : 2},
		"float_mult" : {"quantity" : 2, "clock_cycles" : 10},
		"float_div" : {"quantity" : 1, "clock_cycles" : 40},
	}


	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		In the dictionary below you must declare all
		supported instructions by the architecture.
		The format must be the following:

		"instruction-label" : {
			"functional_unit" : "functional-unit-used",
			"instruction-type" : "single-correspondent-character",
		}

		Please note that "functional-unit-used" MUST BE
		declared in the functional_units dictionary
		just immediately above this commentary block.

		The "instruction-type" follows the MIPS micro-
		processor standards, so it must be a single letter
		between {"R", "I", "J"} representing, respectivelly,
		"Register", "Immediate" and "Jump"-based instructi-
		ons. This parameter affects directly of how the ins-
		truction code will be parsed while reading the input
		assembly code, as it relies on regular expressions. 
		More information is provided in the README file and 
		in the commentaries within "modules/read-input-code.py"
		module source code.
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	instruction_list = {
		"L.D" : {
			"functional_unit" : "integer_alu",
			"instruction_type" : "I",
		},

		"MUL.D" : {
			"functional_unit" : "float_mult",
			"instruction_type" : "R",
		},

		"DIV.D" : {
			"functional_unit" : "float_div",
			"instruction_type" : "R",
		},

		"ADD.D" : {
			"functional_unit" : "float_add_sub",
			"instruction_type" : "R",
		},

		"SUB.D" : {
			"functional_unit" : "float_add_sub",
			"instruction_type" : "R",
		},
	}
	
	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		Delay of scoreboarding non-instruction depen-
		dent pipeline stages.

		Using non-positive values here is illegal.

		format:
		<PIPELINE_STAGE> : int(STAGE_COST_IN_CLOCKS)
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	stage_delay = {
		"issue" : 1,
		"read_operands" : 1,
		"write_result" : 1,
	}

	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		Here you can set ADDITIONAL clock delay to cus-
		tom instructions. This delay will be ADDED DI-
		RECLTY TO THE FUNCTIONAL UNIT that it uses 
		(it DOES NOT OVERRIDE IT!!). 

		So, if you set 1 additional (clock) delay to
		the "L.D" instruction which uses, say, the fun-
		ctional unit "integer_alu" which have 1 clock
		delay too, then each execution os "L.D" instru-
		ction will cost a total of 1 + 1 = 2 clock cycles.

		Using non-positive values here is illegal.

		format:
		<INSTRUCTION_LABEL> : int(ADDITIONAL_CLOCK_CYCLES_COST)
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	custom_inst_additional_delay = {
		"" : 0,
	}

	# Size, in bytes, of a single word size
	WORD_SIZE = 4

	# List here all register implemented in the architecture
	architecture_register_set = {
		"F" + str(i) for i in range(32)
	}.union({"R" + str(i) for i in range(32)})
