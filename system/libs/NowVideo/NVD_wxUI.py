#################################################
#   NowVideo AppUI Builder Class & Functions    #
#            by af_xj@hotmail.com               #
#                Rev 20260812A                  #
#            (C) 25' 26' NowVideo               #
#             Default License: GPL              #
#  -------------------------------------------  #
#  This copy of source code was liscensed to    #
#  the Astemo Group with ** READONLY ** use,    #
#  And Astemo can use this copy of source code  #
#  without open it's software's source code.    #
#################################################


import wx
import wx.lib.inspection
import uuid


class uiElements:
    CONTAINER = True
    Collection = None

    class wxObj:
        UUID = None
        Parent = None
        Body = None
        CONTAINER = False

        def __init__(self,Element:wx.Window|None):
            self.UUID = uuid.uuid4()
            if(Element):
                self.SetElement(Element)

        def SetElement(self,Element:wx.Window):
            self.Body = Element

        def SetParent(self,Element:uiElements.wxObjs):
            self.Parent = Element


    # 用于承载元素的聚合，如一个Line或者Bundle中的所有元素
    class wxObjs:
        UUID = None
        Parent = None
        Children = []
        CONTAINER = True

        def __init__(self):
            self.UUID = uuid.uuid4()

        def AppendElement(self,Element:wx.Window|uiElements.wxObjs|uiElements.wxObj):
            if(type(Element) == wx.Window):
                Temp = uiElements.wxObj(Element)
            else:
                Temp = Element
            Temp.SetParent(self)
            self.Children.append(Temp)
            return Temp.UUID
        
        def SetParent(self,Element:uiElements.wxObjs):
            self.Parent = Element

    def __init__(self):
        self.Collection = self.wxObjs()

    # 遍历子对象
    def Fetch(self):
        print("Wait for write")

    # 通过UUID查找对象
    def FindObjByUUID():
        print("Wait for write")

    # 通过类型查找对象
    def FindObjByType() -> list:
        print("Wait for write")

    def FindLabelByText() -> list:
        print("Wait for write")




class Debug:
    def wxDebug():
        wx.lib.inspection.InspectionTool().Show()


class Sticker:
    Element_MainPanel = None
    Element_vBox = None
    Element_MainText = None
    Element_HitsText = None
    Text_MainText = None
    Text_HitsText = None
    Font_Main = None
    Font_Hits = None

