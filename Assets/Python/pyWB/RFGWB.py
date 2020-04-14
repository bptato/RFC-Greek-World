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

entitydefs = None

class WbParser:
	def __init__(self):
		self.wbValues = {}
		self.lastOpenSlot = gc.getMAX_CIV_PLAYERS() - 1 #last slots are reserved for minors. decrement this everytime a minor civ is added. -1 because of barbs

	def getLastOpenSlot(self):
		return self.lastOpenSlot

	def getWbValue(self, key, default):
		ret = default
		if key in self.wbValues:
			ret = self.wbValues[key]
		return ret

	def getGameValue(self, key, default):
		ret = default
		if key in self.wbValues['Game']:
			ret = self.wbValues['Game'][key]
		return ret

	def getMapValue(self, key, default):
		ret = default
		if key in self.wbValues['Map']:
			ret = self.wbValues['Map'][key]
		return ret

	def getPlayerValue(self, playerID, key, default):
		ret = default
		if key in self.wbValues['Players'][playerID]:
			ret = self.wbValues['Players'][playerID][key]
		return ret

	def getMaxTurns(self):
		if "MaxTurns" in self.wbValues['Game']:
			return self.wbValues['Game']['MaxTurns']
		return 0

	def getDescription(self):
		if "Description" in self.wbValues['Game']:
			return self.wbValues['Game']['Description']
		return "No description"

	def getModPath(self):
		return self.wbValues['Game']['ModPath']
	
	def setupEnabled(self):
		for wbPlayer in self.wbValues['Players']:
			rfcPlayer = riseFall.getRFCPlayer(gc.getInfoTypeForString(wbPlayer['CivType']))
			rfcPlayer.setEnabled(True)
			if "MinorNationStatus" in wbPlayer:
				rfcPlayer.setMinorCiv(True)
			else:
				rfcPlayer.setMinorCiv(False)

	def setupStartingYears(self):
		for wbPlayer in self.wbValues['Players']:
			if not "MinorNationStatus" in wbPlayer or wbPlayer['MinorNationStatus'] == 0: #major civ
				rfcPlayer = riseFall.getRFCPlayer(gc.getInfoTypeForString(wbPlayer['CivType']))
				rfcPlayer.setStartingYear(wbPlayer['StartingYear'])

	def createWBSave(self, name): #Write wbValues to a new save file in JSON format.
		values = OrderedDict({})
		gameValues = OrderedDict({})
		mapValues = OrderedDict({})

		players = []
		provinces = []
		plots = []

		#Game
		gameValues['Calendar'] = gc.getCalendarInfo(game.getCalendar()).getType()
		gameValues['GameTurn'] = game.getGameTurn()
		gameValues['StartYear'] = game.getStartYear()
		if "Game" in self.wbValues and "ModPath" in self.wbValues['Game']:
			gameValues['ModPath'] = self.wbValues['Game']['ModPath'] #TODO
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

				print "getting terrain type"
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
						#TODO experience, etc

				if plot.isCity():
					city = plot.getPlotCity()
					wbPlot['City'] = OrderedDict({})
					wbPlot['City']['CityOwner'] = gc.getCivilizationInfo(gc.getPlayer(city.getOwner()).getCivilizationType()).getType()
					wbPlot['City']['Year'] = game.getGameTurnYear()
					if city.getPopulation() > 1:
						wbPlot['City']['CityPopulation'] = city.getPopulation()
					#TODO religion, culture, etc

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

		#Players
		for i in range(gc.getNumCivilizationInfos()):
			rfcPlayer = riseFall.getRFCPlayer(i)
			if rfcPlayer.isEnabled():
				civInfo = gc.getCivilizationInfo(i)
				wbPlayer = OrderedDict({})
				wbPlayer['CivType'] = civInfo.getType()
				wbPlayer['CivicOptions'] = OrderedDict({})
				for j in range(gc.getNumCivicOptionInfos()):
					startingCivic = rfcPlayer.getStartingCivic(j)
					if startingCivic != -1:
						wbPlayer['CivicOptions'][gc.getCivicOptionInfo(j).getType()] = gc.getCivicInfo(startingCivic).getType()
				wbPlayer['StartingGold'] = rfcPlayer.getStartingGold()
				wbPlayer['StartingTechs'] = []
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

				#Scheduled units&cities
				for j in range(rfcPlayer.getNumScheduledUnits()):
					scheduledUnit = rfcPlayer.getScheduledUnit(j)
					wbPlot = plots[scheduledUnit.getY()*mapWidth + scheduledUnit.getX()]
					if "Units" not in wbPlot:
						wbPlot['Units'] = []
					wbUnit = OrderedDict({})
					if scheduledUnit.getAmount() > 1:
						wbUnit['Amount'] = scheduledUnit.getAmount()
					wbUnit['UnitOwner'] = civInfo.getType()
					wbUnit['UnitType'] = gc.getUnitInfo(scheduledUnit.getUnitType()).getType()
					wbUnit['Year'] = scheduledUnit.getYear()
					if scheduledUnit.getUnitAIType() != -1:
						wbUnit['UnitAIType'] = gc.getUnitAIInfo(scheduledUnit.getUnitAIType()).getType()
					if scheduledUnit.getFacingDirection() != -1 and scheduledUnit.getFacingDirection() != 4:
						wbUnit['FacingDirection'] = scheduledUnit.getFacingDirection()
					wbPlot['Units'].append(wbUnit)

				for j in range(rfcPlayer.getNumScheduledCities()):
					scheduledCity = rfcPlayer.getScheduledCity(j)
					wbPlot = plots[scheduledCity.getY()*mapWidth + scheduledCity.getX()]
					wbCity = OrderedDict({})
					wbCity['CityOwner'] = civInfo.getType()
					wbCity['Year'] = scheduledCity.getYear()
					wbCity['CityPopulation'] = scheduledCity.getPopulation()
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
			wbProvince['Left'] = province.getLeft()
			wbProvince['Bottom'] = province.getBottom()
			wbProvince['Right'] = province.getRight()
			wbProvince['Top'] = province.getTop()
			scheduledUnitsAmount = province.getNumScheduledUnits()
			for i in range(scheduledUnitsAmount):
				scheduledUnit = province.getScheduledUnit(i)
				if "Units" not in wbProvince:
					wbProvince['Units'] = []
				wbUnit = OrderedDict({})
				if scheduledUnit.getAmount() > 1:
					wbUnit['Amount'] = scheduledUnit.getAmount()
				#wbUnit['UnitOwner'] = civInfo.getType() #TODO

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
		values['Map'] = mapValues
		values['Players'] = players
		values['Provinces'] = provinces
		values['Plots'] = plots

		f = file(name, "w")
		f.write("application/json\n")
		unescapedValues = StringUtils.unescape(json.dumps(values, indent=1, separators=(',', ':'))) #replace html character references with human readable characters
		f.write(unescapedValues.encode("utf8"))

	def parseFile(self, name): #Parse a WBSave file.
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
				if '.' in s or '(' in s or ')' in s:
					raise Exception("Error while reading wbSave: json data contains ., ( or )")
				file_str.write(s)
			#Sorry for this. I tried to use literal_eval but apparently that doesn't work in this python version.
			#Not even a backported version of the function I found on the internet!
			#Nor does simplejson, because it uses unicode types and converting all keys to str would take forever.
			#So I just used eval. We also exit instantly if our file contains a '.', '(', or ')' character for at least some safety.
			self.wbValues = eval(file_str.getvalue())
			f.close()
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
		game.setStartYear(self.wbValues['Game']['StartYear'])
		mapWidth = self.wbValues['Map']['grid width']
		mapHeight = self.wbValues['Map']['grid height']
		wrapX = bool(self.wbValues['Map']['wrap X'])
		wrapY = bool(self.wbValues['Map']['wrap Y'])
		worldSize = WorldSizeTypes(CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), self.wbValues['Map']['world size']))
		climate = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), self.wbValues['Map']['climate'])
		seaLevel = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), self.wbValues['Map']['sealevel'])
		cmap.rebuild(mapWidth, mapHeight, self.wbValues['Map']['top latitude'], self.wbValues['Map']['bottom latitude'], wrapX, wrapY, WorldSizeTypes(worldSize), ClimateTypes(climate), SeaLevelTypes(seaLevel), 0, None)

		#Plots
		for wbPlot in self.wbValues['Plots']:
			x = wbPlot['x']
			y = wbPlot['y']
			plot = cmap.plot(x, y)

			#Plot types
			plot.setPlotType(PlotTypes(wbPlot['PlotType']), False, False)

			#Terrain types
			terrainType = gc.getInfoTypeForString(wbPlot['TerrainType'])
			plot.setTerrainType(terrainType, False, False)

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

			#Units
			if "Units" in wbPlot:
				for wbUnit in wbPlot['Units']:
					unitID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), wbUnit['UnitType'])
					ownerID = gc.getInfoTypeForString(wbUnit['UnitOwner'])
					rfcPlayer = riseFall.getRFCPlayer(ownerID)

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

					rfcPlayer.scheduleUnit(year, unitID, x, y, unitAI, facingDirection, amount)

			#City names
			if "CityNames" in wbPlot:
				for i in range(gc.getNumCivilizationInfos()):
					if gc.getCivilizationInfo(i).getType() in wbPlot['CityNames']:
						plot.setCityName(i, wbPlot['CityNames'][gc.getCivilizationInfo(i).getType()])

			#cnm converter thing
			#for i in range(len(CityNameMap.tCityMap)):
			#	if x < 61 and CityNameMap.tCityMap[i][59 - y][x] != "-1":
			#		cityName = CityNameMap.tCityMap[i][mapHeight - 1 - y][x]
			#		plot.setCityName(i, cityName)


			#Barbarians and independent cities
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

				rfcPlayer.scheduleCity(year, x, y, population)

			#Settler values
			if "SettlerValues" in wbPlot:
				for i in range(gc.getNumCivilizationInfos()):
					civType = gc.getCivilizationInfo(i).getType()
					if civType in wbPlot['SettlerValues']:
						plot.setSettlerValue(i, wbPlot['SettlerValues'][civType])

			#for j in range(gc.getNumCivilizationInfos()): #legacy settler map converter thing
			#	rfcPlayer = riseFall.getRFCPlayer(j)
			#	if not rfcPlayer.isMinor():
			#		if not (gc.getCivilizationInfo(j).getType() == "CIVILIZATION_HUNS" and SettlersMaps.tSettlersMaps[j][mapHeight - 1 - y][x]):
			#			plot.setSettlerValue(j, SettlersMaps.tSettlersMaps[j][mapHeight - 1 - y][x])

		cmap.recalculateAreas()


		#Goody huts
		goodyImprovement = -1
		for i in range(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGoody():
				goodyImprovement = i
				break

		#Provinces
		for wbProvince in self.wbValues['Provinces']:
			riseFall.addProvince(wbProvince['Name'], wbProvince['Bottom'], wbProvince['Left'], wbProvince['Top'], wbProvince['Right']);
			rfcProvince = riseFall.getRFCProvince(riseFall.getNumProvinces()-1) #last province should be the one we've just added
			#Goody huts
			amountRand = ((rfcProvince.getTop() - rfcProvince.getBottom()) + (rfcProvince.getRight() - rfcProvince.getLeft()))/5
			amount = game.getSorenRandNum(amountRand, "Goody hut amount roll")

			for i in range(amount):
				randPlotX = rfcProvince.getLeft() + game.getSorenRandNum(rfcProvince.getRight() - rfcProvince.getLeft(), "Random plot x roll")
				randPlotY = rfcProvince.getBottom() + game.getSorenRandNum(rfcProvince.getTop() - rfcProvince.getBottom(), "Random plot y roll")
				
				for wbPlayer in self.wbValues['Players']:
					if wbPlayer['StartingYear'] == self.wbValues['Game']['StartYear']:
						if randPlotX == wbPlayer['StartingX'] and randPlotY == wbPlayer['StartingY']:
							continue
				
				plot = cmap.plot(randPlotX, randPlotY)
				if not (plot.isWater() or plot.isPeak()):
					plot.setImprovementType(goodyImprovement)

			#Units
			if "Units" in wbProvince:
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

					rfcProvince.scheduleUnit(year, unitID, unitAI, facingDirection, amount, endYear, wbUnit['SpawnFrequency'])

		#Players
		for i in range(gc.getMAX_CIV_PLAYERS()):
			gc.getPlayer(i).setStartingPlot(cmap.plot(0, 0), True)

		for wbPlayer in self.wbValues['Players']:
			playerID = gc.getInfoTypeForString(wbPlayer['CivType'])
			rfcPlayer = riseFall.getRFCPlayer(playerID)

			if not "MinorNationStatus" in wbPlayer or wbPlayer['MinorNationStatus'] == 0: #major civ
				if "CoreProvinces" in wbPlayer:
					for wbCoreProvince in wbPlayer['CoreProvinces']:
						rfcPlayer.addCoreProvince(wbCoreProvince)

				rfcPlayer.setStartingPlot(wbPlayer['StartingX'], wbPlayer['StartingY'])

				if "StartingTechs" in wbPlayer:
					for startingTech in wbPlayer['StartingTechs']:
						techType = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), startingTech)
						rfcPlayer.addStartingTech(techType)

				if "CivicOptions" in wbPlayer:
					for i in range(gc.getNumCivicOptionInfos()):
						civicOptionType = gc.getCivicOptionInfo(i).getType()
						if civicOptionType in wbPlayer['CivicOptions']:
							civicOptionTypeNum = CvUtil.findInfoTypeNum(gc.getCivicOptionInfo, gc.getNumCivicOptionInfos(), wbPlayer['CivicOptions'][civicOptionType])
							rfcPlayer.setStartingCivic(i, civicOptionTypeNum)

				if "StartingGold" in wbPlayer:
					rfcPlayer.setStartingGold(wbPlayer['StartingGold'])

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
			elif wbPlayer['CivType'] != "CIVILIZATION_BARBARIAN": #barbarians are minors and always occupy last slot; we don't want them to reduce available slots
				gc.setMinorNationCiv(self.lastOpenSlot, playerID, True)
				self.lastOpenSlot -= 1
			else:
				gc.setMinorNationCiv(gc.getMAX_CIV_PLAYERS(), playerID, True)

		self.setupStartingYears()
