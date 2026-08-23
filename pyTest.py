import wx
import wx.dataview
import sys
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

########## Event Handlers ##########
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

def ChangeWindowSize(Parent:wx.Window):
    if(Parent.GetClientSize()[0] != WINDOW['MAX_SIZE'][0]):
        Parent.SetClientSize(WINDOW['MAX_SIZE'])
    else:
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
    MainWindow_StatusPanel.Bind(wx.EVT_RIGHT_DCLICK,lambda Event:ChangeWindowSize(MainWindow))

    '''
    TableView = wx.dataview.DataViewListCtrl(MainWindow_LeftPanel,size=PANEL['LEFT']['SIZE'],style=wx.dataview.DV_ROW_LINES)
    TableView.AppendColumn(wx.dataview.DataViewColumn("UUID",wx.dataview.DataViewTextRenderer(),0))
    TableView.AppendColumn(wx.dataview.DataViewColumn("Enabled",wx.dataview.DataViewToggleRenderer(mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE),1,width=60))
    TableView.AppendColumn(wx.dataview.DataViewColumn("Name",wx.dataview.DataViewTextRenderer(),2,width=160))
    TableView.AppendColumn(wx.dataview.DataViewColumn("Progress",wx.dataview.DataViewProgressRenderer(),3,width=80))
    TableView.AppendColumn(wx.dataview.DataViewColumn("Status",wx.dataview.DataViewTextRenderer(),4))
    TableView.GetColumn(0).SetHidden(True)
    TableView.AppendItem(["",True,"Name1",60,"Status1"])
    '''
    TableView = ui.ListView(MainWindow_LeftPanel,Size=PANEL['LEFT']['SIZE'])
    TableView.SetCols("Enabled:toggle:60|Name:text:160|Progress:progress:80|Status:text")
    TableView.AppendRow([True,"Name1",60,"60"],"Row1")
    LeftPanel_LeftvBox.AddSpacer(10)
    LeftPanel_LeftvBox.Add(TableView.Body,1,wx.EXPAND|wx.ALL,15)
    LeftPanel_LeftvBox.AddStretchSpacer()
    LeftPanel_LeftvBox.AddSpacer(10)

    STK1_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(330,60),wx.Colour(64,128,80),wx.Colour(255,255,255),"数据1","品目1","SimHei",16,10)
    STK2_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(200,60),wx.Colour(224,128,128),wx.Colour("#FFF"),"FF-FF-FF-FF-FF-FF","无线网卡MAC地址","SimHei",16,10)
    STK2_2 = ui.Sticker(MainWindow_RightPanel,(0,0),(120,60),wx.Colour(128,128,224),wx.Colour("#FFF"),"PF0DLL3X","设备序列号","SimHei",16,10)

    Stickers = []
    Stickers.append(hBoxLine(STK1_1.Body,Border=5))
    Stickers.append(hBoxLine(STK2_1.Body,STK2_2.Body,Border=5))

    RightPanel_RightvBox.AddSpacer(10)
    for line in Stickers:
        RightPanel_RightvBox.Add(line)
    RightPanel_RightvBox.AddStretchSpacer()
    RightPanel_RightvBox.AddSpacer(10)

    StatusText = wx.StaticText(MainWindow_StatusPanel,wx.ID_ANY,"Ready.")
    StatusText.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,faceName="SimHei"))
    StatusText.SetForegroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['FG']))
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
