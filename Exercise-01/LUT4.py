def _validate_init_string(init_string):
    if len(init_string) != 16 or any(bit not in "01" for bit in init_string):
        raise ValueError("Init string must be exactly 16 bits and contain only 0/1.")


def _value_from_init(init_string, truth_index):
    """Read LUT value by truth-table index with init ordered MSB -> LSB.

    Exercise convention:
    - init_string[0] corresponds to truth index 15
    - init_string[15] corresponds to truth index 0 (all inputs = 0)
    """
    return init_string[15 - truth_index]


def identify_unused_inputs(init_string):
    """Return unused input indices (0:a, 1:b, 2:c, 3:d) for a LUT4 init string."""
    _validate_init_string(init_string)

    # a, b, c, d map to truth-table bits 3, 2, 1, 0 respectively.
    input_masks = [0b1000, 0b0100, 0b0010, 0b0001]
    unused_inputs = []

    for input_idx, mask in enumerate(input_masks):
        dependent = False
        for truth_index in range(16):
            flipped_index = truth_index ^ mask
            if _value_from_init(init_string, truth_index) != _value_from_init(
                init_string, flipped_index
            ):
                dependent = True
                break
        if not dependent:
            unused_inputs.append(input_idx)

    return unused_inputs


def identify_dependent_inputs(init_string):
    """Return dependent input indices (0:a, 1:b, 2:c, 3:d) for a LUT4 init string."""
    unused = set(identify_unused_inputs(init_string))
    return [i for i in range(4) if i not in unused]


def test_lut_functions():
    """
    Test the function on the provided Boolean functions.
    """

    # Build init string in the required LUT format: MSB (index 15) down to LSB (index 0).
    def compute_truth_table(f):
        table = ""
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        table += str(f(a, b, c, d))
        return table[::-1]

    # First function: ((a AND b) OR c) XOR d
    f1 = lambda a, b, c, d: ((a and b) or c) ^ d
    init_string1 = compute_truth_table(f1)
    dependent1 = identify_dependent_inputs(init_string1)
    unused1 = identify_unused_inputs(init_string1)

    # Second function: (((a AND b) OR c) XOR d) AND itself
    f2 = lambda a, b, c, d: (((a and b) or c) ^ d) and (((a and b) or c) ^ d)
    init_string2 = compute_truth_table(f2)
    dependent2 = identify_dependent_inputs(init_string2)
    unused2 = identify_unused_inputs(init_string2)

    # Third function: d is ignored on purpose, so input d should be detected as unused.
    f3 = lambda a, b, c, d: (a and b) or c
    init_string3 = compute_truth_table(f3)
    dependent3 = identify_dependent_inputs(init_string3)
    unused3 = identify_unused_inputs(init_string3)

    return {
        "Function 1": {
            "Init String": init_string1,
            "Dependent Inputs": dependent1,
            "Unused Inputs": unused1,
        },
        "Function 2": {
            "Init String": init_string2,
            "Dependent Inputs": dependent2,
            "Unused Inputs": unused2,
        },
        "Function 3 (Input d unused)": {
            "Init String": init_string3,
            "Dependent Inputs": dependent3,
            "Unused Inputs": unused3,
        },
    }


# Run the test
results = test_lut_functions()
for func, data in results.items():
    print(f"{func}:")
    print(f"  Init String: {data['Init String']}")
    print(f"  Dependent Inputs: {data['Dependent Inputs']}")
    print(f"  Unused Inputs: {data['Unused Inputs']}")
