import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font

from PIL import ImageTk, Image
from collections import defaultdict
from pandastable import Table

from constant import *
from frames import *

verbose = True

root = tk.Tk()

root.title('Ban Pick')
root.configure(bg=BG)

# root.geometry('1300x1000+10+0') 
# root.resizable(False, False) 

frames = {}


# 밴픽 정보
global banpick_dict, banpick_list
banpick_dict = defaultdict(dict)
for i in range(1, 6):
    banpick_dict['blue_ban'][i] = 'None'
    banpick_dict['blue_pick'][i] = 'None'
    banpick_dict['red_ban'][i] = 'None' 
    banpick_dict['red_pick'][i] = 'None'

banpick_list = []

global current_turn_num, side, banpick, num
current_turn_num = 0
side, banpick, num = BANPICK_ORDER[current_turn_num].split('_')
banpick_dict[f'{side}_{banpick}'][int(num)] = 'Current'


# 시즌, 팀 선수 선택 관련
global checked_season, checkbox_var_season
checked_season = SEASONS
checkbox_var_season = dict()

global blue_team, blue_team_players, red_team, red_team_players
blue_team = ''
red_team = ''
blue_team_players = dict()
red_team_players = dict()


class champ_selection_frame:

    global side, banpick, num

    def __init__(self, frame):
        self.frame = frame #frames['banpick']

        self.available_champions = dict()
        self.current_selected_position = 'ALL'
        for pos in POSITIONS:
            self.available_champions[pos] = CHAMPION_LIST[pos]

        self.current_selected_champ = 'None'
        self.champ_detail_desc = f'이 챔피언의 이름은 {self.current_selected_champ} 입니다.'

        self.position_photo_dict = dict()
        self.position_button_dict = dict()

        self.column_label_dict = dict()
        self.champion_label_list = list()
        self.champion_photo_list = list()
        self.champion_button_list = list()

        self.sort_col = '챔피언'
        self.sort_ascending = True

        self.champion_label_dict = dict()
        self.champion_photo_dict = dict()
        self.champion_button_dict = dict()

        
        #-------------------------
        # selected champ detail
        #-------------------------
        self.frame_champ_detail = tk.Frame(self.frame, bg=BG)
        self.frame_champ_detail.pack(side='top', anchor='center', fill='both', padx=5, pady=5)
        self.show_champ_detail()
        
        #-------------------------
        # available champ list
        #-------------------------
        self.frame_champ_list_parent = tk.Frame(self.frame, bg='green')
        self.frame_champ_list_parent.pack(side='top', fill='both', anchor='center', expand=True, padx=5, pady=5)
        self.frame_champ_list_parent.grid_rowconfigure(0, weight=1) #option grid
        self.frame_champ_list_parent.grid_rowconfigure(1, weight=12) #column grid
        self.frame_champ_list_parent.grid_columnconfigure(0, weight=1)

        # ---champion option---
        self.frame_champ_option = tk.Frame(self.frame_champ_list_parent, bg='red')
        self.frame_champ_option.grid(row=0, column=0, padx=3, pady=5, ipady=5, sticky='sew')
        # self.frame_champ_option.pack(side='top', fill='x', expand=True, padx=5, pady=5)
        self.show_champ_option()

        # ---champion table---
        self.frame_champ_table = tk.Frame(self.frame_champ_list_parent, bg='skyblue')
        self.frame_champ_table.grid(row=1, column=0, padx=3, pady=3, sticky='nsew')
        # self.frame_champ_table.pack(side='top', fill='both', anchor='center', expand=True, padx=5, pady=5)
        self.frame_champ_table.grid_rowconfigure(0, weight=1)
        self.frame_champ_table.grid_rowconfigure(1, weight=10)
        self.frame_champ_table.grid_columnconfigure(0, weight=1)

            # table column
        self.frame_champ_column = tk.Frame(self.frame_champ_table, bg='yellow')
        self.frame_champ_column.grid(row=0, column=0, padx=3, sticky='sew')

            # table list
            # 챔피언 리스트 캔버스
        self.champion_list_canvas = tk.Canvas(self.frame_champ_table, bg='blue', bd=0, highlightthickness=0)
        self.champion_list_canvas.grid(row=1, column=0, padx=3, pady=3, sticky='nsew')

            # 스크롤바 : 챔피언 리스트 캔버스와 연결
        self.champion_list_scroll = tk.Scrollbar(self.frame_champ_table, orient='vertical', command=self.champion_list_canvas.yview)
        self.champion_list_scroll.grid(row=1, column=1, padx=3, pady=3, sticky='ns')
        self.champion_list_canvas.configure(yscrollcommand=self.champion_list_scroll.set)

            #
        self.frame_champ_list = tk.Frame(self.champion_list_canvas, bg='orange')
        self._frame_id = self.champion_list_canvas.create_window(0,0, window=self.frame_champ_list, anchor='center')
        self.champion_list_canvas.update()
        self.champion_list_canvas.itemconfig(self._frame_id, width=self.champion_list_canvas.winfo_width())

        self.show_available_champions()


    
    def show_champ_detail(self):
        # image
        img = Image.open(f'{IMG_PATH["splash"]}/{self.current_selected_champ}_0.jpg').resize((CHAMP_DETAIL_PHOTO_WIDTH, CHAMP_DETAIL_PHOTO_HEIGHT))
        self.champ_detail_image = ImageTk.PhotoImage(img)
        self.btn_champion_detail_img = tk.Button(self.frame_champ_detail, image=self.champ_detail_image, 
                                    command=lambda champ=self.current_selected_champ: self.select_champion(champ)
                                    )
        self.btn_champion_detail_img.pack(side='left', fill='both', anchor='center', padx=5, pady=5)

        # description
        self.label_champion_detail_desc = tk.Label(self.frame_champ_detail, text=self.champ_detail_desc, bg=BG, fg=FG, width=47)
        self.label_champion_detail_desc.pack(side='left', fill= 'both', padx=5, pady=5)


    def show_champ_option(self):

        self.update_champ_order_team()
        self.update_champ_order_player()

        # 포지션
        for i, pos in enumerate(POSITIONS[::-1]):

            if pos == self.current_selected_position: 
                img = Image.open(f'{IMG_PATH["position"]}/{pos.lower()}_selected.png').resize((POSITION_PHOTO_WIDTH,POSITION_PHOTO_HEIGHT))
            else:
                img = Image.open(f'{IMG_PATH["position"]}/{pos.lower()}.png').resize((POSITION_PHOTO_WIDTH,POSITION_PHOTO_HEIGHT))

            self.position_photo_dict[pos] = ImageTk.PhotoImage(img)
            self.position_button_dict[pos] = tk.Button(self.frame_champ_option, 
                                                    padx=3, pady=3, 
                                                    image=self.position_photo_dict[pos],
                                                    command=lambda pos=pos: self.select_position(pos)
                                                    )
            self.position_button_dict[pos].pack(side='right', padx=3, pady=3)

        
    def update_champ_order_team(self, event=None):

        if hasattr(self, 'combobox_champ_order_team'):
            self.combobox_champ_order_team.destroy()

        # team 목록
        values = ['ALL']
        if blue_team != '':
            values.append(blue_team)
        if red_team != '' and red_team != blue_team:
            values.append(red_team)


        if len(values) != 0:
            # 정렬 순서 세부[team] - combobox
            self.combobox_champ_order_team = ttk.Combobox(self.frame_champ_option,
                                                            values=values,
                                                            height=5, width=12, state='readonly'
                                                            )
            self.combobox_champ_order_team.current(0)
            self.combobox_champ_order_team.bind('<<ComboboxSelected>>', self.champ_order_team_changed)
            self.combobox_champ_order_team.pack(side='left', padx=3, pady=3)

            self.update_champ_order_player()

        self.update_champ_order_player()
        if hasattr(self, 'champion_list_canvas'):
            self.show_available_champions()


    def update_champ_order_player(self):

        if hasattr(self, 'combobox_champ_order_player'):
            self.combobox_champ_order_player.destroy()

        if self.combobox_champ_order_team.get() == 'ALL':
            return

        # player 목록
        values = ['ALL']
        if blue_team == self.combobox_champ_order_team.get():
            for _, player in blue_team_players.items():
                values.append(player)
        if red_team == self.combobox_champ_order_team.get():
            for _, player in red_team_players.items():
                if player not in values:
                    values.append(player)


        # 정렬 순서 세부[player] - combobox
        self.combobox_champ_order_player = ttk.Combobox(self.frame_champ_option,
                                                        values=values,
                                                        height=5, width=12, state='readonly'
                                                        )
        self.combobox_champ_order_player.current(0)
        self.combobox_champ_order_player.bind('<<ComboboxSelected>>', self.champ_order_player_changed)
        self.combobox_champ_order_player.pack(side='left', padx=3, pady=3)


    def champ_order_team_changed(self, event=None):

        self.sort_col = '챔피언'
        self.sort_ascending = True

        self.update_champ_order_player()
        self.show_available_champions()


    def champ_order_player_changed(self, event=None):

        self.sort_col = '챔피언'
        self.sort_ascending = True

        self.show_available_champions()


    def select_position(self, pos):
        self.current_selected_position = pos
        for pos in POSITIONS:

            if pos == self.current_selected_position: 
                img = Image.open(f'{IMG_PATH["position"]}/{pos.lower()}_selected.png').resize((POSITION_PHOTO_WIDTH,POSITION_PHOTO_HEIGHT))
            else:
                img = Image.open(f'{IMG_PATH["position"]}/{pos.lower()}.png').resize((POSITION_PHOTO_WIDTH,POSITION_PHOTO_HEIGHT))

            self.position_photo_dict[pos] = ImageTk.PhotoImage(img)
            self.position_button_dict[pos].config(image=self.position_photo_dict[pos])

        self.show_available_champions()


    def show_available_champions(self):

        for _, col in self.column_label_dict.items():
            col.destroy()

        for label in self.champion_label_list:
            label.destroy()

        for button in self.champion_button_list:
            button.destroy()
        

        data_frame = self.get_champion_data()

        # ---grid 사이즈 조정---
        data_column = list(data_frame.columns)
        
        if self.combobox_champ_order_team.get() == 'ALL' or self.combobox_champ_order_player.get() == 'ALL':
            uniform = 'a'
        else:
            uniform = 'b'

        for i in range(100):
            self.frame_champ_column.grid_columnconfigure(i, weight=0)
            self.frame_champ_list.grid_columnconfigure(i, weight=0)
        for i in range(2,len(data_column)+2):
            self.frame_champ_column.grid_columnconfigure(i, weight=1, uniform=uniform)
            self.frame_champ_list.grid_columnconfigure(i, weight=1, uniform=uniform)
        
        # ---column---
        self.column_label_dict['순서'] = tk.Label(self.frame_champ_column, 
                                    padx=3, pady=3, bg=BG, fg = FG, width=5,
                                    text='순서', font=tkinter.font.Font(size=10)
                                    )
        self.column_label_dict['순서'].grid(row=0, column=0, sticky='sew')

        self.column_label_dict['챔피언'] = tk.Label(self.frame_champ_column, 
                                        padx=3, pady=3, bg=BG, fg=FG, width=5,
                                        text='챔피언', font=tkinter.font.Font(size=10),
                                        )
        self.column_label_dict['챔피언'].bind("<Button-1>", lambda _, col='챔피언': self.sort_champion_list(col))
        self.column_label_dict['챔피언'].grid(row=0, column=1, sticky='sew')

        for c, col in enumerate(data_column):
            self.column_label_dict[col] = tk.Label(self.frame_champ_column, 
                                            padx=3, pady=3, bg=BG, fg=FG,
                                            text=col, font=tkinter.font.Font(size=10),
                                            )
            self.column_label_dict[col].bind("<Button-1>", lambda _, col=col: self.sort_champion_list(col))
            self.column_label_dict[col].grid(row=0, column=c+2, sticky='sew')

        #정렬 기준 column 색깔 표시
        self.column_label_dict[self.sort_col].config(bg='red')

        # ---테이블 내용---
        if self.combobox_champ_order_team.get() == 'ALL' or self.combobox_champ_order_player.get() == 'ALL':
            idx = 0
            for champ in data_frame.index:
                if champ not in self.available_champions[self.current_selected_position]:
                    continue

                self.champion_index_label = tk.Label(self.frame_champ_list,
                                                    padx=3, pady=3, bg=BG, fg=FG, width=5,
                                                    text=idx+1, font=tkinter.font.Font(size=10)
                                                    )
                self.champion_index_label.grid(row=idx+1, column=0, sticky='nsew')
                self.champion_label_list.append(self.champion_index_label)

                img = Image.open(f'{IMG_PATH["tile"]}/{champ}.png').resize((CHAMP_LIST_PHOTO_WIDTH,CHAMP_LIST_PHOTO_HEIGHT))
                self.champion_photo = ImageTk.PhotoImage(img)
                self.champion_button = tk.Button(self.frame_champ_list, 
                                                        padx=3, pady=3, bg=BG, highlightcolor=BG, bd=0, highlightthickness=0, 
                                                        image=self.champion_photo, 
                                                        command=lambda champ=champ: self.update_champion_detail(champ)
                                                        )
                self.champion_button.grid(row=idx+1, column=1, sticky='nsew')
                self.champion_photo_list.append(self.champion_photo)
                self.champion_button_list.append(self.champion_button)

                for c, col in enumerate(data_column):
                    self.champion_label = tk.Label(self.frame_champ_list, 
                                                                padx=3, pady=3, bg=BG, fg=FG, 
                                                                text=data_frame.loc[champ, col], font=tkinter.font.Font(size=10)
                                                                )   
                    self.champion_label.grid(row=idx+1, column=c+2, sticky='nsew')
                    self.champion_label_list.append(self.champion_label)

                idx += 1

        else:
            idx = 0
            for champ in data_frame.index:
                if champ not in self.available_champions[self.current_selected_position]:
                    continue

                self.champion_index_label = tk.Label(self.frame_champ_list,
                                                    padx=3, pady=3, bg=BG, fg=FG, width=5,
                                                    text=idx+1, font=tkinter.font.Font(size=10)
                                                    )
                self.champion_index_label.grid(row=idx+1, column=0, sticky='nsew')
                self.champion_label_list.append(self.champion_index_label)

                img = Image.open(f'{IMG_PATH["tile"]}/{champ}.png').resize((CHAMP_LIST_PHOTO_WIDTH,CHAMP_LIST_PHOTO_HEIGHT))
                self.champion_photo = ImageTk.PhotoImage(img)
                self.champion_button = tk.Button(self.frame_champ_list, 
                                                        padx=3, pady=3, bg=BG, highlightcolor=BG, bd=0, highlightthickness=0, 
                                                        image=self.champion_photo, 
                                                        command=lambda champ=champ: self.update_champion_detail(champ)
                                                        )
                self.champion_button.grid(row=idx+1, column=1, sticky='nsew')

                self.champion_photo_list.append(self.champion_photo)
                self.champion_button_list.append(self.champion_button)

                for c, col in enumerate(data_column):
                    self.champion_label = tk.Label(self.frame_champ_list, 
                                                                padx=3, pady=3, bg=BG, fg=FG, 
                                                                text=data_frame.loc[champ, col], font=tkinter.font.Font(size=10)
                                                                )   
                    self.champion_label.grid(row=idx+1, column=c+2, sticky='nsew')
                    self.champion_label_list.append(self.champion_label)

                idx += 1


        self.frame_champ_list.update_idletasks()
        self.champion_list_canvas.config(scrollregion=self.champion_list_canvas.bbox('all'))
        self.champion_list_canvas.yview_moveto('0.0') #스크롤바 제일 위로


    def sort_champion_list(self, col, event=None):

        if self.sort_col == col:
            if self.sort_ascending:
                self.sort_ascending = False
            else:
                self.sort_ascending = True

        else:
            self.sort_col = col
            self.sort_ascending = False

        self.show_available_champions()


    def get_champion_data(self):

        team = self.combobox_champ_order_team.get()

        if team == 'ALL': #전체 LCK

            dfs = []
            for season in checked_season:
                cleansed_season = '_'.join(season.lower().split())
                temp_df = pd.read_csv(f'{DATA_PATH}/inven_champ_{cleansed_season}.csv').set_index('챔피언')
                dfs.append(temp_df)

            temp_df = pd.concat(dfs)
            add_temp_df = temp_df.groupby(level=0).sum()[CHAMP_ORDER_SUM]
            ave_temp_df = temp_df.groupby(level=0).mean()[CHAMP_ORDER_MEAN].round(2)
            result_df = pd.concat([add_temp_df, ave_temp_df], axis=1)

        else:
            player = self.combobox_champ_order_player.get()

            if player == 'ALL': #특정 팀 전체 선수

                dfs = []
                for season in checked_season:
                    cleansed_season = '_'.join(season.lower().split())
                    temp_df = pd.read_csv(f'{DATA_PATH}/inven_champ_{cleansed_season}_{team}.csv').set_index('챔피언')
                    dfs.append(temp_df)

                temp_df = pd.concat(dfs)
                temp_df = temp_df.astype({x:int for x in CHAMP_ORDER_SUM})
                temp_df = temp_df.astype({x:float for x in CHAMP_ORDER_MEAN})

                add_temp_df = temp_df.groupby(level=0).sum()[CHAMP_ORDER_SUM]
                ave_temp_df = temp_df.groupby(level=0).mean()[CHAMP_ORDER_MEAN].round(2)

                result_df = pd.concat([add_temp_df, ave_temp_df], axis=1)

            else: #특정 팀 특정 선수

                dfs = []
                for season in checked_season:
                    cleansed_season = '_'.join(season.lower().split())
                    temp_df = pd.read_csv(f'{DATA_PATH}/inven_champ_{cleansed_season}_{player}.csv').set_index('챔피언')
                    dfs.append(temp_df)
                    
                temp_df = pd.concat(dfs)
                temp_df.drop(columns=['Unnamed: 0', '소환사명', '경기 정보'], inplace=True)
                temp_df = temp_df.astype({'K':int, 'D':int, 'A':int, 'KDA':float, '킬관여율':float})

                temp_df['승'] = temp_df['승패'].apply(lambda x: 1 if x == '승' else 0)
                temp_df['패'] = temp_df['승패'].apply(lambda x: 1 if x == '패' else 0)
                temp_df_sum = temp_df.groupby(by='챔피언').sum()[['승', '패']].astype(int)
                temp_df_sum['경기수'] = temp_df_sum['승'] + temp_df_sum['패']
                temp_df_sum['승률'] = (temp_df_sum['승']/temp_df_sum['경기수']*100).round(2)

                temp_df_mean = temp_df.groupby(by='챔피언').mean().round(2)[['K', 'D', 'A', 'KDA', '킬관여율']]

                result_df = pd.concat([temp_df_mean, temp_df_sum], axis=1)

        # 정렬
        if self.sort_col == '챔피언':
            result_df.sort_index(ascending=self.sort_ascending, inplace=True)
        else:
            result_df.sort_values(by=self.sort_col, ascending=self.sort_ascending, inplace=True)

        return result_df


    def update_champion_detail(self, champ):

        global current_selected_champ, champ_detail_image, champ_detail_desc
        current_selected_champ = champ

        img = Image.open(f'{IMG_PATH["splash"]}/{current_selected_champ}_0.jpg').resize((CHAMP_DETAIL_PHOTO_WIDTH, CHAMP_DETAIL_PHOTO_HEIGHT))
        champ_detail_image = ImageTk.PhotoImage(img)
        self.btn_champion_detail_img.config(image=champ_detail_image, 
                                command=lambda champ=current_selected_champ: self.select_champion(champ)
                                )

        self.champ_detail_desc = f'이 챔피언의 이름은 {current_selected_champ} 입니다.'
        self.label_champion_detail_desc.config(text=self.champ_detail_desc)


    def select_champion(self, champ):

        #선택된 챔피언 없음
        if champ == 'None': return

        #모두 선택 완료
        if current_turn_num >= 20: return

        #이미 선택된 챔피언
        if champ in banpick_list: return

        
        for pos in POSITIONS:
            try:        
                self.available_champions[pos].remove(champ)

            #해당 포지션 목록에 champ가 없는 경우
            except ValueError as e: 
                pass

        banpick_dict[f'{side}_{banpick}'][int(num)] = champ
        banpick_list.append(champ)

        if banpick == 'ban':
            frames[f'{side}_banpick'].update_ban(banpick_dict[f'{side}_{banpick}'])
        else:
            frames[f'{side}_banpick'].update_pick(banpick_dict[f'{side}_{banpick}'])

        update_turn()
        self.show_available_champions()



