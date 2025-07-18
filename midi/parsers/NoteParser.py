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
    self.difficulty_map = [60, 72, 84, 96]

    self._colour_map = {"red": 0, "green": 1, "yellow": 2, "blue": 3}
    self.lane_map = [0, 1, 2, 3] # r,g,y,b

  def apply_lane_mapping(self, config_str):
    # Assumption: config_str has already been validated
    split_map = [c.strip() for c in config_str.split(",")]
    for assignment in split_map:
        split_assign = assignment.split("=")
        l, r = split_assign[0].strip(), split_assign[1].strip()

        map_idx = self._colour_map[l]
        map_val = self._colour_map[r]

        self.lane_map[map_idx] = map_val

  def get_mapped_lane(self, lane):
    if lane < 0 or lane > 3:
      return 0
    
    return self.lane_map[lane]

  def process_note(self, tempo_map, note, modifiers):
    for i in range(4):
      diff_start = self.difficulty_map[i]
      diff_end = diff_start + self.difficulty_span

      if note.midi_note < diff_start or note.midi_note > diff_end:
        continue

      lane = self.get_mapped_lane((note.midi_note - diff_start) % 4)
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

    # Kicks are at note 60, 72, 84, 96. We dont care about them
    self.difficulty_map = [61, 73, 85, 97]

class GuitarParser(NoteParser):
    def __init__(self):
      super().__init__("PART GUITAR")

class BassParser(NoteParser):
    def __init__(self):
      super().__init__("PART BASS")

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

    def process_note(self, tempo_map, note, modifiers):
      for i in range(4):
        diff_start = self.difficulty_map[i]
        diff_end = diff_start + self.difficulty_span

        if note.midi_note < diff_start or note.midi_note > diff_end:
          continue

        lane = self.get_mapped_lane((note.midi_note - diff_start) % 4)
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

            cur_t_end = note.tick_end
            cur_t_start = note.tick_start
            sus_t = cur_t_end - cur_t_start

            last_gem.tick_duration += sus_t
            last_gem.ms_duration += tempo_map.tick2ms(cur_t_end) - tempo_map.tick2ms(cur_t_start)
            new_mods = (last_gem.modifiers | modifiers) & ~EventType.IgnoreDuration

            self.gems[i][-1] = Gem(last_gem.ms, last_gem.tick, last_gem.ms_duration, last_gem.tick_duration, 1 << lane, new_mods)
            continue

        self.note_hist[i] = note
        self._add_gem(tempo_map, note, i, lane, modifiers)

      

