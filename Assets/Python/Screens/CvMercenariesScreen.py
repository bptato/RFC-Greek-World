#Author: bluepotato
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string
import CvScreensInterface

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

SCREEN_NAME = "MercenariesScreen"
CANCEL_NAME = "MercenariesCancel"
BUTTON_NAME = "MercenariesButton"
BACKGROUND_ID = "MercenariesBackground"
EXIT_ID = "MercenariesExit"
TITLE_NAME = "MercenariesTitle"
AREA_NAME = "MercenariesArea"
AVAILABLE_MERCENARIES = "AvailableMercenaries"
AVAILABLE_MERCENARIES_INNER = "AvailableMercenariesInner"
AVAILABLE_MERCENARIES_TOP = "AvailableMercenariesTopPanel"

HEADER_HEIGHT = 55
TEXT_MARGIN = 15
BUTTON_SIZE = 24
BIG_BUTTON_SIZE = 64

X_CANCEL = 750
Y_CANCEL = 726
X_EXIT = 994
Y_EXIT = 726

X_SCREEN = 500
Y_SCREEN = 396
W_SCREEN = 1024
H_SCREEN = 768
Z_SCREEN = -6.1
Y_TITLE = 8
Z_TEXT = Z_SCREEN - 0.2

def text(s):
	return localText.getText(s, ())

#following functions were shamelessly stolen from the original mercenary mod
#             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def numberToAlpha(iNum):
	strNum = str(iNum)
	strAlpha = ""

	# Go though the alphaList and convert the numbers to letters
	for i in range(len(strNum)):
		strAlpha = strAlpha + alphaList[int(strNum[i])]

	return strAlpha

def alphaToNumber(strAlpha):
	strNum = ""

	# Go though the alphaList and convert the letters to numbers
	for i in range(len(strAlpha)):
		strNum = strNum + str(alphaList.index(strAlpha[i]))

	return int(strNum)

