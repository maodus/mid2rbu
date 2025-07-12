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

**Note**: This tool works best with Fortnite Festival charts, but normal Rock Band charts are supported (although they may not be exactly 1:1).

For a general overview of the program, you can run the program with the help parameter like so:

- `python3 mid2rbu.py -h`

In order to convert a Rock Band/Fortnite Festival midi chart into a Rock Band Unplugged chart, specify the filepath of your Festival chart in the program arguments.

- `python3 mid2rbu.py path/to/song.mid`

This will create a `ZSONG.rbu` file, which you will need to drag-n-drop into the DLC subdirectory of your custom song, as per the instructions found on the [Unplugged Deluxe](https://github.com/maodus/UnpluggedDeluxe#custom-songs) installation guide. This `.rbu` file contains all of the information about your custom chart that the game needs to know about.

## Limitations

Due to the nature of how these custom charts are injected into the game's memory, any track that contains too many notes/gems runs the risk of overwriting existing internal game memory. Other factors such as too much tempo/beat/time signature information can also run this risk, however this is far less likely. If you find that when playing your custom song, you experience crashing or instability, your chart is likely too large and will have to be trimmed.

## Config

### Song

| Key | Description | Example Value |
|---|---|---|
| `Name` | Song title. Maximum length of **47 characters**. | `KNOW YOUR ENEMY` |
| `Artist` | Artist or band name. Maximum length of **47 characters** | `GREEN DAY` |
| `InitialTrack` | Track that is initially displayed when starting the song. <br><br>• `0` = Drums <br>• `1` = Bass <br>• `2` = Guitar <br>• `3` = Vocals | `0` |
| `DifficultyOffset` | Difficulty category in which your song will be displayed under. <br><br>• `0` = Warmup <br>• `1` = Apprentice <br>• `2` = Solid <br>• `3` = Moderate <br>• `4` = Challenging <br>• `5` = Nightmare <br>• `6` = Impossible | `0` |
| `GenreOffset` | Musical genre index.  <br><br>• `0` = Alternative <br>• `1` = Blues <br>• `2` = Classic Rock <br>• `3` = Country <br>• `4` = Emo <br>• `5` = Fusion <br>• `6` = Glam <br>• `7` = Grunge <br>• `8` = Indie Rock <br>• `9` = Jazz <br>• `10` = Metal <br>• `11` = Novelty <br>• `12` = Nu-Metal <br>• `13` = Pop-Rock <br>• `14` = Prog <br>• `15` = Punk <br>• `16` = Rock <br>• `17` = Southern Rock <br>• `18` = Urban <br>• `19` = Other  | `0` |
| `EraOffset` | Musical era index. <br><br>• `0` = 60's <br>• `1` = 70's <br>• `2` = 80's <br>• `3` = 90's <br>• `4` = 00's | `0` |
| `BandDifficulty` | Overall difficulty rating considering all tracks. **Range: 0–6.** | `6` |
| `DrumDifficulty` |  Difficulty rating of the drum track. **Range: 0–6.**   | `1` |
| `BassDifficulty` |  Difficulty rating of the bass track. **Range: 0–6.**   | `2` |
| `GuitarDifficulty` |  Difficulty rating of the guitar track. **Range: 0–6.**   | `3` |
| `VocalDifficulty` |  Difficulty rating of the vocal track. **Range: 0–6.**   | `4` |

### Parser

| Key | Description | Example Value |
|---|---|---|
| `PitchedVocals` | Whether or not to interpret the vocal track as pitched notes. Set this to `True` if the vocal track was not charted like a regular instrument, but instead considers the vocal pitch of the singer (usual case with Rock Band charts). Otherwise, set this value to `False` (like in the case of a Fortnite Festival chart). **\*WIP\*** | `True` |
| `*Instrument*LaneMap` | Enables the ability to re-assign gem colours. If you wanted to move red gems to the blue lane (vice-versa), you would do something like this: `red=blue,yellow=yellow,green=green,blue=red`. <br><br> **Note**: This doesnt actually move the gameplay position of each lane/fret, it only changes the gems that would appear on them. | `red=blue,yellow=yellow,green=green,blue=red` |

### PostProcess

| Key | Description | Example Value |
|---|---|---|
| `EnablePruning` | When converted, some charts position gems in such ways that are almost impossible to hit. This setting attempts to delete some of these offending gems in order to make the chart more playable. | `True` |
| `PruneDelta` | The millisecond threshold between two gems before gem pruning is applied. | `120` |
| `SparseMultiGems` | Many multi-gems (especially on drum tracks) often require the use of a single hand to hit two notes at once. This may feel awkward in many game-play scenarios. This option will convert any of these note instances to a more sparse multi-gem, one that will utilize a two-hand control scheme instead of just one. For example, a red/yellow note multi-gem will be converted to a yellow/blue note multi-gem.  | `False` |

## Acknowledgements

This project would not have been possible without help from the following:

- The mido library for MIDI parsing.
- MiloHax Discord server.
- Contributors of the RB3 decompilation effort.
- [Dylan/Djx](https://www.youtube.com/@djx1100REBORN) for testing, suggestions, and improvements.
