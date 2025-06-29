class Note:
  def __init__(self, midi_note = 0, tick_start = 0, tick_end = 0):
    self.midi_note = midi_note
    self.tick_start = tick_start
    self.tick_end = tick_end

  def start(self, tick):
    self.tick_start = tick
  
  def end(self, sus):
    self.tick_end = self.tick_start + sus

  def clone(self):
    return Note(self.midi_note, self.tick_start, self.tick_end)