import datajoint as dj

from ethopy.core.logger import stimulus
from ethopy.core.stimulus import Stimulus

@stimulus.schema
class Tones(Stimulus, dj.Manual):
    definition = """
    # This class handles the presentation of Tones
    -> stimulus.StimCondition
    ---
    tone_duration             : int                     # tone duration (ms)
    tone_frequency            : int                     # tone frequency (hz)
    tone_volume               : int                     # tone volume (percent)
    tone_pulse_freq           : float                   # frequency of tone pulses (hz)
    """

    def __init__(self):
        super().__init__()
        self.cond_tables = ['Tones']
        self.required_fields = ['tone_duration', 'tone_frequency']
        self.default_key = {'tone_volume': 50, 'tone_pulse_freq': 0}
        self.fill_colors.set({'background': (0, 0, 0),
                              'start': (0.2, 0.2, 0.2),
                              'ready':  (0.3, 0.3, 0.3),
                              'reward': (0.6, 0.6, 0.6),
                              'punish': (0, 0, 0)})

    def start(self):
        tone_frequency = self.curr_cond['tone_frequency']
        tone_volume = self.curr_cond['tone_volume']
        tone_pulse_freq=self.curr_cond['tone_pulse_freq']
        if (1000/tone_pulse_freq)*2 > tone_volume :
            raise ValueError('Tone pulse frequency has to be adjusted for at least 2 clicks per tone duration')
        self.exp.interface.give_sound(tone_frequency, tone_volume, tone_pulse_freq)
        super().start()

    def present(self):
        if self.timer.elapsed_time() > self.curr_cond['tone_duration'] and self.in_operation:
            self.in_operation = False
            self.stop()

    def stop(self):
        self.log_stop()
        self.in_operation = False
        self.exp.interface.stop_sound()

    def exit(self):
        self.exp.interface.stop_sound()