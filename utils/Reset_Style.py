#!/usr/bin/env python3

MAIN_STYLE = """#MainWindow{
	background-color: rgb(48, 51, 41);
}

/*评论是否还有更多的label*/
#no_more_comment_label{
	color: rgb(255, 255, 255);
	font:12pt "MicroSoft YaHei";
}

/*单个评论区的最外层frame*/
#oneComment{
	background-color: rgb(48, 51, 41);
}

/*评论区的scroll area*/
#comment_scrollArea{
	background-color: rgba(255, 255, 255, 0);
}

/*评论区的最外层frame*/
Comment_Widget{
	background-color: rgba(150, 200, 250, 0);
}

QFrame QCommandLinkButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}

/*小图浏览画师名称label*/
QFrame QLabel#authLabel{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
	font: 9pt "MicroSoft YaHei";
}

/*下载按钮上的红点*/
QFrame QLabel#downloadTipsLabel{
	background-color:rgba(0,0,0,0);
}

/*用户头像label*/
QFrame QLabel#login_user_pic_label{
	background-color: rgba(255, 255, 255, 0);
}

/*小图浏览右上角指示作品包含多少图片的Label*/
QFrame QLabel#picnNumLabel{
	background-color: rgba(122, 122, 122, 150);
	font: 16pt "Noto Sans CJK SC";
	color: rgb(255, 255, 255);
}

/*小图浏览作品标题label*/
QFrame QLabel#textLabel{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
	font: 12pt "MicroSoft YaHei";
}

/*评论时间Label*/
QFrame QLabel#time_label{
	color: rgb(209, 209, 209);
}

/*评论用户名Label*/
QFrame QLabel#user_name_label{
	color: rgb(255, 255, 255);
	font: 9pt "MicroSoft YaHei";
}


/*登录的用户名Label*/
QFrame QLabel#usernameLabel{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
	font: 12pt "MicroSoft YaHei";
}

/*小图浏览"だいすき"按钮*/
QFrame QPushButton#likeButton{
	color: rgb(255, 255, 255);
}

/*小图浏览"保存原图"按钮*/
QFrame QPushButton#s_saveButton{
	color: rgb(255, 255, 255);
}

/*装载大图的scroll area*/
QFrame QScrollArea#bigPicScrollArea{
	background-color: rgba(255, 255, 255, 0);
}

/*QFrame Show_Head_Label#user_pic_label{
	background-color: rgba(255, 255, 255, 0);
}*/

#user_pic_label{
	background-color: rgba(255, 255, 255, 0);
}

QFrame clickable_label#picLabel{
	background-color: rgba(255, 255, 255, 0);
}

/*显示作品详细信息的frame*/
QFrame info_frame#Frame{
	background-color: rgb(29, 23, 31);
}

/*搜索框外层frame*/
QFrame search_frame#Frame{
	background-color: rgb(25, 25, 25);
}

/*tabWidget 的子控件widget*/
QStackedWidget my_widget#tab{
	background-color: rgba(255, 255, 255, 0);
}


QWidget QCommandLinkButton#R18Button{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#RankButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#dayFemaleButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#dayMaleButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#dayMangaButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#dayRookieButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#monthButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#recommendButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#weekButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QCommandLinkButton#weekOriginalButton{
	color:rgb(255, 255, 255);
	font: 12pt "Noto Sans CJK SC";
}


QWidget QFrame#SmallFrame{
	background-color: rgba(112, 112, 112, 100);
}


QWidget QFrame#frame{
	background-color: rgba(112, 112, 112, 100);
}

/*装载左下角的功能按钮的frame*/
QWidget QFrame#function_frame{
	background-color: rgba(112, 112, 112, 100);
}


QWidget QLabel#bigPicLabel{
	background-color: rgb(255, 255, 255);
}

/*装载每日、新人、每月等按钮的frame*/
QWidget QScrollArea#cate_scrollArea{
	background-color: rgba(122, 122, 122, 50);
}


QWidget QWidget#comments_scroll{
	background-color: rgba(64, 64, 64, 0);
}

/*下方作品详情的标题label*/
info_frame QLabel#titleText{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
	font: 9pt "MicroSoft YaHei";
}


info_frame QLabel{
	background-color: rgba(255, 255, 255, 0);
	color: white；
}


/*info_frame Show_Head_Label#user_pic_label{
	background-color: rgb(255, 255, 255);
}*/

/*作品详情中的画师名称Label*/
info_frame my_label#authText{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
}


info_frame my_label{
	background-color: rgba(255, 255, 255, 0);
	color: white
}


info_frame text_scroll#text_scroll{
	background-color: rgba(255, 255, 255, 0);
	color: rgb(255, 255, 255);
	border: none
}


my_widget QScrollArea#scrollArea{
	background-color: rgba(255, 255, 255, 0);
}


my_widget show_users_frame#show_users_frame{
	background-color: rgba(122, 122, 122, 150);
}

my_widget small_pic_frame#small_pic_frame{
	background-color: rgba(122,122,122,150)
}


search_frame QComboBox#searchComboBox{
	color: rgb(255, 255, 255);
	background-color: rgba(48, 51, 41, 255);
}

/*搜索框选项下拉样式*/
#searchComboBox QAbstractItemView{
	background-color: rgba(48, 51, 41, 125);
	border: none;
}


search_frame QLineEdit#searchLineEdit{
	color: rgb(255, 255, 255);
	background-color: rgb(50, 50, 50);
}


show_users_frame QLabel#userHeadLabel{
	background-color: rgba(255, 228, 249, 0);
}


show_users_frame clickable_label#label{
	background-color: rgb(232, 255, 148);
}


show_users_frame clickable_label#usernameLabel{
	background-color: rgba(175, 255, 246, 0);
}

QFrame QTabWidget:pane{
	background-color: transparent;
	border:none;
}




QTabBar:tab{
	color:rgb(255, 255, 255);
	background-color: rgba(102, 102, 102, 128);
}

QTabBar:tab:selected{
	background-color: rgba(102, 206, 255, 255);
}


info_frame QPushButton{
	color: rgb(255, 255, 255);
	border:2px;
	border-radius:15px;
	padding:2px 4px
}

info_frame QPushButton:hover{
	background-color:lightblue;
	color:black;
}

info_frame QPushButton:pressed{
	background-color:black
}


search_frame QPushButton{
	color: rgb(255, 255, 255);
	border:2px;
	border-radius:15px;
	padding:2px 4px;
}

search_frame QPushButton:hover{
	background-color:lightblue;
	color:black
}

search_frame QPushButton:pressed{
	background-color:black;
}


TableView QHeaderView::section{
	background-color:rgba(0, 0, 0, 0);
	font:13pt '宋体';
	color: white;
}

/*提示板*/
QToolTip{
	background-color: #000000;
	color: #FFFFFF;
	border: none;
}


show_users_frame QPushButton{
	color: rgb(255, 255, 255);
	border:2px;
	border-radius:15px;
	padding:2px 4px;
}

show_users_frame QPushButton:hover{
	background-color:lightblue;
	color:black;
}

show_users_frame QPushButton:pressed{
	background-color:black;
}

/*以下为手动编辑*/

/*用户名Label*/
#usernameLabel{
	background-color: rgba(255, 255, 255, 0);
    color: rgb(255, 255, 0);
}

/*包裹左边侧栏的分类按钮的QScrollArea*/
#cate_scrollArea{
	background-color: rgba(122, 122, 122, 0);
	border: none;
}

/*包裹左边侧栏的分类按钮的QScrollArea里的widget*/
#cate_widget{
	background-color: rgba(0, 0, 0, 0);
}

/*包裹左下角功能按钮的frame*/
#function_frame{
	background-color: rgba(112, 112, 112, 0);
	border: none;
}

/*侧边所有QCommandLinkButton*/
QCommandLinkButton{
	background-color: rgba(112, 112, 112, 100);
}

QCommandLinkButton QIcon{
	background-image: url(./RES/正常-p.png)
}

/*右边包裹浏览小图、大图、下载详情页的frame*/
#SmallFrame{
	background-color: rgba(112, 112, 112, 100);
}

/*右边显示大图的ScrollArea*/
#bigPicScrollArea{
	background-color: rgba(255, 255, 255, 0);
}

/*右边显示大图的ScrollArea里的widget*/
#scrollAreaWidgetContents_3{
	background-color: rgba(255, 255, 255, 0);
}

#comment_scrollArea{
	background-color: rgba(255, 255, 255, 0);
}

/*展示评论的QTextBrowser*/
QFrame QTextBrowser#comment_text{
	color: rgb(255, 255, 255);
	background-color: rgb(48, 51, 41);
	border: none;
}



/*浏览小图中包含众多小图的widget*/
#scrollAreaWidgetContent{
	background-color: rgba(122, 122, 122, 0);
}

/*小图的最二层frame*/
small_pic_frame QFrame#frame{
	background-color: rgba(122, 122, 122, 0);
}

small_pic_frame QPushButton{
	color: rgb(255, 255, 255);
	border:2px;
	border-radius:15px;
	padding:2px 4px;
}

small_pic_frame QPushButton:hover{
	color: rgb(0,0,0);
	background-color: lightblue;
	border:2px;
	border-radius:15px;
	padding:2px 4px;
}

/*下载页面*/
QTableView{
	color: white;
	background-color: rgba(255, 255, 255, 0);
	alternate-background-color: rgba(180, 180, 180, 150);
	selection-background-color: lightblue;
}

/*QTableView::item:!alternate:!selected{
    background-color: rgba(220, 220, 220, 150);
}
*/
/*下载页面表头*/
QHeaderView{
	background-color: rgba(255, 255, 255, 0);
}

/*浏览小图的外层tabwidget*/
QTabWidget QWidget{
	border: none;
}


/*滚动条*/
QScrollBar:vertical
{
    background-color:rgba(48, 51, 41,0); 
    width: 12px;
}

QScrollBar::handle:vertical:hover{
	background:qlineargradient(
		spread:pad, x1:0, y1:0, x2:0, y2:1, 
		stop:0 rgb(255, 0, 0), 
		stop: 0.17 rgb(255, 165, 0), 
		stop:0.34 rgb(255, 255, 0),
		stop: 0.51 rgb(0, 255, 0), 
		stop: 0.68 rgb(0,127,255), 
		stop: 0.85 rgb(0,0,255), 
		stop: 1 rgb(139, 0, 255)
		);
	border-radius: 6px; 
}

QScrollBar::handle:vertical{
	background:qlineargradient(
		spread:pad, x1:0, y1:0, x2:0, y2:1, 
		stop:0 rgba(255, 0, 0, 100), 
		stop: 0.17 rgba(255, 165, 0, 100), 
		stop:0.34 rgba(255, 255, 0, 100),
		stop: 0.51 rgba(0, 255, 0, 100), 
		stop: 0.68 rgba(0,127,255, 100), 
		stop: 0.85 rgba(0,0,255, 100), 
		stop: 1 rgba(139, 0, 255, 100)
		);
	border-radius: 6px; 
}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical{
	height: 0px;
	width: 0px;
}

#SettingWindow{
	background-color: rgb(150, 200, 250);
}

#pic_title_label, #file_title_label{
	font: 18pt;
	color: rgb(0,0,0);
}
"""

LOGIN_STYLE = """app_login QWidget{
	border-radius:15px;
}

#interrupt_login_button{
	background-color: rgba(255, 255, 255, 0);
	border: none;
}

#loginGIF{
	background-color: rgb(102, 206, 255);
}

#loginText{
	font: 20pt "Noto Sans CJK SC";
	background-color: rgb(102, 206, 255);
}

#widget{
	background-color: rgb(102, 206, 255);
}

#autoLogin{
	background-color: rgb(102, 206, 255);
	font: 9pt "Noto Sans CJK SC"
}

#label, #label_2, #label_3{
	font: 18pt "Noto Sans CJK SC"
}

#lineEdit, #lineEdit_2{
	background-color: rgb(255, 255, 255);
	font: 10pt "Noto Sans CJK SC"
}

#pushButton{
	background-color: rgb(255, 255, 255);
}

#interrupt_login_button, #exit_button{
	border-image: url(./RES/exit.png);
}"""

def reset_loging_style():
	with open('Login_Style.qss', 'w') as f:
		f.write(LOGIN_STYLE)

def reset_main_style():
	with open('Main_Style.qss', 'w') as f:
		f.write(MAIN_STYLE)