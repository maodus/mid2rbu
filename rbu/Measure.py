import struct

class TimeSigChange:
  def __init__(self, measure, numerator, denominator, tick):
    self.measure = measure
    self.numerator = numerator
    self.denominator = denominator
    self.tick = tick

  def get_bytes(self):
    return struct.pack("<IIII", self.measure, self.numerator, self.denominator, self.tick)
  
class MBT:
  def __init__(self, measure, beat, tick):
    self.measure = measure
    self.beat = beat
    self.tick = tick 
  
class MeasureMap():
  def __init__(self):
    self.time_sigs = [TimeSigChange(0, 4, 4, 0)]

  def get_time_sig(self, tick):
    i = 0
    while i < len(self.time_sigs):
      ts = self.time_sigs[i]
      if ts.tick > tick:
        break
      i += 1

    if i != 0:
      i -= 1

    return self.time_sigs[i]
  
  def get_mbt(self, raw_tick):
    time_sig = self.get_time_sig(raw_tick)

    # Normalized per measure/bar
    tpm = (time_sig.numerator * 1920) // time_sig.denominator
    tick_diff = raw_tick - time_sig.tick


    # Approx measure number
    measure_diff = (tick_diff) // tpm
    measure_tick = tick_diff % tpm

    return MBT(time_sig.measure + measure_diff, measure_tick // 480, measure_tick % 480)
  
  def add_time_sig(self, measure, num, den):
    if measure == 0:
      if len(self.time_sigs) == 1:
            self.time_sigs[0].numerator = num
            self.time_sigs[0].denominator = den
    else:
      last_sig = self.time_sigs[-1]
      new_tick = last_sig.tick + (last_sig.numerator * (measure - last_sig.measure) * 1920) // last_sig.denominator
      self.time_sigs.append(TimeSigChange(measure, num, den, new_tick))

  def get_bytes(self):
    byte_arr = bytearray(struct.pack("<I", len(self.time_sigs)))

    for k, time_sig in enumerate(self.time_sigs):
      byte_arr.extend(time_sig.get_bytes())

    return byte_arr