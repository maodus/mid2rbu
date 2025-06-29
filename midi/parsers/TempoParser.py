from rbu.Tempo import TempoInfo, TempoMap

class TempoParser():
  def __init__(self):
    self.tempo_map = None

  def create_tempo_map(self, tempo_track, tpq):
    self.tempo_map = TempoMap(tpq)

    tick = 0
    for msg in tempo_track:
      tick += msg.time
      if msg.is_meta and msg.type == "set_tempo":
          tempo = msg.tempo # Tempo in microseconds per quarter note
          self.tempo_map.tempos.append(TempoInfo(tempo, tick))

    # Set the tick_end for each tempo
    for i in range(len(self.tempo_map.tempos) - 1):
        self.tempo_map.tempos[i].tick_end = self.tempo_map.tempos[i + 1].tick_start

    # Set final tick end to the end of tempo track
    self.tempo_map.tempos[-1].tick_end = tick