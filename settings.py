from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, 
                               participation_fee=6,
                               bonus_payment=6,
                               turned_away_fee=3,)

SESSION_CONFIGS = [
    dict(name='test',
         num_demo_participants=2,
         app_sequence=['prisoner', 'survey'],
         use_browser_bots=False,
         game_type="EV-PD beh-CG",
         random_matching=True,
         is_description=True,
         EV_display=True,
         class_experiment=False,
         ),
    dict(name='test6bots',
         num_demo_participants=6,
         app_sequence=['prisoner', 'survey'],
         use_browser_bots=True,
         game_type="EV-CG beh-PD",
         random_matching=True,
         is_description=True,
         EV_display=True,
         class_experiment=False,
         ),
    dict(name='experiment_main',
         num_demo_participants=6,
         app_sequence=['prisoner', 'survey'],
         use_browser_bots=False,
         game_type="EV-CG beh-PD",
         random_matching=False,
         is_description=True,
         EV_display=False,
         class_experiment=False,
         ),
    dict(name='experiment_main95',
         num_demo_participants=6,
         app_sequence=['prisoner', 'survey'],
         use_browser_bots=False,
         game_type="95EV-CG beh-PD",
         random_matching=True,
         is_description=True,
         EV_display=False,
         class_experiment=True,
         ),
    dict(
        name='forwrd_link',
        display_name='Waiting room to provide the Zoom link to start the experiment',
        app_sequence=['waiting_room'],
        num_demo_participants=1,
        zoom_link="TODO PUT YOUR ZOOM LINK HERE",
    ),
    dict(
        name='turned_away',
        display_name='Turned Away - session to ensure people that get turned away get paid',
        app_sequence=['turned_away'],
        num_demo_participants=1
    ),      
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['total_score', 'chance_to_win', 'random_lottery_number', 'win_bonus', 'bonus', 'mean_cooperation']
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='room1',
        display_name='Room 1',
    ),
    dict(
        name='room2',
        display_name='Room 2',
    ),
        dict(
        name='room3',
        display_name='Room 3',
    ),
    dict(
        name='room_turned_away',
        display_name='Room Turned Away',
    ),
    dict(
        name='waiting_room',
        display_name='Waiting Room',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')  #ppd

DEBUG = environ.get('DEBUG', 'False').lower() == 'true'

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
