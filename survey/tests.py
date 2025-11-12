
from . import RiskPreferences, RiskPreferences2, Demographics
from otree.api import Bot

class PlayerBot(Bot):
    def play_round(self):
        yield RiskPreferences, dict(prefer_300with01_over_23with05=1)
        yield RiskPreferences2, dict(prefer_8with05and12with05_over_30at09andMinus270at01=0)
        yield Demographics, dict(age=20, gender="Male", full_name="John Doe", academic_degree="MSc",
                                 is_english_native_language="No", survey_optional_text="Blah")
