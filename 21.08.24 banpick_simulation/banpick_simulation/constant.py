import pandas as pd


BG = 'black'
FG = 'white'

SIDE_FRAME_WIDTH = 500


CHAMP_NUM_PER_ROW = 10

CHAMP_BAN_PHOTO_WIDTH = 40
CHAMP_BAN_PHOTO_HEIGHT = 40

CHAMP_PICK_PHOTO_WIDTH = 40
CHAMP_PICK_PHOTO_HEIGHT = 70

CHAMP_DETAIL_PHOTO_WIDTH = 300
CHAMP_DETAIL_PHOTO_HEIGHT = 200

POSITION_PHOTO_WIDTH = 30
POSITION_PHOTO_HEIGHT = 30

CHAMP_LIST_PHOTO_WIDTH = 40
CHAMP_LIST_PHOTO_HEIGHT = 40



IMG_PATH = dict()
IMG_PATH['tile'] = '/Users/nia/Desktop/lol_data_analysis/img/champion'
IMG_PATH['splash'] = '/Users/nia/Desktop/lol_data_analysis/img/champion_splash'
IMG_PATH['loading'] = '/Users/nia/Desktop/lol_data_analysis/img/champion_loading'
IMG_PATH['position'] = '/Users/nia/Desktop/lol_data_analysis/img/position'
IMG_PATH['icon'] = '/Users/nia/Desktop/lol_data_analysis/21.08.24 banpick/icon_img'

DATA_PATH = '/Users/nia/Desktop/lol_data_analysis/21.08.24 banpick/inven_data'

VERSION = '11.16.1'

POSITIONS = ['ALL', 'TOP', 'JUG', 'MID', 'ADC', 'SUP']
CHAMP_ORDER = ['ABC', '밴', '밴비율', '픽', '픽비율', '밴+픽', '밴픽률', '승률']
CHAMP_ORDER_MEAN = ['밴비율', '픽비율', '밴픽률', '승률']
CHAMP_ORDER_SUM = ['밴', '픽', '밴+픽']

CHAMPION_DF = dict()
CHAMPION_LIST = dict()

for pos in POSITIONS:

    CHAMPION_DF[pos] = pd.read_csv(f'/Users/nia/Desktop/lol_data_analysis/21.08.24 banpick/champion_data/{pos.lower()}_champ_{VERSION}.csv')
    CHAMPION_LIST[pos] = list(CHAMPION_DF[pos]['id'].values)

SEASONS = ['2021 Spring', '2021 Spring PS', '2021 Summer', '2021 Summer PS']
TEAMS = ['', 'T1', 'GENG', 'DWGKIA', 'HLE']
TEAM_PLAYERS = {
    '':{
        'TOP':[], 
        'JUG':[], 
        'MID':[],
        'ADC':[],
        'SUP':[]
    },

    'T1':{
        'TOP':['Canna', 'Zeus'], 
        'JUG':['Cuzz', 'Oner', 'Ellim'], 
        'MID':['Faker', 'Clozer'],
        'ADC':['Teddy', 'Gumayusi'],
        'SUP':['Keria', 'Hoit']
    },

    'DWGKIA':{
        'TOP':['Khan'], 
        'JUG':['Canyon', 'Marlang'], 
        'MID':['Showmaker'],
        'ADC':['Ghost'],
        'SUP':['Beryl']
    },

    'GENG':{
        'TOP':['Rascal', 'Burdol'], 
        'JUG':['Clid'], 
        'MID':['Bdd'],
        'ADC':['Ruler'],
        'SUP':['Life']
    },

    'HLE':{
        'TOP':['Morgan', 'Dudu'], 
        'JUG':['Willer'], 
        'MID':['Chovy'],
        'ADC':['Deft'],
        'SUP':['Vsta']
    },
}


BANPICK_ORDER = [
    #ban_phase_1
    'blue_ban_1', 'red_ban_1', 'blue_ban_2', 'red_ban_2', 'blue_ban_3', 'red_ban_3', 
    #pick_phase_1
    'blue_pick_1', 'red_pick_1', 'red_pick_2', 'blue_pick_2', 'blue_pick_3', 'red_pick_3', 
    #ban_phase_2
    'red_ban_4', 'blue_ban_4', 'red_ban_5', 'blue_ban_5', 
    #pick_phase_2
    'red_pick_4', 'blue_pick_4', 'blue_pick_5', 'red_pick_5',
    #end
    'end'
    ]

