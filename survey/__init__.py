
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
    in_right_p2 = models.IntegerField(
        label='If player 1 plays OUT, and player 2 plays RIGHT, how much points would player 2 earn?')
    in_left_p2 = models.IntegerField()
    in_right_p1 = models.IntegerField()
    Q_IN_RIGHT_P2_ASNWERS = models.LongStringField(initial='[')
    is_pass_test = models.IntegerField(label=' ')
    survey_optional_text = models.StringField(
        blank=True, label='Do you want to mention anything about your experience?')
    academic_degree = models.StringField(label='What academic degree are you currently pursuing?')
    c7_or_30at09_otherwise_minus270 = models.BooleanField(label='')
    c9_or_30at09_otherwise_minus270 = models.BooleanField()
    c11_or_30at09_otherwise_minus270 = models.BooleanField()
    questions_order = models.StringField()
    is_risk_first = models.BooleanField()
    is_english_native_language = models.BooleanField(label='Is English your native language?')


def calc_is_risk_first(player: Player):
    import random
    player.is_risk_first = random.random() > 0.5


class UnderstandingTest(Page):
    form_model = 'player'
    form_fields = ['in_right_p2', 'is_pass_test']

    @staticmethod
    def is_displayed(player: Player):
        return False


class RiskPreferences(Page):
    form_model = 'player'
    form_fields = ['c9_or_30at09_otherwise_minus270']

    @staticmethod
    def vars_for_template(player: Player):
        calc_is_risk_first(player)
        return dict()


class RiskPreferences2(Page):
    form_model = 'player'
    form_fields = ['c11_or_30at09_otherwise_minus270']


class RiskPreferences3(Page):
    form_model = 'player'
    form_fields = ['c7_or_30at09_otherwise_minus270']


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'full_name', 'academic_degree',
                   'is_english_native_language', 'survey_optional_text']


class Payment_info(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # for player.payoff to resemble experiment payoff, so that participant.payoff_plus_participation_fee() will function properly
        player.payoff = participant.bonus - participant.total_score  
        player.session.config['real_world_currency_per_point'] = 1
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


page_sequence = [UnderstandingTest, RiskPreferences, RiskPreferences2,
                 RiskPreferences3, Demographics, Payment_info, EndOfExperiment]
