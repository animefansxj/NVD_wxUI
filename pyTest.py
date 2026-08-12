import wx
import system.libs.NowVideo.NVD_wxUI as ui
import DetailedInfo as D

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
    MainWindow = wx.Frame(None,wx.ID_ANY,"Test wxPython App (ASTMPD)",size=(800,600),style=wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)
    MainWindow.SetMinSize((800,600))
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

    ui.Sticker(MainWindow_MainPanel,(410,16),(224,64),wx.Colour(224,128,128),"FF-FF-FF-FF-FF-FF","无线网卡MAC地址","SimHei",16,10,wx.Colour("#FFF"))
    ui.Sticker(MainWindow_MainPanel,(640,16),(128,64),wx.Colour(128,128,224),"PF0DLL3X","设备序列号","SimHei",16,10,wx.Colour("#FFF"))

    # 显示主窗口
    MainWindow.Show()
    App.MainLoop()


if __name__ == "__main__":
    WinMain()
