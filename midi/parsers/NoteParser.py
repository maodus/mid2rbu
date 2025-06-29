from rbu.Gem import Gem
from midi.Note import Note
import struct

class NoteParser():
  def __init__(self, track_name):
    self.gems = [[], [], [], []]
    self.track_name = track_name
    self.difficulty_map = [0, 0, 0, 0]
    self.note_hist = [Note(-1, -1, -1), Note(-1, -1, -1), Note(-1, -1, -1), Note(0, -1, -1)]

  def process_note(self, tempo_map, note, modifiers):
    for i in range(4):
      diff_start = self.difficulty_map[i]
      diff_end = diff_start + 3

      if note.midi_note < diff_start or note.midi_note > diff_end:
        continue

      lane = note.midi_note - diff_start
      last_note = self.note_hist[i] # Get the last recorded note for this difficulty

      # If we have multiple notes on the same tick and midi number, we have a multi-gem
      # Dont append a new note in this case, just update the lane info of the last gem
      if last_note.midi_note != -1 and last_note.tick_start == note.tick_start:
        self.gems[i][-1].lane |= (1 << lane)
        continue

      t_start = note.tick_start
      t_end = note.tick_end

      ms_start = tempo_map.tick2ms(t_start)
      ms_end = tempo_map.tick2ms(t_end)

      ms_duration = ms_end - ms_start
      t_duration = t_end - t_start

      self.note_hist[i] = note
      self.gems[i].append(Gem(ms_start, t_start, ms_duration, t_duration, 1 << lane, modifiers))

  def get_bytes(self, diff):
    gems = self.gems[diff]
    byte_arr = bytearray(struct.pack("<I", len(gems)))

    for gem in gems:
      byte_arr.extend(gem.get_bytes())

    return byte_arr


class DrumParser(NoteParser):
  def __init__(self):
    super().__init__("PART DRUMS")

    self.difficulty_map = [61, 72, 84, 96]

class GuitarParser(NoteParser):
    def __init__(self):
      super().__init__("PART GUITAR")

      self.difficulty_map = [60, 72, 84, 96]

class BassParser(NoteParser):
    def __init__(self):
      super().__init__("PART BASS")

      self.difficulty_map = [60, 72, 84, 96]

class VocalParser(NoteParser):
    def __init__(self):
      super().__init__("PART VOCALS")

      self.difficulty_map = [60, 72, 84, 96]

      

