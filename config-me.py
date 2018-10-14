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
		"float_add_sub" : {"quantity" : 1, "clock_cycles" : 1},
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

		As additional information, this script is meant
		to be entirely case-insensitive, so you don't need
		to consider differences between "Add" and "add".
		Please note that Python allows you to create both
		UPPER-CASED and lower-cased dictionary keys represen-
		ting different values, so keep in mind that this can 
		lead to "undefined behavior" during the program exe-
		cution, and by "undefined" I meant "whatever I will 
		consider the best way to work this 'anomally' around 
		when coding the main module". I suggest you to not 
		try breaking this script unless you want to see it
		broken.
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	instruction_list = {
		"add" : {
			"functional_unit" : "integer_alu",
			"instruction_type" : "R",
		},

		"l.d" : {
			"functional_unit" : "integer_alu",
			"instruction_type" : "I",
		},

		"mul.d" : {
			"functional_unit" : "float_mult",
			"instruction_type" : "R",
		},
	}