#生成仪表盘中的单个含背景色Label
    def __init__(self,ParentPanel:wx.Window,Position:wx.Point,Size:wx.Size,BGColor:wx.Colour,MainText:str|None,HitsText:str|None,FontName:str,MainFontSize:int,HitsFontSize:int,FontColor:wx.Colour):
        if(MainText):
            self.Text_MainText = MainText
        else:
            self.Text_MainText = " "
        if(HitsText):
            self.Text_HitsText = HitsText
        else:
            self.Text_HitsText = " "
        
        self.Element_MainPanel = wx.Panel(ParentPanel,wx.ID_ANY,Position,Size)
        self.Element_MainPanel.SetBackgroundColour(wx.Colour(BGColor))
        
        self.Font_Main = wx.Font(MainFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)
        self.Font_Hits = wx.Font(HitsFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)

        self.Element_MainText = wx.StaticText(self.Element_MainPanel,label=self.Text_MainText)
        self.Element_MainText.SetFont(self.Font_Main)
        self.Element_MainText.SetForegroundColour(FontColor)
        self.Element_MainText.Center()
        self.Element_HitsText = wx.StaticText(self.Element_MainPanel,label=self.Text_HitsText)
        self.Element_HitsText.SetFont(self.Font_Hits)
        self.Element_HitsText.SetForegroundColour(FontColor)
        self.Element_vBox = wx.BoxSizer(wx.VERTICAL)
        self.Element_vBox.AddStretchSpacer(1)
        self.Element_vBox.Add(self.Element_HitsText,0,wx.LEFT|wx.BOTTOM,4)
        self.Element_MainPanel.SetSizer(self.Element_vBox)
        self.Element_MainPanel.Layout()
        self.Element_MainPanel.Update()

    def SetTextColor(self,FontColor:wx.Colour) -> None:
        self.Element_MainText.SetForegroundColour(FontColor)
        self.Element_HintsText.SetForegroundColour(FontColor)

    def SetBGColor(self,BGColor:wx.Colour) -> None:
        self.Element_MainPanel.SetBackgroundColour(wx.Colour(BGColor))

    def SetMainText(self,Text:str) -> None:
        self.Element_MainText.SetLabel(Text)

    def GetMainText(self) -> str:
        return self.Element_MainText.GetLabel()

    def SetHitsText(self,Text:str|None) -> None:
        if(Text):
            self.Element_HitsText.SetLabel(Text)
        else:
            self.Element_HitsText.SetLabel(" ")

    def GetHitsText(self) -> str:
        Text = self.Element_HitsText.GetLabel()
        if(Text == " "):
            return None
        else:
            return self.Element_HitsText.GetLabel()

    def SetText(self,MainText:str,HitsText:str):
        self.SetMainText(MainText)
        self.SetHitsText(HitsText)

    def Move(self,Pos:wx.Point) -> None:
        self.Element_MainPanel.SetPosition(Pos)

    def Scale(self,Size:wx.Size) -> None:
        self.Element_MainPanel.SetSize(Size)

    def GetSize(self) -> wx.Size:
        return self.Element_MainPanel.GetSize()


