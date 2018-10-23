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
		self.PIPELINE_STAGES = [
			"issue", 
			"read_operands", 
			"execution", 
			"write_result"
		]

		self.global_clock_timer = 0
		
		# Auxiliar structure to accumulate all changes in the 
		# current clock cycle in order to prevent interferences 
		# from changes of each instruction to the next instruc-
		# tions within the same clock cycle
		self.__to_commit_this_clock = {}

	def load_architecture(self, architecture):
		self.func_unit_status = {
			func_unit : {
				"busy" : [False], 
				"op": [-1],
				"f_i": [None],
				"f_j": [None],
				"f_k": [None],
				"q_j": [None],
				"q_k": [None],
				"r_j": [True],
				"r_k": [True],
				"update_timers": [{
					"clock" : -1, 
					"changed_fields" : set(),
					"changed_register_set" : set(),
				}],
			} for func_unit in architecture["functional_units"]
		}

		self.reg_res_status = {
			reg : [0] for reg in architecture["registers"]
		}

		# Keep a pointer to the dictionary delay of each pipeline stage
		self.stage_delay = architecture["stage_delay"]

		# Keep a pointer to the functional unit list
		self.functional_units = architecture["functional_units"]

		# MIPS standard: 32 bits
		self.word_size = architecture["word_size"]

	def load_instructions(self, instructions):
		if self.word_size <= 0:
			raise UserWarning("Instruction size must be >= 1.",
				"Use \"Scoreboard.load_architecture\"",
				"to configure it correctly.")

		# Identify the instructions by the PC
		self.inst_status = {
			(self.word_size * inst_id) : {
				stage_label : None
				for stage_label in self.PIPELINE_STAGES
			} for inst_id in range(len(instructions))
		}

		# program_size = #_of_Instructions * word_size
		self.program_size = max(self.inst_status) + self.word_size

		# Keep pointer to instruction list
		self.instruction_list = instructions

	def __check_inst_ready(self, cur_inst_pc, cur_inst_stage):
		# Take into account scoreboarding wait tests +
		# clock costs and global clock counter

		if cur_inst_stage != "issue":
			total_cost = 0

			# Method here ~~~~~
			cur_inst_metadata = self.instruction_list[\
				cur_inst_pc // self.word_size]

			cur_inst_func_unit = cur_inst_metadata["functional_unit"]

			if cur_inst_stage == "execution":
				total_cost += self.functional_units[cur_inst_func_unit]["clock_cycles"]

			if cur_inst_stage in self.stage_delay:
				total_cost += self.stage_delay[cur_inst_stage]

			if "additional_cost" in cur_inst_metadata:
				total_cost += cur_inst_metadata["additional_cost"]
			# Method here ~~~~~

			cur_inst_stage_cost = total_cost + self.inst_status[cur_inst_pc]\
				[self.PIPELINE_STAGES[self.PIPELINE_STAGES.index(cur_inst_stage) - 1]]

			# Check if current global clock counter already
			# satisfies current instruction pipeline stage cost

			if cur_inst_stage_cost > self.global_clock_timer:
				# Pipeline stage of this instruction not
				# ready yet, return False
				return False

		# Extract some metadata from the current instruction
		cur_inst_metadata = self.instruction_list[\
			cur_inst_pc // self.word_size]
		cur_inst_label = cur_inst_metadata["label"]
		cur_inst_func_unit = cur_inst_metadata["functional_unit"]

		if cur_inst_stage == "issue":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Issue" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			cur_inst_reg_dest = cur_inst_metadata["reg_dest"]
			if not self.func_unit_status[cur_inst_func_unit]["busy"][-1] and\
				not self.reg_res_status[cur_inst_reg_dest][-1]:
				return True

		elif cur_inst_stage == "read_operands":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Read Operands" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			if self.func_unit_status[cur_inst_func_unit]["r_j"][-1] and \
				self.func_unit_status[cur_inst_func_unit]["r_k"][-1]:
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
			cur_inst_f_i = self.func_unit_status[cur_inst_func_unit]["f_i"][-1]

			for loop_func_unit_label in self.func_unit_status:
				loop_cur_func_unit = self.func_unit_status[loop_func_unit_label]

				if len(loop_cur_func_unit["f_j"]) and \
					loop_cur_func_unit["f_j"][-1] == cur_inst_f_i and\
					loop_cur_func_unit["r_j"][-1]:
					return False

				if len(loop_cur_func_unit["f_k"]) and \
					loop_cur_func_unit["f_k"][-1] == cur_inst_f_i and\
					loop_cur_func_unit["r_k"][-1]:
					return False

			return True

		# Return False by default
		return False

	def __issuepack(self, cur_inst_metadata):
		"""
			Return several information related to the
			"Issue" stage for the current instruction.
		"""
		cur_inst_type = cur_inst_metadata["instruction_type"]

		issue_pack = {
			"f_i" : None,
			"f_j" : None,
			"f_k" : None,
			"q_j" : None,
			"q_k" : None,
			"r_j" : None,
			"r_k" : None,
		}

		if cur_inst_type == "R":
			issue_pack["f_i"] = cur_inst_metadata["reg_dest"]
			issue_pack["f_j"] = cur_inst_metadata["reg_source_j"]
			issue_pack["f_k"] = cur_inst_metadata["reg_source_k"]
			issue_pack["q_j"] = self.reg_res_status[\
				cur_inst_metadata["reg_source_j"]][-1]
			issue_pack["q_k"] = self.reg_res_status[\
				cur_inst_metadata["reg_source_k"]][-1]
			issue_pack["r_j"] = issue_pack["q_j"] == 0
			issue_pack["r_k"] = issue_pack["q_k"] == 0

		elif cur_inst_type == "I":
			issue_pack["f_i"] = cur_inst_metadata["reg_dest"]
			issue_pack["f_j"] = cur_inst_metadata["reg_source"]
			issue_pack["q_j"] = self.reg_res_status[\
				cur_inst_metadata["reg_source"]][-1]
			issue_pack["r_j"] = issue_pack["q_j"] == 0
			issue_pack["r_k"] = True

		else:
			# Type J
			pass

		return issue_pack

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
		cur_func_unit_status = self.func_unit_status[cur_inst_func_unit]

		# Auxiliary data structure to keep all changes of
		# the current clock to prevent interference between
		# instructions within the same clock cycle
		self.__to_commit_this_clock[cur_inst_func_unit] = {
			"fields" : {},
			"registers" : {},
		}
		cur_func_unit_status_aux = self.__to_commit_this_clock\
			[cur_inst_func_unit]["fields"]
		cur_registers_status_aux = self.__to_commit_this_clock\
			[cur_inst_func_unit]["registers"]

		# Keep track of which scoreboard field are changed
		# in this bookkepping call
		changed_field_set = set()

		# The same as above, but with the destiny register
		# status list
		changed_register_set = set()

		# Bookkeep based on the current instruction
		# pipeline stage
		if cur_inst_stage == "issue":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Issue" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			# Select, based on the instruction type "R", "I" or "J"
			# the corrent values to be appended in the scoreboard
			issue_pack = self.__issuepack(cur_inst_metadata)

			cur_func_unit_status_aux["busy"] = True
			cur_func_unit_status_aux["op"] = cur_inst_pc
			cur_func_unit_status_aux["f_i"] = issue_pack["f_i"]
			cur_func_unit_status_aux["f_j"] = issue_pack["f_j"]
			cur_func_unit_status_aux["f_k"] = issue_pack["f_k"]
			cur_func_unit_status_aux["q_j"] = issue_pack["q_j"]
			cur_func_unit_status_aux["q_k"] = issue_pack["q_k"]
			cur_func_unit_status_aux["r_j"] = issue_pack["r_j"]
			cur_func_unit_status_aux["r_k"] = issue_pack["r_k"]
			cur_registers_status_aux[issue_pack["f_i"]] = cur_inst_func_unit

			changed_field_set.update({\
				"busy", "op", "f_i", 
				"f_j", "f_k", "q_j", 
				"q_k", "r_j", "r_k"
			})
			changed_register_set.update({issue_pack["f_i"]})

		elif cur_inst_stage == "read_operands":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Read Operands" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			cur_func_unit_status_aux["r_j"] = False
			cur_func_unit_status_aux["r_k"] = False
			cur_func_unit_status_aux["q_j"] = 0
			cur_func_unit_status_aux["q_k"] = 0

			changed_field_set.update({"r_j", "r_k", "q_j", "q_k"})

		elif cur_inst_stage == "execution":
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Execution" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			pass

		else:
			"""
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				Pipeline "Write Result" stage
				~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""
			# For all functional units waiting for the
			# current functional unit finalize for any of
			# the operand register, set the ready flags to true
			for loop_func_unit_label in self.func_unit_status:
				loop_cur_func_unit = self.func_unit_status[loop_func_unit_label]

				if loop_func_unit_label not in self.__to_commit_this_clock:
					self.__to_commit_this_clock[loop_func_unit_label] = {\
						"fields" : {},
						"registers" : {},
					}

				loop_cur_func_unit_aux = self.__to_commit_this_clock\
					[loop_func_unit_label]["fields"]
					
				loop_cur_changed_field_set = set()

				if len(loop_cur_func_unit["q_k"]) and\
					loop_cur_func_unit["q_k"][-1] == cur_inst_func_unit:
					loop_cur_func_unit_aux["r_k"] = True
					loop_cur_changed_field_set.update({"r_k"})

				if len(loop_cur_func_unit["q_j"]) and\
					loop_cur_func_unit["q_j"][-1] == cur_inst_func_unit:
					loop_cur_func_unit_aux["r_j"] = True
					loop_cur_changed_field_set.update({"r_j"})

				loop_cur_func_unit_aux["update_timers"] = {\
					"clock" : self.global_clock_timer,
					"changed_fields" : loop_cur_changed_field_set,
					"changed_register_set" : set(),
				}

			# Current functional unit current register
			cur_inst_f_i = cur_func_unit_status["f_i"][-1]

			# The destiny register of the current instruction
			# does not depend of any functional unit anymore
			cur_registers_status_aux[cur_inst_f_i] = 0
			cur_func_unit_status_aux["busy"] = False

			changed_field_set.update({"busy"})
			changed_register_set.update({cur_inst_f_i})

		# Mark the current clock cycle plus stage cost in the
		# instruction status
		self.inst_status[cur_inst_pc][cur_inst_stage] =\
			self.global_clock_timer

		# Keep track of which clock corresponds to
		# the current change in order to print corre-
		# ctly after process ends
		cur_func_unit_status_aux["update_timers"] = {\
			"clock" : self.global_clock_timer,
			"changed_fields" : changed_field_set,
			"changed_registers" : changed_register_set,
		}
		
		# Check if instruction was completed
		if cur_inst_stage != self.PIPELINE_STAGES[-1]:
			return self.PIPELINE_STAGES[1 + \
				self.PIPELINE_STAGES.index(cur_inst_stage)]
		return None

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

		# Make sure the auxiliary unit for inner-clock changes
		# is clean
		self.__to_commit_this_clock = {}

		while cur_min_pc < self.program_size:
			self.global_clock_timer += 1

			# For each instruction between the not completed
			# former and the most recently one dispatched...
			for cur_inst_pc in range(cur_min_pc, cur_max_pc + self.word_size, self.word_size):
				# Check the wait conditions of the current stage
				# of the current instruction
				if self.inst_status[cur_inst_pc][LAST_PIPELINE_STAGE] is None:
					# Keep track of the current pipeline stage of
					# each active (dispatched + not completed) instruction
					if cur_inst_pc not in inst_cur_stage:
						inst_cur_stage[cur_inst_pc] = FIRST_PIPELINE_STAGE
					cur_inst_stage = inst_cur_stage[cur_inst_pc]

					# If ready, proceed to the next stage
					if self.__check_inst_ready(cur_inst_pc, cur_inst_stage):
						new_inst_stage = self.__bookkeep(\
								cur_inst_pc, 
								cur_inst_stage,
								cur_min_pc, 
								cur_max_pc)

						# Update current instruction new pipeline stage
						if new_inst_stage:
							inst_cur_stage[cur_inst_pc] = new_inst_stage
						else:
							inst_cur_stage.pop(cur_inst_pc)

						if inst_cur_stage:
							cur_min_pc = min(inst_cur_stage)
							cur_max_pc = min(self.program_size - self.word_size, \
								max(cur_inst_pc + self.word_size, \
								max(inst_cur_stage)))
						else:
							cur_min_pc = cur_max_pc = self.program_size

			# Commit all changes made in the current clock
			for func_unit_label in self.__to_commit_this_clock:
				cur_func_unit_changes = self.__to_commit_this_clock[func_unit_label]
				cur_func_unit_status = self.func_unit_status[func_unit_label]
				# Do fields changes
				cur_f_u_field_changes = cur_func_unit_changes["fields"]
				for field in cur_f_u_field_changes:
					cur_func_unit_status[field].append(cur_f_u_field_changes[field])

				# Do register changes
				cur_f_u_reg_changes = cur_func_unit_changes["registers"]
				for register_label in cur_f_u_reg_changes:
					self.reg_res_status[register_label].append(\
						cur_f_u_reg_changes[register_label])

			# Clean up all changes
			self.__to_commit_this_clock = {}

		# Produce final output
		ans = {
			"inst_status" : self.inst_status,
			"func_unit_status" : self.func_unit_status,
		}

		return ans
