from rbu.Measure import MeasureMap

class TimeSigParser():
  def __init__(self):
    self.measure_map = None

  def create_measure_map(self, tempo_track):
    self.measure_map = MeasureMap()
    tick = 0
    
    for msg in tempo_track:
      tick += msg.time
      if msg.is_meta and msg.type == "time_signature":
          num = msg.numerator 
          den = msg.denominator

          mbt = self.measure_map.get_mbt(tick)
          self.measure_map.add_time_sig(mbt.measure, num, den)