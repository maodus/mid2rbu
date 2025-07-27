# Bit count lookup table for 4-bit values (0-15)
bit_lookup = [0, 1, 1, 2, 1, 2, 2, 3,
              1, 2, 2, 3, 2, 3, 3, 4]

def count_4bit(value):
    """Returns the number of set bits in the low 4 bits of a value (0-15)."""
    return bit_lookup[value & 0xF]

def clean_file_name(file_name):
   clean_name = "".join(c.upper() for c in file_name if c.isalnum())
   return clean_name

def get_closest_gem_extent(gems, tick_start, tick_end):
    if tick_start > tick_end:
        return (-1, -1)

    i = 0
    start_id = -1
    end_id = -1
    while i < len(gems):
        gem = gems[i]

        if gem.tick < tick_start:
            i += 1
            continue

        if gem.tick >= tick_start and start_id < 0:
            start_id = i
            i += 1
            continue

        if gem.tick < tick_end:
            i += 1
        elif gem.tick == tick_end and end_id < 0:
            end_id = i
            break
        else:
            end_id = max(0, i - 1)
            break
    
    return (start_id, end_id)