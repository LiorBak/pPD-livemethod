
from otree.api import *
c = cu
import random

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 100
    ROUNDS_PER_SUPERGAME = 10
    PAYOFF_DC = cu(30)
    PAYOFF_CC = cu(20)
    PAYOFF_DD = cu(10)
    PAYOFF_CD = cu(0)
    PAYOFF_DC_HIGH = cu(300)
    PAYOFF_DC_LOW = cu(0)
    PAYOFF_DC_PROB_LOW = 0.9
    PAYOFF_CD_HIGH = cu(30)
    PAYOFF_CD_LOW = cu(-270)
    PAYOFF_CD_PROB_HIGH = 0.9
    PENALTY = cu(5)
    IS_TEST = False
    DECISION_TIMEOUT = 15
    FIRST_ROUNDS_TIMOUT = 30
    FRIST_ROUNDS_NUM_FOR_EXTRA_TIME = 3
    RANDOM_BONUS_LOWER_BOUND = 1350
    RANDOM_BONUS_UPPER_BOUND = 5700
    PAYOFF_MATRIX = {
        'PD': {
            (False, True): 30,
            (True, True): 20,
            (False, False): 10,
            (True, False): 0,
            },
        'CG': {
            (False, True): 0,
            (True, True): 20,
            (False, False): 10,
            (True, False): 30,
            },
        'EV-PD beh-PD': {  # behavioralPD_evPD
            (False, True): [25, .9, 75],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [5, .9, -45],            
        },
        'EV-PD beh-CG': {  # behavioralCG_evPD
            (False, True): [0, .9, 300],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [30, .9, -270],            
        },
        'EV-CG beh-CG': {  # behavioralCG_evCG
            (False, True): [5, .9, -45],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [25, .9, 75],            
        },
        'EV-CG beh-PD': {  # behavioralCG_evCG
            (False, True): [30, .9, -270],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [0, .9, 300],            
        },
    }

    INSTRUCTIONS_TEMPLATE = 'prisoner/instructions.html'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):

    # ------------------ set the game for 6 players ---------------
    # only activated if this is not a test
    if C.IS_TEST:
        return
    # -------------------------------------------------------------
    
    import math
    
    num_participants = subsession.session.num_participants
    group_matrices = []
    if num_participants == 4:
        group_matrices = [
            [[1, 2], [3, 4]],
            [[1, 3], [2, 4]],
            [[1, 4], [2, 3]],
        ]
    elif num_participants == 6:
        group_matrices = [
            [[1, 2], [3, 4], [5, 6]],
            [[1, 3], [2, 5], [4, 6]],
            [[1, 4], [2, 6], [3, 5]],
            [[1, 5], [2, 4], [3, 6]],
            [[1, 6], [2, 3], [4, 5]],
        ]
    elif num_participants == 8:
        group_matrices = [
            [[1, 2], [3, 4], [5, 6], [7, 8]],
            [[1, 3], [2, 5], [4, 7], [6, 8]],
            [[1, 4], [2, 6], [3, 8], [5, 7]],
            [[1, 5], [2, 7], [3, 6], [4, 8]],
            [[1, 6], [2, 8], [3, 7], [4, 5]],
            [[1, 7], [2, 4], [3, 5], [6, 8]],
            [[1, 8], [2, 3], [4, 6], [5, 7]],
        ]
    
    if len(group_matrices) > 0:
        if subsession.round_number == 1:
            player = subsession.get_players()[0]
            print( player.session.config['game_type'], 'session started.', C.NUM_ROUNDS, 'rounds.', 'random matching' if player.session.config['random_matching'] else ('fixed matching for', C.ROUNDS_PER_SUPERGAME, 'rounds per sp'))
            if player.session.config['random_matching']:
                for i in range(1, C.NUM_ROUNDS + 1):
                    super_game_number = (i-1)%len(group_matrices)
                    subsession.in_round(i).set_group_matrix(group_matrices[super_game_number])

            else:
                for i in range(1, C.NUM_ROUNDS + 1):
                    super_game_number = math.floor((i-1) / C.ROUNDS_PER_SUPERGAME)%len(group_matrices)
                    subsession.in_round(i).set_group_matrix(group_matrices[super_game_number])
                    # print('SP#',super_game_number, i, ":", group_matrices[super_game_number])
    