########################################################################################################################
##blue side frame
########################################################################################################################

frames['blue'] = tk.LabelFrame(root, width=SIDE_FRAME_WIDTH, text='BLUE', background=BG, fg=FG)
frames['blue'].pack(side='left', fill='y', expand=True, anchor='center', padx=5, pady=5, ipadx=5, ipady=5)

frames['blue_banpick'] = banpick_frame(frames['blue'], 'blue')
frames['blue_banpick'].update_ban(banpick_dict['blue_ban'])
frames['blue_banpick'].update_pick(banpick_dict['blue_pick'])
frames['blue_banpick'].update_score()

########################################################################################################################



########################################################################################################################
##banpick frame
########################################################################################################################

frames['banpick'] = tk.LabelFrame(root, text='SELECT', bg=BG, fg=FG)
frames['banpick'].pack(side='left', fill='y', expand=True, padx=5, pady=5, ipadx=5, ipady=5)


#-------------------------
# turn + setting
#-------------------------
frames['team_selection'] = tk.Frame(frames['banpick'], bg=BG)
frames['team_selection'].pack(side='top', fill='both', padx=5, pady=10)
for i in range(5):
    frames['team_selection'].columnconfigure(i,weight=1)


# ---banpick turn label---
label_turn = tk.Label(frames['team_selection'], text=f"{side.upper()} {num} {banpick.upper()}", 
                        bg=BG, fg=side, font=('Helvetica bold', 30)
                        )
