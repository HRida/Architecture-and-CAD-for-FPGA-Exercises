def identify_unused_inputs(init_string):
    """
    Identify unused (don't-care) inputs in a LUT-4 based on the given init string.
    
    Args:
        init_string (str): A 16-character binary string representing the LUT truth table.

    Returns:
        list: A list of unused input indices (0 for 'a', 1 for 'b', etc.).
    """
    if len(init_string) != 16:
        raise ValueError("Init string must be exactly 16 bits long.")

    unused_inputs = []

    for i in range(4):  # Check each input (a, b, c, d)
        dependent = False
        for j in range(16):
            mask = 1 << i  # Bitmask for the current input
            flipped = j ^ mask  # Flip the i-th bit

            if init_string[j] != init_string[flipped]:
                dependent = True
                break

        if not dependent:
            unused_inputs.append(i)

    return unused_inputs

def test_lut_functions():
    """
    Test the function on the provided Boolean functions.
    """
    # Helper to compute the truth table of a given function
    def compute_truth_table(f):
        table = ''
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        table += str(f(a, b, c, d))
        return table[::-1]  # Reverse for MSB downto LSB

    # First function: ((a AND b) OR c) XOR d
    f1 = lambda a, b, c, d: ((a and b) or c) ^ d
    init_string1 = compute_truth_table(f1)
    unused1 = identify_unused_inputs(init_string1)

    # Second function: (((a AND b) OR c) XOR d) AND itself
    f2 = lambda a, b, c, d: (((a and b) or c) ^ d) and (((a and b) or c) ^ d)
    init_string2 = compute_truth_table(f2)
    unused2 = identify_unused_inputs(init_string2)

    return {
        "Function 1": {
            "Init String": init_string1,
            "Unused Inputs": unused1,
        },
        "Function 2": {
            "Init String": init_string2,
            "Unused Inputs": unused2,
        },
    }

# Run the test
results = test_lut_functions()
for func, data in results.items():
    print(f"{func}:")
    print(f"  Init String: {data['Init String']}")
    print(f"  Unused Inputs: {data['Unused Inputs']}")
