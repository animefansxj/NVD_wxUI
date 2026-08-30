#################################################
#   NowVideo AppUI Builder Class & Functions    #
#            by af_xj@hotmail.com               #
#                Rev 20260830A                  #
#            (C) 25' 26' NowVideo               #
#             Default License: GPL              #
#  -------------------------------------------  #
#  This copy of source code was liscensed to    #
#  the Astemo Group with ** READONLY ** use,    #
#  And Astemo can use this copy of source code  #
#  without open it's software's source code.    #
#################################################


import wx
import wx.dataview
import wx.lib.inspection
import uuid
import datetime
import pyperclip
from typing import Any
from enum import Enum

DATETIMEFORMAT = "%Y-%m-%d %H:%M:%S"
COLOR = {
    'LOG': {
        'INFO': {
            'BG': "#FFFFFF",
            'FG': "#0055C5"
        },
        'WARN': {
            'BG': "#FFFFFF",
            'FG': "#BE9200"
        },
        'ERRO': {
            'BG': "#FFFFFF",
            'FG': "#C90043"
        },
        'SUCC': {
            'BG': "#FFFFFF",
            'FG': "#00B45A"
        }
    }
}

class ConstDefs(Enum):
    # CtrlID
    #  03 -- ListView
    # SubID
    #  (ListView) 1 -- Col
    #  (LogView)  1 -- Urgency
    LISTVIEW_COL_TYPE_TEXT = 0x0311
    LISTVIEW_COL_TYPE_TOGGLE = 0x0312
    LISTVIEW_COL_TYPE_PROGRESS = 0x0313
    LOGVIEW_URGENCY_INFO = 0x0411
    LOGVIEW_URGENCY_WARN = 0x0412
    LOGVIEW_URGENCY_ERRO = 0x0413
    LOGVIEW_URGENCY_SUCC = 0x0414


########## 暂时不用的代码 ########
'''
class uiElements:
    CONTAINER = True
    Collection = None

    class wxObj:
        UUID = None
        Parent = None
        Body = None
        CONTAINER = False

        def __init__(self,Element:wx.Window|None=None):
            self.UUID = uuid.uuid4()
            if(Element):
                self.SetElement(Element)

        def SetElement(self,Element:wx.Window):
            self.Body = Element

        def SetParent(self,Element:uiElements.wxObjs):
            self.Parent = Element


    # 用于承载元素的聚合, 如一个Line或者Bundle中的所有元素
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
'''

