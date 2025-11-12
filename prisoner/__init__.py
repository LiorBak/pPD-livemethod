
from otree.api import *
c = cu
import random

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 64
    ROUNDS_PER_SUPERGAME = 8
    PENALTY = cu(5)
    IS_TEST = False
    DECISION_TIMEOUT = 15
    FIRST_ROUNDS_TIMOUT = 30
    FRIST_ROUNDS_NUM_FOR_EXTRA_TIME = 3
    RANDOM_BONUS_LOWER_BOUND = 1350
    RANDOM_BONUS_UPPER_BOUND = 5700
    SCORE_MATRIX = {
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
        
        '-95EV-PD beh-PD': {  # behavioralPD_evPD
            (False, True): [25, .95, 125],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [5, .95, -95],            
        },
        '95EV-PD beh-CG': {  # behavioralCG_evPD
            (False, True): [0, .95, 600],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [30, .95, -570],            
        },
        '-95EV-CG beh-CG': {  # behavioralCG_evCG
            (False, True): [5, .95, -95],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [25, .95, 125],            
        },
        '95EV-CG beh-PD': {  # behavioralCG_evCG
            (False, True): [30, .95, -570],
            (True, True): [17, .5, 23],
            (False, False): [8, .5, 12],
            (True, False): [0, .95, 600],            
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
    # Round-Robin scheduling
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
            [[1, 8], [2, 7], [3, 6], [4, 5]],
            [[1, 7], [8, 6], [2, 5], [3, 4]],
            [[1, 6], [7, 5], [8, 4], [2, 3]],
            [[1, 5], [6, 4], [7, 3], [8, 2]],
            [[1, 4], [5, 3], [6, 2], [7, 8]],
            [[1, 3], [4, 2], [5, 8], [6, 7]],
            [[1, 2], [3, 8], [4, 7], [5, 6]],
        ]

    elif num_participants == 10:
        group_matrices = [
            [[1, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[1, 9], [10, 8], [2, 7], [3, 6], [4, 5]],
            [[1, 8], [9, 7], [10, 6], [2, 5], [3, 4]],
            [[1, 7], [8, 6], [9, 5], [10, 4], [2, 3]],
            [[1, 6], [7, 5], [8, 4], [9, 3], [10, 2]],
            [[1, 5], [6, 4], [7, 3], [8, 2], [9, 10]],
            [[1, 4], [5, 3], [6, 2], [7, 10], [8, 9]],
            [[1, 3], [4, 2], [5, 10], [6, 9], [7, 8]],
            [[1, 2], [3, 10], [4, 9], [5, 8], [6, 7]],
        ]

    elif num_participants == 12:
        group_matrices = [
            [[1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]],
            [[1, 11], [12, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[1, 10], [11, 9], [12, 8], [2, 7], [3, 6], [4, 5]],
            [[1, 9], [10, 8], [11, 7], [12, 6], [2, 5], [3, 4]],
            [[1, 8], [9, 7], [10, 6], [11, 5], [12, 4], [2, 3]],
            [[1, 7], [8, 6], [9, 5], [10, 4], [11, 3], [12, 2]],
            [[1, 6], [7, 5], [8, 4], [9, 3], [10, 2], [11, 12]],
            [[1, 5], [6, 4], [7, 3], [8, 2], [9, 12], [10, 11]],
            [[1, 4], [5, 3], [6, 2], [7, 12], [8, 11], [9, 10]],
            [[1, 3], [4, 2], [5, 12], [6, 11], [7, 10], [8, 9]],
            [[1, 2], [3, 12], [4, 11], [5, 10], [6, 9], [7, 8]],
        ]
    
    elif num_participants == 14:
        group_matrices = [
            [[1, 14], [2, 13], [3, 12], [4, 11], [5, 10], [6, 9], [7, 8]],
            [[1, 13], [14, 12], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]],
            [[1, 12], [13, 11], [14, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[1, 11], [12, 10], [13, 9], [14, 8], [2, 7], [3, 6], [4, 5]],
            [[1, 10], [11, 9], [12, 8], [13, 7], [14, 6], [2, 5], [3, 4]],
            [[1, 9], [10, 8], [11, 7], [12, 6], [13, 5], [14, 4], [2, 3]],
            [[1, 8], [9, 7], [10, 6], [11, 5], [12, 4], [13, 3], [14, 2]],
            [[1, 7], [8, 6], [9, 5], [10, 4], [11, 3], [12, 2], [13, 14]],
            [[1, 6], [7, 5], [8, 4], [9, 3], [10, 2], [11, 14], [12, 13]],
            [[1, 5], [6, 4], [7, 3], [8, 2], [9, 14], [10, 13], [11, 12]],
            [[1, 4], [5, 3], [6, 2], [7, 14], [8, 13], [9, 12], [10, 11]],
            [[1, 3], [4, 2], [5, 14], [6, 13], [7, 12], [8, 11], [9, 10]],
            [[1, 2], [3, 14], [4, 13], [5, 12], [6, 11], [7, 10], [8, 9]],
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
    score =  models.CurrencyField(initial=0)
    forgone_score = models.CurrencyField()
    rnd_num_for_score = models.FloatField()
    opponent_cooperate = models.BooleanField()
    opponent_score = models.CurrencyField()
    opponent_number = models.StringField(initial='A')
    super_game_round_number = models.IntegerField()
    penalty = models.CurrencyField(initial=0)
    opponent_penaly = models.CurrencyField(initial=0)
    total_score = models.CurrencyField(initial=0)
    mean_cooperation = models.FloatField(initial=0)
    chance_to_win_bonus = models.FloatField()
    random_number_for_bonus = models.FloatField()
    win_bonus = models.BooleanField()
    total_experiment_payoffGBP = models.FloatField()
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
    is_UPbutton_cooperation = models.BooleanField()
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
    player.rnd_num_for_score = random.random() if other.field_maybe_none('rnd_num_for_score') is None else other.rnd_num_for_score
    other.rnd_num_for_score = random.random() if player.field_maybe_none('rnd_num_for_score') is None else player.rnd_num_for_score

    def calculate_score(score_val, random_treshold):
        if type(score_val) == list:  # Returns the payoff based on a random draw and the given probabilities
               # sets both rnd tresholds to ensure opponent's score is calculated accuratly
            return score_val[0] if random_treshold < score_val[1] else score_val[2]
        else:
            return score_val

    score_matrix = C.SCORE_MATRIX[player.game_type]        
    player.score = calculate_score(score_matrix[ (player.cooperate, other.cooperate) ], player.rnd_num_for_score)
    player.forgone_score = calculate_score(score_matrix[ (not player.cooperate, other.cooperate) ], player.rnd_num_for_score)
    player.opponent_score = calculate_score(score_matrix[ (other.cooperate, player.cooperate) ], other.rnd_num_for_score)
    
    player.score = player.score - player.penalty
    player.forgone_score = player.forgone_score - player.penalty
    player.opponent_penaly = other.penalty
    player.opponent_score = player.opponent_score - player.opponent_penaly
    
    # setting comulative values
    player.total_score = player.total_score + player.score  # total score is set to previous round when entering desicion page (func 'falues for new round')
    cooperate_int =  1 if player.cooperate else 0
    r = player.round_number
    player.mean_cooperation = cooperate_int if r == 1 else ((player.in_round(r-1).mean_cooperation*(r-1))+cooperate_int) / r
    
    # set more info
    player.opponent_id_in_session = str(other.participant.id_in_session)
    player.opponent_cooperate = other.cooperate
    
    return dict(
        score=player.score,
        forgone=player.forgone_score,
        opponent_score = player.opponent_score,
        penalty = player.penalty,
    )

def values_for_new_round(player: Player):
    player.super_game_round_number = ((player.round_number-1) % C.ROUNDS_PER_SUPERGAME) + 1 # The calculations intends to get round 10 = super_game round 10 instead of 0.
    is_new_opponent = (player.super_game_round_number == 1)
    
    player.is_random_matching = player.session.config['random_matching']
    player.is_description = player.session.config['is_description']
    player.device_info = 'EV_display' if player.session.config['EV_display'] else ''
    
    if player.round_number > 1:
        #set repeeting values
        player.game_type = player.in_round(1).game_type
        player.is_random_matching = player.in_round(1).is_random_matching
        player.is_description = player.in_round(1).is_description
        player.opponent_number = player.in_round(player.round_number - 1).opponent_number
        player.total_score = player.in_round(player.round_number - 1).total_score
        player.subsequent_timeoutes = player.in_round(player.round_number - 1).subsequent_timeoutes
        player.is_dropout = player.subsequent_timeoutes >= 2
        player.is_UPbutton_cooperation = player.in_round(1).is_UPbutton_cooperation
        # set charecter to visualize opponent
        if is_new_opponent:
            player.opponent_number = chr(ord(player.opponent_number)+1) 
        else:
            player.opponent_number = player.in_round(player.round_number - 1).opponent_number
    
    
def set_desicion_time(player: Player, called_from):
    # This funtion is called at page Desicion four times: 
    # a) at vars for template - when page loads, b) when desicion is sent to the server c) when scores are calculated d) at before_bext_page - when page ends
    import time
    now = time.time()
    
    if called_from=='decision vars_for_template':
        player.decision_time = now
    elif called_from=='live_method function - wait for other':
        player.wait_for_other_time = now
        player.decision_time = now - player.decision_time
    elif called_from=='live_method function - set scores':
        player.results_time = now
        if player.field_maybe_none('wait_for_other_time') == None:  # the other player made desicion first
            player.wait_for_other_time = 0
            player.decision_time = now - player.decision_time
        else:  #we already called this fucntion once from set scores
            player.wait_for_other_time = now - player.wait_for_other_time
    elif called_from=='decision before_next_page':
        player.results_time = now - player.results_time 

def calc_total_score(player: Player):    
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
    player.random_number_for_bonus = random_number
    player.win_bonus = chance_to_win > random_number
    bonus = 0
    if player.win_bonus:
        bonus = player.session.config['bonus_payment']
    player.payoff = float(bonus)  # for player.payoff to resemble experiment payoff, so that participant.payoff_plus_participation_fee() will function properly
    total_payoffGBP = player.session.config['participation_fee'] + bonus
    player.total_experiment_payoffGBP = float(total_payoffGBP)
    player.participant.payoff_plus_participation_fee()

    # populate payoff values to participant level
    player.participant.vars['payoff'] = float(bonus)
    player.participant.vars['bonus'] = float(bonus)  # this will be used later to overwrite payoff in the survey app
    player.participant.vars['total_score'] = float(player.total_score)
    player.participant.vars['chance_to_win'] = chance_to_win*100
    player.participant.vars['random_lottery_number'] = random_number*100
    player.participant.vars['win_bonus'] = player.win_bonus
    player.participant.vars['mean_cooperation'] = player.mean_cooperation

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
        player.is_UPbutton_cooperation = False if random.random()<.5 else True
        
        score_matrix = C.SCORE_MATRIX[player.game_type]
        add_got_text = lambda v: 'get '+ str(v) if v == 0 else ('gain '+ str(v) if v > 0 else 'lose ' + str(abs(v))) + ' points'
        # << copied from Desicion >>
        add_points_text = lambda v: str(v) + ' points'
        def score_matrix_to_text(score_val): # Returns the scores text for the table
            if type(score_val) == list: 
                return f'{add_points_text(score_val[0])} with <nobr>{round(score_val[1]*100)}% chance,</nobr> and <nobr>{add_points_text(score_val[2])} with {round((1-score_val[1])*100)}% chance</nobr>'
            else:
                return add_points_text(score_val)
        # << end of copied from Desicion >>

        def score_matrix_to_description(score_val): # Returns the score text for the description
            if type(score_val) == list:  
                return f'{add_got_text(score_val[0])} with <nobr>probability {round(score_val[1],2)} ({round(score_val[1]*100)}% chance),</nobr> and <nobr>{add_got_text(score_val[2])} otherwise ({round((1-score_val[1])*100)}% chance)</nobr>'
            else:
                return add_got_text(score_val)
        
        def get_ev(matrix, player_coop, other_coop):
            value = matrix[(bool(player_coop), bool(other_coop))]
            if isinstance(value, list) and len(value) == 3:
                a, p, b = value
                return cu(int(round(p * a + (1 - p) * b)))
            return cu(int(round(value)))
        
        # ---- set text for desicion table according to game type----
        text_left = {}
        text_right = {}
        text_desc_player = {}
        text_desc_other = {}

        # if full description of payof structure:
        for i in [0, 1]:
            for j in [0,1]:
                ti = 'C' if i == 1 else 'D'
                tj = 'C' if j == 1 else 'D'
                
                text_left[f"{ti}{tj}"] = score_matrix_to_text(score_matrix[(i,j)]) #player
                text_right[f"{ti}{tj}"] = score_matrix_to_text(score_matrix[(j,i)]) #opponent

                # _______<< only for introduction >>__________
                text_desc_player[f"{ti}{tj}"] = score_matrix_to_description(score_matrix[(i,j)])  #player
                text_desc_other[f"{ti}{tj}"] = score_matrix_to_description(score_matrix[(j,i)])  #opponent
                # _______<< end of 'only for introduction' >>______        
        
        if player.session.config['EV_display']:
            def add_ev_text(value):
                return str(int(value)) + ' points in expectation'
            text_left['CC'] = add_ev_text(get_ev(score_matrix, 1, 1))
            text_left['CD'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_left['DC'] = add_ev_text(get_ev(score_matrix, 0, 1))
            text_left['DD'] = add_ev_text(get_ev(score_matrix, 0, 0))

            text_right['CC'] = add_ev_text(get_ev(score_matrix, 1, 1))
            text_right['CD'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_right['DC'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_right['DD'] = add_ev_text(get_ev(score_matrix, 0, 0))
        # << end of copy from Desicion >>
            for k, v in text_left.items():
                text_desc_player[k] = 'get ' + v
            for k, v in text_right.items():
                text_desc_other[k] = 'get ' + v

        # << adjust texts for counterbalanced players >>
        if not player.is_UPbutton_cooperation:
            for d in [text_left, text_right, text_desc_player, text_desc_other]:
                d['CC'], d['DC'] = d['DC'], d['CC']
                d['CD'], d['DD'] = d['DD'], d['CD']
        
        # << if players get don't get any descriptive payoffs - show some text >>
        if not player.session.config['is_description'] and not player.session.config['EV_display']:
            text_left['CC'] = 'Up'
            text_left['CD'] = 'Up'
            text_left['DC'] = 'Down'
            text_left['DD'] = 'Down'

            text_right['CC'] = 'Left'
            text_right['CD'] = 'Right'
            text_right['DC'] = 'Left'
            text_right['DD'] = 'Right'

        
        bonus_example_points = C.NUM_ROUNDS*15 #assuming 15 is the mean score per round

        # << example score >>
        def calculate_score(score_val, random_treshold):
            if type(score_val) == list:  # Returns the payoff based on a random draw and the given probabilities
                return score_val[0] if random_treshold < score_val[1] else score_val[2]
            else:
                return score_val

        random_treshold = 0.1
        score_matrix = C.SCORE_MATRIX[player.game_type]        
        example_action = False if player.is_UPbutton_cooperation else True
        example_action_other = True
        example_score_p1 = add_points_text(calculate_score(score_matrix[ (example_action, example_action_other) ], random_treshold))
        example_forgone_score_p1 =  add_points_text(calculate_score(score_matrix[ (not example_action, example_action_other) ], random_treshold))
        example_score_p2 = add_points_text(calculate_score(score_matrix[ (example_action_other, example_action) ], random_treshold))

        if player.session.config['EV_display']:
            example_score_p1 = get_ev(score_matrix, example_action, example_action_other)
            example_forgone_score_p1 = get_ev(score_matrix, not example_action, example_action_other)
            example_score_p2 = get_ev(score_matrix, example_action_other, example_action)

        return dict(
            t_left = text_left,
            t_right = text_right,
            desc_player = text_desc_player,
            desc_other = text_desc_other,
            is_random_matching = player.session.config['random_matching'],
            is_description = player.session.config['is_description'],
            is_EV_display = player.session.config['EV_display'],
            example_score_p1 = example_score_p1,
            example_score_p2 =  example_score_p2,
            example_forgone_score_p1 = example_forgone_score_p1,
            is_UPbutton_cooperation = player.is_UPbutton_cooperation,
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
                    is_UPcooperation = player.is_UPbutton_cooperation,
                    already_made_desicion = (player.field_maybe_none('cooperate') != None),
                    cooperate = player.field_maybe_none('cooperate'),
                    )
    
    @staticmethod
    def live_method(player: Player, data):
        # player here is the sender of the msg
        player.cooperate = data['cooperate']
        print('received a bid from player', player.id_in_subsession, 'groupID', player.id_in_group, ':', data, type(data))
        opponent = other_player(player)
        opponent_cooperate = opponent.field_maybe_none('cooperate')

        player.penalty = C.PENALTY if data['timeout'] else 0
             
        if opponent_cooperate == None:
            set_desicion_time(player, 'live_method function - wait for other')
            return
        else: 
            set_desicion_time(player, 'live_method function - set scores')
            set_desicion_time(opponent, 'live_method function - set scores')

        scores_dict_me = None
        scores_dict_opponent = None
        if opponent_cooperate is not None:
            scores_dict_me = set_payoff(player)
            scores_dict_opponent = set_payoff(opponent)

        action_data_me = {
            'cooperate': player.cooperate,
            'sender_id_in_group': player.id_in_group,
            'opponent_cooperate': opponent_cooperate,
            'scores_dict': scores_dict_me,
        }
        action_data_opp = {
            'cooperate': opponent.cooperate,
            'sender_id_in_group': opponent.id_in_group,
            'opponent_cooperate': player.cooperate,
            'scores_dict': scores_dict_opponent,
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
        
        # ---- Define score_matrix -------
        score_matrix = C.SCORE_MATRIX[player.game_type]
        add_points_text = lambda v: str(v) + ' points'
        def score_matrix_to_text(score_val):
            if type(score_val) == list:  # Returns the score description for the table
                return f'{add_points_text(score_val[0])} with <nobr>{round(score_val[1]*100)}% chance,</nobr> and <nobr>{add_points_text(score_val[2])} with {round((1-score_val[1])*100)}% chance</nobr>'
            else:
                return add_points_text(score_val)
        
        # ---- set text for desicion table according to game type----
        text_left = {}
        text_right = {}

        for i in [0, 1]:
            for j in [0,1]:
                ti = 'C' if i == 1 else 'D'
                tj = 'C' if j == 1 else 'D'
                text_left[f"{ti}{tj}"] = score_matrix_to_text(score_matrix[(i,j)])  #player
                text_right[f"{ti}{tj}"] = score_matrix_to_text(score_matrix[(j,i)])  #opponent

        if player.session.config['EV_display']:
            def get_ev(matrix, player_coop, other_coop):
                value = matrix[(bool(player_coop), bool(other_coop))]
                if isinstance(value, list) and len(value) == 3:
                    a, p, b = value
                    return cu(int(round(p * a + (1 - p) * b)))
                return cu(int(round(value)))
            def add_ev_text(value):
                return str(int(value)) + ' points in expectation'
            text_left['CC'] = add_ev_text(get_ev(score_matrix, 1, 1))
            text_left['CD'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_left['DC'] = add_ev_text(get_ev(score_matrix, 0, 1))
            text_left['DD'] = add_ev_text(get_ev(score_matrix, 0, 0))

            text_right['CC'] = add_ev_text(get_ev(score_matrix, 1, 1))
            text_right['CD'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_right['DC'] = add_ev_text(get_ev(score_matrix, 1, 0))
            text_right['DD'] = add_ev_text(get_ev(score_matrix, 0, 0))
        # << end of copy from Desicion >>

        # << adjust texts for counterbalanced players >>
        if not player.is_UPbutton_cooperation:
            for d in [text_left, text_right]:
                d['CC'], d['DC'] = d['DC'], d['CC']
                d['CD'], d['DD'] = d['DD'], d['CD']
        

        # << if players get don't get any descriptive payoffs - show some text >>
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
            is_history_table = not player.session.config['random_matching'],
            is_played = (player.field_maybe_none('cooperate') != None),
            is_UPbutton_cooperation = player.is_UPbutton_cooperation,
            class_experiment = player.session.config['class_experiment'],
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
        return (player.super_game_round_number == C.ROUNDS_PER_SUPERGAME) and not player.session.config['random_matching'] and not (player.round_number == C.NUM_ROUNDS)
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
        chance_to_win, random_number = calc_total_score(player)
        
        return dict(
            bonus_chance = chance_to_win*100,
            bonus_prob = chance_to_win,
            lottery_num = random_number,
            show_up_fee = int(player.session.config['participation_fee']),
            bonus_fee = player.session.config['bonus_payment'],
            class_experiment=player.session.config['class_experiment'],
        )
class ReadMe(Page):
    pass
page_sequence = [InformedConsentPage, Introduction, Decision, ResultsWaitPage, EndOfExperiment]
