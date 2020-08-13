# Rhye's and Fall of the Greek World - Historical Victory Goals

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import cPickle as pickle

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#following ids refer to civ types, not slots!
iEgypt = int(CivilizationTypes.CIVILIZATION_EGYPT)
iSumeria = int(CivilizationTypes.CIVILIZATION_SUMERIA)
iIndusValley = int(CivilizationTypes.CIVILIZATION_INDUS_VALLEY)
iElam = int(CivilizationTypes.CIVILIZATION_ELAM)
iMinoa = int(CivilizationTypes.CIVILIZATION_MINOA)
iPhoenicia = int(CivilizationTypes.CIVILIZATION_PHOENICIA)
iBabylonia = int(CivilizationTypes.CIVILIZATION_BABYLON)
iHittites = int(CivilizationTypes.CIVILIZATION_HITTITE)
iMycenae = int(CivilizationTypes.CIVILIZATION_MYCENAE)
iAssyria = int(CivilizationTypes.CIVILIZATION_ASSYRIA)
iIsrael = int(CivilizationTypes.CIVILIZATION_ISRAEL)
iAthens = int(CivilizationTypes.CIVILIZATION_ATHENS)
iSparta = int(CivilizationTypes.CIVILIZATION_SPARTA)
iScythia = int(CivilizationTypes.CIVILIZATION_SCYTHIA)
iCarthage = int(CivilizationTypes.CIVILIZATION_CARTHAGE)
iCeltia = int(CivilizationTypes.CIVILIZATION_CELT)
iEtruria = int(CivilizationTypes.CIVILIZATION_ETRURIA)
iNubia = int(CivilizationTypes.CIVILIZATION_NUBIA)
iPersia = int(CivilizationTypes.CIVILIZATION_PERSIA)
iRome = int(CivilizationTypes.CIVILIZATION_ROME)
iMacedonia = int(CivilizationTypes.CIVILIZATION_MACEDONIA)
iIndia = int(CivilizationTypes.CIVILIZATION_INDIA)
iBactria = int(CivilizationTypes.CIVILIZATION_BACTRIA)
iNumidia = int(CivilizationTypes.CIVILIZATION_NUMIDIA)
iGermania = int(CivilizationTypes.CIVILIZATION_GERMANIA)
iSassanid = int(CivilizationTypes.CIVILIZATION_SASSANID)
iByzantium = int(CivilizationTypes.CIVILIZATION_BYZANTIUM)
iHuns = int(CivilizationTypes.CIVILIZATION_HUNS)
iIndependent = int(CivilizationTypes.CIVILIZATION_INDEPENDENT)
iIndependent2 = int(CivilizationTypes.CIVILIZATION_INDEPENDENT2)
iBarbarian = int(CivilizationTypes.CIVILIZATION_BARBARIAN)

iNumPlayers = gc.getMAX_CIV_PLAYERS() - 2 #-2: independent slots

def tech(techName):
	return CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_" + techName.upper())

def building(buildingName):
	return CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_" + buildingName.upper())

def unit(unitName):
	return CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_" + unitName.upper())

def civ2player(civType):
	for i in range(gc.getMAX_CIV_PLAYERS()):
		if gc.getPlayer(i).getCivilizationType() == civType:
			return i
	return None

def player2civ(playerType):
	return gc.getPlayer(playerType).getCivilizationType()



def controlsProvince(playerType, province):
	for i in range(iNumPlayers):
		if i == playerType:
			if province.getNumCities(i) < 1:
				return False
		else:
			if province.getNumCities(i) >= 1:
				return False
	return True

def religion(religionName):
	return CvUtil.findInfoTypeNum(gc.getReligionInfo, gc.getNumReligionInfos(), "RELIGION_" + religionName.upper())