#############################################
#############################################
#############################################
class ListView:
    #class Cell:
    #    Name: str|None
    #    Value: int|bool|str
    #
    #    def __init__(self,CellName:str|None,CellValue:int|bool|str):
    #        self.Name = CellName
    #        self.Value = CellValue

    class Col:
        UUID: uuid.UUID
        Index: int
        Name: str
        Type: int
        Width: int|None

        def __init__(self,Parent:wx.dataview.DataViewListCtrl,ColIndex:int,ColName:str,ColType:int,ColWidth:int|None=None):
            self.UUID = uuid.uuid4()
            self.Index = ColIndex
            self.Name = ColName
            self.Type = ColType
            if(ColWidth):
                self.Width = ColWidth
            else:
                self.Width = wx.dataview.DVC_DEFAULT_WIDTH

            match ColType:
                case ConstDefs.LISTVIEW_COL_TYPE_TEXT:
                    Parent.AppendColumn(wx.dataview.DataViewColumn(self.Name,wx.dataview.DataViewTextRenderer(),ColIndex,self.Width))
                case ConstDefs.LISTVIEW_COL_TYPE_TOGGLE:
                    Parent.AppendColumn(wx.dataview.DataViewColumn(self.Name,wx.dataview.DataViewToggleRenderer(mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE),ColIndex,self.Width))
                case ConstDefs.LISTVIEW_COL_TYPE_PROGRESS:
                    Parent.AppendColumn(wx.dataview.DataViewColumn(self.Name,wx.dataview.DataViewProgressRenderer(),ColIndex,self.Width))  

    class Row:
        Parent: wx.dataview.DataViewListCtrl
        UUID: uuid.UUID
        Index: int
        Name: str|None
        Cells: list

        def __init__(self,Parent:wx.dataview.DataViewListCtrl,RowIndex:int,RowValues:list,RowName:str|None=None):
            self.Parent = Parent
            self.UUID = uuid.uuid4()
            self.Name = RowName
            self.Cells = RowValues
            # 判断 RowIndex 的合法性
            if((RowIndex >=0) and (RowIndex <= self.Parent.GetItemCount())):
                self.Index = RowIndex
            else:
                self.Index = self.Parent.GetItemCount()

        def Append(self):
            self.Index = self.Parent.GetItemCount()
            self.Parent.AppendItem(self.Cells)

        def SetCell(self,ColIndex:int,Value) -> bool:
            if(ColIndex >= 0 and ColIndex < len(self.Cells)):
                self.Cells[ColIndex] = Value
                self.Parent.SetValue(Value,self.Index,ColIndex)
                return True
            return False

        def IsValueMatched(self,ColIndex:int,Value) -> bool:
            if(ColIndex >= 0 and ColIndex < len(self.Cells)):
                if(self.Cells[ColIndex] == Value):
                    return True
            return False

    
    Cols: list[Col]
    Rows: list[Row]
    # this: last appended of modified row and col index [rowIndex,colIndex]
    this: list[int,int]
    Body: wx.dataview.DataViewListCtrl

    def __init__(self,Parent:wx.Window,Position:wx.Point=wx.DefaultPosition,Size:wx.Size=wx.DefaultSize):
        self.Body = wx.dataview.DataViewListCtrl(Parent,size=Size,style=wx.dataview.DV_ROW_LINES)
        self.Cols = []
        self.Rows = []
        self.this = [0,0]

    def AppendCol(self,Header:str):
        ParamList = Header.split(':')
        ParamCount = len(ParamList)
        # 每列至少有 ColName 及 ColType 两个列参数,Width为可选参数
        if(ParamCount >= 2):
            ColName = ParamList[0]
            ColType = ParamList[1]
            ColWidth = None

            match ColType:
                case "text":
                    ColType = ConstDefs.LISTVIEW_COL_TYPE_TEXT
                case "toggle":
                    ColType = ConstDefs.LISTVIEW_COL_TYPE_TOGGLE
                case "progress":
                    ColType = ConstDefs.LISTVIEW_COL_TYPE_PROGRESS
                case _:
                    ColType = None
                    print("[X] List::AppendCol: \"" + Header + "\" ColType Err,Skiped.")

            # 如果存在第三个列参数
            if(ParamCount > 2):
                if(ParamList[2].isdecimal()):
                    ColWidth = int(ParamList[2])

            # 全部通过检查后创建列并将其加入数组
            if(ColType):
                self.Cols.append(self.Col(self.Body,len(self.Cols),ColName,ColType,ColWidth))
        else:
            print("[X] List::AppendCol: \"" + Header + "\" Params not enough,Skiped.")

    def SetCols(self,Headers:str):
        # Exsample: "ColName:Type:Width|ColName:Type:Width|ColName:Type:Width"
        # 按|分割列
        for i in Headers.split('|'):
            self.AppendCol(i)

    def AppendRow(self,RowValues:list,RowName:str|None=None):
        self.Rows.append(self.Row(self.Body,len(self.Rows),RowValues,RowName))
        self.this = [len(self.Rows)-1,0]
        self.Rows[self.this[0]].Append()

    def GetCurrentCoordinates(self) -> tuple:
        return tuple(self.this)

    def GetColUUIDs(self) -> list:
        ColUUIDs = []
        for i in self.Cols:
            ColUUIDs.append(i.UUID)
        return ColUUIDs

    def GetColIndexByUUID(self,ColUUID:uuid.UUID) -> int:
        for i in self.Cols:
            if(i.UUID == ColUUID):
                return i.Index
        return -1

    def GetColIndexByName(self,ColName:str) -> int:
        ColIndexList = []
        for i in self.Cols:
            if(i.Name == ColName):
                ColIndexList.append(i.Index)
        return ColIndexList

    def GetRowIndexByUUID(self,RowUUID:uuid.UUID) -> int:
        for i in self.Rows:
            if(i.UUID == RowUUID):
                return i.Index
        return -1

    def GetRowIndexByName(self,RowName:str) -> list:
        RowIndexList = []
        for i in self.Rows:
            if(i.Name == RowName):
                RowIndexList.append(i.Index)
        return RowIndexList

    def GetRowIndexByValue(self,CellValue,ColIndex:int=0) -> list:
        RowIndexList = []
        for i in range(len(self.Rows)):
            if self.Rows[i].IsValueMatched(ColIndex,CellValue):
                RowIndexList.append(i)
        return RowIndexList

    def SetValueByIndex(self,CellValue,RowIndex:int=-1,ColIndex:int=0) -> bool:
        # 检查参数有效性
        if((RowIndex >= 0) and (RowIndex < len(self.Rows))):
            if(self.Rows[RowIndex].SetCell(ColIndex,CellValue)):
                self.this = [RowIndex,ColIndex]
                return True
        return False

    def SetValueByUUID(self,CellValue,RowUUID:uuid.UUID,ColUUID:uuid.UUID) -> bool:
        RowIndex = self.GetRowIndexByUUID(RowUUID)
        ColIndex = self.GetColIndexByUUID(ColUUID)
        # 如果能够找到UUID对应的行和列
        if((RowIndex >= 0) and (ColIndex >= 0)):
            return self.SetValueByIndex(CellValue,RowIndex,ColIndex)
        return False