class Group(BaseGroup):
    pass
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)
class Player(BasePlayer):
    cooperate = models.BooleanField(choices=[[True, 'Cooperate'], [False, 'Defect']], doc='This player s decision', widget=widgets.RadioSelect)
    opponent_id_in_session = models.StringField(initial='')
    game_type = models.StringField(initial='')
    forgone_payoff = models.CurrencyField()
    rnd_num_for_payoff = models.FloatField()
    opponent_cooperate = models.BooleanField()
    opponent_payoff = models.CurrencyField()
    opponent_number = models.StringField(initial='A')
    super_game_round_number = models.IntegerField()
    penalty = models.CurrencyField(initial=0)
    opponent_penaly = models.CurrencyField(initial=0)
    total_score = models.CurrencyField(initial=0)
    Email = models.StringField(label='Your e-mail address @exeter (needed for payment and contact)')
    chance_to_win_bonus = models.FloatField()
    win_bonus = models.BooleanField()
    total_experiment_payoffGDP = models.FloatField()
    subsequent_timeoutes = models.IntegerField(initial=0)
    decision_time = models.FloatField()
    wait_for_other_time = models.FloatField()
    results_time = models.FloatField(initial=0)  #initial=0 is set for bots
    experiment_start_time = models.FloatField()
    experiment_end_time = models.FloatField()
    is_random_matching = models.BooleanField()
    is_description = models.BooleanField()
    is_pass = models.IntegerField(label='   ')
    is_dropout = models.BooleanField(initial=False)
    screen_width_px = models.FloatField()
    screen_height_px = models.FloatField()
    mobile_device = models.StringField()
    device_info = models.StringField()
def other_player(player: Player):
    return player.get_others_in_group()[0]
def set_payoff(player: Player):
    if player.field_maybe_none('cooperate') is None:
        return  # for the last 3 rounds of risk preferences survey
    
    other = other_player(player)
    player.rnd_num_for_payoff = random.random() if other.field_maybe_none('rnd_num_for_payoff') is None else other.rnd_num_for_payoff
    other.rnd_num_for_payoff = random.random() if player.field_maybe_none('rnd_num_for_payoff') is None else player.rnd_num_for_payoff

    def calculate_payoff(payoff_val, random_treshold):
        if type(payoff_val) == list:  # Returns the payoff based on a random draw and the given probabilities
               # sets both rnd tresholds to ensure opponent's payoff is calculated accuratly
            return payoff_val[0] if random_treshold < payoff_val[1] else payoff_val[2]
        else:
            return payoff_val

    payoff_matrix = C.PAYOFF_MATRIX[player.game_type]        
    player.payoff = calculate_payoff(payoff_matrix[ (player.cooperate, other.cooperate) ], player.rnd_num_for_payoff)
    player.forgone_payoff = calculate_payoff(payoff_matrix[ (not player.cooperate, other.cooperate) ], player.rnd_num_for_payoff)
    player.opponent_payoff = calculate_payoff(payoff_matrix[ (other.cooperate, player.cooperate) ], other.rnd_num_for_payoff)
    
    player.payoff = player.payoff - player.penalty
    player.forgone_payoff = player.forgone_payoff - player.penalty
    player.opponent_penaly = other.penalty
    player.opponent_payoff = player.opponent_payoff - player.opponent_penaly
    
    player.total_score = player.total_score + player.payoff  # total score is set to previous round when entering desicion page (func 'falues for new round')
    
    # set more info
    player.opponent_id_in_session = str(other.participant.id_in_session)
    player.opponent_cooperate = other.cooperate
    
    return dict(
        payoff=player.payoff,
        forgone=player.forgone_payoff,
        opponent_payoff = player.opponent_payoff,
        penalty = player.penalty,
    )

def values_for_new_round(player: Player):
    player.super_game_round_number = ((player.round_number-1) % C.ROUNDS_PER_SUPERGAME) + 1 # The calculations intends to get round 10 = super_game round 10 instead of 0.
    is_new_opponent = (player.super_game_round_number == 1)
    
    player.is_random_matching = player.session.config['random_matching']
    player.is_description = player.session.config['is_description']
    
    if player.round_number > 1:
        #set repeeting values
        player.game_type = player.in_round(1).game_type
        player.is_random_matching = player.in_round(1).is_random_matching
        player.is_description = player.in_round(1).is_description
        player.opponent_number = player.in_round(player.round_number - 1).opponent_number
        player.total_score = player.in_round(player.round_number - 1).total_score
        player.subsequent_timeoutes = player.in_round(player.round_number - 1).subsequent_timeoutes
        player.is_dropout = player.subsequent_timeoutes >= 2
        # set charecter to visualize opponent
        if is_new_opponent:
            player.opponent_number = chr(ord(player.opponent_number)+1) 
        else:
            player.opponent_number = player.in_round(player.round_number - 1).opponent_number
    
    