class CvMercenariesScreen:

	def __init__(self):
		self.activePlayer = -1

	def getScreen(self):
		return CyGInterfaceScreen(SCREEN_NAME, CvScreenEnums.MERCENARIES_SCREEN)

	def setActivePlayer(self, playerType):
		self.activePlayer = playerType

	def interfaceScreen(self):
		screen = self.getScreen()
		self.setActivePlayer(gc.getGame().getActivePlayer())

		if screen.isActive():
			return

		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setDimensions(screen.centerX(0), screen.centerY(0), W_SCREEN, H_SCREEN)
		screen.addDrawControl(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, W_SCREEN, H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, W_SCREEN, H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("TechTopPanel", u"", u"", True, False, 0, 0, W_SCREEN, HEADER_HEIGHT, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel("TechBottomPanel", u"", u"", True, False, 0, 713, W_SCREEN, HEADER_HEIGHT, PanelStyles.PANEL_STYLE_BOTTOMBAR)

		screen.setText(EXIT_ID, BACKGROUND_ID, u"<font=4>" + text("TXT_KEY_PEDIA_SCREEN_EXIT").upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, X_EXIT, Y_EXIT, Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		screen.setText(TITLE_NAME, BACKGROUND_ID, u"<font=4b>" + text("TXT_KEY_MERCENARIES_SCREEN_TITLE").upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, X_SCREEN, Y_TITLE, Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.drawAvailableMercenariesPanel()
		self.drawMercenaryInfoPanel()
		screen.showWindowBackground(False)

		return 0

	def drawAvailableMercenariesPanel(self):
		riseFall = gc.getRiseFall()
		screen = self.getScreen()
		screen.addPanel("AvailableMercenaries", "", "", True, True, 0, HEADER_HEIGHT, W_SCREEN/2 - TEXT_MARGIN/2, H_SCREEN - HEADER_HEIGHT*2, PanelStyles.PANEL_STYLE_MAIN)
		screen.attachPanel("AvailableMercenaries", "AvailableMercenariesTitlePanel", "", "", False, False, PanelStyles.PANEL_STYLE_MAIN)
		screen.setText("AvailableMercenariesTitle", BACKGROUND_ID, u"<font=3b>" + text("TXT_KEY_AVAILABLE_MERCENARIES").upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (W_SCREEN/2 - TEXT_MARGIN/2)/2, HEADER_HEIGHT + TEXT_MARGIN/4, Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		mercCount = 0
		for i in range(riseFall.getNumProvinces()):
			province = riseFall.getProvince(i)
			if province.getNumCities(self.activePlayer) > 0:
				for j in range(province.getNumMercenaries()):
					mercenary = province.getMercenary(j)
					unitInfo = gc.getUnitInfo(mercenary.getUnitType())
					unitID = "M_" + numberToAlpha(i) + ":" + numberToAlpha(j) #you can't put numbers in panel IDs. I had to figure this out the hard way...
					screen.attachPanel("AvailableMercenaries", unitID, "", "", True, False, PanelStyles.PANEL_STYLE_MAIN)
					firstRow = unitID + "_firstRow"
					secondRow = unitID + "_secondRow"
					screen.attachPanel(unitID, firstRow, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
					screen.attachPanel(unitID, secondRow, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
					screen.attachImageButton(firstRow, unitID + "_picBtn", unitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, True)
					screen.attachLabel(firstRow, unitID + "_nameLabel", u"<font=2b>" + text(unitInfo.getDescription().encode("iso-5988-1")) + u"</font> ")
					
					screen.attachMultiListControlGFC(firstRow, unitID + "_promotions", "", 1, 20, 20, TableStyles.TABLE_STYLE_EMPTY)
					for k in range(mercenary.getNumPromotions()):
						promotionInfo = gc.getPromotionInfo(k)
						screen.appendMultiListButton(unitID + "_promotions", promotionInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.attachLabel(secondRow, unitID + "_provinceLabel", u"\tProvince: " + text(province.getName().encode("iso-5988-1")))
					screen.attachLabel(secondRow, unitID + "_xpLabel", "\t" + text("INTERFACE_PANE_EXPERIENCE") + ": " + str(mercenary.getExperience()))
					screen.attachLabel(secondRow, unitID + "_costLabel", u"\t<color=#FFD700>" + str(mercenary.getHireCost()) + "</color>" + CvUtil.getIcon("gold"))
					if mercenary.getHireCost() <= gc.getPlayer(self.activePlayer).getGold():
						screen.attachImageButton(firstRow, unitID + "_hireBtn", "Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, True)
					mercCount += 1
		
		if (6-mercCount) > 0:
			for i in range(6-mercCount):
				screen.attachPanel("AvailableMercenaries", "padding"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel("padding"+str(i), "", "     ")
				screen.attachLabel("padding"+str(i), "", "     ")
				screen.attachLabel("padding"+str(i), "", "     ")

	def drawMercenaryInfoPanel(self):
		screen = self.getScreen()
		screen.addPanel("MercenaryInfo", "", "", True, True, W_SCREEN/2, HEADER_HEIGHT, W_SCREEN/2 - TEXT_MARGIN/2, H_SCREEN - HEADER_HEIGHT*2, PanelStyles.PANEL_STYLE_MAIN)
		screen.attachPanel("MercenaryInfo", "MercenaryInfoTitlePanel", "", "", False, False, PanelStyles.PANEL_STYLE_MAIN)
		screen.setText("MercenaryInfoTitle", BACKGROUND_ID, u"<font=3b>" + text("TXT_KEY_MERCENARY_INFORMATION").upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, W_SCREEN/2 + (W_SCREEN/2 - TEXT_MARGIN/2)/2, HEADER_HEIGHT + TEXT_MARGIN/4, Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def selectMercenaryInfo(self, provinceId, mercId):
		screen = self.getScreen()
		riseFall = gc.getRiseFall()
		province = riseFall.getProvince(provinceId)
		mercenary = province.getMercenary(mercId)
		unitInfo = gc.getUnitInfo(mercenary.getUnitType())
		screen.setText("MercenaryInfoTitle", BACKGROUND_ID, u"<font=3b>" + text(unitInfo.getDescription().encode("iso-5988-1")).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, W_SCREEN/2 + (W_SCREEN/2 - TEXT_MARGIN/2)/2, HEADER_HEIGHT + TEXT_MARGIN/4, Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addUnitGraphicGFC("MercenaryInfoUnitGraphic", mercenary.getUnitType(), W_SCREEN/2+TEXT_MARGIN, HEADER_HEIGHT * 3 / 2, W_SCREEN/2-TEXT_MARGIN*3, H_SCREEN/2, WidgetTypes.WIDGET_GENERAL, -1, -1, 10, 10, 1, True)


	def mercenaryButton(self, inputClass):
		return 0

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
	
	def resetScreen(self):
		self.hideScreen()
		self.interfaceScreen()

	def handleInput(self, inputClass):
		riseFall = gc.getRiseFall()
		functionName = inputClass.getFunctionName()
		print "Called " + functionName
		if functionName.startswith("M_"):
			functionNameSplit = functionName.split("_")
			mercValues = functionNameSplit[1].split(":")
			provinceNum = alphaToNumber(mercValues[0])
			mercNum = alphaToNumber(mercValues[1])
			province = riseFall.getProvince(provinceNum)
			
			if len(functionNameSplit) > 2:
				btnName = functionNameSplit[2]
				if btnName == "hireBtn":
					province.hireMercenary(self.activePlayer, mercNum)
					self.resetScreen()
			self.selectMercenaryInfo(provinceNum, mercNum)
		return

	def hire(self, provinceID, mercenaryID):
		pass

	def update(self, fDelta):
		return