class LogView:

    class Row:
        Parent: wx.ListCtrl
        UUID: uuid.UUID
        Index: int
        Urgency: int
        Type: str
        DateTime: datetime.datetime
        Source: str
        Message: str

        def __init__(self,Parent:wx.ListCtrl,RowIndex:int,Urgency:int,Source:str,Message:str,DateTimeFormat):
            self.Parent = Parent
            self.UUID = uuid.uuid4()
            self.Index = RowIndex
            self.Urgency = Urgency
            self.DateTime = datetime.datetime.now()
            self.Source = Source
            self.Message = Message
            match(self.Urgency):
                case ConstDefs.LOGVIEW_URGENCY_WARN:
                    self.Type = "WARN"
                case ConstDefs.LOGVIEW_URGENCY_ERRO:
                    self.Type = "ERRO"
                case ConstDefs.LOGVIEW_URGENCY_SUCC:
                    self.Type = "SUCC"
                case _:
                    self.Type = "INFO"
            self.Parent.Append([self.Type,self.DateTime.strftime(DateTimeFormat),self.Source,self.Message])

        def Color(self,Colors:dict):
            self.Parent.SetItemTextColour(self.Index,wx.Colour(Colors['FG']))
            self.Parent.SetItemBackgroundColour(self.Index,wx.Colour(Colors['BG']))

    DateTimeFormat: str
    Rows: list[Row]
    this: int
    Body: wx.ListCtrl
    Colors: dict

    def __init__(self,Parent:wx.Window,Position:wx.Point=wx.DefaultPosition,Size:wx.Size=wx.DefaultSize):
        self.Body = wx.ListCtrl(Parent,wx.ID_ANY,size=Size,style=wx.LC_REPORT)
        self.DateTimeFormat = DATETIMEFORMAT
        self.Body.InsertColumn(0,"Lv",wx.LIST_FORMAT_CENTER,50)
        self.Body.InsertColumn(1,"Time",width=140)
        self.Body.InsertColumn(2,"Source",width=70)
        self.Body.InsertColumn(3,"Message",width=500)
        self.Rows = []
        self.Colors = {
            ConstDefs.LOGVIEW_URGENCY_INFO: {
                'BG': COLOR['LOG']['INFO']['BG'],
                'FG': COLOR['LOG']['INFO']['FG']
            },
            ConstDefs.LOGVIEW_URGENCY_WARN: {
                'BG': COLOR['LOG']['WARN']['BG'],
                'FG': COLOR['LOG']['WARN']['FG']
            },
            ConstDefs.LOGVIEW_URGENCY_ERRO: {
                'BG': COLOR['LOG']['ERRO']['BG'],
                'FG': COLOR['LOG']['ERRO']['FG']
            },
            ConstDefs.LOGVIEW_URGENCY_SUCC: {
                'BG': COLOR['LOG']['SUCC']['BG'],
                'FG': COLOR['LOG']['SUCC']['FG']
            }
        }
        self.this = 0

    def Log(self,Urgency:int,Source:str,Message:str,Color:bool=True):
        self.Rows.append(self.Row(self.Body,len(self.Rows),Urgency,Source,Message,self.DateTimeFormat))
        self.this = len(self.Rows)-1
        if(Color):
            if Urgency in ConstDefs:
                self.Rows[self.this].Color(self.Colors[Urgency])

    def SetColors(self,Urgency:int,FGColor:str|None=None,BGColor:str|None=None):
        if Urgency in ConstDefs:
            if(FGColor):
                self.Colors[Urgency]['FG'] = FGColor
            if(BGColor):
                self.Colors[Urgency]['BG'] = BGColor

    def SetDateTimeFormat(self,Format:str):
        self.DateTimeFormat = Format

    def SetTitles(self,Title:dict={'Urgency':"Lv",'DateTime':"Time",'Source':"Source",'Message':"Message"}):
        if 'Urgency' in Title:
            Column = self.Body.GetColumn(0)
            Column.SetText(Title['Urgency'])
            self.Body.SetColumn(0,Column)
        if 'DateTime' in Title:
            Column = self.Body.GetColumn(1)
            Column.SetText(Title['DateTime'])
            self.Body.SetColumn(1,Column)
        if 'Source' in Title:
            Column = self.Body.GetColumn(2)
            Column.SetText(Title['Source'])
            self.Body.SetColumn(2,Column)
        if 'Message' in Title:
            Column = self.Body.GetColumn(3)
            Column.SetText(Title['Message'])
            self.Body.SetColumn(3,Column)

    def SetColumnsWidth(self,Width:dict={'Urgency':50,'DateTime':140,'Source':70,'Message':500}):
        if 'Urgency' in Width:
            self.Body.SetColumnWidth(0,Width['Urgency'])
        if 'DateTime' in Width:
            self.Body.SetColumnWidth(1,Width['DateTime'])
        if 'Source' in Width:
            self.Body.SetColumnWidth(2,Width['Source'])
        if 'Message' in Width:
            self.Body.SetColumnWidth(3,Width['Message'])
    

