#Author: bluepotato
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPlatyBuilderScreen
import StringUtils
gc = CyGlobalContext()

class WBRFCProvinceScreen:
	def __init__(self):
		self.provinceType = 0
		self.change = 1
		self.screen = None
		self.rfcProvince = None
		self.buttons = {}
		self.changeButtons = {}
		self.booleanButtons = {}
		self.selectedUnit = -1
		self.pbscreen = None
		self.noRefresh = False

	def interfaceScreen(self):
		self.screen = CyGInterfaceScreen("WBRFCProvinceScreen", CvScreenEnums.WB_RFC_PROVINCE)
		if self.provinceType >= CyRiseFall().getNumProvinces():
			self.provinceType = CyRiseFall().getNumProvinces() - 1
		self.rfcProvince = CyRiseFall().getProvince(self.provinceType)

		yellowText = CyTranslator().getText("[COLOR_YELLOW]", ())
		positiveText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		negativeText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())

		xres = self.screen.getXResolution()
		yres = self.screen.getYResolution()
		self.screen.setRenderInterfaceOnly(True)
		self.screen.addPanel("MainBG", u"", u"", True, False, -10, -10, xres + 20, yres + 20, PanelStyles.PANEL_STYLE_MAIN)
		self.screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		self.screen.setText("RFCProvinceExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xres - 30, yres - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		self.y = 20
		self.x = 20

		self.addDropdown("CurrentRFCProvince", xres/5, self.provinceType, 0, CyRiseFall().getNumProvinces(),
			lambda i: i + 1,
			lambda i: ("*", "")[gc.getRiseFall().getProvince(i).getNumPlots() > 0] + self.getProvinceName(i))

		self.y += 30
		self.addDropdown("ChangeBy", xres / 5, self.change, 1, 1000001,
			lambda i: i * (5, 2)[str(i)[0] == "1"],
			lambda i: "(+/-) " + str(i))

		self.y += 40
		self.addText("ProvincePlotsText", CyTranslator().getText("TXT_KEY_WB_PLOTS", (self.rfcProvince.getNumPlots(),)))
		self.y += 20
		self.addText("ProvinceTypeText", CyTranslator().getText("TXT_KEY_WB_TYPE", (self.rfcProvince.getType(),)))
		self.y += 20
		self.addActionButton("ChangeProvinceType", "TXT_KEY_WB_CHANGE", self.changeProvinceType)
		self.y += 40
		self.addList("CoreProvince", gc.getNumCivilizationInfos(), xres / 4 - 20, yres / 4 + yres / 8 - 60, "TXT_KEY_WB_CORE_PROVINCE_OF",
			lambda i: not gc.getRiseFall().getRFCPlayer(i).isMinor(),
			lambda i: (yellowText, positiveText)[self.isCoreOf(i)] + self.getCivName(i),
			lambda i: gc.getCivilizationInfo(i).getButton(),
			7872)

		self.y = yres - 60
		self.addActionButton("ProvinceDelete", "TXT_KEY_WB_DELETE",
			self.deleteProvince)
		self.y -= 40
		self.addActionButton("ProvinceAdd", "TXT_KEY_WB_NEW",
			self.addProvince)

		self.x = xres / 2 + 20
		self.y = 20
		self.addList("WBRFCProvinceUnits", self.rfcProvince.getNumScheduledUnits(), xres / 2 - 30, yres / 2 - 10, "TXT_KEY_WB_SCHEDULED_UNITS",
			lambda i: True,
			lambda i: (yellowText, positiveText)[self.selectedUnit == i] + self.scheduledUnitStr(i),
			lambda i: (self.rfcProvince.getScheduledUnit(i).getUnitType() != UnitTypes.NO_UNIT and gc.getUnitInfo(self.rfcProvince.getScheduledUnit(i).getUnitType()).getButton() or None),
			8211)

		self.y = yres / 2 + 20
		self.x = xres / 2 + 20

		def addScheduledUnit():
			unit = self.rfcProvince.addScheduledUnit()
			unit.setUnitType(0)
			unit.setAmount(1)
			unit.setSpawnFrequency(1)
			unit.setYear(gc.getGame().getGameTurnYear())
			self.selectedUnit = self.rfcProvince.getNumScheduledUnits() - 1

		self.addActionButton("AddScheduledUnit", "TXT_KEY_WB_ADD_UNIT", addScheduledUnit)
		self.y += 40

		if self.rfcProvince.getNumScheduledUnits() <= self.selectedUnit:
			self.selectedUnit = -1

		if self.selectedUnit != -1:
			self.addDropdown("UnitType", xres/5, self.rfcProvince.getScheduledUnit(self.selectedUnit).getUnitType(), 0, gc.getNumUnitInfos(),
				lambda i: i + 1,
				lambda i: gc.getUnitInfo(i).getDescription())
			self.y += 40
			self.addDropdown("UnitAIType", xres/5, self.rfcProvince.getScheduledUnit(self.selectedUnit).getUnitAIType(), 0, UnitAITypes.NUM_UNITAI_TYPES,
				lambda i: i + 1,
				lambda i: gc.getUnitAIInfo(i).getType())
			self.y += 40
			self.addChangeButtons("UnitYear", "TXT_KEY_WB_YEAR",
				self.rfcProvince.getScheduledUnit(self.selectedUnit).getYear,
				self.rfcProvince.getScheduledUnit(self.selectedUnit).setYear)
			self.y += 20
			self.addChangeButtons("UnitAmount", "TXT_KEY_WB_AMOUNT",
				self.rfcProvince.getScheduledUnit(self.selectedUnit).getAmount,
				self.rfcProvince.getScheduledUnit(self.selectedUnit).setAmount)
			self.y += 20
			self.addChangeButtons("UnitSpawnFrequency", "TXT_KEY_WB_SPAWN_FREQUENCY",
				self.rfcProvince.getScheduledUnit(self.selectedUnit).getSpawnFrequency,
				self.rfcProvince.getScheduledUnit(self.selectedUnit).setSpawnFrequency)
			self.y += 30
			self.y = yres - 60
			self.addActionButton("UnitDestroy", "TXT_KEY_WB_DELETE",
					self.destroySelectedUnit)

	def isCoreOf(self, civType):
		rfcPlayer = CyRiseFall().getRFCPlayer(civType)
		for i in xrange(rfcPlayer.getNumCoreProvinces()):
			if self.provinceType == rfcPlayer.getCoreProvince(i):
				return True
		return False

	def toggleCore(self, civType):
		rfcPlayer = CyRiseFall().getRFCPlayer(civType)
		for i in xrange(rfcPlayer.getNumCoreProvinces()):
			if self.provinceType == rfcPlayer.getCoreProvince(i):
				rfcPlayer.removeCoreProvince(i)
				return

		rfcPlayer.addCoreProvince(self.provinceType)

	def getCivName(self, i):
		return CyTranslator().getText(gc.getCivilizationInfo(i).getShortDescriptionKey().encode("iso-8859-1"), ())

	def addProvince(self):
		gc.getRiseFall().addProvince("PROVINCE_UNKNOWN")
		self.provinceType = gc.getRiseFall().getNumProvinces() - 1
		self.changeProvinceType()

	def deleteProvince(self):
		gc.getRiseFall().removeProvince(self.provinceType)

	def changeProvinceType(self):
		self.screen.hideScreen()
		popupInfo = CyPopupInfo()
		popupInfo.setData1(self.provinceType)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PROVINCE_TYPE)
		popupInfo.addPopup(CyGame().getActivePlayer())
		self.noRefresh = True

	def destroySelectedUnit(self):
		self.rfcProvince.removeScheduledUnit(self.selectedUnit)
		self.selectedUnit -= 1

	def scheduledUnitStr(self, i):
		if self.rfcProvince.getScheduledUnit(i).getUnitType() != UnitTypes.NO_UNIT:
			return gc.getUnitInfo(self.rfcProvince.getScheduledUnit(i).getUnitType()).getDescription() + " x" + str(self.rfcProvince.getScheduledUnit(i).getAmount()) + " (" + StringUtils.getStrForYear(self.rfcProvince.getScheduledUnit(i).getYear()) + ")"
		else:
			return "Invalid"

	def getProvinceName(self, i):
		return CyRiseFall().getProvince(i).getName()

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
		self.screen = CyGInterfaceScreen("WBRFCProvinceScreen", CvScreenEnums.WB_RFC_PROVINCE)
		funcName = inputClass.getFunctionName()

		if funcName == "ChangeBy":
			self.change = self.getDropdownData("ChangeBy")
			self.noRefresh = True
		elif funcName == "CurrentRFCProvince":
			self.provinceType = self.getDropdownData("CurrentRFCProvince")
		elif funcName.endswith("Plus") and funcName.replace("Plus", "") in self.changeButtons:
			modifier = self.changeButtons[funcName.replace("Plus", "")]
			modifier['set'](modifier['get']() + self.change)
		elif funcName.endswith("Minus") and funcName.replace("Minus", "") in self.changeButtons:
			modifier = self.changeButtons[funcName.replace("Minus", "")]
			modifier['set'](modifier['get']() - self.change)
		elif funcName in self.booleanButtons:
			button = self.booleanButtons[funcName]
			button['set'](not button['get']())
		elif funcName == "WBRFCProvinceUnits":
			self.selectedUnit = inputClass.getData2()
		elif funcName in self.buttons:
			self.buttons[funcName]()
		elif funcName == "UnitType":
			self.rfcProvince.getScheduledUnit(self.selectedUnit).setUnitType(self.getDropdownData("UnitType"))
		elif funcName == "UnitAIType":
			self.rfcProvince.getScheduledUnit(self.selectedUnit).setUnitAIType(self.getDropdownData("UnitAIType"))
		elif funcName == "CoreProvince":
			self.toggleCore(inputClass.getData2())

		if not self.noRefresh:
			self.interfaceScreen()
		else:
			self.noRefresh = False

		return 1

	def update(self, fDelta):
		return 1

rfcProvinceScreen = WBRFCProvinceScreen()
