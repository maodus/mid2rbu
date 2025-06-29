from enum import IntFlag

class EventType(IntFlag):
  Empty = 0
  Starpower = 1 << 0
  StarpowerEnd = 1 << 1

class TrackEvent():
  def __init__(self, tick, sus, event_types):
    self.tick = tick
    self.sus = sus
    self.event_types = event_types
