#Author: bluepotato

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBTechScreen
import WBTeamScreen
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import CvPlatyBuilderScreen
import Popup
gc = CyGlobalContext()
iChange = 1

class WBRFCPlayerScreen:

	def __init__(self):
		self.iIconSize = 64
		self.civType = None
		self.rfcPlayer = None
		self.civInfo = None

	def interfaceScreen(self, civType):
		screen = CyGInterfaceScreen( "WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)
		self.civType = civType
		self.civInfo = gc.getCivilizationInfo(civType)
		self.rfcPlayer = gc.getRiseFall().getRFCPlayer(civType)

		screen.setRenderInterfaceOnly(True)
		screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setText("PlayerExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		iY = 20
		screen.addDropDownBoxGFC("CurrentPlayer", 20, iY, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getNumCivilizationInfos()):
			civInfo = gc.getCivilizationInfo(i)
			sText = CyTranslator().getText(civInfo.getShortDescriptionKey().encode("iso-8859-1"), ())
			if not gc.getRiseFall().getRFCPlayer(i).isEnabled():
				sText = "*" + sText
			if i == self.civType:
				sText = "[" + sText + "]"
			screen.addPullDownString("CurrentPlayer", sText, i, i, i == self.civType)

		iY += 30
		screen.addDropDownBoxGFC("ChangeBy", 20, iY, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 1000001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		iY += 30

		self.placeStats()
		self.placeCivics()

	def placeStats(self):
		screen = CyGInterfaceScreen( "WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)
		screen.addDDSGFC("CivPic", gc.getCivilizationInfo(self.civType).getButton(), screen.getXResolution() * 5/8 - self.iIconSize/2, 80, self.iIconSize, self.iIconSize, WidgetTypes.WIDGET_PYTHON, 7872, self.civType)
		sText = CyTranslator().getText(self.civInfo.getShortDescriptionKey().encode("iso-8859-1"), ())

	def placeCivics(self):
		screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)

	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)
		return 1

	def update(self, fDelta):
		return 1
