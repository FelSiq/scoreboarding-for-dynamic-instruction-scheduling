# Scoreboarding for Dynamic Instruction Scheduling Simulator

This code implement a very simple simulator of an architecture
with the scoreboarding technique. An architecture with scoreboar-
ding has replicas of some functional units for the EXECUTION PHASE
of the instructions, meaning it can execute several instructions 
at the same instant. Please note that this is **NOT** a superscalar 
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

# Table of Contents
1. [Usage](#Usage)
    1. [How to run](#How-to-run)
    2. [Input file format](#Input-file-format)
    3. [Supported instructions](#Supported-instructions)
2. [Output details](#Output-details)

<a name="Usage"></a>
# Usage

<a name="How-to-run"></a>
## How to run

<a name="Input-file-format"></a>
## Input file format

<a name="Supported-instructions"></a>
## Supported instructions

<a name="Output-details"></a>
# Output details
