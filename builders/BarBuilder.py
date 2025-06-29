import struct

class BarInfo():
  def __init__(self, start_gem_id, end_gem_id, start_ms, end_ms):
    self.start_gem_id = start_gem_id
    self.end_gem_id = end_gem_id
    self.start_ms = start_ms
    self.end_ms = end_ms

  def get_bytes(self):
    return struct.pack("<IIff", self.start_gem_id, self.end_gem_id, self.start_ms, self.end_ms)

  def __repr__(self):
    return f"{self.start_gem_id} {self.end_gem_id} {self.start_ms} {self.end_ms}"

class BarBuilder():
  def __init__(self):
    self.bars = [[], [], [], []]

  def build(self, tempo_map, measure_map, gems, difficulty):
    cur_bar_tick = 0
    last_gem = gems[-1]

    last_tick = last_gem.tick + last_gem.tick_duration
    gem_idx = 0

    while cur_bar_tick < last_tick:
      time_sig = measure_map.get_time_sig(cur_bar_tick)
      bar_start = cur_bar_tick
      bar_end = bar_start + (time_sig.numerator * 1920) // time_sig.denominator

      gem_start = gem_idx
      for i in range(gem_start, len(gems)):
        gem = gems[i]

        # Include gems whos start tick is in the bar window
        gem_idx = i

        if gem.tick > bar_end:
          break

      self.bars[difficulty].append(
        BarInfo(
          gem_start,
          gem_idx,
          tempo_map.tick2ms(bar_start),
          tempo_map.tick2ms(bar_end)
        )
      )
      cur_bar_tick = bar_end

  def get_bytes(self, difficulty):
    bars = self.bars[difficulty]
    byte_arr = bytearray(struct.pack("<I", len(bars)))

    for bar in bars:
      byte_arr.extend(bar.get_bytes())

    return byte_arr


