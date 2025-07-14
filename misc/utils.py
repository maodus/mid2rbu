# Bit count lookup table for 4-bit values (0-15)
bit_lookup = [0, 1, 1, 2, 1, 2, 2, 3,
              1, 2, 2, 3, 2, 3, 3, 4]

def count_4bit(value):
    """Returns the number of set bits in the low 4 bits of a value (0-15)."""
    return bit_lookup[value & 0xF]