class SparseMultiGem():
    def __init__(self):
        self.bit_lookup = [0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4]
    
    def _count_lanes(self, lane_bits):
       return self.bit_lookup[lane_bits & 0xF]

    def separate_gems(self, gems):
      for i in range(len(gems)):
        lanes = gems[i].lane

        if self._count_lanes(lanes) != 2:
          continue

        # Check to see if both gems are on the same side
        if not (lanes ^ 0x3) or not (lanes ^ 0xC):
          lanes ^= 0x9 # Re-arrange gems so that they are not side-by-side

        gems[i].lane = lanes
          