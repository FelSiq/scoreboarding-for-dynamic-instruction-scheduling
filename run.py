from configme import Config
from modules.readfile import ReadFile
from modules.scoreboard import Scoreboard
from modules.interface import TextualInterface
from textwrap import dedent

if __name__ == "__main__":
	import sys

	if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<source_code_filepath>",
			"[--checkreg] [--nogui] [--complete] [--nocolor]\n",
			dedent("""
			Where:
			<source_code_filepath>: full filepath of MIPS assembly-like input file. 
						Please check out "./test-cases/" subdirectory for input file format examples.

			Optional flags:
			--checkreg: 	accepts only registers declared in architecture defined in Configme.py module.
			--nogui: 	disable graphical interface.
			--complete: 	produce step-by-step output for Instruction, Functional Units and Register status tables.
			--nocolor: 	produce all output with just standard terminal color. 
					Makes sense only if used together with "--complete" flag.
			"""))
		exit(1)

	checkreg = "--checkreg" in sys.argv
	nogui = "--nogui" in sys.argv
	full_output = "--complete" in sys.argv
	colored_output = "--nocolor" not in sys.argv

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
