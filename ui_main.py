import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer
import os
import ctypes

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ### 경로설정
        main_ui_rel_path = 'ui_main.ui'
        main_ui_abs_path = __file__.replace('ui_main.py',main_ui_rel_path)
        uic.loadUi(main_ui_abs_path,self) #ui 파일 불러오기

        main_abs_path = __file__.replace('ui_main.py','')

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                # print("clicked")
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # set title bar
        self.main_frame.mouseMoveEvent = moveWindow
        self.frame_content.mouseMoveEvent = moveWindow
        self.frame_position.mouseMoveEvent = moveWindow
        self.frame_spell1.mouseMoveEvent = moveWindow
        self.frame_spell2.mouseMoveEvent = moveWindow
        self.frame_top.mouseMoveEvent = moveWindow
        self.frame_title.mouseMoveEvent = moveWindow

        # 전체 윈도우 투명도 주기
        opacity_effect = QGraphicsOpacityEffect(self.main_frame)
        opacity_effect.setOpacity(0.8)
        self.main_frame.setGraphicsEffect(opacity_effect)
        self.main_frame.setStyleSheet("background-color: black")

        # 점화 방어막 180초 / 유체화 탈진 정화 210초 / 회복 240초 / 텔 360초

        # btn_spell1 background 이미지 설정
        self.btn_spell1_top.setStyleSheet("background-image : url('./img/teleport_35.png');")
        self.btn_spell1_jg.setStyleSheet("background-image : url('./img/smite_35.png');")
        self.btn_spell1_mid.setStyleSheet("background-image : url('./img/ignite_35.png');")
        self.btn_spell1_ad.setStyleSheet("background-image : url('./img/heal_35.png');")
        self.btn_spell1_sup.setStyleSheet("background-image : url('./img/ignite_35.png');")

        self.btn_top.setStyleSheet("background-image : url('./img/flash_35.png');")
        self.btn_jg.setStyleSheet("background-image : url('./img/flash_35.png');")
        self.btn_mid.setStyleSheet("background-image : url('./img/flash_35.png');")
        self.btn_ad.setStyleSheet("background-image : url('./img/flash_35.png');")
        self.btn_sup.setStyleSheet("background-image : url('./img/flash_35.png');")

        # spell list
        self.spell_list = ['teleport','ignite','barrier','heal','ghost','cleanse','exhaust']
        
        # 현재 btn_spell1 상태
        self.current_top_spell = 0
        self.current_mid_spell = 1
        self.current_ad_spell = 3
        self.current_sup_spell = 1

        # 스펠변경을 위해 timer 미리 지정
        self.timer_top_spell1 = QTimer(self)
        self.timer_mid_spell1 = QTimer(self)
        self.timer_ad_spell1 = QTimer(self)
        self.timer_sup_spell1 = QTimer(self)

        # 현재 가진 스펠 변경하기
        self.btn_position_top.clicked.connect(self.top_spell_change)
        self.btn_position_mid.clicked.connect(self.mid_spell_change)
        self.btn_position_ad.clicked.connect(self.ad_spell_change)
        self.btn_position_sup.clicked.connect(self.sup_spell_change)

        # 포지션별 개인 쿨타임 재기
        self.btn_spell1_top.clicked.connect(self.btn_spell1_top_def)
        self.btn_spell1_mid.clicked.connect(self.btn_spell1_mid_def)
        self.btn_spell1_ad.clicked.connect(self.btn_spell1_ad_def)
        self.btn_spell1_sup.clicked.connect(self.btn_spell1_sup_def)


        # 기본 window frmae remove
        # self.setWindowFlag(Qt.WindowStaysOnTopHint) # 하나씩 적용
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 하나씩 적용
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) # 두개 한번에 적용
        self.setAttribute(Qt.WA_TranslucentBackground)  # 배경 투명

        # btn_position style
        self.btn_position_top.setStyleSheet('QPushButton {background-color: #000000; color: white; border-style: solid; border-width: 1px; border-color: #cfcfcf;}QPushButton::hover{background-color: #cfcfcf; color: black;}')
        self.btn_position_jg.setStyleSheet('QPushButton {background-color: #000000; color: white; border-style: solid; border-width: 1px; border-color: #cfcfcf;} QPushButton::hover{background-color: #cfcfcf; color: black;}')
        self.btn_position_mid.setStyleSheet('QPushButton {background-color: #000000; color: white; border-style: solid; border-width: 1px; border-color: #cfcfcf;} QPushButton::hover{background-color: #cfcfcf; color: black;}')
        self.btn_position_ad.setStyleSheet('QPushButton {background-color: #000000; color: white; border-style: solid; border-width: 1px; border-color: #cfcfcf;} QPushButton::hover{background-color: #cfcfcf; color: black;}')
        self.btn_position_sup.setStyleSheet('QPushButton {background-color: #000000; color: white; border-style: solid; border-width: 1px; border-color: #cfcfcf;} QPushButton::hover{background-color: #cfcfcf; color: black;}')
    
        self.btn_top.clicked.connect(self.top_timer)
        self.btn_jg.clicked.connect(self.jg_timer)
        self.btn_mid.clicked.connect(self.mid_timer)
        self.btn_ad.clicked.connect(self.ad_timer)
        self.btn_sup.clicked.connect(self.sup_timer)

        # close btn
        self.btn_close.setStyleSheet('QPushButton {background-color: #000000; color: white; font-weight: bold;} QPushButton::hover{background-color: rgb(255, 0, 4);}')
        self.btn_close.clicked.connect(self.close)

        # label footer
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        # print(screensize[0])
        self.label_footer.setText('SCREEN : '+str(screensize[0])+' x '+str(screensize[1]))
        self.label_footer.setAlignment( Qt.AlignRight)



        self.show()  

    def top_timer(self): 
        if self.btn_top.text() == '':   # 현재 Top 라고 글자가 표시되어 있다면
            self.btn_top.setStyleSheet("background-image : url('./img/flash_opacity_35.png'); color: white; font-weight: bold;")
            self.btn_top.setText('5:00')
            self.time_index_top_sec = 60 # 60초에서 시작
            self.time_index_top_min = 4  # 4분에서 시작
            self.timer_top = QTimer(self)
            self.timer_top.setInterval(1000)  # 1초에 한번씩 self.top 함수 실행
            self.timer_top.timeout.connect(self.top)
            self.timer_top.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_top.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_top.setText('')
            self.timer_top.stop()
        
    def top(self):
        if self.time_index_top_min>=0 and self.time_index_top_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_top_sec -= 1
            if self.time_index_top_sec>=10:
                time_str_top = str(self.time_index_top_min)+':'+str(self.time_index_top_sec)
                self.btn_top.setText(time_str_top)
            elif self.time_index_top_sec<10:
                time_str_top = str(self.time_index_top_min)+':0'+str(self.time_index_top_sec)
                self.btn_top.setText(time_str_top)
            
            if self.time_index_top_min>0 and self.time_index_top_sec==0:  # 0분 초과 / 0초일때
                self.time_index_top_min -= 1
                self.time_index_top_sec = 60
        if self.time_index_top_min==0 and self.time_index_top_sec==0:  # 0분, 0초 일때
            self.btn_top.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_top.setText('')
            self.timer_top.stop()

    def jg_timer(self):
        if self.btn_jg.text() == '':
            self.btn_jg.setStyleSheet("background-image : url('./img/flash_opacity_35.png'); color: white; font-weight: bold;")
            self.btn_jg.setText('5:00')
            self.time_index_jg_sec = 60 # 60초에서 시작
            self.time_index_jg_min = 4  # 4분에서 시작
            self.timer_jg = QTimer(self)
            self.timer_jg.setInterval(1000)
            self.timer_jg.timeout.connect(self.jg)
            self.timer_jg.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_jg.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_jg.setText('')
            self.timer_jg.stop()
    def jg(self):
        if self.time_index_jg_min>=0 and self.time_index_jg_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_jg_sec -= 1
            if self.time_index_jg_sec>=10:
                time_str_jg = str(self.time_index_jg_min)+':'+str(self.time_index_jg_sec)
                self.btn_jg.setText(time_str_jg)
            elif self.time_index_jg_sec<10:
                time_str_jg = str(self.time_index_jg_min)+':0'+str(self.time_index_jg_sec)
                self.btn_jg.setText(time_str_jg)

            if self.time_index_jg_min>0 and self.time_index_jg_sec==0:  # 0분 초과 / 0초일때
                self.time_index_jg_min -= 1
                self.time_index_jg_sec = 60
        if self.time_index_jg_min==0 and self.time_index_jg_sec==0:  # 0분, 0초 일때
            self.btn_jg.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_jg.setText('')
            self.timer_jg.stop()

    def mid_timer(self):
        if self.btn_mid.text() == '':
            self.btn_mid.setStyleSheet("background-image : url('./img/flash_opacity_35.png'); color: white; font-weight: bold;")
            self.btn_mid.setText('5:00')
            self.time_index_mid_sec = 60 # 60초에서 시작
            self.time_index_mid_min = 4  # 4분에서 시작
            self.timer_mid = QTimer(self)
            self.timer_mid.setInterval(1000)
            self.timer_mid.timeout.connect(self.mid)
            self.timer_mid.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_mid.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_mid.setText('')
            self.timer_mid.stop()
    def mid(self):
        if self.time_index_mid_min>=0 and self.time_index_mid_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_mid_sec -= 1
            if self.time_index_mid_sec>=10:
                time_str_mid = str(self.time_index_mid_min)+':'+str(self.time_index_mid_sec)
                self.btn_mid.setText(time_str_mid)
            elif self.time_index_mid_sec<10:
                time_str_mid = str(self.time_index_mid_min)+':0'+str(self.time_index_mid_sec)
                self.btn_mid.setText(time_str_mid)

            if self.time_index_mid_min>0 and self.time_index_mid_sec==0:  # 0분 초과 / 0초일때
                self.time_index_mid_min -= 1
                self.time_index_mid_sec = 60
        if self.time_index_mid_min==0 and self.time_index_mid_sec==0:  # 0분, 0초 일때
            self.btn_mid.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_mid.setText('')
            self.timer_mid.stop()

    def ad_timer(self):
        if self.btn_ad.text() == '':
            self.btn_ad.setStyleSheet("background-image : url('./img/flash_opacity_35.png'); color: white; font-weight: bold;")
            self.btn_ad.setText('5:00')
            self.time_index_ad_sec = 60 # 60초에서 시작
            self.time_index_ad_min = 4  # 4분에서 시작
            self.timer_ad = QTimer(self)
            self.timer_ad.setInterval(1000)
            self.timer_ad.timeout.connect(self.ad)
            self.timer_ad.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_ad.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_ad.setText('')
            self.timer_ad.stop()
    def ad(self):
        if self.time_index_ad_min>=0 and self.time_index_ad_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_ad_sec -= 1
            if self.time_index_ad_sec>=10:
                time_str_ad = str(self.time_index_ad_min)+':'+str(self.time_index_ad_sec)
                self.btn_ad.setText(time_str_ad)
            elif self.time_index_ad_sec<10:
                time_str_ad = str(self.time_index_ad_min)+':0'+str(self.time_index_ad_sec)
                self.btn_ad.setText(time_str_ad)

            if self.time_index_ad_min>0 and self.time_index_ad_sec==0:  # 0분 초과 / 0초일때
                self.time_index_ad_min -= 1
                self.time_index_ad_sec = 60
        if self.time_index_ad_min==0 and self.time_index_ad_sec==0:  # 0분, 0초 일때
            self.btn_ad.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_ad.setText('')
            self.timer_ad.stop()

    def sup_timer(self):
        if self.btn_sup.text() == '':
            self.btn_sup.setStyleSheet("background-image : url('./img/flash_opacity_35.png'); color: white; font-weight: bold;")
            self.btn_sup.setText('5:00')
            self.time_index_sup_sec = 60 # 60초에서 시작
            self.time_index_sup_min = 4  # 4분에서 시작
            self.timer_sup = QTimer(self)
            self.timer_sup.setInterval(1000)
            self.timer_sup.timeout.connect(self.sup)
            self.timer_sup.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_sup.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_sup.setText('')
            self.timer_sup.stop()
    def sup(self):
        if self.time_index_sup_min>=0 and self.time_index_sup_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_sup_sec -= 1
            if self.time_index_sup_sec>=10:
                time_str_sup = str(self.time_index_sup_min)+':'+str(self.time_index_sup_sec)
                self.btn_sup.setText(time_str_sup)
            elif self.time_index_sup_sec<10:
                time_str_sup = str(self.time_index_sup_min)+':0'+str(self.time_index_sup_sec)
                self.btn_sup.setText(time_str_sup)

            if self.time_index_sup_min>0 and self.time_index_sup_sec==0:  # 0분 초과 / 0초일때
                self.time_index_sup_min -= 1
                self.time_index_sup_sec = 60
        if self.time_index_sup_min==0 and self.time_index_sup_sec==0:  # 0분, 0초 일때
            self.btn_sup.setStyleSheet("background-image : url('./img/flash_35.png');")
            self.btn_sup.setText('')
            self.timer_sup.stop()

    #####################################  spell change ###########################################
    # ['teleport','ignite','barrier','heal','ghost','cleanse','exhaust']
    def top_spell_change(self):
        self.spell_change_def(position='top')

    def mid_spell_change(self):
        self.spell_change_def(position='mid')

    def ad_spell_change(self):
        self.spell_change_def(position='ad')

    def sup_spell_change(self):
        self.spell_change_def(position='sup')


    def spell_change_def(self, position):
        position = position
        if position == 'top':
            if self.current_top_spell != 6:
                self.current_top_spell += 1
            elif self.current_top_spell == 6:
                self.current_top_spell = 0
            current_spell1 = self.current_top_spell
            btn = self.btn_spell1_top
            timer = self.timer_top_spell1
        if position == 'mid':
            if self.current_mid_spell != 6:
                self.current_mid_spell += 1
            elif self.current_mid_spell == 6:
                self.current_mid_spell = 0
            current_spell1 = self.current_mid_spell
            btn = self.btn_spell1_mid
            timer = self.timer_mid_spell1
        if position == 'ad':
            if self.current_ad_spell != 6:
                self.current_ad_spell += 1
            elif self.current_ad_spell == 6:
                self.current_ad_spell = 0
            current_spell1 = self.current_ad_spell
            btn = self.btn_spell1_ad
            timer = self.timer_ad_spell1
        if position == 'sup':
            if self.current_sup_spell != 6:
                self.current_sup_spell += 1
            elif self.current_sup_spell == 6:
                self.current_sup_spell = 0
            current_spell1 = self.current_sup_spell
            btn = self.btn_spell1_sup
            timer = self.timer_sup_spell1

        if current_spell1 == 0:
            btn.setStyleSheet("background-image : url('./img/teleport_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 1:
            btn.setStyleSheet("background-image : url('./img/ignite_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 2:
            btn.setStyleSheet("background-image : url('./img/barrier_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 3:
            btn.setStyleSheet("background-image : url('./img/heal_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 4:
            btn.setStyleSheet("background-image : url('./img/ghost_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 5:
            btn.setStyleSheet("background-image : url('./img/cleanse_35.png');")
            timer.stop()
            btn.setText('')
        if current_spell1 == 6:
            btn.setStyleSheet("background-image : url('./img/exhaust_35.png');")
            timer.stop()
            btn.setText('')


    ############################################ spell1 timer ##########################################
    # 텔 360초(6분) / 점화 방어막 180초(3분) / 회복 240초(4분) / 유체화 정화 탈진 210초 (3분30초)
    # self.spell_list = ['teleport','ignite','barrier','heal','ghost','cleanse','exhaust']

    def btn_spell1_top_def(self): 
        if self.btn_spell1_top.text() == '':   # 텍스트가 없다면

            # 시작 text, sec, min을 반환하는 함수
            text, sec, min = self.btn_spell1_time(current_spell1=self.current_top_spell)
            self.btn_spell1_top.setText(text)
            self.time_index_top_spell1_sec = sec
            self.time_index_top_spell1_min = min
            # btn style 변환해주는 함수
            self.btn_spell1_style(position='top',type='opacity')

            # self.timer_top_spell1 = QTimer(self)
            self.timer_top_spell1.setInterval(1000)  # 1초에 한번씩 self.top 함수 실행
            self.timer_top_spell1.timeout.connect(self.top_spell1)
            self.timer_top_spell1.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_spell1_style(position='top',type='original')
            self.btn_spell1_top.setText('')
            self.timer_top_spell1.stop()
        
    def top_spell1(self):
        if self.time_index_top_spell1_min>=0 and self.time_index_top_spell1_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_top_spell1_sec -= 1
            if self.time_index_top_spell1_sec>=10:
                time_str_top = str(self.time_index_top_spell1_min)+':'+str(self.time_index_top_spell1_sec)
                self.btn_spell1_top.setText(time_str_top)
            elif self.time_index_top_spell1_sec<10:
                time_str_top = str(self.time_index_top_spell1_min)+':0'+str(self.time_index_top_spell1_sec)
                self.btn_spell1_top.setText(time_str_top)
            
            if self.time_index_top_spell1_min>0 and self.time_index_top_spell1_sec==0:  # 0분 초과 / 0초일때
                self.time_index_top_spell1_min -= 1
                self.time_index_top_spell1_sec = 60
        if self.time_index_top_spell1_min==0 and self.time_index_top_spell1_sec==0:  # 0분, 0초 일때
            self.btn_spell1_style(position='top',type='original')
            self.btn_spell1_top.setText('')
            self.timer_top_spell1.stop()

    def btn_spell1_mid_def(self): 
        if self.btn_spell1_mid.text() == '':   # 텍스트가 없다면

            # 시작 text, sec, min을 반환하는 함수
            text, sec, min = self.btn_spell1_time(current_spell1=self.current_mid_spell)
            self.btn_spell1_mid.setText(text)
            self.time_index_mid_spell1_sec = sec
            self.time_index_mid_spell1_min = min
            # btn style 변환해주는 함수
            self.btn_spell1_style(position='mid',type='opacity')

            self.timer_mid_spell1 = QTimer(self)
            self.timer_mid_spell1.setInterval(1000)  # 1초에 한번씩 self.mid 함수 실행
            self.timer_mid_spell1.timeout.connect(self.mid_spell1)
            self.timer_mid_spell1.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_spell1_style(position='mid',type='original')
            self.btn_spell1_mid.setText('')
            self.timer_mid_spell1.stop()
        
    def mid_spell1(self):
        if self.time_index_mid_spell1_min>=0 and self.time_index_mid_spell1_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_mid_spell1_sec -= 1
            if self.time_index_mid_spell1_sec>=10:
                time_str_mid = str(self.time_index_mid_spell1_min)+':'+str(self.time_index_mid_spell1_sec)
                self.btn_spell1_mid.setText(time_str_mid)
            elif self.time_index_mid_spell1_sec<10:
                time_str_mid = str(self.time_index_mid_spell1_min)+':0'+str(self.time_index_mid_spell1_sec)
                self.btn_spell1_mid.setText(time_str_mid)
            
            if self.time_index_mid_spell1_min>0 and self.time_index_mid_spell1_sec==0:  # 0분 초과 / 0초일때
                self.time_index_mid_spell1_min -= 1
                self.time_index_mid_spell1_sec = 60
        if self.time_index_mid_spell1_min==0 and self.time_index_mid_spell1_sec==0:  # 0분, 0초 일때
            self.btn_spell1_style(position='mid',type='original')
            self.btn_spell1_mid.setText('')
            self.timer_mid_spell1.stop()

    def btn_spell1_ad_def(self): 
        if self.btn_spell1_ad.text() == '':   # 텍스트가 없다면

            # 시작 text, sec, min을 반환하는 함수
            text, sec, min = self.btn_spell1_time(current_spell1=self.current_ad_spell)
            self.btn_spell1_ad.setText(text)
            self.time_index_ad_spell1_sec = sec
            self.time_index_ad_spell1_min = min
            # btn style 변환해주는 함수
            self.btn_spell1_style(position='ad',type='opacity')

            self.timer_ad_spell1 = QTimer(self)
            self.timer_ad_spell1.setInterval(1000)  # 1초에 한번씩 self.ad 함수 실행
            self.timer_ad_spell1.timeout.connect(self.ad_spell1)
            self.timer_ad_spell1.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_spell1_style(position='ad',type='original')
            self.btn_spell1_ad.setText('')
            self.timer_ad_spell1.stop()
        
    def ad_spell1(self):
        if self.time_index_ad_spell1_min>=0 and self.time_index_ad_spell1_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_ad_spell1_sec -= 1
            if self.time_index_ad_spell1_sec>=10:
                time_str_ad = str(self.time_index_ad_spell1_min)+':'+str(self.time_index_ad_spell1_sec)
                self.btn_spell1_ad.setText(time_str_ad)
            elif self.time_index_ad_spell1_sec<10:
                time_str_ad = str(self.time_index_ad_spell1_min)+':0'+str(self.time_index_ad_spell1_sec)
                self.btn_spell1_ad.setText(time_str_ad)
            
            if self.time_index_ad_spell1_min>0 and self.time_index_ad_spell1_sec==0:  # 0분 초과 / 0초일때
                self.time_index_ad_spell1_min -= 1
                self.time_index_ad_spell1_sec = 60
        if self.time_index_ad_spell1_min==0 and self.time_index_ad_spell1_sec==0:  # 0분, 0초 일때
            self.btn_spell1_style(position='ad',type='original')
            self.btn_spell1_ad.setText('')
            self.timer_ad_spell1.stop()

    def btn_spell1_sup_def(self): 
        if self.btn_spell1_sup.text() == '':   # 텍스트가 없다면

            # 시작 text, sec, min을 반환하는 함수
            text, sec, min = self.btn_spell1_time(current_spell1=self.current_sup_spell)
            self.btn_spell1_sup.setText(text)
            self.time_index_sup_spell1_sec = sec
            self.time_index_sup_spell1_min = min
            # btn style 변환해주는 함수
            self.btn_spell1_style(position='sup',type='opacity')

            self.timer_sup_spell1 = QTimer(self)
            self.timer_sup_spell1.setInterval(1000)  # 1초에 한번씩 self.sup 함수 실행
            self.timer_sup_spell1.timeout.connect(self.sup_spell1)
            self.timer_sup_spell1.start()
        else:  # 숫자로 표시되어 있다면
            self.btn_spell1_style(position='sup',type='original')
            self.btn_spell1_sup.setText('')
            self.timer_sup_spell1.stop()
        
    def sup_spell1(self):
        if self.time_index_sup_spell1_min>=0 and self.time_index_sup_spell1_sec>0:   # 분과 초가 둘다 0 초과
            self.time_index_sup_spell1_sec -= 1
            if self.time_index_sup_spell1_sec>=10:
                time_str_sup = str(self.time_index_sup_spell1_min)+':'+str(self.time_index_sup_spell1_sec)
                self.btn_spell1_sup.setText(time_str_sup)
            elif self.time_index_sup_spell1_sec<10:
                time_str_sup = str(self.time_index_sup_spell1_min)+':0'+str(self.time_index_sup_spell1_sec)
                self.btn_spell1_sup.setText(time_str_sup)
            
            if self.time_index_sup_spell1_min>0 and self.time_index_sup_spell1_sec==0:  # 0분 초과 / 0초일때
                self.time_index_sup_spell1_min -= 1
                self.time_index_sup_spell1_sec = 60
        if self.time_index_sup_spell1_min==0 and self.time_index_sup_spell1_sec==0:  # 0분, 0초 일때
            self.btn_spell1_style(position='sup',type='original')
            self.btn_spell1_sup.setText('')
            self.timer_sup_spell1.stop()


    def btn_spell1_time(self, current_spell1):
        current_spell1 = current_spell1
            
        if current_spell1 == 0:  # 텔레포트
            return '6:00', 60, 5 
        if current_spell1 in [1,2]: # 점화 방어막
            return '3:00', 60, 2 
        if current_spell1 == 3: # 힐
            return '4:00', 60, 3 
        if current_spell1 in [4,5,6]: # 유체화 정화 탈진
            return '3:30', 30, 3 

    def btn_spell1_style(self,position,type):
        position = position
        if position == 'top':
            current_spell1 = self.current_top_spell
            btn = self.btn_spell1_top
        if position == 'mid':
            current_spell1 = self.current_mid_spell
            btn = self.btn_spell1_mid
        if position == 'ad':
            current_spell1 = self.current_ad_spell
            btn = self.btn_spell1_ad
        if position == 'sup':
            current_spell1 = self.current_sup_spell
            btn = self.btn_spell1_sup


        if type == 'opacity':
            if current_spell1 == 0:  # 텔레포트
                btn.setStyleSheet("background-image : url('./img/teleport_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 1:  # 점화
                btn.setStyleSheet("background-image : url('./img/ignite_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 2:  # 베리어
                btn.setStyleSheet("background-image : url('./img/barrier_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 3:  # 힐
                btn.setStyleSheet("background-image : url('./img/heal_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 4:  # 유체화
                btn.setStyleSheet("background-image : url('./img/ghost_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 5:  # 정화
                btn.setStyleSheet("background-image : url('./img/cleanse_opacity_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 6:  # 탈진
                btn.setStyleSheet("background-image : url('./img/exhaust_opacity_35.png'); color: white; font-weight: bold;")

        if type == 'original':
            if current_spell1 == 0:  # 텔레포트
                btn.setStyleSheet("background-image : url('./img/teleport_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 1:  # 점화
                btn.setStyleSheet("background-image : url('./img/ignite_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 2:  # 베리어
                btn.setStyleSheet("background-image : url('./img/barrier_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 3:  # 힐
                btn.setStyleSheet("background-image : url('./img/heal_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 4:  # 유체화
                btn.setStyleSheet("background-image : url('./img/ghost_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 5:  # 정화
                btn.setStyleSheet("background-image : url('./img/cleanse_35.png'); color: white; font-weight: bold;")
            if current_spell1 == 6:  # 탈진
                btn.setStyleSheet("background-image : url('./img/exhaust_35.png'); color: white; font-weight: bold;")

    ### Move window # 상단바 눌러서 window 이동하기위함
    def mousePressEvent(self, event): # 기본내장함수라 이름바꾸면 안됨.
        self.dragPos = event.globalPos()
        # print(self.dragPos)  # 마우스 클릭 좌표 알려줌


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Ui_MainWindow = Ui_MainWindow()
    sys.exit(app.exec_())  # app.exec_() : 이벤트 처리를 위한 루프를 실행 / 메인루프를 실행



