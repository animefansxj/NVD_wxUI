#################################################
#   NowVideo AppUI Builder Class & Functions    #
#            by af_xj@hotmail.com               #
#                Rev 20260731B                  #
#            (C) 25' 26' NowVideo               #
#             Default License: GPL              #
#  -------------------------------------------  #
#  This copy of source code was liscensed to    #
#  the Astemo Group with ** READONLY ** use,    #
#  And Astemo can use this copy of source code  #
#  without open it's software's source code.    #
#################################################


import wx

class AddSticker:
    Bundle_MainPanel = None
    Bundle_vBox = None
    Bundle_MainText = None
    Bundle_HitsText = None
    Font_Main = None
    Font_Hits = None

#生成仪表盘中的单个含背景色Label
    def __init__(self,ParentPanel:wx.Window,Position:wx.Point,Size:wx.Size,BGColor:wx.Colour,MainText:str,HitsText:str,FontName:str,MainFontSize:int,HitsFontSize:int,FontColor:wx.Colour):
        
        self.Bundle_MainPanel = wx.Panel(ParentPanel,wx.ID_ANY,Position,Size)
        self.Bundle_MainPanel.SetBackgroundColour(wx.Colour(BGColor))
        
        self.Font_Main = wx.Font(MainFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)
        self.Font_Hits = wx.Font(HitsFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)

        self.Bundle_MainText = wx.StaticText(self.Bundle_MainPanel,label=MainText)
        self.Bundle_MainText.SetFont(self.Font_Main)
        self.Bundle_MainText.SetForegroundColour(FontColor)
        self.Bundle_MainText.Center()
        self.Bundle_HitsText = wx.StaticText(self.Bundle_MainPanel,label=HitsText)
        self.Bundle_HitsText.SetFont(self.Font_Hits)
        self.Bundle_HitsText.SetForegroundColour(FontColor)
        self.Bundle_vBox = wx.BoxSizer(wx.VERTICAL)
        self.Bundle_vBox.AddStretchSpacer(1)
        self.Bundle_vBox.Add(self.Bundle_HitsText,0,wx.LEFT|wx.BOTTOM,4)
        self.Bundle_MainPanel.SetSizer(self.Bundle_vBox)
        self.Bundle_MainPanel.Layout()
        self.Bundle_MainPanel.Update()

    def SetTextColor(self,FontColor:wx.Colour) -> None:
        self.Bundle_MainText.SetForegroundColour(FontColor)
        self.Bundle_HintsText.SetForegroundColour(FontColor)

    def SetBGColor(self,BGColor:wx.Colour) -> None:
        self.Bundle_MainPanel.SetBackgroundColour(wx.Colour(BGColor))

    def SetMainText(self,Text:str) -> None:
        self.Bundle_MainText.SetLabel(Text)

    def GetMainText(self) -> str:
        return self.Bundle_MainText.GetLabel()

    def SetHitsText(self,Text:str|None) -> None:
        if(Text):
            self.Bundle_HitsText.SetLabel(Text)
        else:
            self.Bundle_HitsText.SetLabel(" ")

    def GetHitsText(self) -> str:
        Text = self.Bundle_HitsText.GetLabel()
        if(Text == " "):
            return None
        else:
            return self.Bundle_HitsText.GetLabel()

    def SetText(self,MainText:str,HitsText:str):
        self.SetMainText(MainText)
        self.SetHitsText(HitsText)

    def Move(self,Pos:wx.Point) -> None:
        self.Bundle_MainPanel.SetPosition(Pos)

    def Scale(self,Size:wx.Size) -> None:
        self.Bundle_MainPanel.SetSize(Size)

    def GetSize(self) -> wx.Size:
        return self.Bundle_MainPanel.GetSize()


