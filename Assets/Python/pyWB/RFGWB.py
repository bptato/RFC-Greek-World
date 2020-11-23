#Author: bluepotato

from CvPythonExtensions import *
from cStringIO import StringIO
import CvUtil
import simplejson as json #for writing json
from OrderedDict import * #for writing json
import StringUtils #for writing json

cmap = CyMap()
gc = CyGlobalContext()
game = CyGame()
riseFall = CyRiseFall()

def parseValue(value): #Just convert strings to integers. Used by the legacy wbSave parser
	if isinstance(value, str) and (value.isdigit() or (value.startswith("-") and value[1:].isdigit())):
		return int(value)
	return value

def getWBPlot(plots, x, y):
	for wbPlot in plots:
		if wbPlot['x'] == x and wbPlot['y'] == y:
			return wbPlot
	wbPlot = OrderedDict({})
	wbPlot['x'] = x
	wbPlot['y'] = y
	plots.append(wbPlot)
	return plots[-1]

#https://stackoverflow.com/a/33571117
def json_load_byteified(file_handle):
	return _byteify(
		json.load(file_handle, object_hook=_byteify),
		ignore_dicts=True
	)

def json_loads_byteified(json_text):
	return _byteify(
		json.loads(json_text, object_hook=_byteify),
		ignore_dicts=True
	)

