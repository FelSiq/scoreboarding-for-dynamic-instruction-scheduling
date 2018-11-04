from colorama import Fore, Style, init as colorama_init
"""
	Module dedicated to produce all program
	output if option "-nogui" is enabled by the
	user in the command line.
"""

class TextualInterface:
	def __init__(self, ans):

		# Maximum PC value of the input instruction set
		max_pc = max(ans["inst_status"])

		# Dummy pointers to increase code readability
		reg_status = ans["reg_dest_status"]
		func_unit_status = ans["func_unit_status"]

		# Order which the instruction status table
		# print method must follow
		self.__inst_print_order = [
			"issue", "read_operands",
			"execution", "write_result"
		]

		if "update_flags" in ans["pipeline_stages"]:
			self.__inst_print_order.append("update_flags")

		# Get the maximum length of the instruction
		# table status field labels declared above
		# ("__inst_print_order")
		self.__inst_fill_len = max([
			len(label) for label in \
			self.__inst_print_order
		]) + 1

		# Print order which functional unit status 
		# table print method must follow
		self.__fu_print_order = [
			"busy", "op", "f_i", "f_j", 
			"f_k", "q_j", "q_k", "r_j", "r_k"
		]

		# Get the maximum length of the labels
		# declared above ("__fu_print_order")
		self.__fu_fill_len_labels = max([
			len(label) for label in \
			self.__fu_print_order
		]) + 2


		# Get the maximum length of the functional unit
		# names concatenated with its ID number
		self.__fu_fill_len_fus = max([
			len(fu_label + str(replica_id))
			for fu_label in func_unit_status
			for replica_id in func_unit_status[fu_label]
		]) + 2

		# Custom spacing for each field in functional 
		# unit status table
		self.__fu_fill_custom_spacing = {
			label : self.__fu_fill_len_labels
			for label in self.__fu_print_order
		}
		self.__fu_fill_custom_spacing["q_j"] = self.__fu_fill_len_fus
		self.__fu_fill_custom_spacing["q_k"] = self.__fu_fill_len_fus

		# Maximum length of the largest PC casted
		# to a string/character type
		self.__max_pc_len = len(str(max_pc)) + 1

		# Count how many registers are not used ever
		# using the given instruction input code
		# sequence (no need to print then)
		self.__ommited_reg_count = sum([
			len(reg_status[reg_label]) <= 1
			for reg_label in reg_status
		])

		# Decoration for functional unit table (horizontal line)
		self.__FU_HORIZ_LINE = (self.__fu_fill_len_fus + 2 +\
			len(self.__fu_fill_custom_spacing) +\
			sum(self.__fu_fill_custom_spacing.values())) * "-"

		# Same as above, but this time for the instruction status
		# table
		self.__INST_HORIZ_LINE = (1 + self.__max_pc_len +\
			(self.__inst_fill_len + 1) * \
			len(self.__inst_print_order)) * "-"

	def __inst_status_table(self, 
		inst_status, 
		clock, 
		colored=True):

		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			START OF Instruction status table Header
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""
		print(self.__INST_HORIZ_LINE)
		print("{val:<{fill}}".format(val="PC", 
			fill=self.__max_pc_len), end=":")
		for print_label in self.__inst_print_order:
			print("{:^{fill}}".format(\
				print_label, fill=self.__inst_fill_len), end="|")
		print("\n", self.__INST_HORIZ_LINE, sep="")
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			END OF Instruction status table Header
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			START OF Instruction status table body
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""

		for pc in sorted(list(inst_status.keys())):
			print("{val:<{fill}}".format(val=pc, fill=self.__max_pc_len), end=":")
			for stage_id in range(len(self.__inst_print_order)):
				val=inst_status[pc][self.__inst_print_order[stage_id]]
				if colored:
					color = Fore.RED if clock != val else Fore.GREEN
					color_reseter = Style.RESET_ALL
				else:
					color = ""
					color_reseter = ""

				print(color + \
					"{:^{fill}}".format(val if val <= clock else "", 
					fill=self.__inst_fill_len) + color_reseter, end="|")
			print()
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			END OF Instruction status table body
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""
		print(self.__INST_HORIZ_LINE)

	def __update_print_indexes(self, 
		cur_func_unit_status,
		cur_update_timers,
		func_unit_print_index,
		index_holder, 
		reg_index_holder,
		func_unit_label, 
		replica_id,
		this_clock_updated_regs,
		clock):
		"""
			This method synchronize the counters of each
			functional unit output metadata and the fields
			metadata. 

			I've had a hard time because I wasn't remembering 
			that these counters are different. The same logic must 
			be applied to the register status table, so watch out
			for this very important detail.
		"""
		# Functional unit print index update
		if func_unit_print_index < len(cur_update_timers)-1 and\
			cur_update_timers[func_unit_print_index+1]["clock"] <= clock:
			index_holder[func_unit_label][replica_id]["func_unit_print_index"] += 1
			func_unit_print_index += 1

		# Field print index update
		if cur_update_timers[func_unit_print_index]["clock"] == clock:
			for changed_field_label in cur_update_timers[func_unit_print_index]["changed_fields"]:
				if index_holder[func_unit_label][replica_id]\
					["field_index"][changed_field_label] < \
					len(cur_func_unit_status[changed_field_label])-1:
					index_holder[func_unit_label][replica_id]\
						["field_index"][changed_field_label] += 1

			for changed_reg_label in cur_update_timers[func_unit_print_index]["changed_registers"]:
				reg_index_holder[changed_reg_label] += 1
				this_clock_updated_regs.update({changed_reg_label})

		return func_unit_print_index

	def __prepare_value(self, val, none_symbol="-"):
		"""
			Process value for functional unit 
			status table print method.
		"""
		# If type is a tuple, then it is a 
		# (func_unit_label, replica_id) pair. 
		# Concatenate then using "_" symbol.
		if type(val) == type(()):
			val = "_".join(map(str, val))

		# Cast value to string/character type,
		# if it is not a None value
		if val is not None:
			val = str(val)
		else:
			val = none_symbol

		# Value processing finished
		return val
		

	def __func_unit_table(self, 
		func_unit_status, 
		clock, 
		index_holder, 
		reg_index_holder,
		colored=True):

		this_clock_updated_regs = set()

		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			START OF Functional unit status table Header
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""
		print(self.__FU_HORIZ_LINE)
		print("{val:<{fill}}".format(val="Functional unit", 
			fill=self.__fu_fill_len_fus), end=": ")
		for print_label in self.__fu_print_order:
			print("{:^{fill}}".format(\
				print_label, 
				fill=self.__fu_fill_custom_spacing[print_label]), 
				end="|")
		print("\n", self.__FU_HORIZ_LINE, sep="")
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			END OF Functional unit status table Header
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			START OF Functional unit status table body
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""

		for func_unit_label in func_unit_status:
			for replica_id in func_unit_status[func_unit_label]:
				# Pull off some dummy variables to increase
				# code readability
				cur_func_unit_status = func_unit_status\
					[func_unit_label][replica_id]
				cur_update_timers = cur_func_unit_status["update_timers"]
				func_unit_print_index = index_holder[func_unit_label]\
					[replica_id]["func_unit_print_index"]

				# Update indexes to keep track of current state
				# of execution
				func_unit_print_index = self.__update_print_indexes(\
					cur_func_unit_status,
					cur_update_timers,
					func_unit_print_index,
					index_holder,
					reg_index_holder,
					func_unit_label,
					replica_id,
					this_clock_updated_regs,
					clock)

				# Functional unit name concatenated with its
				# id between each replicas
				print("{val:<{fill}}".format(\
					val=(func_unit_label + "_" + str(replica_id)), 
					fill=self.__fu_fill_len_fus), end=": ")

				# Effectively print this functional unit status fields
				for table_label in self.__fu_print_order:
					print_index = index_holder[func_unit_label]\
						[replica_id]["field_index"][table_label]

					"""
						~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
						START OF current functional unit field status preparation
						~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
					"""
					val = self.__prepare_value(\
						cur_func_unit_status[table_label][print_index])

					if colored:
						color = Fore.GREEN if \
							(table_label in cur_update_timers\
								[func_unit_print_index]["changed_fields"] and \
							cur_update_timers[func_unit_print_index]["clock"] == clock)\
							else Fore.RED
						color_reseter = Style.RESET_ALL
					else:
						color = ""
						color_reseter = ""
					"""
						~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
						END OF current functional unit field status preparation
						~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
					"""

					print(color + \
						"{:^{fill}}".format(val if val else " ", 
						fill=self.__fu_fill_custom_spacing[table_label]) +\
						color_reseter, end="|")
				print()
		"""
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			END OF Functional unit status table Body
			~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""
		print(self.__FU_HORIZ_LINE)

		return this_clock_updated_regs

	def __reg_dest_table(self, 
		reg_dest_status, 
		clock, 
		index_holder,
		this_clock_updated_regs,
		colored=True):

		for reg_label in reg_dest_status:
			if len(reg_dest_status[reg_label]) > 1:
				print_index = index_holder[reg_label]

				if colored:
					color = Fore.GREEN \
						if reg_label in this_clock_updated_regs\
						else Fore.RED
					color_reseter = Style.RESET_ALL
				else:
					color = ""
					color_reseter = ""

				print(reg_label, ": [", color +\
					self.__prepare_value(reg_dest_status[reg_label][print_index]) +\
					color_reseter, "]", end=" ")

		if self.__ommited_reg_count > 0:
			print("[...] (More", 
				self.__ommited_reg_count, 
				"ommited registers)", 
				end="")
		print()

	def __full_output(self,
		ans, 
		clock_steps=-1,
		decorate="~", 
		item_symbol="->", 
		quantity=100,
		colored=True):

		colorama_init()

		# Fancy decoration line for separate interface elements
		sep_line = decorate * quantity

		# Structure used to orchestrate the print indexes of
		# functional unit output metadata and functional unit
		# fields current data index
		index_holder = { 
			"fields" : {
				func_unit : {
					replica_id : {
						"field_index" : {
							field_label : 0
							for field_label in\
								ans["func_unit_status"][func_unit][replica_id]
						},
						"func_unit_print_index" : 0,
					} for replica_id in ans["func_unit_status"][func_unit]
				} for func_unit in ans["func_unit_status"]
			},
			"registers" : {
				reg_id : 0
				for reg_id in ans["reg_dest_status"]
			}
		}

		prompt_counter = clock_steps
		state_counter = -1

		FINAL_CLOCK_VAL = ans["update_timers"][-1] + 1

		for clock in sorted(ans["update_timers"] + [FINAL_CLOCK_VAL]):
			print(sep_line, ("State for clock cycle " + str(clock) +\
					" of " + str(FINAL_CLOCK_VAL - 1) + " total")\
				if clock != FINAL_CLOCK_VAL \
				else "Final state", 
				sep_line, sep="\n")
			"""
				Instruction status table
			"""
			print("\n", item_symbol, "Instruction status table:")
			self.__inst_status_table(
				ans["inst_status"], 
				clock, 
				colored and clock != FINAL_CLOCK_VAL)

			"""
				Functional Unit status table
			"""
			print("\n", item_symbol, "Functional Unit status table:")
			this_clock_updated_regs = self.__func_unit_table(ans["func_unit_status"], 
				clock, 
				index_holder["fields"], 
				index_holder["registers"], 
				colored and clock != FINAL_CLOCK_VAL)

			"""
				Destiny Register status table
			"""
			print("\n", item_symbol, "Destiny Register status table:")
			self.__reg_dest_table(ans["reg_dest_status"], 
				clock, 
				index_holder["registers"], 
				this_clock_updated_regs,
				colored and clock != FINAL_CLOCK_VAL)

			# Interrupt process if user specify a positive
			# number of clock cycles to be printed each
			# time
			prompt_counter -= 1
			state_counter += 1
			if clock_steps > 0 and prompt_counter == 0:
				prompt_counter = clock_steps
				input("\nPlease press ENTER key to continue..." +\
					" (more " + str(len(ans["update_timers"]) -\
					state_counter) + " states remaining)\n")

	def print_answer(self, 
		ans, 
		clock_steps=-1,
		decorate="~", 
		item_symbol="->", 
		quantity=-1,
		full=False,
		colored=True):

		if quantity <= 0:
			quantity = len(self.__FU_HORIZ_LINE)

		if full:
			self.__full_output(
				ans, 
				clock_steps,
				decorate, 
				item_symbol, 
				quantity,
				colored)
		else:
			self.__inst_status_table(\
				ans["inst_status"],
				max(ans["update_timers"]) + 1,
				colored=False)
