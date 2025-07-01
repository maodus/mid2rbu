from midi.Event import EventType, TrackEvent
from midi.parsers.BeatParser import BeatParser
from midi.parsers.NoteParser import *
from midi.parsers.TimeSigParser import TimeSigParser
from midi.parsers.TempoParser import TempoParser
from builders.BarBuilder import BarBuilder
from midi.Note import Note

class MidiParser:
  def __init__(self, midi_file):
    # midi_file.ticks_per_beat
    self.midi_file = midi_file
    self.tempo_parser = TempoParser()
    self.timesig_parser = TimeSigParser()
    self.beat_parser = BeatParser()
    self.notes = [Note(i) for i in range(128)]
    
    self.note_parsers = {
      "PART DRUMS" : DrumParser(),
      "PART GUITAR" : GuitarParser(),
      "PART BASS" : BassParser(),
      "PART VOCALS" : VocalParser()
    }

    self.bar_builders = {}
    for key in self.note_parsers:
      self.bar_builders[key] = BarBuilder()

  def find_track(self, track_name):
    for track in self.midi_file.tracks:
      if track.name == track_name:
        return track
      
    return None

  def validate_tracks(self):
    if not self.midi_file:
      print("Midi file does not exist")
      return

    req_tracks = ["PART DRUMS", "PART GUITAR", "PART BASS", "PART VOCALS", "BEAT"]
    mid_track_names = set([t.name for t in self.midi_file.tracks])

    for track in req_tracks:
      if track not in mid_track_names:
        raise Exception(f"ERROR: Missing midi track '{track}'")

  def process_sustain(self, sustain):
    cutoff = int(64 * self.midi_file.ticks_per_beat / 192.0)

    if sustain <= cutoff:
      return EventType.IgnoreDuration
  
    return EventType.Empty
  
  def parse_tempo(self):
    tempo_track = self.midi_file.tracks[0]
    if not tempo_track:
      return
    self.tempo_parser.create_tempo_map(tempo_track, self.midi_file.ticks_per_beat)

  def parse_measure(self):
    tempo_track = self.midi_file.tracks[0]
    if not tempo_track:
      return
    self.timesig_parser.create_measure_map(tempo_track)
  
  def parse_beat(self):
    beat_track = self.find_track("BEAT")
    if not beat_track:
      return
    self.beat_parser.create_beatmap(beat_track)

  def get_tempo_map(self):
    return self.tempo_parser.tempo_map
  
  def get_beat_map(self):
    return self.beat_parser.beat_map
  
  def get_measure_map(self):
    return self.timesig_parser.measure_map
  
  def get_final_tick(self):
    last_tick = 0
    for track in self.midi_file.tracks:
      name = track.name

      if name in self.note_parsers:
        final_tick = sum(msg.time for msg in track)
        if final_tick > last_tick:
          last_tick = final_tick

    return last_tick
    
  def build_modifiers(self, track_name):
    track = self.find_track(track_name)
    tick = 0
    events = []
    
    for msg in track:
      tick += msg.time 

      if msg.type == "note_on" and msg.velocity > 0:
        self.notes[msg.note].start(tick) 
      elif (msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0)):
        note = self.notes[msg.note]
        sus = tick - note.tick_start
        note.end(sus)

        if msg.note == 116: # Starpower
          events.append(TrackEvent(note.tick_start, sus, EventType.Starpower))
          events.append(TrackEvent(note.tick_end, 0, EventType.StarpowerEnd))

    events.sort(key=lambda e: e.tick)
    return events

  def parse_tracks(self):
    self.validate_tracks() # Make sure we have needed tracks

    self.parse_tempo()
    self.parse_measure()
    self.parse_beat()

    tempo_map = self.get_tempo_map()
    measure_map = self.get_measure_map()

    final_tick = self.get_final_tick()

    for i in range(len(self.midi_file.tracks)):
      track = self.midi_file.tracks[i]
      track_name = track.name

      if track_name not in self.note_parsers:
        continue

      parser = self.note_parsers[track_name]
      events = self.build_modifiers(track_name)

      tick = 0
      for msg in track:
        tick += msg.time 

        if msg.type == "note_on" and msg.velocity > 0:
          self.notes[msg.note].start(tick) 
        elif (msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0)):
          note = self.notes[msg.note]
          sus = tick - note.tick_start
          note.end(sus)

          modifiers = EventType.Empty
          for event in events:
            if note.tick_start >= event.tick and note.tick_end <= event.tick + event.sus:
              modifiers |= event.event_types

          ignore_flag = self.process_sustain(sus) # Whether or not to ignore the sustain
          parser.process_note(tempo_map, note.clone(), modifiers | ignore_flag)
      
      for j in range(4):
        self.bar_builders[track_name].build(tempo_map, measure_map, parser.gems[j], j, final_tick)