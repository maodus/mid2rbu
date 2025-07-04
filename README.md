# mid2rbu

> This project is not affiliated with or endorsed by Harmonix, MTV Games, EA, or any other official entity associated with Rock Band. It is a fan-made utility for educational and personal use only.

mid2rbu is a Python tool for converting standard MIDI files (.mid) into a format playable by Rock Band Unplugged. 

## Requirements

- Python 3.7+  
  You can check your version with: `python3 --version`

- Python dependencies:
  - mido (MIDI file parsing)

  Install it via pip: `pip install mido`

## Installation

1. Clone the repository:
   `git clone https://github.com/maodus/mid2rbu.git`

2. `cd mid2rbu`

3. Install dependencies: `pip install mido`

## Usage

Note: This tool only currently supports Fortnite Festival midi charts. Support for other Rock Band-style charts will be added in the future. The difference between a Festival chart and a regular Rockband chart is how the vocal notes are charted. Festival vocal notes are charted in a manner similar to any other instrument track (easy 1:1 note to lane mapping). However, vocal charts from other Rock Band games cannot be simply mapped to in-game lanes and will require further parser development. If you choose to use a midi chart that contains complex vocal mappings, the vocal notes will likely not function correctly in game at this time.

<br/>

For a general overview of the program, you can run the program with the help parameter like so:

`python3 mid2rbu.py -h`

<br/>

In order to convert a Fortnite Festival midi chart into a Rock Band Unplugged chart, specify the filepath of your Festival chart in the program arguments.

`python3 mid2rbu.py path/to/song.mid`

This will create a `ZSONG.rbu` file, which you will need to drag-n-drop into the DLC subdirectory of your custom song, as per the instructions found on the [Unplugged Deluxe](https://github.com/maodus/UnpluggedDeluxe#custom-songs) installation guide. This `.rbu` file contains all of the information about your custom chart that the game needs to know about.

## Limitations

Due to the nature of how these custom charts are injected into the game's memory, any track that contains too many notes/gems runs the risk of overwriting existing internal game memory. Other factors such as too much tempo/beat/time signature information can also run this risk, however this is far less likely. If you find that when playing your custom song, you experience crashing or instability, your chart is likely too large and will have to be trimmed.


## Config
Coming soon

## Acknowledgements

This project would not have been possible without help from the following:

- The mido library for MIDI parsing.
- MiloHax Discord server.
- Contributors of the RB3 decompilation effort.
