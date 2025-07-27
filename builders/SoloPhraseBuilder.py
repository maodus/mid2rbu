import struct
from midi.Event import EventType
from misc.utils import get_closest_gem_extent

class SoloPhrase():
    def __init__(self, ms, ms_dur, tick, tick_dur, num_gems):
        self.ms = ms
        self.ms_dur = ms_dur
        self.tick = tick
        self.tick_dur = tick_dur
        self.num_gems = num_gems

    def get_bytes(self):
        return struct.pack(
            "<ffIII",
            self.ms,
            self.ms_dur,
            self.tick,
            self.tick_dur,
            self.num_gems
        )

class SoloPhraseBuilder():
    def __init__(self):
        self.solo_phrases = [[], [], [], []]

    def build_solos(self, tempo_map, gems, track_events, difficulty):
        solo_start = [e for e in track_events if e.event_types == EventType.SoloPhraseStart]
        solo_end = [e for e in track_events if e.event_types == EventType.SoloPhraseEnd]

        for i in range(len(solo_start)): # Iterate through all solo events
            start_tick = solo_start[i].tick
            end_tick = solo_end[i].tick

            start_ms = tempo_map.tick2ms(start_tick)
            end_ms = tempo_map.tick2ms(end_tick)
            
            # Grab the gem boundaries in this solo phrase
            start_id, end_id = get_closest_gem_extent(gems, start_tick, end_tick)

            # Make sure gem ids are valid
            if start_id < 0 or end_id < 0:
                continue

            num_solo_gems = end_id - start_id + 1
            gems[start_id].make_solo_start(num_solo_gems)

            # Apply solo flag to all gems in-between
            for j in range(start_id + 1, end_id):
                gems[j].make_solo()

            gems[end_id].make_solo_end()

            # Build and add the solo phrase
            solo_phrase = SoloPhrase(
                start_ms, 
                end_ms - start_ms, 
                start_tick, 
                end_tick - start_tick, 
                num_solo_gems
            )

            self.solo_phrases[difficulty].append(solo_phrase)

    def get_bytes(self, difficulty):
        solos = self.solo_phrases[difficulty]
        byte_arr = bytearray(struct.pack("<I", len(solos)))

        for solo in solos:
            byte_arr.extend(solo.get_bytes())

        return byte_arr
