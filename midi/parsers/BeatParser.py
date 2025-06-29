from rbu.Beat import BeatInfo, BeatMap

class BeatParser:
  def __init__(self):
    self.beat_map = None

  def create_beatmap(self, beat_track):
    self.beat_map = BeatMap()

    tick = 0
    for msg in beat_track:
      tick += msg.time 
      if msg.type == "note_on":
        level = 1 if msg.note == 12 else 0
        self.beat_map.add_beat(BeatInfo(tick, level))