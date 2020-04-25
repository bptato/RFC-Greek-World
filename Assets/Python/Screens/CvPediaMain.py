# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import string

import CvUtil
import ScreenInput
import CvScreenEnums

import CvPediaScreen
import CvPediaTech
import CvPediaUnit
import CvPediaBuilding
import CvPediaPromotion
import CvPediaUnitChart
import CvPediaBonus
import CvPediaTerrain
import CvPediaFeature
import CvPediaImprovement
import CvPediaCivic
import CvPediaCivilization
import CvPediaLeader
import CvPediaSpecialist
import CvPediaHistory
import CvPediaProject
import CvPediaReligion
import CvPediaCorporation

import UnitUpgradesGraph


gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaMain(CvPediaScreen.CvPediaScreen):

	def __init__(self):
		self.bSortLists = True

		self.PEDIA_MAIN_SCREEN	= "PediaMainScreen"
		self.INTERFACE_ART_INFO	= "SCREEN_BG_OPAQUE"

		self.WIDGET_ID		= "PediaMainWidget"
		self.BACKGROUND_ID	= "PediaMainBackground"
		self.TOP_PANEL_ID	= "PediaMainTopPanel"
		self.BOT_PANEL_ID	= "PediaMainBottomPanel"
		self.HEAD_ID		= "PediaMainHeader"
		self.BACK_ID		= "PediaMainBack"
		self.NEXT_ID		= "PediaMainForward"
		self.EXIT_ID		= "PediaMainExit"
		self.CATEGORY_LIST_ID	= "PediaMainCategoryList"
		self.ITEM_LIST_ID	= "PediaMainItemList"
		self.UPGRADES_GRAPH_ID	= "PediaMainUpgradesGraph"

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.H_PANEL = 55
		self.BUTTON_SIZE = 64
		self.BUTTON_COLUMNS = 9
		self.ITEMS_MARGIN = 18
		self.ITEMS_SEPARATION = 2

		self.X_TOP_PANEL = 0
		self.Y_TOP_PANEL = 0
		self.W_TOP_PANEL = self.W_SCREEN
		self.H_TOP_PANEL = self.H_PANEL

		self.X_BOT_PANEL = 0
		self.Y_BOT_PANEL = self.H_SCREEN - self.H_PANEL
		self.W_BOT_PANEL = self.W_SCREEN
		self.H_BOT_PANEL = self.H_PANEL

		self.X_CATEGORIES = 0
		self.Y_CATEGORIES = (self.Y_TOP_PANEL + self.H_TOP_PANEL) - 4
		self.W_CATEGORIES = 175
		self.H_CATEGORIES = (self.Y_BOT_PANEL + 3) - self.Y_CATEGORIES

		self.X_ITEMS = self.X_CATEGORIES + self.W_CATEGORIES + 2
		self.Y_ITEMS = self.Y_CATEGORIES
		self.W_ITEMS = 210
		self.H_ITEMS = self.H_CATEGORIES

		self.X_PEDIA_PAGE = self.X_ITEMS + self.W_ITEMS + 18
		self.Y_PEDIA_PAGE = self.Y_ITEMS + 13
		self.R_PEDIA_PAGE = self.W_SCREEN - 20
		self.B_PEDIA_PAGE = self.Y_ITEMS + self.H_ITEMS - 16
		self.W_PEDIA_PAGE = self.R_PEDIA_PAGE - self.X_PEDIA_PAGE
		self.H_PEDIA_PAGE = self.B_PEDIA_PAGE - self.Y_PEDIA_PAGE

		self.X_TITLE = self.X_SCREEN
		self.Y_TITLE = 8
		self.X_BACK = 75
		self.Y_BACK = 730
		self.X_NEXT = 210
		self.Y_NEXT = 730
		self.X_EXIT = 994
		self.Y_EXIT = 730

		self.iActivePlayer = -1
		self.nWidgetCount = 0

		self.categoryList = []
		self.categoryGraphics = []
		self.iCategory = -1
		self.pediaHistory = []
		self.pediaFuture = []

		self.mapListGenerators = {
			CvScreenEnums.PEDIA_TECHS		: self.placeTechs,
			CvScreenEnums.PEDIA_UNITS		: self.placeUnits,
			CvScreenEnums.PEDIA_UNIT_UPGRADES	: self.placeUnitUpgrades,
			CvScreenEnums.PEDIA_UNIT_CATEGORIES	: self.placeUnitCategories,
			CvScreenEnums.PEDIA_PROMOTIONS		: self.placePromotions,
			CvScreenEnums.PEDIA_PROMOTION_TREE	: self.placePromotionTree,
			CvScreenEnums.PEDIA_BUILDINGS		: self.placeBuildings,
			CvScreenEnums.PEDIA_NATIONAL_WONDERS	: self.placeNationalWonders,
			CvScreenEnums.PEDIA_GREAT_WONDERS	: self.placeGreatWonders,
			CvScreenEnums.PEDIA_PROJECTS		: self.placeProjects,
			CvScreenEnums.PEDIA_SPECIALISTS		: self.placeSpecialists,
			CvScreenEnums.PEDIA_TERRAINS		: self.placeTerrains,
			CvScreenEnums.PEDIA_FEATURES		: self.placeFeatures,
			CvScreenEnums.PEDIA_BONUSES		: self.placeBonuses,
			CvScreenEnums.PEDIA_IMPROVEMENTS	: self.placeImprovements,
			CvScreenEnums.PEDIA_CIVS		: self.placeCivs,
			CvScreenEnums.PEDIA_LEADERS		: self.placeLeaders,
			CvScreenEnums.PEDIA_CIVICS		: self.placeCivics,
			CvScreenEnums.PEDIA_RELIGIONS		: self.placeReligions,
			CvScreenEnums.PEDIA_CORPORATIONS	: self.placeCorporations,
			CvScreenEnums.PEDIA_CONCEPTS		: self.placeConcepts,
			CvScreenEnums.PEDIA_BTS_CONCEPTS	: self.placeBTSConcepts,
			CvScreenEnums.PEDIA_HINTS		: self.placeHints,
			}

		self.mapScreenFunctions = {
			CvScreenEnums.PEDIA_TECHS		: CvPediaTech.CvPediaTech(self),
			CvScreenEnums.PEDIA_UNITS		: CvPediaUnit.CvPediaUnit(self),
			CvScreenEnums.PEDIA_UNIT_CATEGORIES	: CvPediaUnitChart.CvPediaUnitChart(self),
			CvScreenEnums.PEDIA_PROMOTIONS		: CvPediaPromotion.CvPediaPromotion(self),
			CvScreenEnums.PEDIA_BUILDINGS		: CvPediaBuilding.CvPediaBuilding(self),
			CvScreenEnums.PEDIA_NATIONAL_WONDERS	: CvPediaBuilding.CvPediaBuilding(self),
			CvScreenEnums.PEDIA_GREAT_WONDERS	: CvPediaBuilding.CvPediaBuilding(self),
			CvScreenEnums.PEDIA_PROJECTS		: CvPediaProject.CvPediaProject(self),
			CvScreenEnums.PEDIA_SPECIALISTS		: CvPediaSpecialist.CvPediaSpecialist(self),
			CvScreenEnums.PEDIA_TERRAINS		: CvPediaTerrain.CvPediaTerrain(self),
			CvScreenEnums.PEDIA_FEATURES		: CvPediaFeature.CvPediaFeature(self),
			CvScreenEnums.PEDIA_BONUSES		: CvPediaBonus.CvPediaBonus(self),
			CvScreenEnums.PEDIA_IMPROVEMENTS	: CvPediaImprovement.CvPediaImprovement(self),
			CvScreenEnums.PEDIA_CIVS		: CvPediaCivilization.CvPediaCivilization(self),
			CvScreenEnums.PEDIA_LEADERS		: CvPediaLeader.CvPediaLeader(self),
			CvScreenEnums.PEDIA_CIVICS		: CvPediaCivic.CvPediaCivic(self),
			CvScreenEnums.PEDIA_RELIGIONS		: CvPediaReligion.CvPediaReligion(self),
			CvScreenEnums.PEDIA_CORPORATIONS	: CvPediaCorporation.CvPediaCorporation(self),
			CvScreenEnums.PEDIA_CONCEPTS		: CvPediaHistory.CvPediaHistory(self),
			CvScreenEnums.PEDIA_BTS_CONCEPTS	: CvPediaHistory.CvPediaHistory(self),
			}

		self.pediaBuilding	= CvPediaBuilding.CvPediaBuilding(self)
		self.pediaLeader	= CvPediaLeader.CvPediaLeader(self)



	def getScreen(self):
		return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN, CvScreenEnums.PEDIA_MAIN)



	def pediaShow(self):
		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.iCategory = -1
		if (not self.pediaHistory):
			self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_TECHS))
		current = self.pediaHistory.pop()
		self.pediaFuture = []
		self.pediaHistory = []
		self.pediaJump(current[0], current[1], False, True)



	def pediaJump(self, iCategory, iItem, bRemoveFwdList, bIsLink):
		if (self.pediaHistory == [] or iCategory != CvScreenEnums.PEDIA_MAIN or iItem == CvScreenEnums.PEDIA_UNIT_UPGRADES or iItem == CvScreenEnums.PEDIA_PROMOTION_TREE or iItem == CvScreenEnums.PEDIA_HINTS):
			self.pediaHistory.append((iCategory, iItem))
		if (bRemoveFwdList):
			self.pediaFuture = []

		screen = self.getScreen()
		if not screen.isActive():
			self.deleteAllWidgets()
			self.setPediaCommonWidgets()
			self.placeCategories()

		if (iCategory == CvScreenEnums.PEDIA_MAIN):
			screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iItem - (CvScreenEnums.PEDIA_MAIN + 1))
			self.deleteAllWidgets()
			self.mapListGenerators.get(iItem)()
			self.iCategory = iItem
			return

		if (iCategory == CvScreenEnums.PEDIA_BUILDINGS):
			iCategory = iCategory + self.pediaBuilding.getBuildingType(iItem)

		if (iCategory != self.iCategory):
			screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iCategory - (CvScreenEnums.PEDIA_MAIN + 1))

		if (iCategory != self.iCategory or bIsLink):
			self.mapListGenerators.get(iCategory)()

		if (iCategory != CvScreenEnums.PEDIA_UNIT_UPGRADES and iCategory != CvScreenEnums.PEDIA_PROMOTION_TREE and iCategory != CvScreenEnums.PEDIA_HINTS):
			screen.enableSelect(self.ITEM_LIST_ID, True)
			if (iCategory != self.iCategory or bIsLink):
				i = 0
				for item in self.list:
					if (item[1] == iItem):
						screen.selectRow(self.ITEM_LIST_ID, i, True)
					i += 1

		if (iCategory != self.iCategory):
			self.iCategory = iCategory

		self.deleteAllWidgets()
		func = self.mapScreenFunctions.get(iCategory)
		func.interfaceScreen(iItem)



	def setPediaCommonWidgets(self):
		self.HEAD_TEXT = u"<font=4b>" + localText.getText("TXT_KEY_WIDGET_HELP",          ())         + u"</font>"
		self.BACK_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK",    ()).upper() + u"</font>"
		self.NEXT_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + u"</font>"
		self.EXIT_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT",    ()).upper() + u"</font>"

		self.szCategoryTechs		= localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
		self.szCategoryUnits		= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
		self.szCategoryUnitUpgrades	= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_UPGRADES", ())
		self.szCategoryUnitCategories	= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ())
		self.szCategoryPromotions	= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
		self.szCategoryPromotionTree	= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION_TREE", ())
		self.szCategoryBuildings	= localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		self.szCategoryNationalWonders	= localText.getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ())
		self.szCategoryGreatWonders	= localText.getText("TXT_KEY_PEDIA_CATEGORY_GREAT_WONDERS", ())
		self.szCategoryProjects		= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
		self.szCategorySpecialists	= localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())
		self.szCategoryTerrains		= localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
		self.szCategoryFeatures		= localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
		self.szCategoryBonuses		= localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
		self.szCategoryImprovements	= localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
		self.szCategoryCivs		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
		self.szCategoryLeaders		= localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
		self.szCategoryCivics		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
		self.szCategoryReligions	= localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
		self.szCategoryCorporations	= localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
		self.szCategoryConcepts		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ())
		self.szCategoryConceptsNew	= localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_NEW", ())
		self.szCategoryHints		= localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())

		self.categoryList = [
			["TECHS",	self.szCategoryTechs],
			["UNITS",	self.szCategoryUnits],
			["UNITS",	self.szCategoryUnitUpgrades],
			["UNITS",	self.szCategoryUnitCategories],
			["PROMOTIONS",	self.szCategoryPromotions],
			["PROMOTIONS",	self.szCategoryPromotionTree],
			["BUILDINGS",	self.szCategoryBuildings],
			["BUILDINGS",	self.szCategoryNationalWonders],
			["BUILDINGS",	self.szCategoryGreatWonders],
			["BUILDINGS",	self.szCategoryProjects],
			["SPECIALISTS",	self.szCategorySpecialists],
			["TERRAINS",	self.szCategoryTerrains],
			["TERRAINS",	self.szCategoryFeatures],
			["TERRAINS",	self.szCategoryBonuses],
			["TERRAINS",	self.szCategoryImprovements],
			["CIVS",	self.szCategoryCivs],
			["CIVS",	self.szCategoryLeaders],
			["CIVICS",	self.szCategoryCivics],
			["CIVICS",	self.szCategoryReligions],
			["CIVICS",	self.szCategoryCorporations],
			["HINTS",	self.szCategoryConcepts],
			["HINTS",	self.szCategoryConceptsNew],
			["HINTS",	self.szCategoryHints],
			]

		self.categoryGraphics = {
			"TECHS"		: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()),
			"UNITS"		: u"%c  " %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)),
			"PROMOTIONS"	: u"%c  " %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)),
			"BUILDINGS"	: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()),
			"SPECIALISTS"	: u"%c  " %(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)),
			"TERRAINS"	: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()),
			"CIVS"		: u"%c  " %(CyGame().getSymbolID(FontSymbols.MAP_CHAR)),
			"CIVICS"	: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()),
			"HINTS"		: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()),
			}

		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True)
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel(self.BOT_PANEL_ID, u"", u"", True, False, self.X_BOT_PANEL, self.Y_BOT_PANEL, self.W_BOT_PANEL, self.H_BOT_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		screen.setText(self.HEAD_ID, "Background", self.HEAD_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,      -1, -1)
		screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY,   self.X_BACK,  self.Y_BACK,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK,    1, -1)
		screen.setText(self.NEXT_ID, "Background", self.NEXT_TEXT, CvUtil.FONT_LEFT_JUSTIFY,   self.X_NEXT,  self.Y_NEXT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY,  self.X_EXIT,  self.Y_EXIT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		screen.addListBoxGFC(self.CATEGORY_LIST_ID, "", self.X_CATEGORIES, self.Y_CATEGORIES, self.W_CATEGORIES, self.H_CATEGORIES, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.CATEGORY_LIST_ID, True)
		screen.setStyle(self.CATEGORY_LIST_ID, "Table_StandardCiv_Style")



	def placeCategories(self):
		screen = self.getScreen()
		screen.clearListBoxGFC(self.CATEGORY_LIST_ID)
		i = 1
		for category in self.categoryList:
			graphic = self.categoryGraphics[category[0]]
			screen.appendListBoxStringNoUpdate(self.CATEGORY_LIST_ID, graphic + category[1], WidgetTypes.WIDGET_PEDIA_MAIN, CvScreenEnums.PEDIA_MAIN + i, 0, CvUtil.FONT_LEFT_JUSTIFY)
			i += 1
		screen.updateListBox(self.CATEGORY_LIST_ID)



	def placeTechs(self):
		self.list = self.getSortedList(gc.getNumTechInfos(), gc.getTechInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, gc.getTechInfo)


	def placeUnits(self):
		self.list = self.getSortedList(gc.getNumUnitInfos(), gc.getUnitInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)


	def placeUnitUpgrades(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.UnitUpgradesGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()


	def placeUnitCategories(self):
		self.list = self.getSortedList(gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, gc.getUnitCombatInfo)


	def placePromotions(self):
		self.list = self.getSortedList(gc.getNumPromotionInfos(), gc.getPromotionInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getPromotionInfo)


	def placePromotionTree(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.PromotionsGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()


	def placeBuildings(self):
		self.list = self.pediaBuilding.getBuildingSortedList(0)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeNationalWonders(self):
		self.list = self.pediaBuilding.getBuildingSortedList(1)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeGreatWonders(self):
		self.list = self.pediaBuilding.getBuildingSortedList(2)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeProjects(self):
		self.list = self.getSortedList(gc.getNumProjectInfos(), gc.getProjectInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, gc.getProjectInfo)


	def placeSpecialists(self):
		self.list = self.getSortedList(gc.getNumSpecialistInfos(), gc.getSpecialistInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, gc.getSpecialistInfo)


	def placeTerrains(self):
		self.list = self.getSortedList(gc.getNumTerrainInfos(), gc.getTerrainInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, gc.getTerrainInfo)


	def placeFeatures(self):
		self.list = self.getSortedList(gc.getNumFeatureInfos(), gc.getFeatureInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, gc.getFeatureInfo)


	def placeBonuses(self):
		self.list = self.getSortedList(gc.getNumBonusInfos(), gc.getBonusInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, gc.getBonusInfo)


	def placeImprovements(self):
		self.list = self.getSortedList(gc.getNumImprovementInfos(), gc.getImprovementInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, gc.getImprovementInfo)


	def placeCivs(self):
		self.list = self.getSortedList(gc.getNumCivilizationInfos(), gc.getCivilizationInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getCivilizationInfo)


	def placeLeaders(self):
		self.list = self.getSortedList(gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, gc.getLeaderHeadInfo)


	def placeCivics(self):
		self.list = self.getSortedList(gc.getNumCivicInfos(), gc.getCivicInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, gc.getCivicInfo)


	def placeReligions(self):
		self.list = self.getSortedList(gc.getNumReligionInfos(), gc.getReligionInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, gc.getReligionInfo)


	def placeCorporations(self):
		self.list = self.getSortedList(gc.getNumCorporationInfos(), gc.getCorporationInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, gc.getCorporationInfo)


	def placeConcepts(self):
		self.list = self.getSortedList(gc.getNumConceptInfos(), gc.getConceptInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, gc.getConceptInfo)


	def placeBTSConcepts(self):
		self.list = self.getSortedList(gc.getNumNewConceptInfos(), gc.getNewConceptInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, gc.getNewConceptInfo)


	def placeItems(self, widget, info):
		screen = self.getScreen()
		screen.clearListBoxGFC(self.ITEM_LIST_ID)

		screen.addTableControlGFC(self.ITEM_LIST_ID, 1, self.X_ITEMS, self.Y_ITEMS, self.W_ITEMS, self.H_ITEMS, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.ITEM_LIST_ID, False)
		screen.setStyle(self.ITEM_LIST_ID, "Table_StandardCiv_Style")
		screen.setTableColumnHeader(self.ITEM_LIST_ID, 0, "", self.W_ITEMS)

		i = 0
		for item in self.list:
			if (info == gc.getConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT
				data2 = item[1]
			elif (info == gc.getNewConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			else:
				data1 = item[1]
				data2 = 1
			screen.appendTableRow(self.ITEM_LIST_ID)
			screen.setTableText(self.ITEM_LIST_ID, 0, i, u"<font=3>" + item[0] + u"</font>", info(item[1]).getButton(), widget, data1, data2, CvUtil.FONT_LEFT_JUSTIFY)
			i += 1
		screen.updateListBox(self.ITEM_LIST_ID)


	def placeHints(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		szHintBox = self.getNextWidgetName()
		screen.addListBoxGFC(szHintBox, "", self.X_ITEMS, self.Y_PEDIA_PAGE - 10, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 23, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szHintBox, False)
		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split(szHintsText, "\n")
		for hint in hintText:
			if len(hint) != 0:
				screen.appendListBoxStringNoUpdate(szHintBox, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(szHintBox)



	def back(self):
		if (len(self.pediaHistory) > 1):
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def forward(self):
		if (self.pediaFuture):
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def link(self, szLink):
		if (szLink == "PEDIA_MAIN_TECH"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_TECHS, True, True)
		elif (szLink == "PEDIA_MAIN_UNIT"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_UNITS, True, True)
		elif (szLink == "PEDIA_MAIN_UNIT_GROUP"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_UNIT_CATEGORIES, True, True)
		elif (szLink == "PEDIA_MAIN_PROMOTION"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_PROMOTIONS, True, True)
		elif (szLink == "PEDIA_MAIN_BUILDING"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_BUILDINGS, True, True)
		elif (szLink == "PEDIA_MAIN_PROJECT"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_PROJECTS, True, True)
		elif (szLink == "PEDIA_MAIN_SPECIALIST"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_SPECIALISTS, True, True)
		elif (szLink == "PEDIA_MAIN_TERRAIN"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_TERRAINS, True, True)
		elif (szLink == "PEDIA_MAIN_FEATURE"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_FEATURES, True, True)
		elif (szLink == "PEDIA_MAIN_BONUS"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_BONUSES, True, True)
		elif (szLink == "PEDIA_MAIN_IMPROVEMENT"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_IMPROVEMENTS, True, True)
		elif (szLink == "PEDIA_MAIN_CIV"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_CIVS, True, True)
		elif (szLink == "PEDIA_MAIN_LEADER"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_LEADERS, True, True)
		elif (szLink == "PEDIA_MAIN_CIVIC"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_CIVICS, True, True)
		elif (szLink == "PEDIA_MAIN_RELIGION"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_RELIGIONS, True, True)
		elif (szLink == "PEDIA_MAIN_CONCEPT"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_CONCEPTS, True, True)
		elif (szLink == "PEDIA_MAIN_HINTS"):
			self.pediaJump(CvScreenEnums.PEDIA_MAIN, CvScreenEnums.PEDIA_HINTS, True, True)

		for i in range(gc.getNumTechInfos()):
			if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TECHS, i, True, True)
		for i in range(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNITS, i, True, True)
		for i in range(gc.getNumUnitCombatInfos()):
			if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CATEGORIES, i, True, True)
		for i in range(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROMOTIONS, i, True, True)
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BUILDINGS, i, True, True)
		for i in range(gc.getNumProjectInfos()):
			if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROJECTS, i, True, True)
		for i in range(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPECIALISTS, i, True, True)
		for i in range(gc.getNumTerrainInfos()):
			if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TERRAINS, i, True, True)
		for i in range(gc.getNumFeatureInfos()):
			if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_FEATURES, i, True, True)
		for i in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BONUSES, i, True, True)
		for i in range(gc.getNumImprovementInfos()):
			if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENTS, i, True, True)
		for i in range(gc.getNumCivilizationInfos()):
			if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVS, i, True, True)
		for i in range(gc.getNumLeaderHeadInfos()):
			if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_LEADERS, i, True, True)
		for i in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVICS, i, True, True)
		for i in range(gc.getNumReligionInfos()):
			if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_RELIGIONS, i, True, True)
		for i in range(gc.getNumCorporationInfos()):
			if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CORPORATIONS, i, True, True)
		for i in range(gc.getNumConceptInfos()):
			if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CONCEPTS, i, True, True)
		for i in range(gc.getNumNewConceptInfos()):
			if (gc.getNewConceptInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BTS_CONCEPTS, i, True, True)



	def handleInput (self, inputClass):
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_LEADERS):
			return self.pediaLeader.handleInput(inputClass)
		return 0



	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in range(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0


	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName



	def getSortedList(self, numInfos, getInfo):
		list = [(0,0)] * numInfos
		for i in range(numInfos):
			list[i] = (getInfo(i).getDescription(), i)
                ###invisible dummy tech - sevopedia start
		if getInfo == gc.getTechInfo:
                        for j in range(numInfos-1,-1,-1):
                                if gc.getTechInfo(j).getGridX()<=0 or gc.getTechInfo(j).getGridY()<=0:
                                        list.pop(j)
                ###invisible dummy tech - sevopedia end			
		if self.bSortLists:
			list.sort()
		return list
