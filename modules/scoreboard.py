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
		self.PIPELINE_STAGES = [
			"issue", 
			"read_operands", 
			"execution", 
			"write_result"
		]
		self.global_clock_timer = 0

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
				"update_timers": [],
			} for func_unit in architecture["functional_units"]
		}

		self.reg_res_status = {
			reg : None for reg in architecture["registers"]
		}

		self.stage_costs = architecture["stage_costs"]

		self.functional_units = architecture["functional_units"]

		# MIPS standard: 32 bits
		self.word_size = architecture["word_size"]

	def load_instructions(instructions):
		if self.word_size <= 0:
			raise UserWarning("Instruction size must be >= 1.",
				"Use \"Scoreboard.load_architecture\"",
				"to configure it correctly.")

		# Identify the instructions by the PC
		self.inst_status = {
			(self.word_size * inst_id) : {
				stage_label : None
				for stage_label in self.PIPELINE_STAGES
			} for inst_id in len(instructions)
		}

		# program_size = #_of_Instructions * word_size
		self.program_size = max(self.inst_status) + self.word_size

		# Keep pointer to instruction list
		self.instruction_list = instructions

	def __check_inst_ready(self, cur_inst_pc, cur_inst_stage):
		# Take into account scoreboarding wait tests +
		# clock costs and global clock counter

		cur_inst_stage_cost = self.architecture\
			["stage_costs"][cur_inst_stage] + additional_cost

		# Check if current global clock counter already
		# satisfies current instruction pipeline stage cost
		if cur_inst_stage_cost < self.global_clock_timer:
			# Pipeline stage of this instruction not
			# ready yet, return False
			return False

		# Extract some metadata from the current instruction
		cur_inst_metadata = self.instruction_list[\
			cur_inst_pc // self.word_size]
		cur_inst_label = cur_inst_metadata["label"]
		cur_inst_func_unit = cur_inst_metadata["functional_unit"]

		cur_inst_f_i = None
		...

		if cur_inst_stage == "issue":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Issue" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			if not self.func_unit_status[cur_inst_func_unit]["busy"] and\
				not self.reg_res_status[cur_inst_reg_dest]:
				return True

		elif cur_inst_stage == "read_operands":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Read Operands" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			if self.func_unit_status[cur_inst_func_unit]["r_j"] and \
				self.func_unit_status[cur_inst_func_unit]["r_k"]:
				return True

		elif cur_inst_stage == "execution":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Execution" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			return True

		else:
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Write Result" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			for loop_func_unit_label in self.func_unit_status:
				loop_cur_func_unit = self.func_unit_status[loop_func_unit_label]

				if loop_cur_func_unit["f_j"][-1] == cur_inst_f_i and\
					not loop_cur_func_unit["r_j"][-1]:
					return False

				if loop_cur_func_unit["f_k"][-1] == cur_inst_f_i and\
					not loop_cur_func_unit["r_k"][-1]:
					return False

			return True

		# Return False by default
		return False

	def __update_counters(self, 
		cur_inst_pc, 
		cur_inst_stage, 
		cur_min_pc, 
		cur_max_pc):

		if cur_inst_stage == self.PIPELINE_STAGES[-1]:
			cur_inst_stage = None

			# Move program counter window, if needed
			if cur_inst_pc == cur_max_pc and \
				cur_max_pc < self.program_size:
				cur_max_pc += self.word_size

			elif cur_inst_pc == cur_min_pc:
				cur_min_pc += self.word_size
		else:
			# Set the current instruction state to
			# the next pipeline stage
			cur_inst_stage = self.PIPELINE_STAGES[1 +\
				self.PIPELINE_STAGES.index(cur_inst_stage)]

		return cur_inst_stage, cur_min_pc, cur_max_pc

	def __bookkeep(self, 
		cur_inst_pc, 
		cur_inst_stage, 
		cur_min_pc, 
		cur_max_pc):

		# Extract current instruction metadata
		cur_inst_metadata = self.instruction_list[\
			cur_inst_pc // self.word_size]
		cur_inst_label = cur_inst_metadata["label"]
		cur_inst_func_unit = cur_inst_metadata["functional_unit"]
		cur_inst_type = cur_inst_metadata["instruction_type"]
		cur_func_unit_status = self.funct_unit_status[cur_inst_func_unit]

		cur_inst_f_i = None
		cur_inst_f_j = None
		cur_inst_f_k = None
		cur_inst_q_j = None
		cur_inst_q_k = None
		cur_inst_r_j = None
		cur_inst_r_k = None
		...

		stage_cost = 0

		# Add basic stage cost
		if cur_inst_stage in self.stage_costs:
			stage_cost += self.stage_costs[cur_inst_stage]

		# Bookkeep based on the current instruction
		# pipeline stage
		if cur_inst_stage == "issue":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Issue" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			cur_func_unit_status["busy"].append(True)
			cur_func_unit_status["op"].append(cur_inst_pc)
			cur_func_unit_status["f_i"].append(cur_inst_f_i)
			cur_func_unit_status["f_j"].append(cur_inst_f_j)
			cur_func_unit_status["f_k"].append(cur_inst_f_k)
			cur_func_unit_status["q_j"].append(cur_inst_q_j)
			cur_func_unit_status["q_k"].append(cur_inst_q_k)
			cur_func_unit_status["r_j"].append(cur_inst_r_j)
			cur_func_unit_status["r_k"].append(cur_inst_r_k)
			self.reg_res_status[cur_inst_f_i].append(cur_inst_func_unit)

		elif cur_inst_stage == "read_operands":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Read Operands" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			cur_func_unit_status["r_j"].append(False)
			cur_func_unit_status["r_k"].append(False)
			cur_func_unit_status["q_j"].append(0)
			cur_func_unit_status["q_k"].append(0)

		elif cur_inst_stage == "execution":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Execution" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			# Add cost from the functional unit execution delay
			stage_cost += self.functional_units[cur_inst_func_unit]["clock_cycles"]

			# Check if current instruction has an custom additional cost
			if "additional_cost" in cur_inst_metadata:
				stage_cost += cur_inst_metadata["additional_cost"]

		else:
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Write Result" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			# Copying this code line because "Write Result" stage
			# demands this calculation sooner
			total_cost = self.global_clock_timer + stage_cost

			# For all functional units waiting for the
			# current functional unit finalize for any of
			# the operand register, set the ready flags to true
			for loop_func_unit_label in self.func_unit_status:
				loop_cur_func_unit = self.func_unit_status[loop_func_unit_label]

				if loop_cur_func_unit["q_k"][-1] == cur_func_unit:
					loop_cur_func_unit["r_k"].append(True)

				if loop_cur_func_unit["q_j"][-1] == cur_func_unit:
					loop_cur_func_unit["r_j"].append(True)

				loop_cur_func_unit["update_timers"].append(total_cost)

			self.reg_res_status[cur_inst_f_i].append(0)
			cur_func_unit_status["busy"].append(False)

		# Mark the current clock cycle plus stage cost in the
		# instruction status
		total_cost = self.global_clock_timer + stage_cost
		self.inst_states[cur_inst_stage] = total_cost

		# Keep track of which clock corresponds to
		# the current change in order to print corre-
		# ctly after process ends
		cur_func_unit_status["update_timers"].append(total_cost)
		
		# Check if instruction was completed
		return self.__update_counters(
			cur_inst_pc, 
			cur_inst_stage, 
			cur_min_pc, 
			cur_max_pc)

	def run(self):
		# Check if user called "load_architecture" method before
		if self.func_unit_status is None or \
			self.reg_res_status is None:
			raise UserWarning("Can't find architecture information.",
				"Please use \"Scoreboard.load_architecture\"",
				"to configure it.")

		# Check if user called "load_instructions" method before
		if self.inst_status is None:
			raise UserWarning("Can't find input instruction list.",
				"Please use \"Scoreboard.load_instructions\"",
				"to configure it.")

		# Keep track of the current pipeline stage of
		# each dispatched & not completed instruction, in order
		# to speed up the code execution
		inst_cur_stage = {}

		# Some auxiliary constants to clean up & speed up the code
		LAST_PIPELINE_STAGE = self.PIPELINE_STAGES[-1]
		FIRST_PIPELINE_STAGE = self.PIPELINE_STAGES[0]

		# Dispatched & not completed instruction window
		cur_min_pc = 0
		cur_max_pc = 0

		while cur_min_pc < self.program_size:
			self.global_clock_timer += 1

			# For each instruction between the not completed
			# former and the most recently one dispatched...
			for cur_inst_pc in range(cur_min_pc, cur_max_pc + self.word_size):
				# Check the wait conditions of the current stage
				# of the current instruction
				if self.inst_status[cur_inst_id][LAST_PIPELINE_STAGE] is not None:

					# Keep track of the current pipeline stage of
					# each active (dispatched + not completed) instruction
					if cur_inst_pc not in inst_cut_stage:
						inst_cur_stage[cur_inst_pc] = FIRST_PIPELINE_STAGE
					cur_inst_stage = inst_cur_stage[cur_inst_pc]

					# If ready, proceed to the next stage
					if self.__check_inst_ready(cur_inst_pc, cur_inst_stage):
						new_inst_stage, cur_max_pc, cur_min_pc = \
							self.__bookkeep(\
								cur_inst_pc, 
								cur_inst_stage,
								cur_min_pac, 
								cur_max_pc)

						# Update current instruction new pipeline stage
						if new_inst_stage:
							inst_cur_stage[cur_inst_pc] = new_inst_stage
						else:
							inst_cur_stage.pop(cur_inst_pc)

		# Produce final output
		ans = {
			"inst_status" : self.inst_status,
			"func_unit_status" : self.func_unit_status,
		}

		return ans
