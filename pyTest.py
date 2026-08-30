import wx
import wx.dataview
import sys
import pyperclip
import datetime
import system.libs.NowVideo.NVD_wxUI as ui
import DetailedInfo as D

try:
    PATH_PREFIX = sys._MEPASS + '/'
    print("[!] Boot from: " + PATH_PREFIX)
except:
    PATH_PREFIX = None

########## Const Values ##########
BASE_WINDOW_SIZE = (900,600)
LEFT_PANEL_WIDTH = 540
STATUS_BAR_HEIGHT = 24

WINDOW = {
    'INITIAL_SIZE': BASE_WINDOW_SIZE,
    'MAX_SIZE': (1200,BASE_WINDOW_SIZE[1])
}
PANEL = {
    'LEFT': {
        'POS': (0,0),
        'SIZE': (LEFT_PANEL_WIDTH,WINDOW['INITIAL_SIZE'][1]-STATUS_BAR_HEIGHT)
    },
    'RIGHT': {
        'POS': (0,0),
        'SIZE': (WINDOW['INITIAL_SIZE'][0]-LEFT_PANEL_WIDTH,WINDOW['INITIAL_SIZE'][1]-STATUS_BAR_HEIGHT)
    },
    'STATUS_BAR': {
        'POS': (0,WINDOW['INITIAL_SIZE'][1]-STATUS_BAR_HEIGHT),
        'SIZE': (WINDOW['MAX_SIZE'][0],STATUS_BAR_HEIGHT)
    },
    'DEBUG': {
        'POS': (WINDOW['INITIAL_SIZE'][0],0),
        'SIZE': (WINDOW['MAX_SIZE'][0]-WINDOW['INITIAL_SIZE'][0],WINDOW['INITIAL_SIZE'][1]-STATUS_BAR_HEIGHT)
    }
}
COLOR = {
    'WINDOW': {
        'SELF': {
            'BG': "#FFFFFF",
            'FG': "#000000"
        },
        'TEXT': {
            'BG': "#FFFFFF",
            'FG': "#000000"
        }
    },
    'DEBUG': {
        'INFO': {
            'BG': "#FFFFFF",
            'FG': "#0055C5"
        },
        'WARN': {
            'BG': "#FFFFFF",
            'FG': "#BE9200"
        },
        'ERR': {
            'BG': "#FFFFFF",
            'FG': "#C90043"
        },
        'SUCC': {
            'BG': "#FFFFFF",
            'FG': "#00B45A"
        }
    },
    'STATUS_BAR': {
        'READY': {
            'BG': "#000000",
            'FG': "#FFFFFF"
        },
        'RUNNING': {
            'BG': "#77D4FF",
            'FG': "#005D88"
        },
        'FAILED': {
            'BG': "#FF7E7E",
            'FG': "#880000"
        },
        'SUCCESSED': {
            'BG': "#7DFF9E",
            'FG': "#008321"
        }
    }
}

########## Function predefined ##########
def GetDateTime():
    return str(datetime.datetime.now())[0:-7]

def hBoxLine(wxObj1:wx.Window,wxObj2:wx.Window=None,Border:int|None=None):
    hBox = wx.BoxSizer(wx.HORIZONTAL)
    if(Border):
        FinalBroder = Border
    else:
        FinalBroder = 0
    hBox.Add(wxObj1,1,wx.EXPAND|wx.ALL,FinalBroder)
    if(wxObj2):
        hBox.Add(wxObj2,1,wx.EXPAND|wx.ALL,FinalBroder)
    hBox.AddStretchSpacer()
    return hBox

########## Event Handlers ##########
def OnClickExit():
    exit(0)

def OnClickWxDebug():
    ui.Debug.wxDebug()

def OnClickAbout(Parent:wx.Window):

    AboutDialog = ui.AboutDialog(
        Parent,"About this App...",
        "system/medias/images/AboutLogo.png",
        None,
        "NVDTEST",
        "A test program for build NVD_wxUI",
        "Version: 20260803A",
        "This Program is licensing under GPL",
        D.DetailedInformation,
        (480,400))
    AboutDialog.Show()

