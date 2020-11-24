#Author: bluepotato

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPlatyBuilderScreen
gc = CyGlobalContext()
riseFall = CyRiseFall()

class WBRFCPlayerScreen:

	def __init__(self):
		self.iIconSize = 64
		self.civType = None
		self.rfcPlayer = None
		self.civInfo = None
		self.change = -1
		self.screen = None

	def interfaceScreen(self, civType):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)
		self.civType = civType
		self.civInfo = gc.getCivilizationInfo(civType)
		self.rfcPlayer = gc.getRiseFall().getRFCPlayer(civType)

		xres = self.screen.getXResolution()
		yres = self.screen.getYResolution()
		self.screen.setRenderInterfaceOnly(True)
		self.screen.addPanel("MainBG", u"", u"", True, False, -10, -10, xres + 20, yres + 20, PanelStyles.PANEL_STYLE_MAIN)
		self.screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		self.screen.setText("RFCPlayerExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xres - 30, yres - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		self.y = 20
		self.x = 20

		self.addDropdown("CurrentRFCPlayer", xres/5, self.civType, 0, gc.getNumCivilizationInfos(),
				lambda i: i + 1,
				lambda i: ("*", "")[riseFall.getRFCPlayer(i).isEnabled()] + CyTranslator().getText(gc.getCivilizationInfo(i).getShortDescriptionKey(), ()))

		self.y += 30
		self.addDropdown("ChangeBy", xres/5, self.change, 1, 1000001,
				lambda i: i * (5, 2)[str(i)[0] == "1"],
				lambda i: "(+/-) " + str(i))

	def addDropdown(self, name, size, current, minimum, maximum, pulldownNext, pulldownName):
		self.screen.addDropDownBoxGFC(name, self.x, self.y, size, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = minimum
		while i < maximum:
			self.screen.addPullDownString(name, pulldownName(i), i, i, i == current)
			i = pulldownNext(i)
	
	def getDropdownData(self, name):
		return screen.getPullDownData(name, screen.getSelectedPullDownID(name))

	def handleInput(self, inputClass):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_PLAYER)
		if inputClass == "ChangeBy":
			self.change = self.getDropdownData("ChangeBy")
		elif inputClass == "CurrentRFCPlayer":
			self.civType = self.getDropdownData("CurrentRFCPlayer")

		return 1

	def update(self, fDelta):
		return 1
