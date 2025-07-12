import mido
import struct
import configparser
import argparse
from pathlib import Path

from midi.parsers.MidiParser import MidiParser

VERSION = 1

# Song Info
default_song_config = {
  "Name" : "CUSTOM SONG",
  "Artist": "UNKNOWN",
  "DifficultyOffset": 0,
  "GenreOffset" : 0,
  "EraOffset" : 0,
  "InitialTrack" : 3,
  "DrumDifficulty" : 1,
  "GuitarDifficulty" : 2,
  "BassDifficulty" : 3,
  "VocalDifficulty" : 4,
  "BandDifficulty" : 5,
}

# Parsing
default_parser_config = {
  "PitchedVocals" : True,
  "DrumLaneMap" : "red=red, yellow=yellow, green=green, blue=blue",
  "BassLaneMap" : "red=red, yellow=yellow, green=green, blue=blue",
  "GuitarLaneMap" : "red=red, yellow=yellow, green=green, blue=blue",
  "VocalLaneMap" : "red=red, yellow=yellow, green=green, blue=blue"
}

# Post Processing
default_pp_config = {
   "EnablePruning" : True,
   "PruneDelta" : 120,
   "SparseMultiGems" : True
}

def parse_value(value, default):
  '''Converts the value to the type of the default, or returns the default on failure.'''
  try:
      return type(default)(value)
  except (ValueError, TypeError):
      print(f"Warning: Could not parse '{value}' as {type(default).__name__}, using default '{default}'")
      return default
  
def parse_bool(config, sect, key, default):
  try:
    return config.getboolean(sect, key, fallback=default)
  except (ValueError, TypeError):
    print(f"Warning: Key {key} could not be parsed as a boolean, using default '{default}'")
    return default 

def validate_lane_maps(config, default_config):
  instruments = ["Drum", "Bass", "Guitar", "Vocal"]

  for instr in instruments:
    colours = {"red" : 0, "green" : 0, "yellow" : 0, "blue" : 0}
    key = instr + "LaneMap"

    # Assumption: config has already parsed and is not missing keys
    mapping_str = config[key]
    split_map = [c.strip() for c in mapping_str.split(",")]

    if len(split_map) != 4:
        config[key] = default_config[key]
        continue

    for assignment in split_map:
      split_assign = assignment.split("=")
    
      if len(split_assign) != 2:
        break
      
      l, r = split_assign[0].strip(), split_assign[1].strip()

      if l not in colours or r not in colours:
        break
      
      colours[l] += 1
      colours[r] += 1
  
    for colour in colours:
      if colours[colour] != 2:
        config[key] = default_config[key]
        break
    
  
def load_config_ini(file_path):
  config = configparser.ConfigParser()
  config.read(file_path)
  return config

def load_config_section(sect, config, defaults):
  results = {}
  config_sect = config[sect] if sect in config else {}
  if not config_sect:
      print(f"Warning: {sect} section missing. Using defaults for all fields.")

  for key, default_value in defaults.items():
      if key in config_sect:
          if type(default_value) == type(True):
            results[key] = parse_bool(config, sect, key, default_value)
          else:
            results[key] = parse_value(config_sect[key], default_value)
      else:
          print(f"Warning: Key '{key}' is missing, using default value.")
          results[key] = default_value

  return results

def print_section_info(header_str, section):
  print(header_str)
  for key, value in section.items():
      print(f"  {key}: {value}")

def clean_file_name(file_name):
   clean_name = "".join(c.upper() for c in file_name if c.isalnum())
   return "Z" + clean_name + ".rbu"

def parse_args():
  parser = argparse.ArgumentParser(description="Converts a MIDI file into a Rockband Unplugged chart.")
  parser.add_argument("midi_path", help="Path to the MIDI file.")
  parser.add_argument("-c", "--config", default="config.ini", help="Path to the config.ini config file (default: config.ini)")
  return parser.parse_args()

if __name__ == "__main__":
  # Parse CL args
  args = parse_args()

  # Parse and display config value
  ini_config = load_config_ini(args.config)
  song_info = load_config_section("Song", ini_config, default_song_config)
  parser_config = load_config_section("Parser", ini_config, default_parser_config)
  pp_config = load_config_section("PostProcess", ini_config, default_pp_config)

  validate_lane_maps(parser_config, default_parser_config)

  print_section_info("Extracted song info:", song_info)
  print_section_info("Extracted parser config:", parser_config)
  print_section_info("Extracted post processing config:", pp_config)

  # Load and parse midi file
  mid = mido.MidiFile(args.midi_path)
  midi_parser = MidiParser(mid, parser_config, pp_config)
  midi_parser.parse_tracks()

  part_order = ["PART DRUMS", "PART BASS", "PART GUITAR", "PART VOCALS"]
  difficulties = ["easy", "medium", "hard", "expert"]
  rbu_file_name = clean_file_name(Path(args.midi_path).stem)
  with open (rbu_file_name, "wb") as f:

    track_difficulties = (
      (song_info["DrumDifficulty"]   & 0xF) |
      (song_info["GuitarDifficulty"] & 0xF) << 4 |
      (song_info["BassDifficulty"]   & 0xF) << 8 |
      (song_info["VocalDifficulty"]  & 0xF) << 12 |
      (song_info["BandDifficulty"]   & 0xF) << 16
    )

    header = struct.pack(
      "<I48s48sIIIII124x",
      VERSION,
      song_info["Name"].encode('ascii'),
      song_info["Artist"].encode('ascii'),
      song_info["DifficultyOffset"],
      song_info["GenreOffset"],
      song_info["EraOffset"],
      song_info["InitialTrack"],
      track_difficulties
    )

    # Write header
    f.write(header)

    # Write tempo map
    f.write(midi_parser.get_tempo_map().get_bytes())

    # Write beat map
    f.write(midi_parser.get_beat_map().get_bytes())

    # Write measure map
    f.write(midi_parser.get_measure_map().get_bytes())

    for difficulty in range(4):
      diff_start = f.tell()
      f.write(struct.pack("<I", 0)) # Write difficulty length stub
      for part in part_order:
        f.write(midi_parser.note_parsers[part].get_bytes(difficulty)) # Length followed by gem data

      gem_size = f.tell() - diff_start

      for part in part_order:
        f.write(midi_parser.bar_builders[part].get_bytes(difficulty)) # Length followed by bar data

      diff_end = f.tell()
      section_size = diff_end - diff_start - 4

      f.seek(diff_start, 0)
      f.write(struct.pack("<I", section_size)) # Fill in section length stub
      f.seek(diff_end, 0)

      print(f"Size of {difficulties[difficulty]} section: {diff_end - diff_start} bytes")