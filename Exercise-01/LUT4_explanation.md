# LUT4 Exercise Explanation

## Goal of the exercise
The assignment asks us to analyze a LUT4 init string and detect which inputs are actually used by the implemented Boolean function.

A LUT4 has 4 inputs (a, b, c, d) and 16 truth-table entries.
The key rule is:
- An input is unused (don't-care) if flipping only that input never changes the output.

The program therefore needs to:
1. Read a 16-bit init string.
2. Compare truth-table entries that differ by only one input bit.
3. Report dependent inputs and unused inputs.

## Why bit ordering matters
The sheet says init strings are arranged from MSB down to LSB.
That means:
- The first character in the string is truth-table index 15.
- The last character in the string is truth-table index 0 (all inputs = 0).

If we ignore this mapping, we compare the wrong LUT entries and can get wrong dependency results.

## Step-by-step walkthrough of LUT4.py

### 1) Validate input format
Function: _validate_init_string(init_string)

What it does:
- Checks length is exactly 16.
- Checks every character is 0 or 1.

Why we do it:
- LUT4 has exactly 16 configuration bits.
- Invalid strings would make all later comparisons meaningless.

### 2) Map truth index to string position
Function: _value_from_init(init_string, truth_index)

What it does:
- Converts a truth-table index (0..15) into the correct position in the MSB->LSB init string.
- Uses: init_string[15 - truth_index]

Why we do it:
- The assignment's ordering is reversed relative to natural index growth.
- This keeps the logic correct and aligned with the exercise definition.

### 3) Detect unused inputs
Function: identify_unused_inputs(init_string)

What it does:
- For each input (a, b, c, d), it flips only that bit for every truth index.
- Compares output before and after flip.
- If any comparison changes output, input is dependent.
- If output never changes, input is unused.

Important detail:
- Input masks are [0b1000, 0b0100, 0b0010, 0b0001].
- This maps index 0->a, 1->b, 2->c, 3->d.

Why we do it:
- This directly implements the assignment definition of don't-care inputs.

### 4) Return dependent inputs
Function: identify_dependent_inputs(init_string)

What it does:
- Calls identify_unused_inputs.
- Returns the complement set from [0, 1, 2, 3].

Why we do it:
- Part (a) asks for dependent variables.
- Unused list is useful too, so both are provided.

### 5) Build test init strings from functions
Function: test_lut_functions()

What it does:
- Computes truth tables for each test function.
- Reverses generated table to MSB->LSB string format.
- Runs dependency/unused detection for each function.

Why we do it:
- Part (b) asks to try the program on given functions.
- Reversing is required to match the assignment's LUT string convention.

## What each test demonstrates

### Function 1
f(a,b,c,d) = ((a AND b) OR c) XOR d

Expected behavior:
- Uses all four inputs.

Observed result:
- Dependent Inputs: [0, 1, 2, 3]
- Unused Inputs: []

### Function 2
f(a,b,c,d) = (((a AND b) OR c) XOR d) AND (((a AND b) OR c) XOR d)

Reasoning:
- X AND X = X, so this function is equivalent to Function 1.

Observed result:
- Same as Function 1.
- Dependent Inputs: [0, 1, 2, 3]
- Unused Inputs: []

### Function 3 (added for verification)
f(a,b,c,d) = (a AND b) OR c

Reasoning:
- d is not used in expression.

Observed result:
- Dependent Inputs: [0, 1, 2]
- Unused Inputs: [3]

This confirms the detector correctly identifies an actually unused input.

## Short summary
We are doing this to prove whether each LUT input really affects output.
The code follows the exact LUT4 ordering rule from the exercise and checks dependency by single-bit flips, which is the formal definition of a don't-care input in this assignment.
