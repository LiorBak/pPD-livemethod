
from otree.api import BaseConstants, BaseGroup, BasePlayer, BaseSubsession, Page, models, widgets


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Q_IN_RIGHT_P2 = -5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', max=125, min=13)
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Non-binary', 'Non-binary'], [
                                'Prefer not to say', 'Prefer not to say']], label='Indicate your gender', widget=widgets.RadioSelect)
    full_name = models.LongStringField(label='What is your full name? (for payment purposes only)')
    email = models.LongStringField(label='Your e-mail address @exeter (needed for payment and contact)')
    is_pass_test = models.IntegerField(label=' ')
    survey_optional_text = models.StringField(
        blank=True, label='Do you want to mention anything about your experience?')
    academic_degree = models.StringField(label='What academic degree are you currently pursuing?')
    prefer_300with01_over_23with05 = models.BooleanField()
    prefer_8with05and12with05_over_30at09andMinus270at01 = models.BooleanField()
    questions_order_300_first = models.BooleanField()
    is_risk_first = models.BooleanField()
    is_english_native_language = models.BooleanField(label='Is English your native language?')


def calc_is_risk_first(player: Player):
    import random
    player.is_risk_first = random.random() > 0.5


class RiskPreferences(Page):
    form_model = 'player'
    form_fields = ['prefer_300with01_over_23with05']

    @staticmethod
    def vars_for_template(player: Player):
        calc_is_risk_first(player)
        return dict()


class RiskPreferences2(Page):
    form_model = 'player'
    form_fields = ['prefer_8with05and12with05_over_30at09andMinus270at01']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'full_name', 'academic_degree',
                   'is_english_native_language', 'survey_optional_text']


class Payment_info(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # player.payoff = float(participant.bonus)  # for player.payoff to resemble experiment payoff, so that participant.payoff_plus_participation_fee() will function properly
        return dict(
            fwd_url=get_fwd_url(
                participant.payoff_plus_participation_fee(),
                (participant.label or participant.code)
            )
        )


class EndOfExperiment(Page):
    form_model = 'player'


def get_fwd_url(payment, label: str):
    import base64
    import json
    data = {'computername': label, 'payment': float(payment)}

    enc_data = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    url = "http://ph.feele.exeter.ac.uk?epd="

    return url + enc_data


page_sequence = [RiskPreferences, RiskPreferences2,
                 Demographics, Payment_info, EndOfExperiment]
