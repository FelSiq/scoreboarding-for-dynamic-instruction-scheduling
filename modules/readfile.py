"""
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	MODULE SYNTHESIS:

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import re

class ReadFile:
	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		INPUT FILE INFORMATION:

		The input file format must follow
		the standard assembly code format:

		INSTRUCTION_LABEL_1 arg1, arg2, arg3 # Commentary is
		INSTRUCTION_LABEL_2 arg1, arg2, arg3 # allowed. ;) 
		INSTRUCTION_LABEL_3 arg1, arg2, arg3
		...
		INSTRUCTION_LABEL_n arg1, arg2, arg3

		The instructions itself must follow
		the MIPS microprocessor instruction formats. 
		All instruction used in the input file code
		must also be declared in the config-me.py
		module. All details about how to do this
		is specified in the README file and also
		deeply explained inside the config-me.py
		source code and is strongly recommended
		you spare a few minutes reading it.

		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		MIPS INSTRUCTION TYPES:

		The MIPS microprocessor has three different
		instruction formats: "R", "I" and "J". The
		binary interpretation by the processor for 
		each instruction type is different, but I
		don't expect you to think deeply about this 
		while using this program. Which you truly need
		to know is the "human format" of each type of
		instruction, which must be strictly followed
		in order to everything happen just as expec-
		ted, so I'll remember you this formats imme-
		diately below.

		Type "R":
			INSTRUCTION_LABEL REG_DEST, REG_OPERAND_1, REG_OPERAND_2

		Type "I":
			INSTRUCTION_LABEL REG_DEST, IMMEDIATE_VALUE(REG_OPERAND)

			Note: IMMEDIATE_VALUE must be a SIGNED INTEGER. (like
			16 or -12).

		Type "J":
			INSTRUCTION_LABEL JUMP_LABEL

			Note: JUMP_LABEL must be a label specified somewhere
			in the given input code.

		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__():
		# Load regular expressions
		re_match_commentary = re.compile(r"#.*$")

		re_readinst_type_r = re.compile("""
			# Regex to match just R-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s]+)\s*,		# Get destiny register (rd)
			\s*([^\s]+)\s*,		# Get first operand reg (rs)
			\s*([^\s]+)		# Get second operand reg (rt)
			""", re.VERBOSE)

		re_readinst_type_i = re.compile("""
			# Regex to match just I-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s]+)\s*,		# Get destiny register (rs)
			\s*([-+0-9]+)		# Get the immediate value
			\s*\(([^\s]+)\)		# Get the opperand reg (rt)
			""", re.VERBOSE)

		re_readinst_type_j = re.compile("""
			# Regex to match just J-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s]+)		# Get branch label
			""", re.VERBOSE)
