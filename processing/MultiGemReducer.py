from misc.utils import count_4bit
from rbu.Gem import Gem

class MultiGemReducer():

  reduction_map = [
      0,              # 0b0000 - no gem
      Gem.RED,        # 0b0001 - RED only
      Gem.YELLOW,     # 0b0010 - YELLOW only
      Gem.RED,        # 0b0011 - RED + YELLOW -> RED
      Gem.GREEN,      # 0b0100 - GREEN only
      Gem.GREEN,      # 0b0101 - RED + GREEN -> GREEN
      Gem.YELLOW,     # 0b0110 - YELLOW + GREEN -> YELLOW
      Gem.GREEN,      # 0b0111 - RED + YELLOW + GREEN -> GREEN
      Gem.BLUE,       # 0b1000 - BLUE only
      Gem.BLUE,       # 0b1001 - RED + BLUE -> BLUE
      Gem.YELLOW,     # 0b1010 - YELLOW + BLUE -> YELLOW
      Gem.BLUE,       # 0b1011 - RED + YELLOW + BLUE -> BLUE
      Gem.GREEN,      # 0b1100 - GREEN + BLUE -> GREEN
      Gem.BLUE,       # 0b1101 - RED + GREEN + BLUE -> BLUE
      Gem.YELLOW,     # 0b1110 - YELLOW + GREEN + BLUE -> YELLOW
      Gem.RED,        # 0b1111 - All 4 colors -> RED
  ]

  def __init__(self):
    self._reduced_count = 0

  def reduce_multis(self, gems):
    gem_len = len(gems)
    start_id = 0

    while start_id < gem_len:
      end_id = min(start_id + 4, gem_len)

      needs_reduction = True
      for i in range(start_id + 1, end_id):
        prev_gem = gems[i - 1]
        cur_gem = gems[i]

        # Are both gems multi-gems?
        is_multi = count_4bit(prev_gem.lane) >= 2 and count_4bit(cur_gem.lane) >= 2

        # 180ms is just an arbitrary number I chose
        in_window = int(cur_gem.ms - prev_gem.ms) <= 180

        if not is_multi or not in_window:
          needs_reduction = False

      if not needs_reduction or end_id - start_id != 4:
        start_id += 1
        continue

      # Reduce multi-gem to just a single gem
      for i in range(start_id, end_id):
        gems[i].lane = MultiGemReducer.reduction_map[gems[i].lane & 0xF]

      self._reduced_count += 4
      start_id += 4

  def get_reduction_count(self):
    return self._reduced_count