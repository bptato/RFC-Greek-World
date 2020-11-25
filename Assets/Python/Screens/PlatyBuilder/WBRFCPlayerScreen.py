#Author: bluepotato

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPlatyBuilderScreen
gc = CyGlobalContext()

class WBRFCPlayerScreen:
	def __init__(self):
		self.iIconSize = 64
		self.civType = None
		self.rfcPlayer = None
		self.civInfo = None
		self.change = 1
		self.screen = None
		self.modifiers = {}

	def interfaceScreen(self, civType):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_RFC_PLAYER)
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
				lambda i: ("*", "")[gc.getRiseFall().getRFCPlayer(i).isEnabled()] + CyTranslator().getText(gc.getCivilizationInfo(i).getShortDescriptionKey().encode("iso-8859-1"), ()))

		self.y += 30
		self.addDropdown("ChangeBy", xres/5, self.change, 1, 1000001,
				lambda i: i * (5, 2)[str(i)[0] == "1"],
				lambda i: "(+/-) " + str(i))

		self.y += 30
		self.addModifiers()

	def addModifiers(self):
		self.addModifier("CompactEmpireModifier", "TXT_KEY_WB_COMPACT_EMPIRE_MODIFIER", self.rfcPlayer.getCompactEmpireModifier, self.rfcPlayer.setCompactEmpireModifier)
		self.addModifier("UnitUpkeepModifier", "TXT_KEY_WB_UNIT_UPKEEP_MODIFIER", self.rfcPlayer.getUnitUpkeepModifier, self.rfcPlayer.setUnitUpkeepModifier)
		self.addModifier("ResearchModifier", "TXT_KEY_WB_RESEARCH_MODIFIER", self.rfcPlayer.getResearchModifier, self.rfcPlayer.setResearchModifier)
		self.addModifier("DistanceMaintenanceModifier", "TXT_KEY_WB_DISTANCE_MAINTENANCE_MODIFIER", self.rfcPlayer.getDistanceMaintenanceModifier, self.rfcPlayer.setDistanceMaintenanceModifier)
		self.addModifier("NumCitiesMaintenanceModifier", "TXT_KEY_WB_NUM_CITIES_MAINTENANCE_MODIFIER", self.rfcPlayer.getNumCitiesMaintenanceModifier, self.rfcPlayer.setNumCitiesMaintenanceModifier)
		self.addModifier("UnitProductionModifier", "TXT_KEY_WB_UNIT_PRODUCTION_MODIFIER", self.rfcPlayer.getUnitProductionModifier, self.rfcPlayer.setUnitProductionModifier)
		self.addModifier("CivicUpkeepModifier", "TXT_KEY_WB_CIVIC_UPKEEP_MODIFIER", self.rfcPlayer.getCivicUpkeepModifier, self.rfcPlayer.setCivicUpkeepModifier)
		self.addModifier("HealthBonusModifier", "TXT_KEY_WB_HEALTH_BONUS_MODIFIER", self.rfcPlayer.getHealthBonusModifier, self.rfcPlayer.setHealthBonusModifier)
		self.addModifier("BuildingProductionModifier", "TXT_KEY_WB_BUILDING_PRODUCTION_MODIFIER", self.rfcPlayer.getBuildingProductionModifier, self.rfcPlayer.setBuildingProductionModifier)
		self.addModifier("WonderProductionModifier", "TXT_KEY_WB_WONDER_PRODUCTION_MODIFIER", self.rfcPlayer.getWonderProductionModifier, self.rfcPlayer.setWonderProductionModifier)
		self.addModifier("GreatPeopleModifier", "TXT_KEY_WB_GREAT_PEOPLE_MODIFIER", self.rfcPlayer.getGreatPeopleModifier, self.rfcPlayer.setGreatPeopleModifier)
		self.addModifier("InflationModifier", "TXT_KEY_WB_INFLATION_MODIFIER", self.rfcPlayer.getInflationModifier, self.rfcPlayer.setInflationModifier)
		self.addModifier("GrowthModifier", "TXT_KEY_WB_GROWTH_MODIFIER", self.rfcPlayer.getGrowthModifier, self.rfcPlayer.setGrowthModifier)

	def addModifier(self, name, txtkey, getter, setter):
		self.y += 20
		self.x = 20
		self.addPlusButton(name + "Plus")
		self.x += 25
		self.addMinusButton(name + "Minus")
		self.x += 30
		self.y += 1
		self.addText(name + "Text", CyTranslator().getText(txtkey, ()) + ": " + str(getter()))
		self.modifiers[name] = {};
		self.modifiers[name]['get'] = getter
		self.modifiers[name]['set'] = setter

	def addDropdown(self, name, size, current, minimum, maximum, pulldownNext, pulldownName):
		self.screen.addDropDownBoxGFC(name, self.x, self.y, size, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = minimum
		while i < maximum:
			self.screen.addPullDownString(name, pulldownName(i), i, i, i == current)
			i = pulldownNext(i)

	def addText(self, name, text):
		self.screen.setText(name, "Background", text, CvUtil.FONT_LEFT_JUSTIFY, self.x, self.y, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def addPlusButton(self, name):
		self.addTextButton(name, 1030, 24, 24, ButtonStyles.BUTTON_STYLE_CITY_PLUS)

	def addMinusButton(self, name):
		self.addTextButton(name, 1031, 24, 24, ButtonStyles.BUTTON_STYLE_CITY_MINUS)

	def addTextButton(self, name, textid, w, h, style):
		self.screen.setButtonGFC(name, "", "", self.x, self.y, w, h, WidgetTypes.WIDGET_PYTHON, textid, -1, style)

	def getDropdownData(self, name):
		return self.screen.getPullDownData(name, self.screen.getSelectedPullDownID(name))

	def handleInput(self, inputClass):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_RFC_PLAYER)
		funcName = inputClass.getFunctionName()
		if funcName == "ChangeBy":
			self.change = self.getDropdownData("ChangeBy")
		elif funcName == "CurrentRFCPlayer":
			self.interfaceScreen(self.getDropdownData("CurrentRFCPlayer"))
		elif funcName.endswith("Plus") and funcName.replace("Plus", "") in self.modifiers:
			modifier = self.modifiers[funcName.replace("Plus", "")]
			modifier['set'](modifier['get']() + self.change)
			self.interfaceScreen(self.civType)
		elif funcName.endswith("Minus") and funcName.replace("Minus", "") in self.modifiers:
			modifier = self.modifiers[funcName.replace("Minus", "")]
			modifier['set'](modifier['get']() - self.change)
			self.interfaceScreen(self.civType)

		return 1

	def update(self, fDelta):
		return 1

rfcPlayerScreen = WBRFCPlayerScreen()