def set_desicion_time(player: Player, called_from):
    # This funtion is called at page Desicion four times: 
    # a) at vars for template - when page loads, b) when desicion is sent to the server c) when payoffs are calculated d) at before_bext_page - when page ends
    import time
    now = time.time()
    
    if called_from=='decision vars_for_template':
        player.decision_time = now
    elif called_from=='live_method function - wait for other':
        player.wait_for_other_time = now
        player.decision_time = now - player.decision_time
    elif called_from=='live_method function - set payoffs':
        player.results_time = now
        if player.field_maybe_none('wait_for_other_time') == None:  # the other player made desicion first
            player.wait_for_other_time = 0
            player.decision_time = now - player.decision_time
        else:  #we already called this fucntion once from set payoffs
            player.wait_for_other_time = now - player.wait_for_other_time
    elif called_from=='decision before_next_page':
        player.results_time = now - player.results_time 

def calc_total_payoff(player: Player):    
    chance_to_win = (float(player.total_score) + C.RANDOM_BONUS_LOWER_BOUND)/C.RANDOM_BONUS_UPPER_BOUND
    '''
    The lower and upper bounds of probability will be such that if a player plays only (C,D) [or  only (D,C)] for all 100 rounds, he will only have  a 5% (actually 4%) chance to hit the boundary. (Cumulative probability: P(x>15) when x is #getting -270 witn prob .1 in each)
    So p(bonus) = [1350 + Sigma(v_i)] / 5700 
    (We used binomial calculator for the 7.3%, which gets to 10 losses of 270, 15*(-270) + 90*30 = 1,350.
    On the other hand, 300, 15 times, is 4,500. also with 4% prob.
    Finally, we assume mean score per round to be 15. So for 100 rounds it is 1500. 1500+1350/4500=63%
    Thus we increase the dominator to 5,700
    To conclude, the range of points in the probability games are [0, 5700] (with prob. 4% to hit each end, note that since you can’t hit both ends at the same time, the probability of not hitting any end is bigger than 96%, and not 92%).
    '''
    player.chance_to_win_bonus = chance_to_win
    random_number = random.uniform(0, 1)
    player.win_bonus = chance_to_win > random_number
    bonus = 0
    if player.win_bonus:
        bonus = player.session.config['bonus_payment']
    total_payoff = player.session.config['participation_fee'] + bonus
    player.total_experiment_payoffGDP = float(total_payoff)

    # populate payoff values to participant level
    player.participant.vars['payoff'] = float(bonus)
    player.participant.vars['bonus'] = float(bonus)  # this will be used later to overwrite payoff in the survey app
    player.participant.vars['total_score'] = float(player.total_score)
    player.participant.vars['chance_to_win'] = chance_to_win*100
    player.participant.vars['random_lottery_number'] = random_number*100
    player.participant.vars['win_bonus'] = player.win_bonus

    return [chance_to_win, random_number]


class InformedConsentPage(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not C.IS_TEST
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            show_up_fee = int(player.session.config['participation_fee']),
            bonus_fee = player.session.config['bonus_payment'],
        )