def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, unicode):
		return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
		return [ _byteify(item, ignore_dicts=True) for item in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
		return dict((_byteify(key, ignore_dicts=True), _byteify(value, ignore_dicts=True)) for key, value in data.iteritems())
	# if it's anything else, return it in its original form
	return data

class WbParser:
	def __init__(self):
		self.wbValues = {}
		self.scenarioValues = {}
		self.mapValues = {}
		self.splitFile = False
		self.lastOpenSlot = gc.getMAX_CIV_PLAYERS() - 1 #last slots are reserved for minors. decrement this everytime a minor civ is added. -1 because of barbs

	def getLastOpenSlot(self):
		return self.lastOpenSlot

	def getWbValue(self, key, default):
		ret = default
		if key in self.scenarioValues:
			ret = self.scenarioValues[key]
		return ret

	def getGameValue(self, key, default):
		ret = default
		if key in self.scenarioValues['Game']:
			ret = self.scenarioValues['Game'][key]
		return ret

	def getMapValue(self, key, default):
		ret = default
		if key in self.mapValues['Map']:
			ret = self.mapValues['Map'][key]
		return ret

	def getPlayerValue(self, civType, key, default):
		ret = default
		if key in self.scenarioValues['Players'][civType]:
			ret = self.scenarioValues['Players'][civType][key]
		return ret

	def getMaxTurns(self):
		if "MaxTurns" in self.scenarioValues['Game']:
			return self.scenarioValues['Game']['MaxTurns']
		return 0

	def getDescription(self):
		if "Description" in self.scenarioValues['Game']:
			return self.scenarioValues['Game']['Description']
		return "No description"

	def getModPath(self):
		if "Game" in self.scenarioValues:
			return self.scenarioValues['Game']['ModPath']
		else:
			return "Mods\\RFC-Greek-World"

	def getMapsPath(self): #TODO: actually detect this
		return self.getModPath() + "\\PrivateMaps\\"

	def setupEnabled(self):
		for wbPlayer in self.scenarioValues['Players']:
			rfcPlayer = riseFall.getRFCPlayer(gc.getInfoTypeForString(wbPlayer['CivType']))
			rfcPlayer.setEnabled(True)
			if "MinorNationStatus" in wbPlayer:
				rfcPlayer.setMinorCiv(True)
			else:
				rfcPlayer.setMinorCiv(False)

	def setupStartingYears(self):
		for wbPlayer in self.scenarioValues['Players']:
			if not "MinorNationStatus" in wbPlayer or wbPlayer['MinorNationStatus'] == 0: #major civ
				rfcPlayer = riseFall.getRFCPlayer(gc.getInfoTypeForString(wbPlayer['CivType']))
				rfcPlayer.setStartingYear(wbPlayer['StartingYear'])

	def getMapFile(self):
		return riseFall.getMapFile()

	def saveMapFile(self, name): #Save map data.
		values = OrderedDict({})
		mapValues = OrderedDict({})

		provinces = []
		plots = []

		#Plots
		mapWidth = cmap.getGridWidth()
		mapHeight = cmap.getGridHeight()

		numPlotsWritten = 0
		for y in range(mapHeight):
			for x in range(mapWidth):
				plot = cmap.plot(x, y)
				wbPlot = OrderedDict({})

				wbPlot['x'] = x
				wbPlot['y'] = y

				wbPlot['PlotType'] = int(plot.getPlotType())

				wbPlot['TerrainType'] = gc.getTerrainInfo(plot.getTerrainType()).getType()

				if plot.getFeatureType() != -1:
					wbPlot['FeatureType'] = gc.getFeatureInfo(plot.getFeatureType()).getType()
					wbPlot['FeatureVariety'] = plot.getFeatureVariety()

				if plot.getBonusType(-1) != -1:
					wbPlot['BonusType'] = gc.getBonusInfo(plot.getBonusType(-1)).getType()

				if plot.isWOfRiver():
					wbPlot['isWOfRiver'] = True
					wbPlot['RiverNSDirection'] = int(plot.getRiverNSDirection())
				if plot.isNOfRiver():
					wbPlot['isNOfRiver'] = True
					wbPlot['RiverWEDirection'] = int(plot.getRiverWEDirection())

				for i in range(gc.getNumCivilizationInfos()):
					if plot.getCityName(i, True) != "":
						if "CityNames" not in wbPlot:
							wbPlot['CityNames'] = OrderedDict({})
						wbPlot['CityNames'][gc.getCivilizationInfo(i).getType()] = plot.getCityName(i, True)

				#Settler values
				for i in range(gc.getNumCivilizationInfos()):
					rfcPlayer = riseFall.getRFCPlayer(i)
					if not rfcPlayer.isMinor():
						settlerValue = plot.getSettlerValue(i)
						if settlerValue != 20: #20 is the default value
							if "SettlerValues" not in wbPlot:
								wbPlot['SettlerValues'] = OrderedDict({})
							wbPlot['SettlerValues'][gc.getCivilizationInfo(i).getType()] = settlerValue

				plots.append(wbPlot)
				numPlotsWritten += 1

		#Map
		mapValues['grid width'] = mapWidth
		mapValues['grid height'] = mapHeight
		mapValues['top latitude'] = cmap.getTopLatitude()
		mapValues['bottom latitude'] = cmap.getBottomLatitude()
		mapValues['climate'] = gc.getClimateInfo(cmap.getClimate()).getType()
		mapValues['sealevel'] = gc.getSeaLevelInfo(cmap.getSeaLevel()).getType()
		mapValues['num plots written'] = numPlotsWritten

		mapValues['wrap X'] = int(cmap.isWrapX())
		mapValues['wrap Y'] = int(cmap.isWrapY())
		mapValues['world size'] = gc.getWorldInfo(cmap.getWorldSize()).getType()

		#Provinces
		for i in range(riseFall.getNumProvinces()):
			province = riseFall.getRFCProvince(i)
			wbProvince = OrderedDict({})
			wbProvince['Name'] = province.getName()
			wbProvince['Left'] = province.getLeft()
			wbProvince['Bottom'] = province.getBottom()
			wbProvince['Right'] = province.getRight()
			wbProvince['Top'] = province.getTop()
			provinces.append(wbProvince)

		values['Map'] = mapValues
		values['Provinces'] = provinces
		values['Plots'] = plots

		f = file(name, "w")
		f.write("application/json\n")
		unescapedValues = StringUtils.unescape(json.dumps(values, indent=1, separators=(',', ':'))) #replace html character references with human readable characters
		f.write(unescapedValues.encode("utf8"))

	def saveScenarioFile(self, name, mapName): #Save scenario data.
		values = OrderedDict({})
		values['MapFile'] = mapName
		gameValues = OrderedDict({})

		players = []
		provinces = []
		plots = []

		#Game
		gameValues['Calendar'] = gc.getCalendarInfo(game.getCalendar()).getType()
		gameValues['GameTurn'] = game.getGameTurn()
		gameValues['StartYear'] = game.getStartYear()
		if "Game" in self.scenarioValues and "ModPath" in self.scenarioValues['Game']:
			gameValues['ModPath'] = self.scenarioValues['Game']['ModPath'] #TODO
		else:
			gameValues['ModPath'] = ""

		if gc.getNumGameOptionInfos() > 0:
			gameValues['Options'] = []
			for i in range(gc.getNumGameOptionInfos()):
				if game.isOption(i):
					gameValues['Options'].append(gc.getGameOptionInfo(i).getType())

		if gc.getNumVictoryInfos() > 0:
			gameValues['Victories'] = []
			for i in range(gc.getNumVictoryInfos()):
				if game.isVictoryValid(i):
					gameValues['Victories'].append(gc.getVictoryInfo(i).getType())

		#Goody huts
		disableGoodies = "GAMEOPTION_NO_GOODY_HUTS" in self.scenarioValues['Game']['Options']
		goodyImprovement = -1
		for i in range(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGoody():
				goodyImprovement = i
				break

		#Plots
		mapWidth = cmap.getGridWidth()
		mapHeight = cmap.getGridHeight()

		numPlotsWritten = 0
		for y in range(mapHeight):
			for x in range(mapWidth):
				plot = cmap.plot(x, y)
				wbPlot = OrderedDict({})

				wbPlot['x'] = x
				wbPlot['y'] = y
				shouldSave = False

				if plot.getImprovementType() != -1:
					if disableGoodies or plot.getImprovementType() != goodyImprovement:
						wbPlot['ImprovementType'] = gc.getImprovementInfo(plot.getImprovementType()).getType()
						shouldSave = True

				if plot.getRouteType() != -1:
					wbPlot['RouteType'] = gc.getRouteInfo(plot.getRouteType()).getType()
					shouldSave = True

				if plot.getNumUnits() > 0:
					wbPlot['Units'] = []
					for i in range(plot.getNumUnits()):
						unit = plot.getUnit(i)
						wbUnit = OrderedDict({})
						wbUnit['UnitOwner'] = gc.getCivilizationInfo(gc.getPlayer(unit.getOwner()).getCivilizationType()).getType()
						wbUnit['UnitType'] = gc.getUnitInfo(unit.getUnitType()).getType()
						wbUnit['FacingDirection'] = int(unit.getFacingDirection())
						wbUnit['UnitAIType'] = gc.getUnitAIInfo(unit.getUnitAIType()).getType()
						wbUnit['Year'] = game.getGameTurnYear()
						wbPlot['Units'].append(wbUnit)
						#TODO experience, promotions
					shouldSave = True

				if plot.isCity():
					city = plot.getPlotCity()
					wbPlot['City'] = OrderedDict({})
					wbCity = wbPlot['City']

					wbCity['CityOwner'] = gc.getCivilizationInfo(gc.getPlayer(city.getOwner()).getCivilizationType()).getType()
					wbCity['Year'] = game.getGameTurnYear()
					if city.getPopulation() > 1:
						wbCity['CityPopulation'] = city.getPopulation()

					for i in range(gc.getNumBuildingInfos()):
						if city.getNumRealBuilding(i) > 0:
							if "Buildings" not in wbCity:
								wbCity['Buildings'] = {}
							wbCity['Buildings'][gc.getBuildingInfo(i).getType()] = city.getNumRealBuilding(i)

					for i in range(gc.getNumReligionInfos()):
						if city.isHasReligion(i):
							if "Religions" not in wbCity:
								wbCity['Religions'] = {}
							wbCity['Religions'][gc.getReligionInfo(i).getType()] = True

					for i in range(gc.getNumReligionInfos()):
						if city.isHolyCityByType(i):
							if "HolyCityReligions" not in wbCity:
								wbCity['HolyCityReligions'] = {}
							wbCity['HolyCityReligions'][gc.getReligionInfo(i).getType()] = True
					for i in range(gc.getNumCivilizationInfos()):
						if city.getCulture(i) > 0:
							if "Culture" not in wbCity:
								wbCity['Culture'] = {}
							wbCity['Culture'][gc.getCivilizationInfo(i).getType()] = city.getCulture(i)
					shouldSave = True

				if shouldSave:
					plots.append(wbPlot)

		#Players
		for i in range(gc.getNumCivilizationInfos()):
			rfcPlayer = riseFall.getRFCPlayer(i)
			if rfcPlayer.isEnabled():
				civInfo = gc.getCivilizationInfo(i)
				wbPlayer = OrderedDict({})
				wbPlayer['CivType'] = civInfo.getType()
				wbPlayer['StartingTechs'] = []
				wbPlayer['CivicOptions'] = OrderedDict({})

				alive = false
				for j in range(gc.getMAX_PLAYERS()):
					player = gc.getPlayer(j)
					if player.isAlive() and player.getCivilizationType() == i:
						for j in range(gc.getNumCivicOptionInfos()):
							startingCivic = player.getCivics(j)
							if startingCivic != -1:
								wbPlayer['CivicOptions'][gc.getCivicOptionInfo(j).getType()] = gc.getCivicInfo(startingCivic).getType()
						wbPlayer['StartingGold'] = player.getGold()
						if player.getStateReligion() != ReligionTypes.NO_RELIGION:
							wbPlayer['StartingReligion'] = gc.getReligionInfo(player.getStateReligion()).getType()

						for k in range(gc.getNumTechInfos()):
							if gc.getTeam(player.getTeam()).isHasTech(k):
								wbPlayer['StartingTechs'].append(gc.getTechInfo(k).getType())
						alive = True
						break

				if not alive:
					for j in range(gc.getNumCivicOptionInfos()):
						startingCivic = rfcPlayer.getStartingCivic(j)
						if startingCivic != -1:
							wbPlayer['CivicOptions'][gc.getCivicOptionInfo(j).getType()] = gc.getCivicInfo(startingCivic).getType()

					wbPlayer['StartingGold'] = rfcPlayer.getStartingGold()
					if rfcPlayer.getStartingReligion() != ReligionTypes.NO_RELIGION:
						wbPlayer['StartingReligion'] = gc.getReligionInfo(rfcPlayer.getStartingReligion()).getType()

					for j in range(gc.getNumTechInfos()):
						if rfcPlayer.isStartingTech(j):
							wbPlayer['StartingTechs'].append(gc.getTechInfo(j).getType())

				wbPlayer['StartingWars'] = []
				for j in range(gc.getNumCivilizationInfos()):
					if rfcPlayer.isStartingWar(j):
						wbPlayer['StartingWars'].append(gc.getCivilizationInfo(j).getType())

				wbPlayer['RelatedLanguages'] = []
				for j in range(gc.getNumCivilizationInfos()):
					if i != j:
						if rfcPlayer.isRelatedLanguage(j):
							wbPlayer['RelatedLanguages'].append(gc.getCivilizationInfo(j).getType())

				wbPlayer['StartingX'] = rfcPlayer.getStartingPlotX()
				wbPlayer['StartingY'] = rfcPlayer.getStartingPlotY()

				#Scheduled units & cities
				for j in range(rfcPlayer.getNumScheduledUnits()):
					scheduledUnit = rfcPlayer.getScheduledUnit(j)
					wbPlot = getWBPlot(plots, scheduledUnit.getX(), scheduledUnit.getY())
					if "Units" not in wbPlot:
						wbPlot['Units'] = []
					wbUnit = OrderedDict({})
					if scheduledUnit.getAmount() > 1:
						wbUnit['Amount'] = scheduledUnit.getAmount()
					wbUnit['UnitOwner'] = civInfo.getType()
					wbUnit['UnitType'] = gc.getUnitInfo(scheduledUnit.getUnitType()).getType()
					wbUnit['Year'] = scheduledUnit.getYear()
					if scheduledUnit.getUnitAIType() != UnitAITypes.NO_UNITAI:
						wbUnit['UnitAIType'] = gc.getUnitAIInfo(scheduledUnit.getUnitAIType()).getType()
					if scheduledUnit.getFacingDirection() != -1 and scheduledUnit.getFacingDirection() != 4:
						wbUnit['FacingDirection'] = scheduledUnit.getFacingDirection()
					if scheduledUnit.isAIOnly():
						wbUnit['AIOnly'] = scheduledUnit.isAIOnly()
					if scheduledUnit.isDeclareWar():
						wbUnit['DeclareWar'] = scheduledUnit.isDeclareWar()
					wbPlot['Units'].append(wbUnit)

				for j in range(rfcPlayer.getNumScheduledCities()):
					scheduledCity = rfcPlayer.getScheduledCity(j)
					wbPlot = getWBPlot(plots, scheduledCity.getX(), scheduledCity.getY())
					wbCity = OrderedDict({})
					wbCity['CityOwner'] = civInfo.getType()
					wbCity['Year'] = scheduledCity.getYear()
					wbCity['CityPopulation'] = scheduledCity.getPopulation()
					for i in range(gc.getNumBuildingInfos()):
						if scheduledCity.getNumBuilding(i) > 0:
							if "Buildings" not in wbCity:
								wbCity['Buildings'] = {}
							wbCity['Buildings'][gc.getBuildingInfo(i).getType()] = city.getNumBuilding(i)

					for i in range(gc.getNumReligionInfos()):
						if scheduledCity.getHolyCityReligion(i):
							if "HolyCityReligions" not in wbCity:
								wbCity['HolyCityReligions'] = {}
							wbCity['HolyCityReligions'][gc.getReligionInfo(i).getType()] = True
					for i in range(gc.getNumCivilizationInfos()):
						if scheduledCity.getCulture(i) > 0:
							if "Culture" not in wbCity:
								wbCity['Culture'] = {}
							wbCity['Culture'][gc.getCivilizationInfo(i).getType()] = scheduledCity.getCulture(i)

					wbPlot['City'] = wbCity

				#Core provinces
				wbPlayer['CoreProvinces'] = []
				for j in range(rfcPlayer.getNumCoreProvinces()):
					coreProvince = rfcPlayer.getCoreProvince(j)
					wbPlayer['CoreProvinces'].append(rfcPlayer.getCoreProvince(j))

				wbPlayer['StartingYear'] = rfcPlayer.getStartingYear()

				#Minor nation?
				if rfcPlayer.isMinor():
					wbPlayer['MinorNationStatus'] = 1

				#Already flipped?
				wbPlayer['Flipped'] = rfcPlayer.isFlipped()

				#Modifiers
				wbPlayer['CompactEmpireModifier'] = rfcPlayer.getCompactEmpireModifier()
				wbPlayer['UnitUpkeepModifier'] = rfcPlayer.getUnitUpkeepModifier()
				wbPlayer['ResearchModifier'] = rfcPlayer.getResearchModifier()
				wbPlayer['DistanceMaintenanceModifier'] = rfcPlayer.getDistanceMaintenanceModifier()
				wbPlayer['NumCitiesMaintenanceModifier'] = rfcPlayer.getNumCitiesMaintenanceModifier()
				wbPlayer['UnitProductionModifier'] = rfcPlayer.getUnitProductionModifier()
				wbPlayer['CivicUpkeepModifier'] = rfcPlayer.getCivicUpkeepModifier()
				wbPlayer['HealthBonusModifier'] = rfcPlayer.getHealthBonusModifier()
				wbPlayer['BuildingProductionModifier'] = rfcPlayer.getBuildingProductionModifier()
				wbPlayer['WonderProductionModifier'] = rfcPlayer.getWonderProductionModifier()
				wbPlayer['GreatPeopleModifier'] = rfcPlayer.getGreatPeopleModifier()
				wbPlayer['InflationModifier'] = rfcPlayer.getInflationModifier()
				wbPlayer['GrowthModifier'] = rfcPlayer.getGrowthModifier()

				players.append(wbPlayer)

		#Provinces
		for i in range(riseFall.getNumProvinces()):
			province = riseFall.getRFCProvince(i)
			wbProvince = OrderedDict({})
			wbProvince['Name'] = province.getName()
			scheduledUnitsAmount = province.getNumScheduledUnits()
			for i in range(scheduledUnitsAmount):
				scheduledUnit = province.getScheduledUnit(i)
				if "Units" not in wbProvince:
					wbProvince['Units'] = []
				wbUnit = OrderedDict({})
				if scheduledUnit.getAmount() > 1:
					wbUnit['Amount'] = scheduledUnit.getAmount()
				#wbUnit['UnitOwner'] = civInfo.getType()

				wbUnit['UnitType'] = gc.getUnitInfo(scheduledUnit.getUnitType()).getType()
				wbUnit['Year'] = scheduledUnit.getYear()
				wbUnit['EndYear'] = scheduledUnit.getEndYear()
				if scheduledUnit.getUnitAIType() != -1 and scheduledUnit.getUnitAIType() != UnitAITypes.UNITAI_ATTACK: #UNITAI_ATTACK is the default barb unitai
					wbUnit['UnitAIType'] = gc.getUnitAIInfo(scheduledUnit.getUnitAIType()).getType()
				if scheduledUnit.getFacingDirection() != -1 and scheduledUnit.getFacingDirection() != 4:
					wbUnit['FacingDirection'] = scheduledUnit.getFacingDirection()

				wbUnit['SpawnFrequency'] = scheduledUnit.getSpawnFrequency()

				wbProvince['Units'].append(wbUnit)

			provinces.append(wbProvince)

		values['Game'] = gameValues
		values['Players'] = players
		values['Provinces'] = provinces
		values['Plots'] = plots

		f = file(name, "w")
		f.write("application/json\n")
		unescapedValues = StringUtils.unescape(json.dumps(values, indent=1, separators=(',', ':'))) #replace html character references with human readable characters
		f.write(unescapedValues.encode("utf8"))

	def createSplitWBSave(self, mapName, scenarioName):
		mapPath = scenarioName.split('/')
		mapPath.pop(len(mapPath)-1)
		self.saveMapFile('/'.join(mapPath) + '/' + mapName)
		self.saveScenarioFile(scenarioName, mapName)

	def parseFile(self, name): #Parse a WBSave file.
		print name
		f = open(name, "r")
		bGame = False
		bPlayer = False
		bMap = False
		bPlot = False
		bUnit = False
		bCity = False
		bProvince = False

		player = {}
		plot = {}
		unit = {}
		city = {}
		province = {}

		values = {}
		gameValues = {}
		mapValues = {}

		players = []
		provinces = []
		plots = []
		civics = []
		Options = []
		Victories = []

		if "application/json" in f.readline():
			wbValuesStr = ""
			file_str = StringIO()
			while 1:
				line = f.readline()
				if line == '': break
				s = line.strip().decode("utf-8").encode("ascii", "xmlcharrefreplace")
				file_str.write(s)
			self.wbValues = json_loads_byteified(file_str.getvalue())
			f.close()
			if "MapFile" in self.wbValues:
				self.scenarioValues = self.wbValues
				riseFall.setMapFile(self.wbValues['MapFile'])
				self.parseFile(self.getMapsPath() + self.wbValues['MapFile'])
				self.mapValues = self.wbValues
				self.splitFile = True
			return

		#normal wbsave parser. warning: this is incomplete
		lineNum = 0
		for line in f.readlines():
			if "=" in line or "OfRiver" in line:
				splitLine = line.replace("	", "") \
				.replace("\n", "") \
				.replace(", ", "=") \
				.replace(",", "=") \
				.decode("utf-8") \
				.encode("ascii", "xmlcharrefreplace") \
				.split("=") #We decode unicode characters and then encode them in xml format.
				#BeginGame to EndGame
				if bGame:
					if splitLine[0] == "Option":
						Options.append(splitLine[1])
					elif splitLine[0] == "Victory":
						Victories.append(splitLine[1])
					else:
						gameValues[splitLine[0]] = parseValue(splitLine[1])
					gameValues['Options'] = Options
					gameValues['Victories'] = Victories
				#BeginPlayer to EndPlayer
				elif bPlayer:
					if player == None:
						player = {}
					if splitLine[0] == "CivicOption":
						if "CivicOptions" not in player:
							player['CivicOptions'] = {}
						player['CivicOptions'][parseValue(splitLine[1])] = parseValue(splitLine[3])
					elif splitLine[0] == "StartingX":
						player[splitLine[0]] = parseValue(splitLine[1])
						if splitLine[2] == "StartingY":
							player[splitLine[2]] = parseValue(splitLine[3])
						else:
							raise Exception(str(lineNum) + ": no Y position found for " + parseValue(splitLine[1]) + "!")
					elif splitLine[0] == "Techs":
						startingTechs = []
						for i in range(len(splitLine) - 1): #do not add "Techs" to the list
							startingTechs.append(splitLine[i + 1])
						player['StartingTechs'] = startingTechs
					else:
						player[splitLine[0]] = parseValue(splitLine[1])
				#BeginMap to EndMap
				elif bMap:
					mapValues[splitLine[0]] = parseValue(splitLine[1])
				#BeginProvince to EndProvince
				elif bProvince:
					province[splitLine[0]] = parseValue(splitLine[1])
					#BeginUnit to EndUnit
					if bUnit:
						if splitLine[0] == "UnitType":
							unit[splitLine[0]] = parseValue(splitLine[1])
							if splitLine[2] == "UnitOwner":
								unit[splitLine[2]] = parseValue(splitLine[3])
							else:
								raise Exception(str(lineNum) + ": no owner for unit!")
						elif splitLine[0] == "Level":
							unit[splitLine[0]] = parseValue(splitLine[1])
							if splitLine[2] == "Experience":
								unit[splitLine[2]] = parseValue(splitLine[3])
							else:
								raise Exception(str(lineNum) + ": no experience for unit!")
						else:
							unit[splitLine[0]] = parseValue(splitLine[1])
				#BeginPlot to EndPlot
				elif bPlot:
					if plot == None:
						plot = {}
					#BeginUnit to EndUnit
					if bUnit:
						if splitLine[0] == "UnitType":
							unit[splitLine[0]] = parseValue(splitLine[1])
							if splitLine[2] == "UnitOwner":
								unit[splitLine[2]] = parseValue(splitLine[3])
							else:
								raise Exception(str(lineNum) + ": no owner for unit!")
						elif splitLine[0] == "Level":
							unit[splitLine[0]] = parseValue(splitLine[1])
							if splitLine[2] == "Experience":
								unit[splitLine[2]] = parseValue(splitLine[3])
							else:
								raise Exception(str(lineNum) + ": no experience for unit!")
						else:
							unit[splitLine[0]] = parseValue(splitLine[1])
					elif bCity:
						city[splitLine[0]] = parseValue(splitLine[1])
					elif splitLine[0] == "x":
						plot[splitLine[0]] = parseValue(splitLine[1])
						if splitLine[2] == "y":
							plot[splitLine[2]] = parseValue(splitLine[3])
						else:
							raise Exception(str(lineNum) + ": no y at plot!")
					elif splitLine[0] == "FeatureType":
						plot[splitLine[0]] = parseValue(splitLine[1])
						if splitLine[2] == "FeatureVariety":
							plot[splitLine[2]] = parseValue(splitLine[3])
						else:
							raise Exception(str(lineNum) + ": no FeatureVariety at plot!")

					else:
						if len(splitLine) > 1:
							plot[splitLine[0]] = parseValue(splitLine[1])
						else:
							plot[splitLine[0]] = True
			else:
				if "BeginGame" in line:
					bGame = True
				if "EndGame" in line:
					bGame = False
				if "BeginPlayer" in line:
					bPlayer = True
				if "EndPlayer" in line:
					bPlayer = False
				if "BeginProvince" in line:
					bProvince = True
				if "EndProvince" in line:
					bProvince = False
				if "BeginMap" in line:
					bMap = True
				if "EndMap" in line:
					bMap = False
				if "BeginPlot" in line:
					bPlot = True
				if "EndPlot" in line:
					bPlot = False
				if "BeginUnit" in line:
					bUnit = True
				if "EndUnit" in line:
					bUnit = False
				if "BeginCity" in line:
					bCity = True
				if "EndCity" in line:
					bCity = False
			if player != {} and not bPlayer:
				players.append(player)
				player = {}
				civics = []
			if plot != {} and not bPlot:
				plots.append(plot)
				plot = {}
			if unit != {} and not bUnit:
				if "Units" not in plot:
					plot['Units'] = []
				plot['Units'].append(unit)
				unit = {}
			if city != {} and not bCity:
				plot['City'] = city
				city = {}
			if province != {} and not bProvince:
				provinces.append(province)
				province = {}
			lineNum += 1
		values['Game'] = gameValues
		values['Map'] = mapValues
		values['Players'] = players
		values['Plots'] = plots
		values['Provinces'] = provinces

		self.wbValues = values
		f.close()

	def buildMap(self):
		print "RFGWB.buildMap()"
		self.lastOpenSlot = gc.getMAX_CIV_PLAYERS() - 1 #needs to be reset, TODO maybe not here?

		if "StartYear" in self.scenarioValues['Game']:
			game.setStartYear(self.scenarioValues['Game']['StartYear'])

		if "Map" in self.mapValues:
			mapWidth = self.mapValues['Map']['grid width']
			mapHeight = self.mapValues['Map']['grid height']
			wrapX = bool(self.mapValues['Map']['wrap X'])
			wrapY = bool(self.mapValues['Map']['wrap Y'])
			worldSize = WorldSizeTypes(CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), self.mapValues['Map']['world size']))
			climate = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), self.mapValues['Map']['climate'])
			seaLevel = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), self.mapValues['Map']['sealevel'])
			cmap.rebuild(mapWidth, mapHeight, self.mapValues['Map']['top latitude'], self.mapValues['Map']['bottom latitude'], wrapX, wrapY, WorldSizeTypes(worldSize), ClimateTypes(climate), SeaLevelTypes(seaLevel), 0, None)

		#Plots
		for wbPlot in self.mapValues['Plots']:
			x = wbPlot['x']
			y = wbPlot['y']
			plot = cmap.plot(x, y)

			#Plot types
			if "PlotType" in wbPlot:
				plot.setPlotType(PlotTypes(wbPlot['PlotType']), False, False)

			#Terrain types
			if "TerrainType" in wbPlot:
				terrainType = gc.getInfoTypeForString(wbPlot['TerrainType'])
				plot.setTerrainType(terrainType, False, False)

		cmap.recalculateAreas()

		for wbPlot in self.mapValues['Plots']:
			x = wbPlot['x']
			y = wbPlot['y']
			plot = cmap.plot(x, y)
			#Bonuses
			if "BonusType" in wbPlot:
				plot.setBonusType(gc.getInfoTypeForString(wbPlot['BonusType']))

			#Features
			if "FeatureType" in wbPlot:
				plot.setFeatureType(gc.getInfoTypeForString(wbPlot['FeatureType']), wbPlot['FeatureVariety'])

			#Rivers
			directions = [CardinalDirectionTypes.NO_CARDINALDIRECTION, CardinalDirectionTypes.NO_CARDINALDIRECTION]
			if "RiverNSDirection" in wbPlot:
				if wbPlot['RiverNSDirection'] == 0:
					directions[1] = CardinalDirectionTypes.CARDINALDIRECTION_NORTH
				if wbPlot['RiverNSDirection'] == 2:
					directions[1] = CardinalDirectionTypes.CARDINALDIRECTION_SOUTH
			if "RiverWEDirection" in wbPlot:
				if wbPlot['RiverWEDirection'] == 1:
					directions[0] = CardinalDirectionTypes.CARDINALDIRECTION_EAST
				if wbPlot['RiverWEDirection'] == 3:
					directions[0] = CardinalDirectionTypes.CARDINALDIRECTION_WEST
			if "isNOfRiver" in wbPlot:
				plot.setNOfRiver(True, directions[0])
			if "isWOfRiver" in wbPlot:
				plot.setWOfRiver(True, directions[1])

			#City names
			if "CityNames" in wbPlot:
				for i in range(gc.getNumCivilizationInfos()):
					if gc.getCivilizationInfo(i).getType() in wbPlot['CityNames']:
						plot.setCityName(i, wbPlot['CityNames'][gc.getCivilizationInfo(i).getType()])

			#Settler values
			if "SettlerValues" in wbPlot:
				for i in range(gc.getNumCivilizationInfos()):
					civType = gc.getCivilizationInfo(i).getType()
					if civType in wbPlot['SettlerValues']:
						plot.setSettlerValue(i, wbPlot['SettlerValues'][civType])

			#legacy settler map converter thing
			#for j in range(gc.getNumCivilizationInfos()):
			#	rfcPlayer = riseFall.getRFCPlayer(j)
			#	if not rfcPlayer.isMinor():
			#		if not (gc.getCivilizationInfo(j).getType() == "CIVILIZATION_HUNS" and SettlersMaps.tSettlersMaps[j][mapHeight - 1 - y][x]):
			#			plot.setSettlerValue(j, SettlersMaps.tSettlersMaps[j][mapHeight - 1 - y][x])

			#cnm converter thing
			#for i in range(len(CityNameMap.tCityMap)):
			#	if x < 61 and CityNameMap.tCityMap[i][59 - y][x] != "-1":
			#		cityName = CityNameMap.tCityMap[i][mapHeight - 1 - y][x]
			#		plot.setCityName(i, cityName)

		for wbPlot in self.scenarioValues['Plots']:
			x = wbPlot['x']
			y = wbPlot['y']
			plot = cmap.plot(x, y)

			#Units
			if "Units" in wbPlot:
				for wbUnit in wbPlot['Units']:
					unitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), wbUnit['UnitType'])
					ownerType = gc.getInfoTypeForString(wbUnit['UnitOwner'])
					rfcPlayer = riseFall.getRFCPlayer(ownerType)

					if "FacingDirection" in wbUnit:
						facingDirection = wbUnit['FacingDirection']
					else:
						facingDirection = DirectionTypes.DIRECTION_SOUTH

					if "Amount" in wbUnit:
						amount = wbUnit['Amount']
					else:
						amount = 1

					if "UnitAIType" in wbUnit:
						unitAI = CvUtil.findInfoTypeNum(gc.getUnitAIInfo, UnitAITypes.NUM_UNITAI_TYPES, wbUnit['UnitAIType'])
					else:
						unitAI = UnitAITypes.NO_UNITAI

					if "Year" in wbUnit:
						year = wbUnit['Year']
					else:
						year = game.getGameTurnYear()

					if "AIOnly" in wbUnit:
						aiOnly = wbUnit['AIOnly']
					else:
						aiOnly = False

					if "DeclareWar" in wbUnit:
						declareWar = wbUnit['DeclareWar']
					else:
						declareWar = False

					rfcUnit = rfcPlayer.addScheduledUnit()
					rfcUnit.setYear(year)
					rfcUnit.setUnitType(unitType)
					rfcUnit.setX(x)
					rfcUnit.setY(y)
					rfcUnit.setUnitAIType(unitAI)
					rfcUnit.setFacingDirection(facingDirection)
					rfcUnit.setAmount(amount)
					rfcUnit.setAIOnly(aiOnly)
					rfcUnit.setDeclareWar(declareWar)


			#Cities
			if "City" in wbPlot:
				wbCity = wbPlot['City']
				ownerID = gc.getInfoTypeForString(wbCity['CityOwner'])
				rfcPlayer = riseFall.getRFCPlayer(ownerID)

				if "CityPopulation" in wbCity:
					population = wbCity['CityPopulation']
				else:
					population = 1

				if "Year" in wbCity:
					year = wbCity['Year']
				else:
					year = game.getGameTurnYear()

				scheduledCity = rfcPlayer.addScheduledCity()
				scheduledCity.setYear(year)
				scheduledCity.setX(x)
				scheduledCity.setY(y)
				scheduledCity.setPopulation(population)

				if "Buildings" in wbCity:
					for i in range(gc.getNumBuildingInfos()):
						buildingType = gc.getBuildingInfo(i).getType()
						if buildingType in wbCity['Buildings']:
							scheduledCity.setNumBuilding(i, wbCity['Buildings'][buildingType])

				if "Religions" in wbCity:
					for i in range(gc.getNumReligionInfos()):
						religionType = gc.getReligionInfo(i).getType()
						if religionType in wbCity['Religions']:
							scheduledCity.setReligion(i, wbCity['Religions'][religionType])

				if "HolyCityReligions" in wbCity:
					for i in range(gc.getNumReligionInfos()):
						religionType = gc.getReligionInfo(i).getType()
						if religionType in wbCity['HolyCityReligions']:
							scheduledCity.setHolyCityReligion(i, wbCity['HolyCityReligions'][religionType])

				if "Culture" in wbCity:
					for i in range(gc.getNumCivilizationInfos()):
						civType = gc.getCivilizationInfo(i).getType()
						if civType in wbCity['Culture']:
							scheduledCity.setCulture(i, wbCity['Culture'][civType])

			#Improvements
			if "ImprovementType" in wbPlot:
				improvementType = gc.getInfoTypeForString(wbPlot['ImprovementType'])
				plot.setImprovementType(improvementType)

			#Roads
			if "RouteType" in wbPlot:
				routeType = gc.getInfoTypeForString(wbPlot['RouteType'])
				plot.setRouteType(routeType)

		#Goody huts
		disableGoodies = "GAMEOPTION_NO_GOODY_HUTS" in self.scenarioValues['Game']['Options']
		goodyImprovement = -1
		for i in range(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGoody():
				goodyImprovement = i
				break

		#Provinces
		for wbProvince in self.mapValues['Provinces']:
			rfcProvince = riseFall.addProvince(wbProvince['Name'], wbProvince['Bottom'], wbProvince['Left'], wbProvince['Top'], wbProvince['Right'])
			#Goody huts
			if not disableGoodies:
				amountRand = ((rfcProvince.getTop() - rfcProvince.getBottom()) + (rfcProvince.getRight() - rfcProvince.getLeft()))/5
				amount = game.getSorenRandNum(amountRand, "Goody hut amount roll")

				plots = []
				for x in range(rfcProvince.getLeft(), rfcProvince.getRight()):
					for y in range(rfcProvince.getBottom(), rfcProvince.getTop()):
						plot = cmap.plot(x, y)
						if plot.isWater() or plot.isPeak():
							continue
						unavail = false
						for wbPlayer in self.scenarioValues['Players']:
							if wbPlayer['StartingYear'] == self.scenarioValues['Game']['StartYear']:
								if x == wbPlayer['StartingX'] and y == wbPlayer['StartingY']:
									unavail = True
									break
						if unavail:
							continue

						plots.append(plot)

				if len(plots):
					for i in range(amount):
						rndNum = gc.getGame().getSorenRandNum(len(plots), 'Goody hut location roll')

						plot = plots[rndNum]
						plot.setImprovementType(goodyImprovement)

		for wbProvince in self.scenarioValues['Provinces']:
			#Units
			if "Units" in wbProvince:
				rfcProvince = riseFall.getRFCProvince(wbProvince['Name'])
				for wbUnit in wbProvince['Units']:
					if "Year" not in wbUnit or "EndYear" not in wbUnit:
						raise Exception("No starting/ending date of barbarian unit " + str(wbUnit))

					if "FacingDirection" in wbUnit:
						facingDirection = wbUnit['FacingDirection']
					else:
						facingDirection = DirectionTypes.DIRECTION_SOUTH

					if "Amount" in wbUnit:
						amount = wbUnit['Amount']
					else:
						amount = 1

					if "UnitAIType" in wbUnit:
						unitAI = CvUtil.findInfoTypeNum(gc.getUnitAIInfo, UnitAITypes.NUM_UNITAI_TYPES, wbUnit['UnitAIType'])
					else:
						unitAI = UnitAITypes.UNITAI_ATTACK

					year = wbUnit['Year']
					endYear = wbUnit['EndYear']

					unitID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), wbUnit['UnitType'])

					rfcUnit = rfcProvince.addScheduledUnit()
					rfcUnit.setYear(year)
					rfcUnit.setUnitType(unitID)
					rfcUnit.setUnitAIType(unitAI)
					rfcUnit.setFacingDirection(facingDirection)
					rfcUnit.setAmount(amount)
					rfcUnit.setEndYear(endYear)
					rfcUnit.setSpawnFrequency(wbUnit['SpawnFrequency'])

		#Players
		for i in range(gc.getMAX_CIV_PLAYERS()):
			gc.getPlayer(i).setStartingPlot(cmap.plot(0, 0), True)

		for wbPlayer in self.scenarioValues['Players']:
			civType = gc.getInfoTypeForString(wbPlayer['CivType'])
			rfcPlayer = riseFall.getRFCPlayer(civType)

			if not "MinorNationStatus" in wbPlayer or wbPlayer['MinorNationStatus'] == 0: #major civ
				if "CoreProvinces" in wbPlayer:
					for wbCoreProvince in wbPlayer['CoreProvinces']:
						rfcPlayer.addCoreProvince(wbCoreProvince)

				if "StartingX" in wbPlayer and "StartingY" in wbPlayer:
					rfcPlayer.setStartingPlot(wbPlayer['StartingX'], wbPlayer['StartingY'])

				if "StartingTechs" in wbPlayer:
					for startingTech in wbPlayer['StartingTechs']:
						techType = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), startingTech)
						rfcPlayer.addStartingTech(techType)

				if "CivicOptions" in wbPlayer:
					for i in range(gc.getNumCivicOptionInfos()):
						civicOptionType = gc.getCivicOptionInfo(i).getType()
						if civicOptionType in wbPlayer['CivicOptions']:
							civicOptionTypeNum = gc.getInfoTypeForString(wbPlayer['CivicOptions'][civicOptionType])
							rfcPlayer.setStartingCivic(i, civicOptionTypeNum)

				if "StartingGold" in wbPlayer:
					rfcPlayer.setStartingGold(wbPlayer['StartingGold'])

				if "StartingReligion" in wbPlayer:
					rfcPlayer.setStartingReligion(gc.getInfoTypeForString(wbPlayer['StartingReligion']))

				if "StartingWars" in wbPlayer:
					for startingWar in wbPlayer['StartingWars']:
						rfcPlayer.addStartingWar(gc.getInfoTypeForString(startingWar))

				if "RelatedLanguages" in wbPlayer:
					for relatedLanguage in wbPlayer['RelatedLanguages']:
						rfcPlayer.addRelatedLanguage(gc.getInfoTypeForString(relatedLanguage))

				#Modifiers
				if "CompactEmpireModifier" in wbPlayer:
					rfcPlayer.setCompactEmpireModifier(wbPlayer['CompactEmpireModifier'])
				if "UnitUpkeepModifier" in wbPlayer:
					rfcPlayer.setUnitUpkeepModifier(wbPlayer['UnitUpkeepModifier'])
				if "ResearchModifier" in wbPlayer:
					rfcPlayer.setResearchModifier(wbPlayer['ResearchModifier'])
				if "DistanceMaintenanceModifier" in wbPlayer:
					rfcPlayer.setDistanceMaintenanceModifier(wbPlayer['DistanceMaintenanceModifier'])
				if "NumCitiesMaintenanceModifier" in wbPlayer:
					rfcPlayer.setNumCitiesMaintenanceModifier(wbPlayer['NumCitiesMaintenanceModifier'])
				if "UnitProductionModifier" in wbPlayer:
					rfcPlayer.setUnitProductionModifier(wbPlayer['UnitProductionModifier'])
				if "CivicUpkeepModifier" in wbPlayer:
					rfcPlayer.setCivicUpkeepModifier(wbPlayer['CivicUpkeepModifier'])
				if "HealthBonusModifier" in wbPlayer:
					rfcPlayer.setHealthBonusModifier(wbPlayer['HealthBonusModifier'])
				if "BuildingProductionModifier" in wbPlayer:
					rfcPlayer.setBuildingProductionModifier(wbPlayer['BuildingProductionModifier'])
				if "WonderProductionModifier" in wbPlayer:
					rfcPlayer.setWonderProductionModifier(wbPlayer['WonderProductionModifier'])
				if "GreatPeopleModifier" in wbPlayer:
					rfcPlayer.setGreatPeopleModifier(wbPlayer['GreatPeopleModifier'])
				if "InflationModifier" in wbPlayer:
					rfcPlayer.setInflationModifier(wbPlayer['InflationModifier'])
				if "GrowthModifier" in wbPlayer:
					rfcPlayer.setGrowthModifier(wbPlayer['GrowthModifier'])
				if "StartingYear" in wbPlayer:
					rfcPlayer.setStartingYear(wbPlayer['StartingYear'])
				if "Flipped" in wbPlayer:
					rfcPlayer.setFlipped(wbPlayer['Flipped'])
			elif wbPlayer['CivType'] != "CIVILIZATION_BARBARIAN": #barbarians are minors and always occupy last slot; we don't want them to reduce available slots
				gc.setMinorNationCiv(self.lastOpenSlot, civType, True)
				self.lastOpenSlot -= 1
			else:
				gc.setMinorNationCiv(gc.getMAX_CIV_PLAYERS(), civType, True)