class Victory:
	def initGlobals(self):
		global iNumCivs
		iNumCivs = gc.getNumCivilizationInfos()

		global i4000BC
		global i3000BC
		global i2200BC
		global i2180BC
		global i2000BC
		global i1900BC
		global i1800BC
		global i1690BC
		global i1500BC
		global i1400BC
		global i1300BC
		global i1200BC
		global i1250BC
		global i1100BC
		global i1070BC
		global i1000BC
		global i900BC
		global i800BC
		global i671BC
		global i600BC
		global i587BC
		global i500BC
		global i450BC
		global i400BC
		global i350BC
		global i300BC
		global i250BC
		global i100BC
		global i63BC

		i4000BC = getTurnForYear(-4000)
		i3000BC = getTurnForYear(-3000)
		i2200BC = getTurnForYear(-2200)
		i2180BC = getTurnForYear(-2180)
		i2000BC = getTurnForYear(-2000)
		i1900BC = getTurnForYear(-1900)
		i1800BC = getTurnForYear(-1800)
		i1690BC = getTurnForYear(-1690)
		i1500BC = getTurnForYear(-1500)
		i1400BC = getTurnForYear(-1400)
		i1300BC = getTurnForYear(-1300)
		i1200BC = getTurnForYear(-1200)
		i1250BC = getTurnForYear(-1250)
		i1100BC = getTurnForYear(-1100)
		i1070BC = getTurnForYear(-1070)
		i1000BC = getTurnForYear(-1000)
		i900BC = getTurnForYear(-900)
		i800BC = getTurnForYear(-800)
		i671BC = getTurnForYear(-671)
		i600BC = getTurnForYear(-600)
		i587BC = getTurnForYear(-587)
		i500BC = getTurnForYear(-500)
		i450BC = getTurnForYear(-450)
		i400BC = getTurnForYear(-400)
		i350BC = getTurnForYear(-350)
		i300BC = getTurnForYear(-300)
		i250BC = getTurnForYear(-250)
		i100BC = getTurnForYear(-100)
		i63BC = getTurnForYear(-63)


		global provPalestine
		global provPhoenicia
		global provUpperEgypt
		global provLowerEgypt
		global provNubia
		global provSumer
		global provAkkad
		global provSubartu
		global provKhuzestan
		global provAfrica
		global provCyprus
		global provSouthernIberia
		global provPeloponnese
		global provAttica
		global provMacedonia
		global provCentralGreece
		global provEuboea
		global provCyclades

		riseFall = CyRiseFall()
		provPalestine = riseFall.getRFCProvince("Palestine")
		provPhoenicia = riseFall.getRFCProvince("Phoenicia")
		provUpperEgypt = riseFall.getRFCProvince("Upper Egypt")
		provLowerEgypt = riseFall.getRFCProvince("Lower Egypt")
		provNubia = riseFall.getRFCProvince("Nubia")
		provSumer = riseFall.getRFCProvince("Sumer")
		provAkkad = riseFall.getRFCProvince("Akkad")
		provSubartu = riseFall.getRFCProvince("Subartu")
		provKhuzestan = riseFall.getRFCProvince("Khuzestan")
		provAfrica = riseFall.getRFCProvince("Africa")
		provCyprus = riseFall.getRFCProvince("Cyprus")
		provSouthernIberia = riseFall.getRFCProvince("Southern Iberia")
		provPersia = riseFall.getRFCProvince("Persia")
		provPeloponnese = riseFall.getRFCProvince("Peloponnese")
		provAttica = riseFall.getRFCProvince("Attica")
		provMacedonia = riseFall.getRFCProvince("Macedonia")
		provCentralGreece = riseFall.getRFCProvince("Central Greece")
		provEuboea = riseFall.getRFCProvince("Euboea")
		provCyclades = riseFall.getRFCProvince("Cyclades")

	def getGoal(self, i, j):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['lGoals'][i][j]

	def setGoal(self, i, j, iNewValue):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['lGoals'][i][j] = iNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))
		if iNewValue == 0:
			return
		if self.getGoal(i, 0) == 1 and self.getGoal(i, 1) == 1 and self.getGoal(i, 2) == 1:
			if gc.getGame().getWinner() == -1:
				for j in range(gc.getMAX_CIV_PLAYERS()):
					if gc.getPlayer(j).getCivilizationType() == i:
						gc.getGame().setWinner(j, 7)

	def getEnslavedUnits(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['iEnslavedUnits']

	def getBabyloniaKilledCivs(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['babyloniaKilledCivs']

	def setBabyloniaKilledCivs(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['babyloniaKilledCivs'] = i
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getMycenaeTombsBuilt(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['mycenaeTombsBuilt']

	def setMycenaeTombsBuilt(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['mycenaeTombsBuilt'] = i
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getAthensHarborBuilt(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['AthensharborBuilt']

	def setAthensHarborBuilt(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['AthensharborBuilt'] = i
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getHittiteKilledUnits(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['hittiteKilledUnits']

	def setHittiteKilledUnits(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['hittiteKilledUnits'] = i
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def get2OutOf3(self, iCiv):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['l2OutOf3'][iCiv]

	def set2OutOf3(self, iCiv, bNewValue):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['l2OutOf3'][iCiv] = bNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getSumerianTechs(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['lSumerianTechs'][i]

	def setSumerianTechs(self, i, iNewValue):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['lSumerianTechs'][i] = iNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getAthensTechs(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['lAthensTechs'][i]

	def setAthensTechs(self, i, iNewValue):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['lAthensTechs'][i] = iNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getWondersBuilt( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lWondersBuilt'][iCiv]

	def setWondersBuilt( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lWondersBuilt'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getReligionFounded(self, iCiv):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['lReligionFounded'][iCiv]

	def setReligionFounded(self, iCiv, iNewValue ):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['lReligionFounded'][iCiv] = iNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def onLoadGame(self):
		self.initGlobals()

	def onGameStart(self):
		self.initGlobals()

		#init script data
		scriptDict = {
					'lGoals': [[-1 for i in range(iNumCivs)] for j in range(iNumCivs)], #bluepotato: [[-1,-1,-1]]*con.iNumCivs would copy the same array over and over. see https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
					'iEnslavedUnits': 0,
					'lSumerianTechs': [-1, -1, -1],
					'lAthensTechs': [-1, -1, -1],
					'lWondersBuilt': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					'babyloniaKilledCivs': 0,
					'hittiteKilledUnits': 0,
					'mycenaeTombsBuilt': 0,
					'AthensharborBuilt': 0,
					'lReligionFounded': [-1, -1, -1, -1, -1, -1, -1],
					'l2OutOf3': [False] * iNumCivs,
		}
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def ownedCityPlots(self, tCoords, result, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if (pCurrent.getOwner() == argsList):
			if (pCurrent.isCity()):
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def ownedCityPlotsAdjacentArea(self, tCoords, result, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if (pCurrent.getOwner() == argsList[0] and pCurrent.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area())):
			if (pCurrent.isCity()):
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		pPlayer = gc.getPlayer(iPlayer)

		if not pPlayer.isAlive():
			return

		civType = pPlayer.getCivilizationType()

		if (civType == iEgypt):
			if (iGameTurn <= i1070BC):
				if (iGameTurn == i2180BC):
					if (pPlayer.countTotalCulture() >= 1000):
						self.setGoal(iEgypt, 0, 1)
					else:
						self.setGoal(iEgypt, 0, 0)
				elif (iGameTurn == i1690BC):
					if (gc.getGame().getTeamRank(pPlayer.getTeam()) == 0):
						self.setGoal(iEgypt, 1, 1)
					else:
						self.setGoal(iEgypt, 1, 0)
				elif (iGameTurn > i1690BC):
					bPhoenicia = provPhoenicia.getNumCities(iPlayer) >= 2
					bPalestine = provPalestine.getNumCities(iPlayer) >= 2
					bEgypt = provUpperEgypt.getNumCities(iPlayer) + provLowerEgypt.getNumCities(iPlayer) >= 2
					bNubia = provNubia.getNumCities(iPlayer) >= 2
					if (bPhoenicia and bPalestine and bEgypt and bNubia):
						self.setGoal(iEgypt, 2, 1)
					elif iGameTurn > i1070BC:
						self.setGoal(iEgypt, 2, 0)
		elif (civType == iSumeria):
			if (iGameTurn == i2200BC):
				bSumer = provSumer.getNumCities(iPlayer) >= 1
				bAkkad = provAkkad.getNumCities(iPlayer) >= 1
				bSubartu = provSubartu.getNumCities(iPlayer) >= 1
				bKhuzestan = provKhuzestan.getNumCities(iPlayer) >= 1
				if (bSumer and bAkkad and bSubartu and bKhuzestan):
					self.setGoal(iSumeria, 2, 1)
				else:
					self.setGoal(iSumeria, 2, 0)

			if (iGameTurn == i2000BC):
				bestCity = self.calculateTopCityCulture(46, 19)
				if (bestCity != -1):
					if (bestCity.getOwner() == iPlayer and bestCity.getX() == 46 and bestCity.getY() == 19):
						self.setGoal(iSumeria, 1, 1)
					else:
						self.setGoal(iSumeria, 1, 0)
				else:
					self.setGoal(iSumeria, 1, 0)
		elif (civType == iIndusValley):
			if (iGameTurn == i1250BC):
				iIndusValleyResource = 0
				bResources = True
				for iBonus in range(gc.getNumBonusInfos()):
					if (pPlayer.getNumAvailableBonuses(iBonus) > 0):
						iIndusValleyResource += 1
				for iCiv in range(iNumPlayers):
					if (iCiv != iIndusValley):
						pCiv = gc.getPlayer(iCiv)
						iElseResource = 0
						if (pCiv.isAlive()):
							for iBonusA in range(gc.getNumBonusInfos()):
								if (pCiv.getNumAvailableBonuses(iBonusA) > 0):
									iElseResource += 1
							if (iElseResource > iIndusValleyResource):
								bResources = False
								break
				if (bResources):
					self.setGoal(iIndusValley, 1, 1)
				else:
					self.setGoal(iIndusValley, 1, 0)

			if (iGameTurn == i1500BC):
				iPop = pPlayer.getRealPopulation()
				bFirst = True
				for iCiv in range(iNumPlayers):
					if (iPop < gc.getPlayer(iCiv).getRealPopulation()):
						bFirst = False
						break
				if (bFirst):
					self.setGoal(iIndusValley, 0, 1)
				else:
					self.setGoal(iIndusValley, 0, 0)

			if (iGameTurn == i1000BC):
				if (self.getGoal(iIndusValley, 2) == -1): #see onCityAcquired()
					self.setGoal(iIndusValley, 2, 1)

		elif civType == iElam and iGameTurn <= i1000BC:
			if iGameTurn < i1900BC:
				cIndusValley = civ2player(iIndusValley)
				if civ2player(cIndusValley) != None and pPlayer.canContact(cIndusValley) and pPlayer.canTradeNetworkWith(cIndusValley):
					self.setGoal(iElam, 1, 1)
			elif iGameTurn == i1900BC and self.getGoal(iElam, 1) == -1:
				self.setGoal(iElam, 1, 0)
			elif iGameTurn < i1500BC and self.getGoal(iElam, 2) == -1:
				if provPersia.getNumCities(iPlayer) >= 5:
					self.setGoal(iElam, 2, 1)
			elif iGameTurn == i1500BC and self.getGoal(iElam, 2) == -1:
				if provPersia.getNumCities(iPlayer) >= 5:
					self.setGoal(iElam, 2, 1)
				else:
					self.setGoal(iElam, 2, 0)
		elif (civType == iMinoa):
			if (iGameTurn == i1400BC):
				if (gc.getTeam(pPlayer.getTeam()).isHasTech(tech('calendar'))):
					self.setGoal(iMinoa, 0, 1)
				else:
					self.setGoal(iMinoa, 0, 0)

			if (iGameTurn == i1200BC):
				if (gc.getGame().getTeamRank(pPlayer.getTeam()) == 0):
					self.setGoal(iMinoa, 1, 1)
				else:
					self.setGoal(iMinoa, 1, 0)

			if (iGameTurn == i1000BC):
				bestCity = self.calculateTopCityCulture(33, 21)
				if (bestCity != -1):
					if (bestCity.getOwner() == iPlayer and bestCity.getX() == 33 and bestCity.getY() == 21):
						self.setGoal(iMinoa, 2, 1)
					else:
						self.setGoal(iMinoa, 2, 0)
				else:
					self.setGoal(iMinoa, 2, 0)

		elif (civType == iPhoenicia):
			if (iGameTurn == i900BC):
				bPhoenicia = provPhoenicia.getNumCities(iPlayer) >= 1
				bAfrica = provAfrica.getNumCities(iPlayer) >= 1
				bCyprus = provCyprus.getNumCities(iPlayer) >= 1
				bSouthernIberia = provSouthernIberia.getNumCities(iPlayer) >= 1
				if bPhoenicia and bAfrica and bCyprus and bSouthernIberia:
					self.setGoal(iPhoenicia, 0, 1)
				else:
					self.setGoal(iPhoenicia, 0, 0)

			if (iGameTurn == i600BC):
				lRevealedMap = [0] * iNumPlayers
				for iCiv in range(iNumPlayers):
					mapWidth = CyMap().getGridWidth()
					mapHeight = CyMap().getGridHeight()
					for x in range(mapWidth):
						for y in range(mapHeight):
							if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
								lRevealedMap[iCiv] += 1
				bBestMap = True
				for iCiv in range(iNumPlayers):
					if (lRevealedMap[iPlayer] < lRevealedMap[iCiv]):
						bBestMap = False
						break

				if bBestMap:
					self.setGoal(iPhoenicia, 1, 1)
				else:
					self.setGoal(iPhoenicia, 1, 0)

			if (iGameTurn == i500BC):
				iPhoeniciaResource = 0
				bResources = True
				for iBonus in range(gc.getNumBonusInfos()):
					if (pPlayer.getNumAvailableBonuses(iBonus) > 0):
						iPhoeniciaResource += 1
				for iCiv in range(iNumPlayers):
					if (iCiv != iPlayer):
						pCiv = gc.getPlayer(iCiv)
						iElseResource = 0
						if (pCiv.isAlive()):
							for iBonusA in range(gc.getNumBonusInfos()):
								if (pCiv.getNumAvailableBonuses(iBonusA) > 0):
									iElseResource += 1
							if (iElseResource > iPhoeniciaResource):
								bResources = False
								break
				if (bResources):
					self.setGoal(iPhoenicia, 2, 1)
				else:
					self.setGoal(iPhoenicia, 2, 0)

		elif civType == iBabylonia and iGameTurn <= i600BC:
			babylonPlot = gc.getMap().plot(46, 22)
			if iGameTurn < i1000BC:
				if babylonPlot.isCity():
					if babylonPlot.getPlotCity().getNumWorldWonders() >= 6:
						self.setGoal(iBabylonia, 0, 1)
			elif iGameTurn == i1000BC:
				if not babylonPlot.isCity() or babylonPlot.getPlotCity().getNumWorldWonders() < 6:
					self.setGoal(iBabylonia, 0, 0)
				else:
					self.setGoal(iBabylonia, 0, 1)
			if iGameTurn < i600BC:
				if self.getBabyloniaKilledCivs() >= 3:
					self.setGoal(iBabylonia, 2, 1)
			elif iGameTurn == i600BC:
				if self.getBabyloniaKilledCivs() < 3:
					self.setGoal(iBabylonia, 2, 0)
				else:
					self.setGoal(iBabylonia, 2, 1)
		elif civType == iHittites:
			if self.getGoal(iHittites, 0) == -1 and iGameTurn > i1400BC:
				self.setGoal(iHittites, 0, 0)
			if iGameTurn == i1300BC:
				self.setGoal(iHittites, 1, controlsProvince(iPlayer, provPhoenicia))
			elif iGameTurn < i1200BC:
				if self.getHittiteKilledUnits() >= 15:
					self.setGoal(iHittites, 2, 1)
			if self.getGoal(iHittites, 2) == -1 and iGameTurn > i1200BC:
				self.setGoal(iHittites, 2, 0)
		elif civType == iMycenae:
			if self.getGoal(iMycenae, 0) == -1 and iGameTurn > i1300BC:
				self.setGoal(iMycenae, 0, 0)
			if self.getGoal(iMycenae, 1) == -1 and iGameTurn > i1100BC:
				self.setGoal(iMycenae, 1, 0)
			if iGameTurn == i1000BC:
				barbCities = provLydia.getNumCities(civ2player(iBarbarian)) \
				+ provLydia.getNumCities(civ2player(iIndependent)) \
				+ provLydia.getNumCities(civ2player(iIndependent2)) \
				+ provAnatolia.getNumCities(civ2player(iBarbarian)) \
				+ provAnatolia.getNumCities(civ2player(iIndependent)) \
				+ provAnatolia.getNumCities(civ2player(iIndependent2))

				if barbCities > 0:
					self.setGoal(iMycenae, 2, 0)
				else:
					self.setGoal(iMycenae, 2, 1)
		elif civType == iAssyria:
			if self.getGoal(iAssyria, 0) == -1:
				goalCompleted = controlsProvince(iPlayer, provSubartu) and \
						controlsProvince(iPlayer, provAkkad) and \
						controlsProvince(iPlayer, provPhoenicia) and \
						controlsProvince(iPlayer, provSumer)
				if goalCompleted:
					self.setGoal(iAssyria, 0, 1)
				elif iGameTurn > i1250BC:
					self.setGoal(iAssyria, 0, 0)
			if self.getGoal(iAssyria, 1) == -1:
				holyCityCondition = False
				anunnaki = gc.getInfoTypeForString("RELIGION_ANUNNAKI")
				holyCity = gc.getGame().getHolyCity(anunnaki)
				if holyCity:
					if holyCity.getOwner() == iPlayer and holyCity.isCapital():
						ashurbanipalLibrary = gc.getInfoTypeForString("BUILDING_ASHURBANIPAL_LIBRARY")
						if holyCity.isHasBuilding(ashurbanipalLibrary):
							self.setGoal(Assyria, 1, 1)
			if self.getGoal(iAssyria, 2) == -1:
				goalCompleted = controlsProvince(iPlayer, provSubartu) and \
						controlsProvince(iPlayer, provAkkad) and \
						controlsProvince(iPlayer, provPhoenicia) and \
						controlsProvince(iPlayer, provSumer) and \
						controlsProvince(iPlayer, provKhuzestan) and \
						controlsProvince(iPlayer, provLowerEgypt) and \
						controlsProvince(iPlayer, provAnatolia) and \
						controlsProvince(iPlayer, provPalestine)

				if goalCompleted:
					self.setGoal(iAssyria, 2, 1)
				elif iGameTurn > i671BC:
					self.setGoal(iAssyria, 2, 0)

		elif civType == iIsrael:
			if (self.getGoal(iIsrael, 1) == -1):
					if (iGameTurn <= i63BC):
						Judaism = gc.getInfoTypeForString("RELIGION_JUDAISM")
						religionPercent = gc.getGame().calculateReligionPercent(Judaism)
						if (religionPercent >= 30.0):
							self.setGoal(iIsrael, 1, 1)
					else:
							self.setGoal(iIsrael, 1, 0)
			if self.getGoal(iIsrael, 0) == -1:
				goalCompleted = controlsProvince(iPlayer, provPhoenicia) and \
					controlsProvince(iPlayer, provPalestine)
				if goalCompleted:
					self.setGoal(iIsrael, 0, 1)
				elif iGameTurn > i587BC:
					self.setGoal(iIsrael, 0, 0)

		elif civType == iAthens:
			if self.getGoal(iAthens, 2) == -1 and iGameTurn > i400BC:
				self.setGoal(iAthens, 2, 0)

			if self.getGoal(iAthens, 1) == -1 and iGameTurn > i450BC:
				self.setGoal(iAthens, 1, 0)

		elif civType == iSparta:
			if self.getGoal(iSparta, 1) == -1:
				goalCompleted = controlsProvince(iPlayer, provPeloponnese) and \
						controlsProvince(iPlayer, provAttica) and \
						controlsProvince(iPlayer, provMacedonia) and \
						controlsProvince(iPlayer, provCentralGreece) and \
						controlsProvince(iPlayer, provEuboea) and \
						controlsProvince(iPlayer, provCyclades)
				if goalCompleted:
					self.setGoal(iSparta, 1, 1)
				elif iGameTurn >= i400BC - 1: #TODO: remove this ASAP
					self.setGoal(iSparta, 1, 0)

			if (iGameTurn == i350BC):
					if (gc.getGame().getTeamRank(pPlayer.getTeam()) == 0):
						self.setGoal(iSparta, 2, 1)
					else:
						self.setGoal(iSparta, 2, 0)

			if (iGameTurn == i450BC):
					if (pPlayer.getNumUnits() >= 30):
						self.setGoal(iSparta, 0, 1)
					else:
						self.setGoal(iSparta, 0, 0)

	def onCityBuilt(self, city):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()

	def onReligionFounded(self, iReligion, iFounder):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()
		civType = gc.getPlayer(iFounder).getCivilizationType()

		if (civType == iIsrael):
			self.setReligionFounded(iReligion, 1)
		elif (self.getGoal(iIsrael, 0) == -1):
			if (iReligion == religion('Judaism')):
					self.setGoal(iIsrael, 2, 0)
			elif (iReligion == religion('Christianity')):
					self.setGoal(iIsrael, 2, 0)

		if (self.getReligionFounded(religion('Judaism')) == 1 and self.getReligionFounded(religion('Christianity')) == 1):
			self.setGoal(iIsrael, 2, 1)

	def onCityAcquired(self, owner, attacker, city, bConquest):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()
		cityX = city.getX()
		cityY = city.getY()

		ownerType = gc.getPlayer(owner).getCivilizationType()
		attackerType = gc.getPlayer(attacker).getCivilizationType()

		if self.getGoal(iElam, 0) == -1 and cityX == 46 and cityY == 19: #Ur captured by Elam
			if attackerType == iElam:
				self.setGoal(iElam, 0, 1)
			else:
				self.setGoal(iElam, 0, 0)

		if self.getGoal(iHittites, 0) == -1 and cityX == 46 and cityY == 22: #Babylon captured by Hittites
			if attackerType == iHittites:
				self.setGoal(iHittites, 0, 1)

		if (ownerType == iIndusValley):
			if (bConquest):
				if (self.getGoal(iIndusValley, 2) == -1):
					if (iGameTurn <= i1000BC):
						if (attackerType == iBarbarian):
							self.setGoal(iIndusValley, 2, 0)

		if attackerType == iBabylonia:
			if gc.getPlayer(owner).getNumCities() == 0:
				self.setBabyloniaKilledCivs(self.getBabyloniaKilledCivs()+1)

	def onCityRazed(self, city, conqueror, owner):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		if self.getGoal(iElam, 0) == -1 and city.getX() == 46 and city.getY() == 19: #Ur captured by Elam
			if gc.getPlayer(conqueror).getCivilizationType() == iElam:
				self.setGoal(iElam, 0, 1)
			else:
				self.setGoal(iElam, 0, 0)

	def onTechAcquired(self, iTech, iPlayer):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()
		if iGameTurn == gc.getGame().getStartTurn():
			return

		civType = gc.getPlayer(iPlayer).getCivilizationType()

		if (civType == iSumeria):
			if (self.getGoal(iSumeria, 0) == -1):
				if (iTech == tech('the_wheel')):
					self.setSumerianTechs(0, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setSumerianTechs(0, 0)
				elif (iTech == tech('masonry')):
					self.setSumerianTechs(1, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setSumerianTechs(1, 0)
				elif (iTech == tech('cuneiform')):
					self.setSumerianTechs(2, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setSumerianTechs(2, 0)
				if (self.getSumerianTechs(0) == 1 and self.getSumerianTechs(1) == 1 and self.getSumerianTechs(2) == 1):
					self.setGoal(iSumeria, 0, 1)
				elif (self.getSumerianTechs(0) == 0 or self.getSumerianTechs(1) == 0 or self.getSumerianTechs(2) == 0):
					self.setGoal(iSumeria, 0, 0)

		elif (civType == iAthens):
			if (self.getGoal(iAthens, 0) == -1):
				if (iTech == tech('drama')):
					self.setAthensTechs(0, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setAthensTechs(0, 0)
				elif (iTech == tech('democracy')):
					self.setAthensTechs(1, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setAthensTechs(1, 0)
				elif (iTech == tech('engineering')):
					self.setAthensTechs(2, 1)
					for iCiv in range(iNumPlayers):
						if (iCiv != iPlayer):
							if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
								self.setAthensTechs(2, 0)
				if (self.getAthensTechs(0) == 1 and self.getAthensTechs(1) == 1 and self.getAthensTechs(2) == 1):
					self.setGoal(iAthens, 0, 1)
				elif (self.getAthensTechs(0) == 0 or self.getAthensTechs(1) == 0 or self.getAthensTechs(2) == 0):
					self.setGoal(iAthens, 0, 0)

		elif civType == iBabylonia:
			if self.getGoal(iBabylonia, 1) == -1:
				if iTech == tech('code_of_laws'):
					self.setGoal(iBabylonia, 1, 1)
					for iCiv in range(iNumPlayers):
						if iCiv != iPlayer:
							if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech):
								self.setGoal(iBabylonia, 1, 0)
								break

	def onBuildingBuilt(self, iPlayer, iBuilding):
		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		iGameTurn = gc.getGame().getGameTurn()
		civType = gc.getPlayer(iPlayer).getCivilizationType()

		if civType == iMycenae:
			if iBuilding == building('mycenae_tholoi'):
				if self.getGoal(iMycenae, 0) == -1:
					self.setMycenaeTombsBuilt(self.getMycenaeTombsBuilt() + 1)
					if self.getMycenaeTombsBuilt() >= 4:
						self.setGoal(iMycenae, 0, 1)
			elif iBuilding == building('lion_gate'):
				if self.getGoal(iMycenae, 1) == -1:
					self.setGoal(iMycenae, 1, 1)

		elif civType == iAthens:
			if iBuilding == building('harbor'):
				if self.getGoal(iAthens, 2) == -1:
					self.setAthensHarborBuilt(self.getAthensHarborBuilt() + 1)
					if self.getAthensHarborBuilt() >= 7:
						self.setGoal(iAthens, 2, 1)
			if (self.getGoal(iAthens, 1) == -1):
					if (iBuilding == building('Oracle') or iBuilding == building('Colossus') or iBuilding == building('Parthenon') or iBuilding == building('Artemis')):
						self.setWondersBuilt(iAthens, self.getWondersBuilt(iAthens) + 1)
					if (self.getWondersBuilt(iAthens) == 4):
						self.setGoal(iAthens, 1, 1)

	def onCombatResult(self, argsList):

		if (not gc.getGame().isVictoryValid(7)): #7 == historical
			return

		pWinningUnit,pLosingUnit = argsList
		pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
		pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		iPlayer = pWinningPlayer.getID()
		civType = gc.getPlayer(iPlayer).getCivilizationType()
		if civType == iHittites:
			if pWinningUnit.getUnitType() == unit('hittite_huluganni'):
				self.setHittiteKilledUnits(self.getHittiteKilledUnits() + 1)

	def calculateTopCityCulture(self, x, y):
		iBestCityValue = 0
		pCurrent = gc.getMap().plot(x, y)
		if (pCurrent.isCity()):
			bestCity = pCurrent.getPlotCity()
			for iPlayerLoop in range(gc.getMAX_PLAYERS()):
				apCityList = PyPlayer(iPlayerLoop).getCityList()

				for pCity in apCityList:
					iTotalCityValue = pCity.GetCy().countTotalCultureTimes100()
					if (iTotalCityValue > iBestCityValue and not pCity.isBarbarian()):
						bestCity = pCity
						iBestCityValue = iTotalCityValue
			return bestCity
		return -1

	def calculateTopCityPopulation(self, x, y):
		iBestCityValue = 0
		pCurrent = gc.getMap().plot(x, y)
		if (pCurrent.isCity()):
			bestCity = pCurrent.getPlotCity()
			for iPlayerLoop in range(gc.getMAX_PLAYERS()):
				apCityList = PyPlayer(iPlayerLoop).getCityList()

				for pCity in apCityList:
					iTotalCityValue = pCity.getPopulation()
					if (iTotalCityValue > iBestCityValue and not pCity.isBarbarian()):
						bestCity = pCity
						iBestCityValue = iTotalCityValue
			return bestCity
		return -1
