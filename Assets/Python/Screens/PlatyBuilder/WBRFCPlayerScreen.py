#Author: bluepotato
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPlatyBuilderScreen
import StringUtils
gc = CyGlobalContext()

class WBRFCPlayerScreen:
	def __init__(self):
		self.civType = -1
		self.civDesc = ""
		self.change = 1
		self.screen = None
		self.rfcPlayer = None
		self.civInfo = None
		self.buttons = {}
		self.changeButtons = {}
		self.booleanButtons = {}
		self.selectedUnit = -1
		self.selectedCity = -1
		self.selectedCultureCiv = 0
		self.pbscreen = None
		self.noRefresh = False

	def interfaceScreen(self, civType):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_RFC_PLAYER)
		if self.civType != civType:
			self.selectedUnit = -1
			self.selectedCity = -1
		self.civType = civType
		self.civInfo = gc.getCivilizationInfo(self.civType)
		self.rfcPlayer = gc.getRiseFall().getRFCPlayer(self.civType)
		self.civDesc = self.getCivName(self.civType)

		yellowText = CyTranslator().getText("[COLOR_YELLOW]", ())
		positiveText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		negativeText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())

		xres = self.screen.getXResolution()
		yres = self.screen.getYResolution()
		self.screen.setRenderInterfaceOnly(True)
		self.screen.addPanel("MainBG", u"", u"", True, False, -10, -10, xres + 20, yres + 20, PanelStyles.PANEL_STYLE_MAIN)
		self.screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		self.screen.setText("RFCPlayerExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xres - 30, yres - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		self.y = 20
		self.x = 20

		self.addDropdown("CurrentRFCPlayer", xres/5, self.civType, 0, gc.getNumCivilizationInfos(),
			lambda i: i + 1,
			lambda i: ("*", "")[gc.getRiseFall().getRFCPlayer(i).isEnabled()] + self.getCivName(i))

		self.y += 30
		self.addDropdown("ChangeBy", xres / 5, self.change, 1, 1000001,
			lambda i: i * (5, 2)[str(i)[0] == "1"],
			lambda i: "(+/-) " + str(i))

		self.y += 40
		self.addBooleanButton("PlayerEnabled", "TXT_KEY_WB_ENABLED", self.rfcPlayer.isEnabled, self.rfcPlayer.setEnabled)
		self.y += 20
		self.addBooleanButton("PlayerFlipped", "TXT_KEY_WB_FLIPPED", self.rfcPlayer.isFlipped, self.rfcPlayer.setFlipped)
		self.y += 20
		self.addStartingValues()
		self.y += 30

		def religionName(i):
			if i == ReligionTypes.NO_RELIGION:
				return CyTranslator().getText("TXT_KEY_MISC_NO_STATE_RELIGION", ())
			else:
				return gc.getReligionInfo(i).getDescription()
		self.addDropdown("WBRFCPlayerStartingReligion", xres/5, self.rfcPlayer.getStartingReligion(), -1, gc.getNumReligionInfos(),
			lambda i: i + 1,
			lambda i: religionName(i))

		self.y = yres - 40 - yres / 4 + yres / 8
		self.x = 20
		self.addTable("WBRFCPlayerCivics", gc.getNumCivicOptionInfos(), gc.getNumCivicInfos(), xres / 2 - 20, yres - self.y - 20,
			lambda i: gc.getCivicOptionInfo(i).getDescription(),
			lambda i, j: gc.getCivicInfo(j).getCivicOptionType() == i,
			lambda i, j: (yellowText, positiveText)[self.rfcPlayer.getStartingCivic(i) == j] + gc.getCivicInfo(j).getDescription(),
			lambda j: gc.getCivicInfo(j).getButton(),
			8205)

		self.x = xres / 4 + 30
		self.y = 20

		self.addList("WBRFCPlayerTechs", gc.getNumTechInfos(), xres / 4 - 30, yres / 2 + yres / 4 + yres / 8 - 80, "TXT_KEY_WB_STARTING_TECHS",
			lambda i: True,
			lambda i: (yellowText, positiveText)[self.rfcPlayer.isStartingTech(i)] + gc.getTechInfo(i).getDescription(),
			lambda i: gc.getTechInfo(i).getButton(),
			7871)
		
		self.x = 20
		self.y = yres / 2

		self.addList("WBRFCPlayerWars", gc.getNumCivilizationInfos(), xres / 4 - 20, yres / 4 + yres / 8 - 60, "TXT_KEY_WB_STARTING_WARS",
			lambda i: (i < self.civType or gc.getRiseFall().getRFCPlayer(i).isMinor()) and i != CivilizationTypes.CIVILIZATION_BARBARIAN,
			lambda i: (yellowText, negativeText)[self.rfcPlayer.isStartingWar(i)] + self.getCivName(i),
			lambda i: gc.getCivilizationInfo(i).getButton(),
			7872)

		self.x = xres / 2 + 20
		self.y = 20
		self.addList("WBRFCPlayerUnits", self.rfcPlayer.getNumScheduledUnits(), xres / 4 - 30, yres / 2 - 10, "TXT_KEY_WB_SCHEDULED_UNITS",
			lambda i: True,
			lambda i: (yellowText, positiveText)[self.selectedUnit == i] + self.scheduledUnitStr(i),
			lambda i: (self.rfcPlayer.getScheduledUnit(i).getUnitType() != UnitTypes.NO_UNIT and gc.getUnitInfo(self.rfcPlayer.getScheduledUnit(i).getUnitType()).getButton() or None),
			8208)

		self.x += xres / 4 - 10
		self.addList("WBRFCPlayerCities", self.rfcPlayer.getNumScheduledCities(), xres / 4 - 30, yres / 2 - 10, "TXT_KEY_WB_SCHEDULED_CITIES",
			lambda i: True,
			lambda i: (yellowText, positiveText)[self.selectedCity == i]
				+ gc.getMap().plot(self.rfcPlayer.getScheduledCity(i).getX(), self.rfcPlayer.getScheduledCity(i).getY()).getCityName(self.civType, False)
				+ " (" + StringUtils.getStrForYear(self.rfcPlayer.getScheduledCity(i).getYear()) + ")",
			lambda i: None,
			8210)

		self.y = yres / 2 + 20
		self.x = xres / 2 + 20

		def addScheduledUnit():
			unit = self.rfcPlayer.addScheduledUnit()
			unit.setUnitType(0)
			unit.setAmount(1)
			unit.setYear(gc.getGame().getGameTurnYear())
			self.selectedCity = -1
			self.selectedUnit = self.rfcPlayer.getNumScheduledUnits() - 1

		def addScheduledCity():
			city = self.rfcPlayer.addScheduledCity()
			city.setX(0)
			city.setY(0)
			city.setPopulation(1)
			city.setYear(gc.getGame().getGameTurnYear())
			self.selectedUnit = -1
			self.selectedCity = self.rfcPlayer.getNumScheduledCities() - 1

		self.addActionButton("AddScheduledUnit", "TXT_KEY_WB_ADD_UNIT", addScheduledUnit)
		self.y += 40
		self.addActionButton("AddScheduledCity", "TXT_KEY_WB_ADD_CITY", addScheduledCity)
		self.y += 40

		if self.rfcPlayer.getNumScheduledUnits() <= self.selectedUnit:
			self.selectedUnit = -1
		if self.rfcPlayer.getNumScheduledCities() <= self.selectedCity:
			self.selectedCity = -1

		if self.selectedUnit != -1:
			self.addDropdown("UnitType", xres/5, self.rfcPlayer.getScheduledUnit(self.selectedUnit).getUnitType(), 0, gc.getNumUnitInfos(),
				lambda i: i + 1,
				lambda i: gc.getUnitInfo(i).getDescription())
			self.y += 40
			self.addDropdown("UnitAIType", xres/5, self.rfcPlayer.getScheduledUnit(self.selectedUnit).getUnitAIType(), 0, UnitAITypes.NUM_UNITAI_TYPES,
				lambda i: i + 1,
				lambda i: gc.getUnitAIInfo(i).getType())
			self.y += 40
			self.addDropdown("FacingDirection", xres/5, self.rfcPlayer.getScheduledUnit(self.selectedUnit).getFacingDirection(), 0, DirectionTypes.NUM_DIRECTION_TYPES,
				lambda i: i + 1,
				lambda i: ("North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest")[i]) #TODO expose and use getDirectionTypeString instead
			self.y += 40
			self.addBooleanButton("UnitAIOnly", "TXT_KEY_WB_AI_ONLY",
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).isAIOnly,
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).setAIOnly)
			self.y += 20
			self.addBooleanButton("UnitDeclareWar", "TXT_KEY_WB_DECLARE_WAR",
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).isDeclareWar,
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).setDeclareWar)
			self.y += 20
			self.addChangeButtons("UnitYear", "TXT_KEY_WB_YEAR",
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).getYear,
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).setYear)
			self.y += 20
			self.addChangeButtons("UnitAmount", "TXT_KEY_WB_AMOUNT",
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).getAmount,
				self.rfcPlayer.getScheduledUnit(self.selectedUnit).setAmount)
			self.y += 30
			self.addText("UnitXY", "X: " +
					str(self.rfcPlayer.getScheduledUnit(self.selectedUnit).getX())
					+ " Y: " +
					str(self.rfcPlayer.getScheduledUnit(self.selectedUnit).getY()))
			self.y += 20
			self.addActionButton("UnitMove", "TXT_KEY_MISSION_MOVE_TO",
					self.moveSelectedUnit)
			self.y = yres - 60
			self.addActionButton("UnitDestroy", "TXT_KEY_WB_DELETE",
					self.destroySelectedUnit)
		elif self.selectedCity != -1:
			self.addChangeButtons("CityYear", "TXT_KEY_WB_YEAR",
				self.rfcPlayer.getScheduledCity(self.selectedCity).getYear,
				self.rfcPlayer.getScheduledCity(self.selectedCity).setYear)
			self.y += 20
			self.addChangeButtons("CityPopulation", "TXT_KEY_WB_POPULATION",
				self.rfcPlayer.getScheduledCity(self.selectedCity).getPopulation,
				self.rfcPlayer.getScheduledCity(self.selectedCity).setPopulation)
			self.y += 20
			self.addText("CityXY", "X: " +
					str(self.rfcPlayer.getScheduledCity(self.selectedCity).getX())
					+ " Y: " +
					str(self.rfcPlayer.getScheduledCity(self.selectedCity).getY()))
			self.y += 20
			self.addActionButton("CityMove", "TXT_KEY_MISSION_MOVE_TO",
					self.moveSelectedCity)

			self.y += 40
			self.addChangeButtons("CityCultureMod", self.getCivName(self.selectedCultureCiv).encode("iso-8859-1"),
				lambda: self.rfcPlayer.getScheduledCity(self.selectedCity).getCulture(self.selectedCultureCiv),
				lambda i: self.rfcPlayer.getScheduledCity(self.selectedCity).setCulture(self.selectedCultureCiv, i))
			self.y += 30
			self.addList("CityCulture", gc.getNumCivilizationInfos(), xres / 4 - 40, yres - self.y - 60, "TXT_KEY_CONCEPT_CULTURE",
				lambda i: True,
				lambda i: (yellowText, positiveText)[self.selectedCultureCiv == i]
					+ self.getCivName(i)
					+ ": "
					+ str(self.rfcPlayer.getScheduledCity(self.selectedCity).getCulture(i)),
				lambda i: gc.getCivilizationInfo(i).getButton(),
				7872)

			self.y = yres - 50
			self.addActionButton("CityDestroy", "TXT_KEY_WB_DELETE",
					self.destroySelectedCity)
			

			self.y = yres / 2 + 20
			self.x = xres / 2 + xres / 8 + 10
			self.addList("CityReligions", gc.getNumReligionInfos(), xres / 8 - 25, yres / 4 - 60, "TXT_KEY_PEDIA_CATEGORY_RELIGION",
				lambda i: True,
				lambda i: (yellowText, positiveText)[self.rfcPlayer.getScheduledCity(self.selectedCity).getReligion(i)]
					+ gc.getReligionInfo(i).getDescription(),
				lambda i: gc.getReligionInfo(i).getButton(),
				7869)

			self.x += xres / 8 - 5
			self.addList("HolyCityReligions", gc.getNumReligionInfos(), xres / 8 - 25, yres / 4 - 60, "TXT_KEY_WB_HOLY_CITY",
				lambda i: True,
				lambda i: (yellowText, positiveText)[self.rfcPlayer.getScheduledCity(self.selectedCity).getHolyCityReligion(i)]
					+ gc.getReligionInfo(i).getDescription(),
				lambda i: gc.getReligionInfo(i).getButton(),
				7869)

			self.x += xres / 8 - 5
			self.addList("CityBuildings", gc.getNumBuildingInfos(), xres / 8 - 5, yres - 50 - self.y, "TXT_KEY_WB_BUILDINGS",
				lambda i: True,
				lambda i: (yellowText, positiveText)[self.rfcPlayer.getScheduledCity(self.selectedCity).getNumBuilding(i) > 0]
					+ gc.getBuildingInfo(i).getDescription(),
				lambda i: gc.getBuildingInfo(i).getButton(),
				7870)

	def destroySelectedUnit(self):
		self.rfcPlayer.removeScheduledUnit(self.selectedUnit)
		self.selectedUnit -= 1

	def destroySelectedCity(self):
		self.rfcPlayer.removeScheduledCity(self.selectedCity)
		self.selectedCity -= 1

	def moveSelectedUnit(self):
		self.pbscreen.iPlayerAddMode = "MoveRFCUnit"
		self.screen.hideScreen()
		self.noRefresh = True

	def moveSelectedCity(self):
		self.pbscreen.iPlayerAddMode = "MoveRFCCity"
		self.screen.hideScreen()
		self.noRefresh = True

	def scheduledUnitStr(self, i):
		if self.rfcPlayer.getScheduledUnit(i).getUnitType() != UnitTypes.NO_UNIT:
			return gc.getUnitInfo(self.rfcPlayer.getScheduledUnit(i).getUnitType()).getDescription() + " x" + str(self.rfcPlayer.getScheduledUnit(i).getAmount()) + " (" + StringUtils.getStrForYear(self.rfcPlayer.getScheduledUnit(i).getYear()) + ")"
		else:
			return "Invalid"

	def getCivName(self, i):
		return CyTranslator().getText(gc.getCivilizationInfo(i).getShortDescriptionKey().encode("iso-8859-1"), ())

	def addStartingValues(self):
		self.x = 20
		self.y += 20
		self.addChangeButtons("StartingGold", "TXT_KEY_WB_STARTING_GOLD", self.rfcPlayer.getStartingGold, self.rfcPlayer.setStartingGold)
		self.y += 20
		self.addChangeButtons("StartingYear", "TXT_KEY_WB_STARTING_YEAR", self.rfcPlayer.getStartingYear, self.rfcPlayer.setStartingYear)
		self.y += 20
		self.addModifiers()

	def addModifiers(self):
		self.y += 20
		self.addChangeButtons("CompactEmpireModifier", "TXT_KEY_WB_COMPACT_EMPIRE_MODIFIER", self.rfcPlayer.getCompactEmpireModifier, self.rfcPlayer.setCompactEmpireModifier)
		self.y += 20
		self.addChangeButtons("UnitUpkeepModifier", "TXT_KEY_WB_UNIT_UPKEEP_MODIFIER", self.rfcPlayer.getUnitUpkeepModifier, self.rfcPlayer.setUnitUpkeepModifier)
		self.y += 20
		self.addChangeButtons("ResearchModifier", "TXT_KEY_WB_RESEARCH_MODIFIER", self.rfcPlayer.getResearchModifier, self.rfcPlayer.setResearchModifier)
		self.y += 20
		self.addChangeButtons("DistanceMaintenanceModifier", "TXT_KEY_WB_DISTANCE_MAINTENANCE_MODIFIER", self.rfcPlayer.getDistanceMaintenanceModifier, self.rfcPlayer.setDistanceMaintenanceModifier)
		self.y += 20
		self.addChangeButtons("NumCitiesMaintenanceModifier", "TXT_KEY_WB_NUM_CITIES_MAINTENANCE_MODIFIER", self.rfcPlayer.getNumCitiesMaintenanceModifier, self.rfcPlayer.setNumCitiesMaintenanceModifier)
		self.y += 20
		self.addChangeButtons("UnitProductionModifier", "TXT_KEY_WB_UNIT_PRODUCTION_MODIFIER", self.rfcPlayer.getUnitProductionModifier, self.rfcPlayer.setUnitProductionModifier)
		self.y += 20
		self.addChangeButtons("CivicUpkeepModifier", "TXT_KEY_WB_CIVIC_UPKEEP_MODIFIER", self.rfcPlayer.getCivicUpkeepModifier, self.rfcPlayer.setCivicUpkeepModifier)
		self.y += 20
		self.addChangeButtons("HealthBonusModifier", "TXT_KEY_WB_HEALTH_BONUS_MODIFIER", self.rfcPlayer.getHealthBonusModifier, self.rfcPlayer.setHealthBonusModifier)
		self.y += 20
		self.addChangeButtons("BuildingProductionModifier", "TXT_KEY_WB_BUILDING_PRODUCTION_MODIFIER", self.rfcPlayer.getBuildingProductionModifier, self.rfcPlayer.setBuildingProductionModifier)
		self.y += 20
		self.addChangeButtons("WonderProductionModifier", "TXT_KEY_WB_WONDER_PRODUCTION_MODIFIER", self.rfcPlayer.getWonderProductionModifier, self.rfcPlayer.setWonderProductionModifier)
		self.y += 20
		self.addChangeButtons("GreatPeopleModifier", "TXT_KEY_WB_GREAT_PEOPLE_MODIFIER", self.rfcPlayer.getGreatPeopleModifier, self.rfcPlayer.setGreatPeopleModifier)
		self.y += 20
		self.addChangeButtons("InflationModifier", "TXT_KEY_WB_INFLATION_MODIFIER", self.rfcPlayer.getInflationModifier, self.rfcPlayer.setInflationModifier)
		self.y += 20
		self.addChangeButtons("GrowthModifier", "TXT_KEY_WB_GROWTH_MODIFIER", self.rfcPlayer.getGrowthModifier, self.rfcPlayer.setGrowthModifier)
	
	def addChangeButtons(self, name, txtkey, getter, setter):
		ox = self.x
		self.addPlusButton(name + "Plus")
		self.x += 25
		self.addMinusButton(name + "Minus")
		self.x += 30
		self.y += 1
		self.addText(name + "Text", CyTranslator().getText(txtkey, ()) + ": " + str(getter()))
		self.changeButtons[name] = {};
		self.changeButtons[name]['get'] = getter
		self.changeButtons[name]['set'] = setter
		self.x = ox

	def addDropdown(self, name, size, current, minimum, maximum, pulldownNext, pulldownName):
		self.screen.addDropDownBoxGFC(name, self.x, self.y, size, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = minimum
		while i < maximum:
			self.screen.addPullDownString(name, pulldownName(i), i, i, i == current)
			i = pulldownNext(i)

	def addText(self, name, text):
		self.screen.setText(name, "Background", text, CvUtil.FONT_LEFT_JUSTIFY, self.x, self.y, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def addPlusButton(self, name):
		self.addTextButton(name, "+", 24, 24, ButtonStyles.BUTTON_STYLE_CITY_PLUS)

	def addMinusButton(self, name):
		self.addTextButton(name, "-", 24, 24, ButtonStyles.BUTTON_STYLE_CITY_MINUS)

	def addTextButton(self, name, text, w, h, style):
		self.screen.setButtonGFC(name, CyTranslator().getText(text, ()), "", self.x, self.y, w, h, WidgetTypes.WIDGET_GENERAL, -1, -1, style)
	
	def addActionButton(self, name, textkey, action):
		self.addTextButton(name, textkey, 120, 30, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.buttons[name] = action

	def addBooleanButton(self, name, textkey, getter, setter):
		if getter():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		else:
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		self.screen.setText(name, "Background", sColor + CyTranslator().getText(textkey, ()) + "</color>", CvUtil.FONT_LEFT_JUSTIFY, self.x, self.y, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.booleanButtons[name] = {}
		self.booleanButtons[name]['get'] = getter
		self.booleanButtons[name]['set'] = setter

	def addList(self, name, items, w, h, title, showItem, itemText, itemButton, tableid):
		self.screen.addTableControlGFC(name, 2, self.x, self.y, w, h, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		self.screen.setTableColumnHeader(name, 0, "", w)

		self.screen.appendTableRow(name)
		self.screen.setTableText(name, 0, 0, "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + CyTranslator().getText(title, ()) + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		row = 1
		for i in xrange(items):
			if not showItem(i): continue
			self.screen.appendTableRow(name)
			self.screen.setTableText(name, 0, row, "<font=3>" + itemText(i) + "</font></color>", itemButton(i), WidgetTypes.WIDGET_PYTHON, tableid, i, CvUtil.FONT_LEFT_JUSTIFY)
			row += 1


	def addTable(self, name, columns, items, w, h, colTitle, showItem, itemText, itemButton, tableid):
		self.screen.addTableControlGFC(name, columns, self.x, self.y, w, h, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in xrange(columns):
			self.screen.setTableColumnHeader(name, i, "", w / columns)

		maxRow = -1
		currentMaxRow = 0

		for i in xrange(columns):
			column = i % columns
			row = currentMaxRow
			if row > maxRow:
				self.screen.appendTableRow(name)
				maxRow = row
			self.screen.setTableText(name, column, row, "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + colTitle(i) + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

			for j in xrange(items):
				if not showItem(i, j): continue
				row += 1
				if row > maxRow:
					self.screen.appendTableRow(name)
					maxRow = row
				self.screen.setTableText(name, column, row, "<font=3>" + itemText(i, j) + "</font></color>", itemButton(j), WidgetTypes.WIDGET_PYTHON, tableid, j, CvUtil.FONT_LEFT_JUSTIFY)

			if i % columns == columns - 1 and i < columns - 1:
				self.screen.appendTableRow(name)
				currentMaxRow = maxRow + 2

	def getDropdownData(self, name):
		return self.screen.getPullDownData(name, self.screen.getSelectedPullDownID(name))

	def handleInput(self, inputClass):
		self.screen = CyGInterfaceScreen("WBRFCPlayerScreen", CvScreenEnums.WB_RFC_PLAYER)
		funcName = inputClass.getFunctionName()

		if funcName == "ChangeBy":
			self.change = self.getDropdownData("ChangeBy")
			self.noRefresh = True
		elif funcName == "CurrentRFCPlayer":
			self.civType = self.getDropdownData("CurrentRFCPlayer")
		elif funcName.endswith("Plus") and funcName.replace("Plus", "") in self.changeButtons:
			modifier = self.changeButtons[funcName.replace("Plus", "")]
			modifier['set'](modifier['get']() + self.change)
		elif funcName.endswith("Minus") and funcName.replace("Minus", "") in self.changeButtons:
			modifier = self.changeButtons[funcName.replace("Minus", "")]
			modifier['set'](modifier['get']() - self.change)
		elif funcName in self.booleanButtons:
			button = self.booleanButtons[funcName]
			button['set'](not button['get']())
		elif funcName == "WBRFCPlayerCivics":
			civic = inputClass.getData2()
			self.rfcPlayer.setStartingCivic(gc.getCivicInfo(civic).getCivicOptionType(), civic)
		elif funcName == "WBRFCPlayerWars":
			civ = inputClass.getData2()
			self.rfcPlayer.setStartingWar(civ, not self.rfcPlayer.isStartingWar(civ))
		elif funcName == "WBRFCPlayerTechs":
			tech = inputClass.getData2()
			self.rfcPlayer.setStartingTech(tech, not self.rfcPlayer.isStartingTech(tech))
		elif funcName == "WBRFCPlayerUnits":
			self.selectedUnit = inputClass.getData2()
			self.selectedCity = -1
		elif funcName == "WBRFCPlayerCities":
			self.selectedCity = inputClass.getData2()
			self.selectedUnit = -1
		elif funcName in self.buttons:
			self.buttons[funcName]()
		elif funcName == "UnitType":
			self.rfcPlayer.getScheduledUnit(self.selectedUnit).setUnitType(self.getDropdownData("UnitType"))
		elif funcName == "UnitAIType":
			self.rfcPlayer.getScheduledUnit(self.selectedUnit).setUnitAIType(self.getDropdownData("UnitAIType"))
		elif funcName == "CityReligions":
			religion = inputClass.getData2()
			scheduledCity = self.rfcPlayer.getScheduledCity(self.selectedCity)
			if not religion: #avoid holy cities w/o religion
				scheduledCity.setHolyCityReligion(religion, True)

			scheduledCity.setReligion(religion,
				not scheduledCity.getReligion(religion))
		elif funcName == "HolyCityReligions":
			religion = inputClass.getData2()
			scheduledCity = self.rfcPlayer.getScheduledCity(self.selectedCity)
			if religion: #avoid holy cities w/o religion
				scheduledCity.setReligion(religion, True)

			scheduledCity.setHolyCityReligion(religion,
				not scheduledCity.getHolyCityReligion(religion))
		elif funcName == "CityBuildings":
			building = inputClass.getData2()
			scheduledCity = self.rfcPlayer.getScheduledCity(self.selectedCity)
			if scheduledCity.getNumBuilding(building) > 0:
				amount = 0
			else:
				amount = 1
			scheduledCity.setNumBuilding(building, amount)
		elif funcName == "CityCulture":
			self.selectedCultureCiv = inputClass.getData2()

		if self.noRefresh:
			self.noRefresh = False
		else:
			self.interfaceScreen(self.civType)

		return 1

	def update(self, fDelta):
		return 1

rfcPlayerScreen = WBRFCPlayerScreen()
