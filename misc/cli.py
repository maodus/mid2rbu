import argparse

def parse_args():
  parser = argparse.ArgumentParser(description="Converts a MIDI file into a Rockband Unplugged chart.")
  parser.add_argument("midi_path", help="Path to the MIDI file.")

  parser.add_argument(
    "-c", 
    "--config", 
    default = "config.ini",
    help = "Path to the config.ini config file (default: config.ini)",
    metavar = "config_path",
  )

  parser.add_argument(
    "-np", 
    "--no-package", 
    default = False,
    action = "store_true",
    help = "Path to the config.ini config file (default: config.ini)",
  )
  return parser.parse_args()