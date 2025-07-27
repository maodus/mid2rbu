import struct
from midi.Event import EventType

class Gem:
  RED = 1 << 0
  YELLOW = 1 << 1
  GREEN = 1 << 2
  BLUE = 1 << 3

  def __init__(self, ms, tick, ms_duration, tick_duration, lane, modifiers):
    self.modifiers = modifiers

    self.ms = ms # float32
    self.tick = tick # int32
    self.ms_duration = int(ms_duration) # int16
    self.tick_duration = tick_duration # int16
    self.unk = 0x7FFF # int16, not read from memory?

    # int8 bit field
    self.lane = lane # 0:3
    self.unk2 = 0 # 4:7 Doesnt let the gem be played if not 0?

    self.unk3 = 0x8 # int8, ignore strum?
    if modifiers & EventType.IgnoreDuration:
      self.unk3 |= 2 # ignore duration


    # Format -> Bit: Purpose 
    # 31: Unknown
    # 30: Gem is end of phrase flag (makes gem big and glow)
    # 29: Gem is visible flag
    # 28: Start solo
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
  
  def has_mod(self, modifier):
    return self.modifiers & modifier
  
  def make_solo(self):
    self.unk4 |= 0x08000000
  
  def make_solo_start(self, count):
    self.make_solo()
    self.unk4 = (self.unk4 & 0xFFFF0000) | (1 << 28) | count

  def make_solo_end(self):
    self.make_solo()
    self.unk4 = (self.unk4 & 0xFFFF0000) | (2 << 28)
  
  def __str__(self):
    return f"{self.ms} {self.tick} {self.tick_duration} {bin(self.lane)} {bin(self.modifiers)}"
  
  def __repr__(self):
    return str(self)