class Introduction(Page):
    form_model = 'player'
    form_fields = ['screen_width_px', 'screen_height_px', 'mobile_device', 'device_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 # and not C.IS_TEST
    @staticmethod
    def vars_for_template(player: Player):
        import time
        player.experiment_start_time = time.time()
        player.game_type = player.session.config['game_type']
        
        
        payoff_matrix = C.PAYOFF_MATRIX[player.game_type]
        add_got_text = lambda v: 'get '+ str(v) if v == 0 else ('gain '+ str(v) if v > 0 else 'lose ' + str(abs(v))) + ' points'
        # << copied from Desicion >>
        add_points_text = lambda v: str(v) + ' points'
        def payoff_matrix_to_text(payoff_val): # Returns the payoffs text for the table
            if type(payoff_val) == list: 
                return f'{add_points_text(payoff_val[0])} with <nobr>{round(payoff_val[1]*100)}% chance,</nobr> and <nobr>{add_points_text(payoff_val[2])} with {round((1-payoff_val[1])*100)}% chance</nobr>'
            else:
                return add_points_text(payoff_val)
        # << end of copied from Desicion >>

        def payoff_matrix_to_description(payoff_val): # Returns the payoff text for the description
            if type(payoff_val) == list:  
                return f'{add_got_text(payoff_val[0])} with <nobr>probability {round(payoff_val[1],1)} ({round(payoff_val[1]*100)}% chance),</nobr> and <nobr>{add_got_text(payoff_val[2])} otherwise ({round((1-payoff_val[1])*100)}% chance)</nobr>'
            else:
                return add_got_text(payoff_val)
        
        # ---- set text for desicion table according to game type----
        text_left = {}
        text_right = {}
        text_desc_player = {}
        text_desc_other = {}

        for i in [0, 1]:
            for j in [0,1]:
                ti = 'C' if i == 1 else 'D'
                tj = 'C' if j == 1 else 'D'
                
                text_left[f"{ti}{tj}"] = payoff_matrix_to_text(payoff_matrix[(i,j)]) #player
                text_right[f"{ti}{tj}"] = payoff_matrix_to_text(payoff_matrix[(j,i)]) #opponent

                # _______<< only for introduction >>__________
                text_desc_player[f"{ti}{tj}"] = payoff_matrix_to_description(payoff_matrix[(i,j)])  #player
                text_desc_other[f"{ti}{tj}"] = payoff_matrix_to_description(payoff_matrix[(j,i)])  #opponent
                # _______<< end of 'only for introduction' >>______        
        
        if not player.session.config['is_description']:
            text_left['CC'] = 'Up'
            text_left['CD'] = 'Up'
            text_left['DC'] = 'Down'
            text_left['DD'] = 'Down'

            text_right['CC'] = 'Left'
            text_right['CD'] = 'Right'
            text_right['DC'] = 'Left'
            text_right['DD'] = 'Right'
        # << end of copy from Desicion >>

        bonus_example_points = C.NUM_ROUNDS*15 #assuming 15 is the mean payoff per round
        return dict(
            t_left = text_left,
            t_right = text_right,
            desc_player = text_desc_player,
            desc_other = text_desc_other,
            is_random_matching = player.session.config['random_matching'],
            is_description = player.session.config['is_description'],
            example_payoff_p1 = add_points_text(payoff_matrix[(False, True)][0]),
            example_payoff_p2 =  add_points_text(payoff_matrix[(True, False)][0]),
            example_forgone_payoff_p1 = add_points_text(payoff_matrix[(True, True)][0]),
            show_up_fee = int(player.session.config['participation_fee']),
            bonus_fee = player.session.config['bonus_payment'],
            bonus_example_points = bonus_example_points,
            bonus_example_chance = round(100*(bonus_example_points+C.RANDOM_BONUS_LOWER_BOUND)/C.RANDOM_BONUS_UPPER_BOUND),
            num_opponents = C.NUM_ROUNDS/C.ROUNDS_PER_SUPERGAME,
        )
class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate', 'is_pass', 'subsequent_timeoutes', 'is_dropout']

    
    @staticmethod
    def js_vars(player: Player):
        is_random_matching = player.session.config['random_matching']
        is_extra_time = (player.round_number if is_random_matching else player.super_game_round_number) <= C.FRIST_ROUNDS_NUM_FOR_EXTRA_TIME
        time_limit = dict(
            decision = C.FIRST_ROUNDS_TIMOUT if is_extra_time else C.DECISION_TIMEOUT,
            results = C.FIRST_ROUNDS_TIMOUT if is_extra_time else C.DECISION_TIMEOUT,
        )
        return dict(subsequent_timeoutes=player.subsequent_timeoutes,
                    is_dropout=player.is_dropout,
                    time_limit = time_limit,
                    is_random_matching = is_random_matching,
                    already_made_desicion = (player.field_maybe_none('cooperate') != None),
                    cooperate = player.field_maybe_none('cooperate'),
                    )
    
    @staticmethod
    def live_method(player: Player, data):
        # player here is the sender of the msg
        player.cooperate = data['cooperate']
        print('received a bid from player', player.id_in_group, ':', data, type(data))
        opponent = other_player(player)
        opponent_cooperate = opponent.field_maybe_none('cooperate')

        player.penalty = C.PENALTY if data['timeout'] else 0
             
        if opponent_cooperate == None:
            set_desicion_time(player, 'live_method function - wait for other')
            return
        else: 
            set_desicion_time(player, 'live_method function - set payoffs')
            set_desicion_time(opponent, 'live_method function - set payoffs')

        payoffs_dict_me = None
        payoffs_dict_opponent = None
        if opponent_cooperate is not None:
            payoffs_dict_me = set_payoff(player)
            payoffs_dict_opponent = set_payoff(opponent)

        action_data_me = {
            'cooperate': player.cooperate,
            'sender_id_in_group': player.id_in_group,
            'opponent_cooperate': opponent_cooperate,
            'payoffs_dict': payoffs_dict_me,
        }
        action_data_opp = {
            'cooperate': opponent.cooperate,
            'sender_id_in_group': opponent.id_in_group,
            'opponent_cooperate': player.cooperate,
            'payoffs_dict': payoffs_dict_opponent,
            'passive': True,
        }

        return {
                player.id_in_group: action_data_me,
                opponent.id_in_group: action_data_opp,
                }  # 0 broadcasts it to the whole group, other wise, can explicitly state player id's {2: data, 3: data}
        
    def vars_for_template(player: Player):        
        if C.IS_TEST:
            player.game_type = player.session.config['game_type']
        values_for_new_round(player)
        set_desicion_time(player, 'decision vars_for_template')
        is_new_opponent = True if player.session.config['random_matching'] else (player.super_game_round_number == 1)
        
        # ---- set history for historical scores table -------
        history = []
        history_first_game = player.round_number + 1 - player.super_game_round_number
        if player.session.config['random_matching']:
            history_first_game = 1
        for round_number in range(player.round_number - 1, history_first_game - 1, -1):
            past_player = player.in_round(round_number)
            history.append(past_player)
        
        # ---- Define payoff_matrix -------
        payoff_matrix = C.PAYOFF_MATRIX[player.game_type]
        add_points_text = lambda v: str(v) + ' points'
        def payoff_matrix_to_text(payoff_val):
            if type(payoff_val) == list:  # Returns the payoff description for the table
                return f'{add_points_text(payoff_val[0])} with <nobr>{round(payoff_val[1]*100)}% chance,</nobr> and <nobr>{add_points_text(payoff_val[2])} with {round((1-payoff_val[1])*100)}% chance</nobr>'
            else:
                return add_points_text(payoff_val)
        
        # ---- set text for desicion table according to game type----
        text_left = {}
        text_right = {}

        for i in [0, 1]:
            for j in [0,1]:
                ti = 'C' if i == 1 else 'D'
                tj = 'C' if j == 1 else 'D'
                text_left[f"{ti}{tj}"] = payoff_matrix_to_text(payoff_matrix[(i,j)])  #player
                text_right[f"{ti}{tj}"] = payoff_matrix_to_text(payoff_matrix[(j,i)])  #opponent
        
        if not player.session.config['is_description']:
            text_left['CC'] = 'Up'
            text_left['CD'] = 'Up'
            text_left['DC'] = 'Down'
            text_left['DD'] = 'Down'

            text_right['CC'] = 'Left'
            text_right['CD'] = 'Right'
            text_right['DC'] = 'Left'
            text_right['DD'] = 'Right'

        # ------------------
        return dict(
            is_new_supergame = (is_new_opponent and not player.session.config['random_matching']),
            history = history,
            t_left = text_left,
            t_right = text_right,
            is_random_matching = player.session.config['random_matching'],
            is_history_table = player.session.config['is_description'],
            is_played = (player.field_maybe_none('cooperate') != None),
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_desicion_time(player, 'decision before_next_page') # last run as the page ends

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    @staticmethod
    def is_displayed(player: Player):
        # just fot bots to prevent them from submitting pages ahead of time
        return player.session.config['use_browser_bots']

class EndOfSuperGame(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.super_game_round_number == C.ROUNDS_PER_SUPERGAME) and not player.session.config['random_matching']
    @staticmethod
    def vars_for_template(player: Player):
        # ---- set history for historical scores table -------
        history = []
        super_game_start = player.round_number + 1 - player.super_game_round_number
        for round_number in range(super_game_start, player.round_number + 1):
                past_player = player.in_round(round_number)
                history.append(past_player)
        
        game_num = round(player.round_number/C.ROUNDS_PER_SUPERGAME)
        
        return dict(
            history = history,
            game_num = game_num,
        )
    @staticmethod
    def get_timeout_seconds(player: Player):
        return (5/3)*C.DECISION_TIMEOUT
class EndOfExperiment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        import time
        player.experiment_end_time = time.time()
        player.experiment_start_time = player.in_round(1).field_maybe_none('experiment_start_time')
        chance_to_win, random_number = calc_total_payoff(player)
        
        return dict(
            bonus_chance = chance_to_win*100,
            bonus_prob = chance_to_win,
            lottery_num = random_number,
            show_up_fee = int(player.session.config['participation_fee']),
            bonus_fee = player.session.config['bonus_payment'],
        )
class ReadMe(Page):
    pass
page_sequence = [InformedConsentPage, Introduction, Decision, ResultsWaitPage, EndOfExperiment]
