
import random
from . import InformedConsentPage, Introduction, Decision, EndOfSuperGame, EndOfExperiment, ReadMe, Bot, C, Submission

class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield InformedConsentPage
            yield Introduction
        yield Submission(
            Decision,
            dict(
                cooperate=True if random.randint(0, 1) == 1 else False,
                is_pass=0,
                subsequent_timeoutes=0,
                is_dropout=False,
                ),
            check_html=False)
        if (self.player.super_game_round_number == C.ROUNDS_PER_SUPERGAME) and not C.RANDOM_MATCHING:
            yield EndOfSuperGame
        #if self.player.round_number == C.NUM_ROUNDS:
        #    yield EndOfExperiment
