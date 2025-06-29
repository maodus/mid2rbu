import struct

class TempoInfo:
  def __init__(self, tempo, tick_start):
    self.tempo = tempo
    self.tick_start = tick_start
    self.tick_end = 2147483647

  def get_bytes(self, ms):
    return struct.pack("<fII", ms, self.tick_start, self.tempo)
  

class TempoMap():
  def __init__(self, tpq):
    self.tempos = []
    self.tpq = tpq

  def tick2ms(self, tick):
    total_ms = 0
    for tempo_rng in self.tempos:
      if tempo_rng.tick_end <= tick:
        ticks = tempo_rng.tick_end - tempo_rng.tick_start
        total_ms += (ticks * (tempo_rng.tempo / 1000)) / self.tpq
      else:
        ticks = tick - tempo_rng.tick_start
        total_ms += (ticks * (tempo_rng.tempo / 1000)) / self.tpq
        return total_ms

    return total_ms
  
  def get_bytes(self):
    byte_arr = bytearray(struct.pack("<I", len(self.tempos)))

    for k, tempo_info in enumerate(self.tempos):
      ms = self.tick2ms(tempo_info.tick_start)
      #print(k, ms, tempo_info.tempo, tempo_info.tick_start, tempo_info.tick_end)
      byte_arr.extend(tempo_info.get_bytes(ms))

    return byte_arr