class IntervalGemPruner():
  def __init__(self):
      pass

  def prune_gems(self, gems, min_tick_gap):
    gem_len = len(gems)
    l = gem_len - 1
    r = l - 1

    while r >= 0:
      l_gem = gems[l]
      r_gem = gems[r]

      gem_dist = l - r

      if not (r_gem.lane ^ l_gem.lane) and l_gem.tick - r_gem.tick <= min_tick_gap * (gem_dist):
        r -= 1 # Increase window
        continue
      elif gem_dist >= 2: # Atleast 3 gems in window
        # Delete every second gem in interval
        gem_offset = gem_dist & 1
        for i in range(l - gem_offset, r - 1, -2):
          if i >= 0:
            gems.pop(i)

        l = r
        r = l - 1
        continue

      l -= 1
      r -= 1