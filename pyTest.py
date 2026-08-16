import wx
import system.libs.NowVideo.NVD_wxUI as ui
import DetailedInfo as D

def hBoxLine(wxObj1:wx.Window,wxObj2:wx.Window,Border:int|None=None):
    hBox = wx.BoxSizer(wx.HORIZONTAL)
    if(Border):
        FinalBroder = Border
    else:
        FinalBroder = 0
    hBox.Add(wxObj1,1,wx.EXPAND|wx.ALL,FinalBroder)
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
    MainWindow = wx.Frame(None,wx.ID_ANY,"Test wxPython App",size=(900,600),style=wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)
    MainWindow.SetMinSize((900,600))
    MainWindow.SetMaxSize((1200,600))

    MainMenu = wx.MenuBar()
    FileMenu = wx.Menu()
    HelpMenu = wx.Menu()
    MainMenu.Append(FileMenu,"&File")
    MainMenu.Append(HelpMenu,"&Help")
    FileMenu_Exit = FileMenu.Append(wx.ID_EXIT,"&Exit")
    HelpMenu_wxDebug = HelpMenu.Append(9051,"wxDebug")
    HelpMenu_About = HelpMenu.Append(wx.ID_ABOUT,"&About")
    MainWindow.SetMenuBar(MainMenu)
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickExit(),FileMenu_Exit)
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickAbout(MainWindow),HelpMenu_About)
    MainWindow.Bind(wx.EVT_MENU,lambda Event:OnClickWxDebug(),HelpMenu_wxDebug)


    # 设置主窗口位置和底色
    MainWindow.Center()
    MainWindow.SetBackgroundColour(wx.Colour("#FFF"))
    MainWindow.Update()

    MainWindow_MainPanel = wx.Panel(MainWindow)
    MainWindow_LeftPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,(0,0),(500,MainWindow.GetSize().GetHeight()))
    MainWindow_RightPanel = wx.Panel(MainWindow_MainPanel,wx.ID_ANY,(500,1),(400,MainWindow.GetSize().GetHeight()))
    MainWindow_LeftvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_RightvBox = wx.BoxSizer(wx.VERTICAL)
    MainWindow_LeftPanel.SetSizer(MainWindow_LeftvBox)
    MainWindow_RightPanel.SetSizer(MainWindow_RightvBox)
    #MainWindow_LeftPanel.Layout()
    #MainWindow_RightPanel.Layout()

    text1 = wx.StaticText(MainWindow_LeftPanel,wx.ID_ANY,"test")
    MainWindow_LeftvBox.Add(text1,1)
    STK1_1 = ui.Sticker(MainWindow_RightPanel,(0,0),(220,60),wx.Colour(224,128,128),wx.Colour("#FFF"),"FF-FF-FF-FF-FF-FF","无线网卡MAC地址","SimHei",16,10)
    STK1_2 = ui.Sticker(MainWindow_RightPanel,(0,0),(140,60),wx.Colour(128,128,224),wx.Colour("#FFF"),"PF0DLL3X","设备序列号","SimHei",16,10)
    STK1_hBox = hBoxLine(STK1_1.Body,STK1_2.Body,4)

    MainWindow_RightvBox.AddSpacer(10)
    MainWindow_RightvBox.Add(STK1_hBox)

    MainWindow_RightPanel.Layout()

    # 显示主窗口
    MainWindow.Show()
    App.MainLoop()


if __name__ == "__main__":
    WinMain()