class Debug:
    def wxDebug():
        wx.lib.inspection.InspectionTool().Show()


class Sticker:
    Body: wx.Panel
    Element_vBox: wx.BoxSizer
    Element_Data: wx.StaticText
    Element_Subject: wx.StaticText
    Text_Data: str
    Text_Subject: str
    Font_Data: wx.Font
    Font_Subject: wx.Font

#生成仪表盘中的单个含背景色的贴条
    def __init__(self,ParentPanel:wx.Window,Position:wx.Point,Size:wx.Size,BGColor:wx.Colour,FontColor:wx.Colour,Data:str|None=None,Subject:str|None=None,FontName:str="Tahoma",MainFontSize:int=16,HitsFontSize:int=10):
        if(Data):
            self.Text_Data = Data
        else:
            self.Text_Data = " "
        if(Subject):
            self.Text_Subject = Subject
        else:
            self.Text_Subject = " "
        
        self.Body = wx.Panel(ParentPanel,wx.ID_ANY,Position,Size)
        self.Body.SetBackgroundColour(wx.Colour(BGColor))
        
        self.Font_Data = wx.Font(MainFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)
        self.Font_Subject = wx.Font(HitsFontSize,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,FontName,wx.FONTENCODING_DEFAULT)

        self.Element_Data = wx.StaticText(self.Body,label=self.Text_Data)
        self.Element_Data.SetFont(self.Font_Data)
        self.Element_Data.SetForegroundColour(FontColor)
        self.Element_Data.Center()
        self.Element_Subject = wx.StaticText(self.Body,label=self.Text_Subject)
        self.Element_Subject.SetFont(self.Font_Subject)
        self.Element_Subject.SetForegroundColour(FontColor)
        self.Element_vBox = wx.BoxSizer(wx.VERTICAL)
        self.Element_vBox.AddStretchSpacer(1)
        self.Element_vBox.Add(self.Element_Subject,0,wx.LEFT|wx.BOTTOM,4)
        self.Body.SetSizer(self.Element_vBox)
        self.Body.Layout()
        self.Body.Update()

    def SetTextColor(self,FontColor:wx.Colour) -> None:
        self.Element_Data.SetForegroundColour(FontColor)
        self.Element_HintsText.SetForegroundColour(FontColor)

    def SetBGColor(self,BGColor:wx.Colour) -> None:
        self.Body.SetBackgroundColour(wx.Colour(BGColor))

    def SetData(self,Text:str) -> None:
        self.Element_Data.SetLabel(Text)

    def GetData(self) -> str:
        return self.Element_Data.GetLabel()

    def SetSubject(self,Text:str|None) -> None:
        if(Text):
            self.Element_Subject.SetLabel(Text)
        else:
            self.Element_Subject.SetLabel(" ")

    def GetSubject(self) -> str:
        Text = self.Element_Subject.GetLabel()
        if(Text == " "):
            return None
        else:
            return self.Element_Subject.GetLabel()

    def SetText(self,Data:str,Subject:str):
        self.SetData(Data)
        self.SetSubject(Subject)

    def Move(self,Pos:wx.Point) -> None:
        self.Body.SetPosition(Pos)

    def Scale(self,Size:wx.Size) -> None:
        self.Body.SetSize(Size)

    def GetSize(self) -> wx.Size:
        return self.Body.GetSize()

    def Bind(self,Event:wx.PyEventBinder,Handler:function):
        self.Body.Bind(Event,Handler)
        self.Element_Data.Bind(Event,Handler)
        self.Element_Subject.Bind(Event,Handler)

    def ClickCopyData(self,Event:wx.PyEventBinder):
        self.Body.Bind(Event,lambda Event:pyperclip.copy(self.Text_Data))
        self.Element_Data.Bind(Event,lambda Event:pyperclip.copy(self.Text_Data))
        self.Element_Subject.Bind(Event,lambda Event:pyperclip.copy(self.Text_Data))


class AboutDialog:
    Element_AboutDialog: wx.Dialog
    Element_MainPanel: wx.Panel
    Container_MainvBox: wx.BoxSizer
    Container_NamehBox: wx.BoxSizer
    Container_SubtitlehBox: wx.BoxSizer
    Container_VersionhBox: wx.BoxSizer
    Container_CopyrighthBox: wx.BoxSizer
    Container_DetailhBox: wx.BoxSizer
    Container_DetailTextvBox: wx.BoxSizer
    Container_ButtonhBox: wx.BoxSizer
    Element_ProductName: wx.StaticText
    Element_ProductSubtitle: wx.StaticText
    Element_ProductVersion: wx.StaticText
    Element_ProductCopyright: wx.StaticText
    Element_ProductDetailContainer: wx.Panel
    Element_ProductDetail: wx.TextCtrl
    Element_ButtonOK: wx.Button
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

