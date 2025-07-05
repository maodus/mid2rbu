from midi.Event import EventType
from rbu.Gem import Gem
from midi.Note import Note
import struct

class NoteParser():
  def __init__(self, track_name):
    self.gems = [[] for _ in range(4)]
    self.note_hist = [Note(-1, -1, -1) for _ in range(4)]
    self.track_name = track_name
    self.difficulty_span = 3 # Number of notes from start to end of difficulty
    self.difficulty_map = [0] * 4

  def process_note(self, tempo_map, note, modifiers):
    for i in range(4):
      diff_start = self.difficulty_map[i]
      diff_end = diff_start + self.difficulty_span

      if note.midi_note < diff_start or note.midi_note > diff_end:
        continue

      lane = (note.midi_note - diff_start) % 4
      last_note = self.note_hist[i] # Get the last recorded note for this difficulty

      # If we have multiple notes on the same tick and midi number, we have a multi-gem
      # Dont append a new note in this case, just update the lane info of the last gem
      if last_note.midi_note != -1 and last_note.tick_start == note.tick_start:
        self.gems[i][-1].lane |= (1 << lane)
        continue

      self.note_hist[i] = note
      self._add_gem(tempo_map, note, i, lane, modifiers)

    
  def _add_gem(self, tempo_map, note, difficulty, lane, modifiers):
    t_start = note.tick_start
    t_end = note.tick_end

    ms_start = tempo_map.tick2ms(t_start)
    ms_end = tempo_map.tick2ms(t_end)

    ms_duration = ms_end - ms_start
    t_duration = t_end - t_start

    self.gems[difficulty].append(Gem(ms_start, t_start, ms_duration, t_duration, 1 << lane, modifiers))

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
    def __init__(self, pitched_vocals):
      super().__init__("PART VOCALS")
      self.pitched_vocals = pitched_vocals

      if pitched_vocals:
        # With pitched vocals, we will not have "difficulties"
        # for now, instead we just calulate the lane from the octave.
        # Every 4 semitones constitutes each 4-way mapping of lanes/frets.
        self.difficulty_span = 47
        self.difficulty_map = [36, 36, 36, 36]
      else:
        self.difficulty_map = [60, 72, 84, 96]

    def process_note(self, tempo_map, note, modifiers):
      for i in range(4):
        diff_start = self.difficulty_map[i]
        diff_end = diff_start + self.difficulty_span

        if note.midi_note < diff_start or note.midi_note > diff_end:
          continue

        lane = (note.midi_note - diff_start) % 4
        last_note = self.note_hist[i] # Get the last recorded note for this difficulty


        if last_note.midi_note != -1:
          # If we have multiple notes on the same tick and midi number, we have a multi-gem
          # Dont append a new note in this case, just update the lane info of the last gem
          if last_note.tick_start == note.tick_start:
            self.gems[i][-1].lane |= (1 << lane)
            continue

          # On pitch based mappings, notes appear too frequently, so lets just
          # combine notes and extend the initial sustain
          if (self.pitched_vocals
              and last_note.midi_note == note.midi_note
              and (note.tick_start - last_note.tick_end) < 240):            
            last_gem = self.gems[i][-1] # Copy of last gem

            sus_t = note.tick_end - note.tick_start
            last_gem.tick_duration += sus_t
            last_gem.ms_duration += tempo_map.tick2ms(sus_t)
            new_mods = (last_gem.modifiers | modifiers) & ~EventType.IgnoreDuration

            self.gems[i][-1] = Gem(last_gem.ms, last_gem.tick, last_gem.ms_duration, last_gem.tick_duration, 1 << lane, new_mods)
            continue

        self.note_hist[i] = note
        self._add_gem(tempo_map, note, i, lane, modifiers)

      

