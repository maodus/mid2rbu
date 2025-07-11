class IntervalGemPruner():
  def __init__(self):
      pass
  
  def _prune_range(self, gems, l, r):
    gem_dist = r - l
    gem_offset = gem_dist & 1
    for i in range(r - gem_offset, l, -2):
        if i >= 0:
          gems.pop(i)

  def prune_gems(self, gems, min_tick_gap):
    # First pass prunes based on gem color
    # Second pass prunes across frets/lanes/chords
    prune_pass = 0 

    while prune_pass < 2:
      gem_len = len(gems)
      r = gem_len - 1
      l = r - 1

      while l >= 0:
        l_gem = gems[l]
        r_gem = gems[r]

        gem_dist = r - l
        account_lane = bool(l_gem.lane & r_gem.lane) if prune_pass == 0 else True

        if account_lane and r_gem.tick - l_gem.tick <= min_tick_gap * gem_dist:
          l -= 1 # Increase window
          continue
        elif gem_dist > 1: # Atleast 2 gems (includes r_gem) in window
          self._prune_range(gems, l, r)

          # Restart from the gem tick that broke the pruning chain
          r = l
          l = r - 1
          continue

        l -= 1
        r -= 1

      if l < 0 and r > 0:
        self._prune_range(gems, l, r)

      prune_pass += 1