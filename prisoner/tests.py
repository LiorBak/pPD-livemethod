
import random
from . import InformedConsentPage, Introduction, Decision, EndOfSuperGame, EndOfExperiment, ReadMe, Bot, C, Submission

class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield InformedConsentPage
            yield Introduction, dict(screen_width_px=1, screen_height_px=1, mobile_device='test_bot', device_info='test_bot')
        yield Submission(
            Decision,
            dict(
                cooperate=True if random.randint(0, 1) == 1 else False,
                is_pass=0,
                subsequent_timeoutes=0,
                is_dropout=False,
                ),
            check_html=False)
        if (self.player.super_game_round_number == C.ROUNDS_PER_SUPERGAME) and not self.player.session.config['random_matching']:
            yield EndOfSuperGame
        if self.player.round_number == C.NUM_ROUNDS:
            pass
        #    yield EndOfExperiment
