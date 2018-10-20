from configme import Config
from modules.readfile import ReadFile
from modules.scoreboard import Scoreboard

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<source_code_filepath>")
		exit(1)

	rf = ReadFile()

	# Load architecture from configme.py module
	architecture = rf.load_architecture()

	# Load instructions from given assembly input
	# file source code
	inst_list = rf.load_instructions(sys.argv[1], architecture)

	sc = Scoreboard()

	# Load architecture to the scoreboard module
	sc.load_architecture(architecture)
	
	# Load instruction set to the scoreboard module
	sc.load_instructions(inst_list)

	ans = sc.run()
	
	print_order = ["issue", "read_operands",
		"execution", "write_result"]

	inst_status = ans["inst_status"]
	for pc in sorted(list(inst_status.keys())):
		print(pc, end="\t:\t")
		for stage_id in range(len(print_order)):
			print(inst_status[pc][print_order[stage_id]], end="\t")
		print()
