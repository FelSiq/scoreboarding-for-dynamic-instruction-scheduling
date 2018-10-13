# Scoreboarding for Dynamic Instruction Scheduling Simulator

This code implement a very simple simulator of an architecture
with the scoreboarding technique. An architecture with scoreboar-
ding has replicas of some functional units for the EXECUTION PHASE
of the instructions, meaning it can execute several instructions 
at the same instant. Please note that this is *NOT* a superscalar 
architecture, which is a very similar concept also connected with 
dynamic instruction scheduling.

The major difference between the two techniques is that the scoreboarding
relies only on multiple functional units in the EXECUTION phase of
the instruction, so only a single instruction can be dispached and peform
write back in the same computer clock. In contrast, the superscalar 
architecture have replicated functional units for every phase.

Note that both techniques may execute instructions out-of-order
(whenever false dependencies in the code are not an constraint),
but the COMMIT/WRITE BACK phase (the last phase of every instruction) 
must happen strictly in the same order wrote in the program code.

# Summary
1. [Usage](#Usage)
    1. [Input file format](#Input-file-format)
    2. [Supported instructions](#Supported-instructions)
    3. [Expected output](#Expected-output)

# Usage

<a name="Input-file-format"></a>
## Input file format

<a name="Supported-instructions"></a>
## Supported instructions

<a name="Expected-output"></a>
## Expected output
