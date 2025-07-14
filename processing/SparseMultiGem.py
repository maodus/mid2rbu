from misc.utils import count_4bit
from rbu.Gem import Gem

class SparseMultiGem():
  def __init__(self):
    self._sparse_count = 0

  def separate_gems(self, gems):
    for i in range(len(gems)):
      lanes = gems[i].lane

      if count_4bit(lanes) != 2:
        continue

      left_combo = Gem.RED | Gem.YELLOW
      right_combo = Gem.GREEN | Gem.BLUE
      # Check to see if both gems are on the same side
      if not (lanes ^ left_combo) or not (lanes ^ right_combo):
        self._sparse_count += 1
        lanes ^= (Gem.RED | Gem.BLUE) # Re-arrange gems so that they are not side-by-side

      gems[i].lane = lanes

  def get_sparse_count(self):
    return self._sparse_count
          