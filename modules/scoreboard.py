from collections import OrderedDict

class Scoreboard:
	"""
		Instruction Status:
		An nxm matrix, n = # of instructions in the input code
		and m = number of stages within the scoreboarding pipeline.
		Keeps which clock cycle each instruction finished the corres-
		pondent pipeline stage.

		Functional Unit Status:
		busy:	boolean, keep track in functional unit is busy on the
			current clock cycle or not.

		op:	integer, keep track of the id of the current instruction that
			is currently using the correspondent functional unit.

		f_i:	string, destiny register.

		f_j:	stirng, source register A.

		f_k:	string, source register B.

		q_j:	string, functional unit currently producing f_j, if any.

		q_k:	string, functional unit currently producing f_k, if any.

		r_j:	boolean, indicate if f_j is ready to be read for
			the first time.

		r_k:	boolean, indicate if f_j is ready to be read for
			the first time.
		
		Register Result Status:
		Indicates which functional unit will write in which 
		destiny register, if any.
	"""
	def __init__(self):
		self.func_unit_status = None
		self.reg_res_status = None
		self.inst_status = None
		self.word_size = 0
		self.program_size = 0
		self.DONE_LABEL = "done"

	def load_architecture(architecture):
		self.func_unit_status = {
			func_unit : {
				"busy" : [], 
				"op": [],
				"f_i": [],
				"f_j": [],
				"f_k": [],
				"q_j": [],
				"q_k": [],
				"r_j": [],
				"r_k": [],
			} for func_unit in architecture["functional_units"]
		}

		self.reg_res_status = {
			reg : None for reg in architecture["registers"]
		}

		# MIPS standard: 32 bits
		self.word_size = architecture["word_size"]

	def load_instructions(instructions):
		if self.word_size <= 0:
			raise UserWarning("Instruction size must be >= 1.",
				"Use \"Scoreboard.load_architecture\"",
				"to configure it correctly.")

		self.inst_status = {
			(self.word_size * inst_id) : {
				"issue" : None,
				"read_operand" : None,
				"exec_completed" : None,
				"write_result" : None,
			} for inst_id in len(instructions)
		}

		# #_of_Instructions * word_size
		self.program_size = max(self.inst_status)

	def check_inst_ready(instruction_pack):
		pass

	def bookkeep(instruction_pack):
		pass

	def produce_inst_pack(pc):
		pass

	def run():
		if self.func_unit_status is None or \
			self.reg_res_status is None:
			raise UserWarning("Can't find architecture information.",
				"Please use \"Scoreboard.load_architecture\"",
				"to configure it.")

		if self.inst_status is None:
			raise UserWarning("Can't find input instruction list.",
				"Please use \"Scoreboard.load_instructions\"",
				"to configure it.")

		inst_in_execution = OrderedDict()
		
		pc = 0
		# For each instruction between the not completed
		# former and the most recently one dispatched...
		for inst in inst_in_execution:
			# Check the wait conditions of the current stage
			# of the current instruction
			ready = self.check_inst_ready(inst_in_exectuion[inst])
				
			# If ready, proceed to the next stage
			if ready:
				self.bookkeep(inst_in_execution[inst])

				# Check if current instruction is done
				# (passed by "Write Result" stage
				if inst_in_execution[inst]["stage"] == self.DONE_LABEL:
					inst_in_execution.pop(inst)
					# Move PC if needed
					if pc < self.program_size:
						pc += self.word_size
						inst_in_execution[pc] =\
							self.produce_inst_pack(pc)

		# Produce final output
		ans = {
			"inst_status" : self.inst_status,
			"func_unit_status" : self.func_unit_status,
		}

		return ans