def ToggleWindowSize(Parent:wx.Window):
    if(Parent.GetClientSize()[0] != WINDOW['MAX_SIZE'][0]):
        print("StatusBar Double Click Event Recived, Expand Workspace!")
        Parent.SetClientSize(WINDOW['MAX_SIZE'])
    else:
        print("StatusBar Double Click Event Recived, Shrink Workspace!")
        Parent.SetClientSize(WINDOW['INITIAL_SIZE'])


########## Main Window ###########
def WinMain():
    App = wx.App()
    MainWindow = wx.Frame(None,wx.ID_ANY,"Test wxPython App",style=wx.CLOSE_BOX|wx.MINIMIZE_BOX)
    # For Resizeable, Add wx.RESIZE_BORDER to flags
    #MainWindow = wx.Frame(None,wx.ID_ANY,"Test wxPython App",style=wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)

    MainMenu = wx.MenuBar()
    FileMenu = wx.Menu()
    HelpMenu = wx.Menu()
    MainMenu.Append(FileMenu,"&File")
    MainMenu.Append(HelpMenu,"&Help")
    FileMenu_Exit = FileMenu.Append(wx.ID_EXIT,"&Exit")
    HelpMenu_wxDebug = HelpMenu.Append(9051,"wxDebug")
    HelpMenu_About = HelpMenu.Append(wx.ID_ABOUT,"&About")
    MainWindow.SetMenuBar(MainMenu)

    MainWindow.SetMinClientSize(WINDOW['INITIAL_SIZE'])
    MainWindow.SetMaxClientSize(WINDOW['MAX_SIZE'])
    MainWindow.SetClientSize(WINDOW['INITIAL_SIZE'])
    
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickExit(),FileMenu_Exit)
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickAbout(MainWindow),HelpMenu_About)
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickWxDebug(),HelpMenu_wxDebug)


    # 设置主窗口位置和底色
    MainWindow.Center()
    MainWindow.SetBackgroundColour(wx.Colour(COLOR['WINDOW']['SELF']['BG']))
    MainWindow.Update()

    MainWindow_MainPanel = wx.Panel(MainWindow)
    MainWindow_LeftPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['LEFT']['POS'],PANEL['LEFT']['SIZE'])
    MainWindow_RightPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['RIGHT']['POS'],PANEL['RIGHT']['SIZE'])
    MainWindow_StatusPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['STATUS_BAR']['POS'],PANEL['STATUS_BAR']['SIZE'])
    MainWindow_DebugPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['DEBUG']['POS'],PANEL['DEBUG']['SIZE'])
    MainWindow_MainvBox = wx.BoxSizer(wx.VERTICAL)
    MainvBox_ContenthBox = wx.BoxSizer(wx.HORIZONTAL)
    MainWindow_MainvBox.Add(MainvBox_ContenthBox,0,wx.EXPAND|wx.ALL)
    MainWindow_MainvBox.Add(MainWindow_StatusPanel,0,wx.EXPAND|wx.ALL)
    MainvBox_ContenthBox.Add(MainWindow_LeftPanel,0,wx.EXPAND|wx.ALL)
    MainvBox_ContenthBox.Add(MainWindow_RightPanel,0,wx.EXPAND|wx.ALL)
    MainvBox_ContenthBox.Add(MainWindow_DebugPanel,0,wx.EXPAND|wx.ALL)
    LeftPanel_LeftvBox = wx.BoxSizer(wx.VERTICAL)
    RightPanel_RightvBox = wx.BoxSizer(wx.VERTICAL)
    DebugPanel_DebugvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_MainPanel.SetSizer(MainWindow_MainvBox)
    MainWindow_LeftPanel.SetSizer(LeftPanel_LeftvBox)
    MainWindow_RightPanel.SetSizer(RightPanel_RightvBox)
    MainWindow_DebugPanel.SetSizer(DebugPanel_DebugvBox)
    StatusBar_StatushBox = wx.BoxSizer(wx.HORIZONTAL)
    MainWindow_StatusPanel.SetSizer(StatusBar_StatushBox)
    MainWindow_StatusPanel.SetForegroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['FG']))
    MainWindow_StatusPanel.SetBackgroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['BG']))
    MainWindow_StatusPanel.Bind(wx.EVT_RIGHT_DCLICK,lambda Event:ToggleWindowSize(MainWindow))

    TableView = ui.ListView(MainWindow_LeftPanel,Size=PANEL['LEFT']['SIZE'])
    TableView.SetCols("Enabled:toggle:60|Name:text:160|Progress:progress:80|Status:text")
    TableView.AppendRow([True,"Name 1",60,"Status 1"],"Row1")
    LeftPanel_LeftvBox.AddSpacer(10)
    LeftPanel_LeftvBox.Add(TableView.Body,1,wx.EXPAND|wx.ALL,15)
    LeftPanel_LeftvBox.AddStretchSpacer()
    LeftPanel_LeftvBox.AddSpacer(10)
    TableView.SetValueByIndex("Modified 1",0,TableView.GetColIndexByName("Status")[0])
    print(TableView.GetColIndexByName("Status"))
    print(TableView.GetRowIndexByValue("Modified 1",TableView.GetColIndexByName("Status")[0]))

    STK1_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(330,60),wx.Colour(64,128,80),wx.Colour(255,255,255),"Data 1","Subject 1","SimHei",16,10)
    STK2_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(200,60),wx.Colour(224,128,128),wx.Colour("#FFF"),"Data 2","Subject 2","SimHei",16,10)
    STK2_2 = ui.Sticker(MainWindow_RightPanel,(0,0),(120,60),wx.Colour(128,128,224),wx.Colour("#FFF"),"Data 3","Subject 3","SimHei",16,10)
    STK1_1.Body.Bind(wx.EVT_RIGHT_UP,lambda Event:pyperclip.copy("Data 1"))
    STK2_1.Body.Bind(wx.EVT_RIGHT_UP,lambda Event:pyperclip.copy("Data 2"))
    STK2_2.Body.Bind(wx.EVT_RIGHT_UP,lambda Event:pyperclip.copy("Data 3"))

    Stickers = []
    Stickers.append(hBoxLine(STK1_1.Body,Border=5))
    Stickers.append(hBoxLine(STK2_1.Body,STK2_2.Body,Border=5))

    RightPanel_RightvBox.AddSpacer(10)
    for line in Stickers:
        RightPanel_RightvBox.Add(line)
    RightPanel_RightvBox.AddStretchSpacer()
    RightPanel_RightvBox.AddSpacer(10)


    DebugPanel_DebugView = ui.LogView(MainWindow_DebugPanel,Size=PANEL['DEBUG']['SIZE'])
    DebugPanel_DebugView.SetDateTimeFormat("%Y-%m-%d %H:%M")
    DebugPanel_DebugView.SetTitles({'Urgency':"级别",'DateTime':"时间",'Source':"来源",'Message':"消息"})
    if(PATH_PREFIX):
        DebugPanel_DebugView.Append(ui.ConstDefs.LOGVIEW_URGENCY_INFO,"Main","Boot from: " + PATH_PREFIX)
    DebugPanel_DebugView.Append(ui.ConstDefs.LOGVIEW_URGENCY_INFO,"Main","Test Msg.")
    DebugPanel_DebugView.Append(ui.ConstDefs.LOGVIEW_URGENCY_WARN,"Main","Test Msg.")
    DebugPanel_DebugView.Append(ui.ConstDefs.LOGVIEW_URGENCY_ERRO,"Main","Test Msg.")
    DebugPanel_DebugView.Append(ui.ConstDefs.LOGVIEW_URGENCY_SUCC,"Main","Test Msg.")
    DebugPanel_DebugvBox.Add(DebugPanel_DebugView.Body,1,wx.EXPAND|wx.ALL,15)


    StatusText = wx.StaticText(MainWindow_StatusPanel,wx.ID_ANY,"Ready.")
    StatusText.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,faceName="SimHei"))
    StatusText.SetForegroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['FG']))
    StatusText.Bind(wx.EVT_RIGHT_DCLICK,lambda Event:ToggleWindowSize(MainWindow))
    StatusBar_StatushBox.AddSpacer(10)
    StatusBar_StatushBox.Add(StatusText,1,wx.ALIGN_CENTER,4)

    MainWindow_LeftPanel.Layout()
    MainWindow_RightPanel.Layout()
    MainWindow_DebugPanel.Layout()
    MainWindow_StatusPanel.Layout()
    MainWindow_MainPanel.Layout()

    # 显示主窗口
    MainWindow.Show()
    App.MainLoop()


if __name__ == "__main__":
    WinMain()
