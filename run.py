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
			"[--checkreg] [--nogui] [--complete] [--nocolor] [--noufstage] [--clockstep n]\n",
			dedent("""
			Where:
			<source_code_filepath>: full filepath of MIPS assembly-like input file. 
						Please check out "./test-cases/" subdirectory for input file format examples.

			Optional flags:
			--checkreg	: accepts only registers declared in architecture defined in Configme.py module.
			--nogui		: (no effect) disable graphical interface.
			--complete	: produce step-by-step output for Instruction, Functional Units and Register status tables.
			--nocolor	: produce all output with just standard terminal color. 
					Makes sense only if used together with "--complete" flag.
			--noufstage	: disable the "update_flags" pipeline stage, used to prevent deadlocks in RAW dependencies 
					if two instructions in the ("write_result", "read_operands") pipeline stages pair matches in 
					the same clock cycle while the first one write in a register and the second one read from it. 
					If this flag is enabled, the functional unit flag updating  will be done in the "write_result" 
					pipeline stage instead.
			--clockstep	: specify how many clock cycles must be shown each iteration. If ommited, then all cycles will
					be printed by default. This argument only makes sense if used together with "--complete" flag.
			"""))
		exit(1)

	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		START OF Setting up program arguments
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	checkreg = "--checkreg" in sys.argv
	nogui = "--nogui" in sys.argv or True # Graphical interface not implemented yet
	full_output = "--complete" in sys.argv
	colored_output = "--nocolor" not in sys.argv
	update_flags_stage = "--noufstage" not in sys.argv

	clock_steps = -1
	if "--clockstep" in sys.argv:
		try:
			clock_steps = int(sys.argv[1 + sys.argv.index("--clockstep")])
			if clock_steps <= 0:
				raise Exception
		except:
			print("\"--clockstep\" argument demands"+\
				" a positive integer as parameter")
			exit(2)
	"""
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		END OF Setting up program arguments
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""

	rf = ReadFile()

	# Load architecture from configme.py module
	architecture = rf.load_architecture()

	# Load instructions from given assembly input
	# file source code
	inst_list = rf.load_instructions(\
		sys.argv[1], 
		architecture, 
		verify_reg=checkreg)

	sc = Scoreboard(update_flags_stage=update_flags_stage)

	# Load architecture to the scoreboard module
	sc.load_architecture(architecture)
	
	# Load instruction set to the scoreboard module
	sc.load_instructions(inst_list)

	ans = sc.run()
	
	if nogui:
		ti = TextualInterface(ans)
		ti.print_answer(ans, 
			full=full_output, 
			clock_steps=clock_steps,
			colored=colored_output)
