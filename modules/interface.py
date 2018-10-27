from colorama import Fore, Style, init as colorama_init
from numpy import array
"""
	Module dedicated to produce all program
	output if option "-nogui" is enabled by the
	user in the command line.
"""

class TextualInterface:
	def __init__(self, ans):
		max_pc = max(ans["inst_status"])
		reg_status = ans["reg_dest_status"]
		func_unit_status = ans["func_unit_status"]

		self.__inst_print_order = [
			"issue", "read_operands",
			"execution", "write_result"
		]

		self.__inst_fill_len = max([
			len(label) for label in \
			self.__inst_print_order
		]) + 1

		self.__fu_print_order = [
			"busy", "op", "f_i", "f_j", 
			"f_k", "q_j", "q_k", "r_j", "r_k"
		]

		self.__fu_fill_len_labels = max([
			len(label) for label in \
			self.__fu_print_order
		]) + 2


		self.__fu_fill_len_fus = max([
			len(fu_label + str(replica_id))
			for fu_label in func_unit_status
			for replica_id in func_unit_status[fu_label]
		]) + 2

		self.__max_pc_len = len(str(max_pc)) + 1

		self.__ommited_reg_count = sum([
			len(reg_status[reg_label]) > 1
			for reg_label in reg_status
		])

	def __inst_status_table(self, inst_status, clock):
		print("{val:<{fill}}".format(val="PC", 
			fill=self.__max_pc_len), end=":")
		for print_label in self.__inst_print_order:
			print("{:^{fill}}".format(\
				print_label, fill=self.__inst_fill_len), end="|")
		print()

		for pc in sorted(list(inst_status.keys())):
			print("{val:<{fill}}".format(val=pc, fill=self.__max_pc_len), end=":")
			for stage_id in range(len(self.__inst_print_order)):
				val=inst_status[pc][self.__inst_print_order[stage_id]]
				color = Fore.RED if clock != val else Fore.GREEN
				print(color + \
					"{:^{fill}}".format(val if val <= clock else "", 
					fill=self.__inst_fill_len) + Style.RESET_ALL, end="|")
			print()

	def __func_unit_table(self, func_unit_status, clock, index_holder):
		print("{val:<{fill}}".format(val="Functional unit", 
			fill=self.__fu_fill_len_fus), end=": ")
		for print_label in self.__fu_print_order:
			print("{:^{fill}}".format(\
				print_label, fill=self.__fu_fill_len_labels), end="|")
		print()

		for func_unit_label in func_unit_status:
			for replica_id in func_unit_status[func_unit_label]:
				cur_func_unit_status = func_unit_status[func_unit_label][replica_id]
				cur_update_timers = cur_func_unit_status["update_timers"]

				# Functional unit name concatenated with its
				# id between each replicas
				print("{val:<{fill}}".format(\
					val=(func_unit_label + "_" + str(replica_id)), 
					fill=self.__fu_fill_len_fus), end=": ")

				for table_label in self.__fu_print_order:
					print_index = index_holder[func_unit_label][replica_id][table_label]

					if print_index < len(cur_func_unit_status[table_label])-1 and\
						table_label in cur_update_timers[print_index+1]["changed_fields"] and\
						cur_update_timers[print_index+1]["clock"] <= clock:
						index_holder[func_unit_label][replica_id][table_label] += 1
						print_index += 1

					val = cur_func_unit_status[table_label][print_index]
					val = str(val) if val is not None else "-"
					prev_clock = cur_update_timers[print_index]["clock"]
					color = Fore.RED if prev_clock != clock else Fore.GREEN
					print(color + \
						"{:^{fill}}".format(val if val else " ", 
						fill=self.__fu_fill_len_labels) +\
						Style.RESET_ALL, end="|")
				print()

	def __reg_dest_table(self, reg_dest_status, clock, index_holder):
		print("[...] (More", self.__ommited_reg_count, "ommited registers)")

	def print_answer(self, ans, decorate="~", item_symbol="->", quantity=50):
		colorama_init()

		sep_line = decorate * quantity

		index_holder = { 
			"fields" : {
				func_unit : {
					replica_id : {
						field_label : 0
						for field_label in ans["func_unit_status"][func_unit][replica_id]
					} for replica_id in ans["func_unit_status"][func_unit]
				} for func_unit in ans["func_unit_status"]
			},
			"registers" : {
				reg_id : 0
				for reg_id in ans["reg_dest_status"]
			}
		}

		for clock in ans["update_timers"] + [ans["update_timers"][-1] + 1]:
			print(sep_line, "Clock timer = " + str(clock), sep_line, sep="\n")
			"""
				Instruction status table
			"""
			print(item_symbol, "Instruction status table:")
			self.__inst_status_table(ans["inst_status"], clock)

			"""
				Functional Unit status table
			"""
			print(item_symbol, "Functional Unit status table:")
			self.__func_unit_table(ans["func_unit_status"], 
				clock, index_holder["fields"])

			"""
				Destiny Register status table
			"""
			print(item_symbol, "Destiny Register status table:")
			self.__reg_dest_table(ans["reg_dest_status"], 
				clock, index_holder["registers"])

