"""
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	MODULE SYNTHESIS:
	Methods to load the architecture from the
	"configme.py" module and to load assembly 
	input file source code given by the user.
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import sys
sys.path.insert(0, "../")
from configme import Config
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
	def __init__(self):
		# Load regular expressions
		self.re_match_commentary = re.compile(r"#.*$")

		self.re_get_inst_label = re.compile(r"([^\s]+)")

		re_readinst_type_r = re.compile(r"""
			# Regex to match just R-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s,]+)\s*,	# Get destiny register (rd)
			\s*([^\s,]+)\s*,	# Get first operand reg (rs)
			\s*([^\s]+)		# Get second operand reg (rt)
			""", re.VERBOSE)

		re_readinst_type_i = re.compile(r"""
			# Regex to match just I-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s,]+)\s*,	# Get destiny register (rs)
			\s*([-+0-9]+)		# Get the immediate value
			\s*\(([^\s]+)\)		# Get the opperand reg (rt)
			""", re.VERBOSE)

		re_readinst_type_j = re.compile(r"""
			# Regex to match just J-type instructions
			\s*([^\s]+)		# Get instruction label
			\s*([^\s]+)		# Get branch label
			""", re.VERBOSE)

		self.re_list_matchers = {
			"R" : re_readinst_type_r,
			"I" : re_readinst_type_i,
			"J" : re_readinst_type_j,
		}

	def load_architecture(self):
		"""
			All architecture configuration should be set
			in the "configme.py" module.
		"""

		architecture = {
			"functional_units" : {**Config.functional_units},
			"stage_delay" : {**Config.stage_delay},
			"word_size" : Config.WORD_SIZE,
			"registers" : Config.architecture_register_list,
		}

		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			Consistency checking of the configuration
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""

		# Check if architecture word size is a natural positive number
		if architecture["word_size"] <= 0 or type(architecture["word_size"]) is not int:
			raise Exception("Config.WORD_SIZE must be a >= 1 integer.")

		# Check if any register is configured at all
		if len(architecture["registers"]) == 0:
			raise Exception("No registers configured"+\
				" (in \"Config.architecture_register_list\""+\
				" at configme.py module)")

		# Check if the architecture has at least one functional unit
		if len(architecture["functional_units"]) == 0:
			raise Exception("No functional units configured"+\
				" (in \"Config.functional_units\""+\
				" at configme.py module)")

		# Check if all pipeline stages (which don't depend of instructions)
		# has positive delay values
		for pipeline_stage in architecture["stage_delay"]:
			if architecture["stage_delay"][pipeline_stage] <= 0:
				raise Exception("No pipeline stage can have delay <= 0."+\
					" Wait for the quantum version release of this program.")

		# Check if all functional unit delays are positive values
		for func_unit_label in architecture["functional_units"]:
			func_unit = architecture["functional_units"][func_unit_label]
			if func_unit["clock_cycles"] <= 0:
				raise Exception("No functional unit can have delay <= 0."+\
					" Wait for the quantum version release of this program.")
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			End of the configuration consistency checking.
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""

		return architecture

	def load_instructions(self, filepath, architecture):
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			Input file format:

			inst_label_1 reg_dest0, imm(reg_operand)
			inst_label_2 reg_dest1, reg_operand_a, reg_operand_b
			# You can use commentaries with the "#" sign
			inst_label_3 reg_dest2, reg_operand_c, reg_operand_d
			...
			inst_label_n reg_destn, imm(reg_operand) # Commentaries
			# here are allowed.
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			Check out real samples inside "test-cases" directiory.

			Note that all used registers and instructions must be
			declared in the correct dictionary inside the "configme.py" 
			module!
		"""


		# Hold all instructions with some metadata
		instruction_list = []

		with open(filepath) as f:
			program_line_counter = -1
			for instruction_line in f:
				# Remove commentaries, if any
				instruction = self.re_match_commentary.sub("", instruction_line)
				inst_label_match = self.re_get_inst_label.match(instruction)

				if inst_label_match:
					inst_label = inst_label_match.group(1)
					inst_pack = {
						"label" : inst_label, 
						**Config.instruction_list[inst_label],
					}
					inst_type = inst_pack["instruction_type"]

					if inst_type not in {"R", "I", "J"}:
						raise Exception("Unknown instruction type \"" +\
							inst_type + "\". Need be in {\"R\", \"I\", \"J\"}")
					
					program_line_counter += 1
					match = self.re_list_matchers[inst_type].match(instruction)

					if match:
						# Load instruction metadata from configme.py file

						if inst_pack["functional_unit"] not in architecture["functional_units"]:
							raise Exception("Unknown funcional unit \"" + inst_pack["functional_unit"] +\
								"\" of instruction \"" + inst_label + "\" (in line " +\
								str(1 + program_line_counter) + ", PC " + \
								str(program_line_counter * architecture["word_size"]) +")")

						if inst_label in Config.custom_inst_additional_delay:
							inst_pack["additional_cost"] = Config.\
								custom_inst_additional_delay[inst_label]

						if inst_type == "R":
							inst_pack["reg_dest"] = match.group(2)
							inst_pack["reg_source_j"] = match.group(3)
							inst_pack["reg_source_k"] = match.group(4)

						elif inst_type == "I":
							inst_pack["reg_dest"] = match.group(2)
							inst_pack["immediate"] = match.group(3)
							inst_pack["reg_source"] = match.group(4)

						else:
							inst_pack["jmp_label"] = match.group(2)

						instruction_list.append(inst_pack)
					
		return instruction_list

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<input_filepath>")
		exit(1)

	load_module = ReadFile()
	architecture = load_module.load_architecture()
	inst_list = load_module.load_instructions(\
		sys.argv[1], 
		architecture)

	for inst_id in range(len(inst_list)):
		print("{pc:<{fill}}".format(\
			pc=architecture["word_size"] * inst_id, 
			fill=8), inst_list[inst_id])