class AboutDialog:
    AboutDialog = None
    MainPanel = None
    MainvBox = None
    NamehBox = None
    SubtitlehBox = None
    VersionhBox = None
    CopyrighthBox = None
    DetailhBox = None
    DetailTextvBox = None
    ButtonhBox = None
    ProductName = None
    ProductSubtitle = None
    ProductVersion = None
    ProductCopyright = None
    ProductDetail = None
    ButtonOK = None
    LOGO_MAX_WIDTH = 256
    LOGO_MAX_HEIGHT = 80
    
    def __init__(self,Parent:wx.Window,Title:str,LogoPath:str|None,LogoScale:float|None,ProductName:str,ProductSubtitle:str,ProductVersion:str,ProductCopyright:str,ProductDetail:str,Size:wx.Size):
        UsedHeight = 0
        self.AboutDialog = wx.Dialog(Parent,wx.ID_ANY,Title,size=Size)
        self.MainPanel = wx.Panel(self.AboutDialog,wx.ID_ANY)
        self.MainvBox = wx.BoxSizer(wx.VERTICAL)
        self.NamehBox = wx.BoxSizer(wx.HORIZONTAL)
        self.SubtitlehBox = wx.BoxSizer(wx.HORIZONTAL)
        self.VersionhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.CopyrighthBox = wx.BoxSizer(wx.HORIZONTAL)
        self.DetailhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.DetailTextvBox = wx.BoxSizer(wx.VERTICAL)
        self.ButtonhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.MainvBox.AddStretchSpacer(10)
        self.MainvBox.Add(self.NamehBox,2,wx.ALIGN_CENTER)
        self.MainvBox.AddStretchSpacer(10)
        self.MainvBox.Add(self.SubtitlehBox,1,wx.ALIGN_CENTER)
        self.MainvBox.Add(self.VersionhBox,1,wx.ALIGN_CENTER)
        self.MainvBox.Add(self.CopyrighthBox,1,wx.ALIGN_CENTER)
        self.MainvBox.AddStretchSpacer(5)
        self.MainvBox.Add(self.DetailhBox,4,wx.ALIGN_CENTER)
        self.MainvBox.AddStretchSpacer(5)
        self.MainvBox.Add(self.ButtonhBox,1,wx.ALIGN_CENTER)
        self.MainvBox.AddStretchSpacer(10)

        self.ProductName = wx.StaticText(self.MainPanel,wx.ID_ANY,ProductName)
        self.ProductSubtitle = wx.StaticText(self.MainPanel,wx.ID_ANY,ProductSubtitle)
        self.ProductVersion = wx.StaticText(self.MainPanel,wx.ID_ANY,ProductVersion)
        self.ProductCopyright = wx.StaticText(self.MainPanel,wx.ID_ANY,ProductCopyright)
        self.ProductDetailContainer = wx.Panel(self.MainPanel,wx.ID_ANY)
        self.ProductDetail = wx.TextCtrl(self.ProductDetailContainer,wx.ID_ANY,ProductDetail,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE)
        #self.ProductDetailContainer = wx.Panel(self.MainPanel,wx.ID_ANY,size=(int(Size[0]-62),int(Size[0]/2)+2))
        #self.ProductDetail = wx.TextCtrl(self.ProductDetailContainer,wx.ID_ANY,ProductDetail,pos=(1,1),size=(int(Size[0]-64),int(Size[0]/2)),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE)
        self.ButtonOK = wx.Button(self.MainPanel,wx.ID_ANY,"&OK")

        self.ProductName.SetForegroundColour("#880000")
        self.ProductName.SetFont(wx.Font(24,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.ProductSubtitle.SetForegroundColour("#555555")
        self.ProductSubtitle.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.ProductVersion.SetForegroundColour("#555555")
        self.ProductVersion.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.ProductCopyright.SetForegroundColour("#555555")
        self.ProductCopyright.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.ProductDetailContainer.SetBackgroundColour("#2FB6FF")
        self.ProductDetail.SetBackgroundColour(self.MainPanel.GetBackgroundColour())

        UsedHeight = self.ProductName.GetBestSize().GetHeight()

        if(LogoPath):
            try:
                ScaleRatio = 1
                self.LogoImage = wx.Image()
                self.LogoImage.LoadFile(LogoPath,wx.BITMAP_TYPE_PNG)
                if(LogoScale):
                    self.LogoImage = self.LogoImage.Scale(int(self.LogoImage.Width*LogoScale),int(self.LogoImage.Height*LogoScale),wx.IMAGE_QUALITY_HIGH)
                if(((self.LogoImage.Width / self.LOGO_MAX_WIDTH) >1) or ((self.LogoImage.Height / self.LOGO_MAX_HEIGHT) >1)):
                    if((self.LogoImage.GetSize().GetWidth() / self.LOGO_MAX_WIDTH) > (self.LogoImage.GetSize().GetHeight() / self.LOGO_MAX_HEIGHT)):
                        ScaleRatio = self.LOGO_MAX_WIDTH / self.LogoImage.Width
                    else:
                        ScaleRatio = self.LOGO_MAX_HEIGHT / self.LogoImage.Height
                self.LogoImage = self.LogoImage.Scale(int(self.LogoImage.Width*ScaleRatio),int(self.LogoImage.Height*ScaleRatio),wx.IMAGE_QUALITY_HIGH)
                self.Logo = wx.StaticBitmap(self.MainPanel,wx.ID_ANY,self.LogoImage)
                self.NamehBox.Add(self.Logo,3,wx.ALIGN_CENTER)
                if(self.Logo.GetSize().GetHeight > UsedHeight):
                    UsedHeight = self.Logo.GetSize().GetHeight
            except:
                print("Unable to load logo.")

        UsedHeight = UsedHeight + \
            self.ProductSubtitle.GetSize().GetHeight() + \
            self.ProductVersion.GetSize().GetHeight() + \
            self.ProductCopyright.GetSize().GetHeight() + \
            self.ButtonOK.GetSize().GetHeight() + \
            120

        self.DetailTextvBox.Add(self.ProductDetail,1,wx.EXPAND|wx.ALL,1)
        self.ProductDetailContainer.SetSizer(self.DetailTextvBox)
        self.ProductDetailContainer.SetMinSize((int(Size[0]-64),Size[1] - UsedHeight - 10))
        self.ProductDetail.SetMinSize((int(Size[0]-64),Size[1] - UsedHeight - 12))

        self.NamehBox.Add(self.ProductName,2,wx.ALIGN_CENTER)
        self.SubtitlehBox.Add(self.ProductSubtitle,1)
        self.VersionhBox.Add(self.ProductVersion,1)
        self.CopyrighthBox.Add(self.ProductCopyright,1)
        self.DetailhBox.Add(self.ProductDetailContainer,1)
        self.ButtonhBox.Add(self.ButtonOK,1)
            
        self.ButtonOK.Bind(wx.EVT_BUTTON,self.OnClose)

        self.AboutDialog.Center()
        self.MainPanel.SetSizer(self.MainvBox)
        self.MainPanel.Layout()
        self.MainPanel.Update()

    def Show(self) -> None:
        self.AboutDialog.ShowModal()

    def OnClose(self,Event) -> None:
        # OSX下直接Destory会卡死
        if(wx.Platform == '__WXMAC__'):
            self.AboutDialog.EndModal(0)
        self.AboutDialog.Destroy()
    