class IntervalGemPruner():
  def __init__(self):
      self._prune_count = 0

  def prune_gems(self, gems, ms_window):
    gem_len = len(gems)

    r = gem_len - 1
    l = r - 1

    # Sliding window that will prune every 2nd gem 
    # if the ms timing is too small
    while l >= 0:
      r_gem = gems[r]
      l_gem = gems[l]

      if int(r_gem.ms - l_gem.ms) <= ms_window:
        gems.pop(l)
        self._prune_count += 1

        r = l
        l = r - 1
      else:
        r -= 1
        l -= 1

  def get_prune_count(self):
    return self._prune_count      