import struct

class BeatInfo:
  def __init__(self, tick, level):
    self.tick = tick
    self.level = level

  def get_bytes(self):
    return struct.pack("<II", self.tick, self.level)

class BeatMap:
  def __init__(self):
    self.beats = []

  def add_beat(self, beat):
    self.beats.append(beat)

  def get_bytes(self):
    byte_arr = bytearray(struct.pack("<I", len(self.beats)))

    for beat in self.beats:
      byte_arr.extend(beat.get_bytes())

    return byte_arr