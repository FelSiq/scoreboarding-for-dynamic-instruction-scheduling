from configme import Config
from modules.readfile import ReadFile
from modules.scoreboard import Scoreboard
from modules.interface import TextualInterface

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<source_code_filepath>",
			"[-checkreg] [-nogui] [-complete] [-nocolor]")
		exit(1)

	checkreg = "-checkreg" in sys.argv
	nogui = "-nogui" in sys.argv
	full_output = "-complete" in sys.argv
	colored_output = "-nocolor" not in sys.argv

	rf = ReadFile()

	# Load architecture from configme.py module
	architecture = rf.load_architecture()

	# Load instructions from given assembly input
	# file source code
	inst_list = rf.load_instructions(\
		sys.argv[1], 
		architecture, 
		verify_reg=checkreg)

	sc = Scoreboard()

	# Load architecture to the scoreboard module
	sc.load_architecture(architecture)
	
	# Load instruction set to the scoreboard module
	sc.load_instructions(inst_list)

	ans = sc.run()
	
	if nogui:
		ti = TextualInterface(ans)
		ti.print_answer(ans, 
			full=full_output, 
			colored=colored_output)
