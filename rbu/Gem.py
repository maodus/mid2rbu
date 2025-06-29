import struct
from midi.Event import EventType

class Gem:
  def __init__(self, ms, tick, ms_duration, tick_duration, lane, modifiers):
    self.ms = ms # float32
    self.tick = tick # int32
    self.ms_duration = int(ms_duration) # int16
    self.tick_duration = tick_duration # int16
    self.unk = 0 # int16, normally 0x3c

    # int8 bit field
    self.lane = lane # 0:3
    self.unk2 = 0 # 4:7 Doesnt let the gem be played if not 0?

    self.unk3 = 0 # int8, normally 0xA

    # Format -> Bit: Purpose 
    # 31: Start solo?
    # 30: Gem is end of phrase flag (makes gem big and glow)
    # 29: Gem is visible flag
    # 28: Unknown
    # 27: Disables phrases?
    # 26: End of starpower flag
    # 25: Starpower flag
    # 24: Unknown
    self.unk4 = 0 # int32


    if modifiers & EventType.StarpowerEnd:
      self.unk4 |= 1 << (31-5)

    if modifiers & EventType.Starpower:
      self.unk4 |= 1 << (31-6)

  def get_bytes(self):
    return struct.pack(
      "<fIHHHBBI",
      self.ms,
      self.tick,
      self.ms_duration,
      self.tick_duration,
      self.unk,
      (self.unk2 << 4) | self.lane,
      self.unk3,
      self.unk4
    )
  
  def __str__(self):
    return f"{self.ms} {self.tick} {self.tick_duration} {self.lane}"
  
  def __repr__(self):
    return str(self)