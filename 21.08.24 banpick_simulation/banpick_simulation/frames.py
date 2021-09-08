import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
from PIL import ImageTk, Image

from constant import *

class banpick_frame:

    def __init__(self, frame, side):

        self.frame = frame
        self.side = side

        #---------------
        # ban frame
        #---------------        
        self.frame_ban = tk.Frame(self.frame, background=BG)
        self.frame_ban.pack(side='top', fill='both', expand=True, padx=3, pady=3, ipadx=3, ipady=3)

        #---------------
        # pick frame
        #---------------        
        self.frame_pick = tk.Frame(self.frame, background=BG)
        self.frame_pick.pack(side='top', fill='both', expand=True, padx=3, pady=3, ipadx=3, ipady=3)

        #---------------
        # score frame
        #---------------
        self.frame_score = tk.LabelFrame(self.frame, text="SCORE", bg=BG, fg=FG)
        self.frame_score.pack(side='top', fill='both', expand=True, padx=3, pady=3, ipadx=3, ipady=3)


        self.ban_dict = {}
        self.ban_photo_dict = {}
        self.ban_label_dict = {}
        
        self.pick_dict = {}
        self.pick_photo_dict = {}
        self.pick_label_dict = {}
        self.pick_graph_dict = {}


    def update_ban(self, ban_dict):

        self.ban_dict = ban_dict

        for i in range(1,6):
            img = Image.open(f'{IMG_PATH["tile"]}/{self.ban_dict[i]}.png').resize((CHAMP_BAN_PHOTO_WIDTH, CHAMP_BAN_PHOTO_HEIGHT))
            temp_photo = ImageTk.PhotoImage(img)
            self.ban_photo_dict[i] = temp_photo

            temp_label = tk.Label(self.frame_ban, image=self.ban_photo_dict[i])
            self.ban_label_dict[i] = temp_label
            
            self.ban_label_dict[i].grid(row=0, column=i, padx=3, pady=3, sticky='ew')

        
    def update_pick(self, pick_dict):

        self.pick_dict = pick_dict

        for i in range(1,6):
            img = Image.open(f'{IMG_PATH["loading"]}/{self.pick_dict[i]}_0.jpg').resize((CHAMP_PICK_PHOTO_WIDTH, CHAMP_PICK_PHOTO_HEIGHT))
            temp_photo = ImageTk.PhotoImage(img)
            self.pick_photo_dict[i] = temp_photo

            temp_label = tk.Label(self.frame_pick, image=self.pick_photo_dict[i])
            self.pick_label_dict[i] = temp_label
            
            self.pick_label_dict[i].grid(row=i-1, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')

        
            # fig = plt.figure(figsize=(2,0.2))
            # fig.add_subplot(111).plot([1,2,3],[1,2,3])
            # temp_graph = FigureCanvasTkAgg(fig, self.frame_pick)
            # temp_graph.draw()
            # self.pick_graph_dict[i] = temp_graph
            # self.pick_graph_dict[i].get_tk_widget().grid(row=i-1, column=2, columnspan=3, padx=3, pady=3, sticky='nsew')
            # plt.clf()
            # plt.close()

    
    def update_score(self):
 
        score_label = tk.Label(self.frame_score, text=f'This is {self.side.upper()} team\'s score', bg=BG, fg=FG, height=200)
        score_label.pack()


class select_team_frame():

    def __init__(self, popup_window, side, team, team_players):

        self.side = side
        self.team = team
        self.team_players = team_players.copy()

        self.frame = tk.LabelFrame(popup_window, text=self.side.upper())
        self.frame.pack(side='top', fill='both', anchor='center', padx=5, pady=10, ipadx=5, ipady=10)
        for r in range(5):
            self.frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.frame.grid_columnconfigure(c, weight=1)

        self.player_radios = []
        self.player_selected = self.team_players

        self.show_team()
        
    
    def show_team(self):
        self.combobox_team_selection = ttk.Combobox(self.frame, 
                                                    values=TEAMS, 
                                                    height=5, width=10, state='readonly'
                                                    )
        
        self.combobox_team_selection.current(TEAMS.index(self.team))                                                       
        self.combobox_team_selection.grid(row=0, column=0, padx=5, pady=5, sticky='w')      

        self.combobox_team_selection.bind('<<ComboboxSelected>>', self.select_team)
        self.show_players()


    def show_players(self):

        for r in self.player_radios:
            r.destroy()

        self.player_radios = []
        self.player_selected = {}

        for idx, (pos, players) in enumerate(TEAM_PLAYERS[self.team].items()):
            # 포지션별 라벨
            label_pos = tk.Label(self.frame, text=pos)
            label_pos.grid(row=idx+1, column=0, padx=5, pady=5, sticky='w')    

            # 포지션별 선수
            self.player_selected[pos] = tk.StringVar(self.frame)

            for p, player in enumerate(players):
                radiobtn_player = tk.Radiobutton(self.frame, 
                                                text=player, value=player, var=self.player_selected[pos],
                                                command=lambda position=pos, player=player: self.select_player(position, player)
                                                )
                self.player_radios.append(radiobtn_player)
                radiobtn_player.grid(row=idx+1, column=p+1, padx=5, sticky='w')

                if player == self.team_players[pos]: 
                    self.player_selected[pos].set(player)


    def select_player(self, position, player):
        self.team_players[position] = player


    # 선택된 팀에 맞춰서 선수 목록 제시
    def select_team(self, event=None):
        

        self.team = self.combobox_team_selection.get()
        for pos, players in TEAM_PLAYERS[self.team].items():
            if len(players) != 0: self.team_players[pos] = players[0]
        
        self.show_players()