label_turn.grid(row=0, column=2, sticky='ew')


# ---team & season setting---
def open_setting_popup():

    setting_popup = tk.Toplevel()
    setting_popup.title("SETTING")
    setting_popup.geometry("600x700+350+50")

    # 시즌 선택
    frame_season = tk.LabelFrame(setting_popup, text='SEASON')
    frame_season.pack(side='top', fill='both', anchor='center', padx=5, pady=10, ipadx=5, ipady=10)
    frame_season.grid_columnconfigure(0, weight=1)
    frame_season.grid_columnconfigure(1, weight=1)

    global checked_season, checkbox_var_season
    checkbox_season = dict()    

    for idx, s in enumerate(SEASONS):
        checkbox_var_season[s] = tk.IntVar()
        checkbox_season[s] = tk.Checkbutton(frame_season, text=s, variable=checkbox_var_season[s])
        checkbox_season[s].grid(row=idx//2, column=idx%2, padx=5, pady=3, sticky='w')
        
        if s in checked_season: 
            checkbox_season[s].select()
        
        
    # 팀 선택
    frame_blue = select_team_frame(setting_popup, 'blue', blue_team, blue_team_players)
    frame_red = select_team_frame(setting_popup, 'red', red_team, red_team_players)


    # 확인/취소 버튼
    frame_button = tk.Frame(setting_popup)
    frame_button.pack(side='top', fill='both', anchor='center', padx=5, pady=10, ipadx=5, ipady=10)
    
    def save_setting():
        global checkbox_var_season, checked_season
        global blue_team, blue_team_players, red_team, red_team_players
        
        checked_season = list()
        for season, checked in checkbox_var_season.items():

            if checked.get(): checked_season.append(season)

        blue_team = frame_blue.team
        blue_team_players = frame_blue.team_players

        red_team = frame_red.team
        red_team_players = frame_red.team_players

        frames['blue'].config(text=f'BLUE : {blue_team}' if blue_team != '' else 'BLUE')
        frames['red'].config(text=f'RED : {red_team}' if red_team != '' else 'RED')

        frames['champ_selection'].sort_col = '챔피언'
        frames['champ_selection'].sort_ascending = True
        setting_popup.destroy()

        frames['champ_selection'].update_champ_order_team()
        
    def cancel_setting():
        setting_popup.destroy()

    btn_cancel = tk.Button(frame_button, text='CANCEL', 
                        padx=5, pady=5, highlightbackground='gray', bg='gray', fg='black', width=10,
                        command=cancel_setting
                        )
    btn_cancel.pack(side='right', padx=5, pady=5)

    btn_save = tk.Button(frame_button, text='SAVE', 
                        padx=5, pady=5, highlightbackground='blue', bg='blue', fg='black', width=10,
                        command=save_setting
                        )
    btn_save.pack(side='right', padx=5, pady=5)

    
# setting 버튼
img = Image.open(f'{IMG_PATH["icon"]}/setting_black.png').resize((30,30))
setting_img = ImageTk.PhotoImage(img)
setting_btn = tk.Button(frames['team_selection'], image=setting_img, 
                        highlightbackground=BG, 
                        padx=10, pady=5, command=open_setting_popup
                        )
setting_btn.grid(row=0, column=4, sticky='e')


#-------------------------
# champion selection
#-------------------------
frames['champ_selection'] = champ_selection_frame(frames['banpick'])

########################################################################################################################



########################################################################################################################
##red side frame
########################################################################################################################

frames['red'] = tk.LabelFrame(root, width=SIDE_FRAME_WIDTH, text='RED', background=BG, fg=FG)
frames['red'].pack(side='left', fill='y', expand=True, padx=5, pady=5, ipadx=5, ipady=5)

frames['red_banpick'] = banpick_frame(frames['red'], 'red')
frames['red_banpick'].update_ban(banpick_dict['red_ban'])
frames['red_banpick'].update_pick(banpick_dict['red_pick'])
frames['red_banpick'].update_score()

########################################################################################################################



def update_turn():
    global current_turn_num, side, banpick, num

    current_turn_num += 1
    if current_turn_num >= 20:
        label_turn.config(text=f"END", fg='white')
        return

    side, banpick, num = BANPICK_ORDER[current_turn_num].split('_')
    banpick_dict[f'{side}_{banpick}'][int(num)] = 'Current'

    label_turn.config(text=f"{side.upper()} {num} {banpick.upper()}", fg=side)
    if banpick == 'ban':
        frames[f'{side}_banpick'].update_ban(banpick_dict[f'{side}_{banpick}'])
    else:
        frames[f'{side}_banpick'].update_pick(banpick_dict[f'{side}_{banpick}'])




root.mainloop()


