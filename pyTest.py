import wx
import system.libs.NowVideo.NVD_wxUI as ui
import DetailedInfo as D

BASE_WINDOW_SIZE = (900,600)
LEFT_PANEL_WIDTH = 520
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
        'SIZE': (WINDOW['INITIAL_SIZE'][0],STATUS_BAR_HEIGHT)
    },
    'DEBUG': {
        'POS': (WINDOW['INITIAL_SIZE'][0],0),
        'SIZE': (WINDOW['MAX_SIZE'][0]-WINDOW['INITIAL_SIZE'][0],WINDOW['INITIAL_SIZE'][1]-STATUS_BAR_HEIGHT)
    }
}
COLOR = {
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

def WinMain():
    App = wx.App()
    MainWindow = wx.Frame(None,wx.ID_ANY,"Test wxPython App",style=wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)

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
    MainWindow.SetBackgroundColour(wx.Colour("#FFF"))
    MainWindow.Update()

    MainWindow_MainPanel = wx.Panel(MainWindow)
    MainWindow_LeftPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['LEFT']['POS'],PANEL['LEFT']['SIZE'])
    MainWindow_RightPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['RIGHT']['POS'],PANEL['RIGHT']['SIZE'])
    MainWindow_StatusPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['STATUS_BAR']['POS'],PANEL['STATUS_BAR']['SIZE'])
    MainWindow_DebugPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,PANEL['DEBUG']['POS'],PANEL['DEBUG']['SIZE'])
    MainWindow_MainvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_ContenthBox = wx.BoxSizer(wx.HORIZONTAL)
    MainWindow_StatushBox = wx.BoxSizer(wx.HORIZONTAL)
    MainWindow_MainvBox.Add(MainWindow_ContenthBox,0,wx.EXPAND|wx.ALL)
    MainWindow_MainvBox.Add(MainWindow_StatushBox,0,wx.EXPAND|wx.ALL)
    MainWindow_ContenthBox.Add(MainWindow_LeftPanel,0,wx.EXPAND|wx.ALL)
    MainWindow_ContenthBox.Add(MainWindow_RightPanel,0,wx.EXPAND|wx.ALL)
    MainWindow_ContenthBox.Add(MainWindow_DebugPanel,0,wx.EXPAND|wx.ALL)
    MainWindow_StatushBox.Add(MainWindow_StatusPanel,0,wx.EXPAND|wx.ALL)
    MainWindow_LeftvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_RightvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_DebugvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_MainPanel.SetSizer(MainWindow_MainvBox)
    MainWindow_LeftPanel.SetSizer(MainWindow_LeftvBox)
    MainWindow_RightPanel.SetSizer(MainWindow_RightvBox)
    MainWindow_DebugPanel.SetSizer(MainWindow_DebugvBox)
    MainWindow_StatusPanel.SetForegroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['FG']))
    MainWindow_StatusPanel.SetBackgroundColour(wx.Colour(COLOR['STATUS_BAR']['READY']['BG']))

    Text1 = wx.StaticText(MainWindow_LeftPanel,wx.ID_ANY,"Left wxObj Test.")
    MainWindow_LeftvBox.AddSpacer(10)
    MainWindow_LeftvBox.Add(Text1,1)
    MainWindow_LeftvBox.AddStretchSpacer()
    MainWindow_LeftvBox.AddSpacer(10)

    STK1_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(330,60),wx.Colour(64,128,80),wx.Colour(255,255,255),"数据1","品目1","SimHei",16,10)
    STK2_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(200,60),wx.Colour(224,128,128),wx.Colour("#FFF"),"FF-FF-FF-FF-FF-FF","无线网卡MAC地址","SimHei",16,10)
    STK2_2 = ui.Sticker(MainWindow_RightPanel,(0,0),(120,60),wx.Colour(128,128,224),wx.Colour("#FFF"),"PF0DLL3X","设备序列号","SimHei",16,10)

    Stickers = []
    Stickers.append(hBoxLine(STK1_1.Body,Border=5))
    Stickers.append(hBoxLine(STK2_1.Body,STK2_2.Body,Border=5))

    MainWindow_RightvBox.AddSpacer(10)
    for line in Stickers:
        MainWindow_RightvBox.Add(line)
    MainWindow_RightvBox.AddStretchSpacer()
    MainWindow_RightvBox.AddSpacer(10)

    MainWindow_LeftPanel.Layout()
    MainWindow_RightPanel.Layout()
    MainWindow_DebugPanel.Layout()
    MainWindow_MainPanel.Layout()

    # 显示主窗口
    MainWindow.Show()
    App.MainLoop()


if __name__ == "__main__":
    WinMain()
