## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

#edited by bluepotato to work with our custom WBSave parser
from CvPythonExtensions import *
import CvWBPopups
import CvUtil
import RFGWB
import time

# globals
lastFileRead = None
gc = CyGlobalContext()
wbParser = RFGWB.WbParser()

def writeDesc(argsList):
	"Save out a high-level desc of the world, for WorldBuilder"
	fileName = argsList[0]
	global lastFileRead
	lastFileRead=None
	return wbParser.createSplitWBSave(gc.getRiseFall().getMapFile(), fileName)

def readAndApplyDesc(argsList):
	print "CvWBInterface.readAndApplyDesc()"
	"Read in and apply a high-level desc of the world.  In-game load only"
	fileName = argsList[0]
	wbParser.parseFile(fileName)
	wbParser.buildMap()
	return 0

def readDesc(argsList):
	"Read in a high-level desc of the world, for WorldBuilder.  Must call applyMap and applyInitialItems to finish the process"
	global lastFileRead
	fileName = argsList[0]
	if (fileName!=lastFileRead):
		wbParser.parseFile(fileName)
		lastFileRead=fileName	
	return 0
		
def applyMapDesc():
	print "CvWBInterface.applyMapDesc()"
	"After reading, applies the map loaded data"
	wbParser.buildMap()
	return 0

def applyInitialItems():	
	"After reading, applies player units, cities, and techs"
	return 0

def getAssignedStartingPlots():
	"Reads in starting plots for random players"
	return 0

def initWBEditor(argsList):
	"Called from the Worldbuilder app - sends to CvWBPopups for handling"
	return CvWBPopups.CvWBPopups().initWB(argsList)
	
def getGameData():
	"after reading a save file, return game/player data as a tuple"
	t=()
	gameTurn = wbParser.getGameValue("GameTurn", 0)
	maxTurns = wbParser.getGameValue("MaxTurns", 0)
	maxCityElimination = wbParser.getGameValue("MaxCityElimination", 0)
	numAdvancedStartPoints = wbParser.getGameValue("NumAdvancedStartPoints", 0)
	targetScore = wbParser.getGameValue("TargetScore", 0)
	worldSizeType = CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), wbParser.getMapValue("world size", None))
	climateType = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), wbParser.getMapValue("climate", None))
	seaLevelType = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), wbParser.getMapValue("sealevel", None))
	eraType = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), wbParser.getGameValue("EraType", "NONE"))
	gameSpeedType = CvUtil.findInfoTypeNum(gc.getGameSpeedInfo, gc.getNumGameSpeedInfos(), wbParser.getGameValue("SpeedType", "NONE"))
	calendarType = CvUtil.findInfoTypeNum(gc.getCalendarInfo, gc.getNumCalendarInfos(), wbParser.getGameValue("CalendarType", "CALENDAR_DEFAULT"))
	
	t=t+(worldSizeType,)
	t=t+(climateType,)
	t=t+(seaLevelType,)
	t=t+(eraType,)
	t=t+(gameSpeedType,)
	t=t+(calendarType,)
	
	options = wbParser.getGameValue("Options", [])
	
	t=t+(len(options),)
	for i in range(len(options)):
		option = CvUtil.findInfoTypeNum(gc.getGameOptionInfo, gc.getNumGameOptionInfos(), options[i])
		t=t+(option,)
	
	mpOptions = wbParser.getGameValue("MpOptions", []) #TODO
	
	t=t+(len(mpOptions),)
	for i in range(len(mpOptions)):
		mpOption = CvUtil.findInfoTypeNum(gc.getMPOptionInfo, gc.getNumMPOptionInfos(), mpOptions[i])
		t=t+(mpOption,)
	
	forceControls = wbParser.getGameValue("ForceControls", []) #TODO
	
	t=t+(len(forceControls),)
	for i in range(len(forceControls)):
		forceControl = CvUtil.findInfoTypeNum(gc.getForceControlInfo, gc.getNumForceControlInfos(), forceControls[i])
		t=t+(forceControl,)
	
	victories = wbParser.getGameValue("Victories", []) #looks like this doesn't really work too great. TODO?
	
	t=t+(len(victories),)
	for i in range(len(victories)):
		victory = CvUtil.findInfoTypeNum(gc.getVictoryInfo, gc.getNumVictoryInfos(), victories[i])
		t=t+(victory,)
	
	t=t+(gameTurn,)
	t=t+(maxTurns,)
	t=t+(maxCityElimination,)
	t=t+(numAdvancedStartPoints,)
	t=t+(targetScore,)
	
	return t
	
def getModPath():
	"Returns the path for the Mod that this scenario should load (if applicable)"
	return wbParser.getModPath()
	
def getMapDescriptionKey():
	"Returns the TXT_KEY Description of the map to be displayed in the map/mod selection screen"
	return wbParser.getDescription()
	
def isRandomMap():
	"If true, this is really a mod, not a scenario"
	return False

def getPlayerData():
	print "CvWBInterface.getPlayerData()"
	"after reading a save file, return player data as a tuple, terminated by -1"
	t=()
	for i in range(gc.getMAX_CIV_PLAYERS()):
		leaderType = CvUtil.findInfoTypeNum(gc.getLeaderHeadInfo, gc.getNumLeaderHeadInfos(), "NONE")
		civType = CvUtil.findInfoTypeNum(gc.getCivilizationInfo, gc.getNumCivilizationInfos(), "NONE")
		color = CvUtil.findInfoTypeNum(gc.getPlayerColorInfo, gc.getNumPlayerColorInfos(), "NONE")
		artStyle = gc.getTypesEnum("NONE")
		handicapType = CvUtil.findInfoTypeNum(gc.getHandicapInfo, gc.getNumHandicapInfos(), gc.getHandicapInfo(gc.getDefineINT("STANDARD_HANDICAP")).getType())
		team = i
		playableCiv = 1
		if i >= gc.getMAX_CIV_PLAYERS() - 2:
			playableCiv = 0

		t=t+(civType,)
		t=t+(playableCiv,)
		t=t+(leaderType,)
		t=t+(handicapType,)
		t=t+(team,)
		t=t+(color,)
		t=t+(artStyle,)
		t=t+(0,)
		t=t+(0,)
	gc.onCivSelectionScreenLoaded()
	wbParser.setupEnabled()
	gc.setupEnabled()
	wbParser.setupStartingYears()
	return t

def getPlayerDesc():
	print "CvWBInterface.getPlayerDesc()"
	"after reading a save file, return player description data (wide strings) as a tuple"
	t=()
	for i in range(gc.getMAX_CIV_PLAYERS()):
		t=t+("",)
		t=t+("",)
		t=t+("",)
		t=t+("",)
		t=t+("",)
	return t