class AboutDialog:
    Element_AboutDialog = None
    Element_MainPanel = None
    Container_MainvBox = None
    Container_NamehBox = None
    Container_SubtitlehBox = None
    Container_VersionhBox = None
    Container_CopyrighthBox = None
    Container_DetailhBox = None
    Container_DetailTextvBox = None
    Container_ButtonhBox = None
    Element_ProductName = None
    Element_ProductSubtitle = None
    Element_ProductVersion = None
    Element_ProductCopyright = None
    Element_ProductDetailContainer = None
    Element_ProductDetail = None
    Element_ButtonOK = None
    LOGO_MAX_WIDTH = 256
    LOGO_MAX_HEIGHT = 80
    BOX_SIZER_MARGIN_STEPPING = 5
    # 若最终显示的TextCtrl高度过大或过小，调整此值
    DETAIL_HEIGHT_OFFSET = -60
    
    def __init__(self,Parent:wx.Window,Title:str,LogoPath:str|None,LogoScale:float|None,ProductName:str,ProductSubtitle:str,ProductVersion:str,ProductCopyright:str,ProductDetail:str,Size:wx.Size):
        UsedHeight = 0
        self.Element_AboutDialog = wx.Dialog(Parent,wx.ID_ANY,Title,size=Size)
        self.Element_MainPanel = wx.Panel(self.Element_AboutDialog,wx.ID_ANY)
        self.Container_MainvBox = wx.BoxSizer(wx.VERTICAL)
        self.Container_NamehBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_SubtitlehBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_VersionhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_CopyrighthBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_DetailhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_DetailTextvBox = wx.BoxSizer(wx.VERTICAL)
        self.Container_ButtonhBox = wx.BoxSizer(wx.HORIZONTAL)
        self.Container_MainvBox.AddStretchSpacer(self.BOX_SIZER_MARGIN_STEPPING * 2)
        self.Container_MainvBox.Add(self.Container_NamehBox,2,wx.ALIGN_CENTER)
        self.Container_MainvBox.AddStretchSpacer(self.BOX_SIZER_MARGIN_STEPPING * 2)
        self.Container_MainvBox.Add(self.Container_SubtitlehBox,1,wx.ALIGN_CENTER)
        self.Container_MainvBox.Add(self.Container_VersionhBox,1,wx.ALIGN_CENTER)
        self.Container_MainvBox.Add(self.Container_CopyrighthBox,1,wx.ALIGN_CENTER)
        self.Container_MainvBox.AddStretchSpacer(self.BOX_SIZER_MARGIN_STEPPING)
        self.Container_MainvBox.Add(self.Container_DetailhBox,4,wx.ALIGN_CENTER)
        self.Container_MainvBox.AddStretchSpacer(self.BOX_SIZER_MARGIN_STEPPING)
        self.Container_MainvBox.Add(self.Container_ButtonhBox,1,wx.ALIGN_CENTER)
        self.Container_MainvBox.AddStretchSpacer(self.BOX_SIZER_MARGIN_STEPPING * 2)

        self.Element_ProductName = wx.StaticText(self.Element_MainPanel,wx.ID_ANY,ProductName)
        self.Element_ProductSubtitle = wx.StaticText(self.Element_MainPanel,wx.ID_ANY,ProductSubtitle)
        self.Element_ProductVersion = wx.StaticText(self.Element_MainPanel,wx.ID_ANY,ProductVersion)
        self.Element_ProductCopyright = wx.StaticText(self.Element_MainPanel,wx.ID_ANY,ProductCopyright)
        self.Element_ProductDetailContainer = wx.Panel(self.Element_MainPanel,wx.ID_ANY)
        self.Element_ProductDetail = wx.TextCtrl(self.Element_ProductDetailContainer,wx.ID_ANY,ProductDetail,style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE)
        #self.Element_ProductDetailContainer = wx.Panel(self.Element_MainPanel,wx.ID_ANY,size=(int(Size[0]-62),int(Size[0]/2)+2))
        #self.Element_ProductDetail = wx.TextCtrl(self.Element_ProductDetailContainer,wx.ID_ANY,ProductDetail,pos=(1,1),size=(int(Size[0]-64),int(Size[0]/2)),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE)
        self.Element_ButtonOK = wx.Button(self.Element_MainPanel,wx.ID_ANY,"&OK")

        self.Element_ProductName.SetForegroundColour("#880000")
        self.Element_ProductName.SetFont(wx.Font(24,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.Element_ProductSubtitle.SetForegroundColour("#555555")
        self.Element_ProductSubtitle.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.Element_ProductVersion.SetForegroundColour("#555555")
        self.Element_ProductVersion.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.Element_ProductCopyright.SetForegroundColour("#555555")
        self.Element_ProductCopyright.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,False,"SimHei",wx.FONTENCODING_DEFAULT))
        self.Element_ProductDetailContainer.SetBackgroundColour("#2FB6FF")
        self.Element_ProductDetail.SetBackgroundColour(self.Element_MainPanel.GetBackgroundColour())

        # 先取得产品名称控件的最终高度
        UsedHeight = self.Element_ProductName.GetBestSize().GetHeight()

        # 如果调用时指定了要显示Logo
        if(LogoPath):
            try:
                ScaleRatio = 1
                self.LogoImage = wx.Image()
                self.LogoImage.LoadFile(LogoPath,wx.BITMAP_TYPE_PNG)
                # 判断图像加载是否成功
                if(self.LogoImage.IsOk()):
                    # 若调用时定义了预缩放比例，则先执行一次缩放
                    if(LogoScale):
                        self.LogoImage = self.LogoImage.Scale(int(self.LogoImage.Width*LogoScale),int(self.LogoImage.Height*LogoScale),wx.IMAGE_QUALITY_HIGH)
                    # 判断Logo的高度或宽度是否超出了限制大小
                    if(((self.LogoImage.Width / self.LOGO_MAX_WIDTH) > 1) or ((self.LogoImage.Height / self.LOGO_MAX_HEIGHT) > 1)):
                        # 判断宽度和高度超出限制的比例，若宽度超出更多则通过宽度计算缩放比例，若高度超过更多则通过高度计算错放比例
                        if((self.LogoImage.GetSize().GetWidth() / self.LOGO_MAX_WIDTH) > (self.LogoImage.GetSize().GetHeight() / self.LOGO_MAX_HEIGHT)):
                            ScaleRatio = self.LOGO_MAX_WIDTH / self.LogoImage.Width
                        else:
                            ScaleRatio = self.LOGO_MAX_HEIGHT / self.LogoImage.Height
                    self.LogoImage = self.LogoImage.Scale(int(self.LogoImage.Width*ScaleRatio),int(self.LogoImage.Height*ScaleRatio),wx.IMAGE_QUALITY_HIGH)
                    self.Logo = wx.StaticBitmap(self.Element_MainPanel,wx.ID_ANY,self.LogoImage)
                    self.Container_NamehBox.Add(self.Logo,3,wx.ALIGN_CENTER)
                    # 将Logo高度与产品名称控件的高度做比较，取最大值 (UsedHeight=LogoImage.Height>UsedHeight?LogoImage.Height:UsedHeight)
                    if(self.LogoImage.Height > UsedHeight):
                        UsedHeight = self.LogoImage.Height
            except BaseException as e:
                print("Error: [AboutDialog][LoadImage]: " + str(e))

        # 计算TextCtrl以外控件的高度总和，若直接从BoxSizer取会得到错误的高度
        UsedHeight = UsedHeight + \
            self.Element_ProductSubtitle.GetSize().GetHeight() + \
            self.Element_ProductVersion.GetSize().GetHeight() + \
            self.Element_ProductCopyright.GetSize().GetHeight() + \
            self.Element_ButtonOK.GetSize().GetHeight()

        # 使用带底色的Panel作为TextCtrl的底色，保留四边1个像素来绘制TextCtrl的边框
        self.Container_DetailTextvBox.Add(self.Element_ProductDetail,1,wx.EXPAND|wx.ALL,1)
        # 如果不使用BoxSizer来布局TextCtrl，会导致Panel尺寸改变后TextCtrl无法增加尺寸
        self.Element_ProductDetailContainer.SetSizer(self.Container_DetailTextvBox)
        self.Element_ProductDetailContainer.SetMinSize((int(Size[0]-64),Size[1] - UsedHeight - 50 + self.DETAIL_HEIGHT_OFFSET))
        self.Element_ProductDetail.SetMinSize((int(Size[0]-64),Size[1] - UsedHeight - 52 + self.DETAIL_HEIGHT_OFFSET))

        self.Container_NamehBox.Add(self.Element_ProductName,2,wx.ALIGN_CENTER)
        self.Container_SubtitlehBox.Add(self.Element_ProductSubtitle,1)
        self.Container_VersionhBox.Add(self.Element_ProductVersion,1)
        self.Container_CopyrighthBox.Add(self.Element_ProductCopyright,1)
        self.Container_DetailhBox.Add(self.Element_ProductDetailContainer,1)
        self.Container_ButtonhBox.Add(self.Element_ButtonOK,1)
            
        self.Element_ButtonOK.Bind(wx.EVT_BUTTON,self.OnClose)

        self.Element_AboutDialog.Center()
        self.Element_MainPanel.SetSizer(self.Container_MainvBox)
        self.Element_MainPanel.Layout()
        self.Element_MainPanel.Update()

    def Show(self) -> None:
        self.Element_AboutDialog.ShowModal()

    def OnClose(self,Event) -> None:
        # OSX下直接Destory会卡死
        if(wx.Platform == '__WXMAC__'):
            self.Element_AboutDialog.EndModal(0)
        self.Element_AboutDialog.Destroy()


# 一个带标题栏的垂直滚动列表控件，每列一个控件
class ListView:
    
    Lines = []

    def __init__(self):
        # 先占位，等待后续编写 TBW
        print("It's Run")

    def AddLine(self,Elements:uiElements):
        # 先占位，等待后续编写 TBW
        print("It's Run")
