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
iEgypt = CivilizationTypes.CIVILIZATION_EGYPT
iSumeria = CivilizationTypes.CIVILIZATION_SUMERIA
iIndusValley = CivilizationTypes.CIVILIZATION_INDUS_VALLEY
iElam = CivilizationTypes.CIVILIZATION_ELAM
iMinoa = CivilizationTypes.CIVILIZATION_MINOA
iPhoenicia = CivilizationTypes.CIVILIZATION_PHOENICIA
iBabylonia = CivilizationTypes.CIVILIZATION_BABYLON
iHittites = CivilizationTypes.CIVILIZATION_HITTITE
iMycenae = CivilizationTypes.CIVILIZATION_MYCENAE
iAssyria = CivilizationTypes.CIVILIZATION_ASSYRIA
iIsrael = CivilizationTypes.CIVILIZATION_ISRAEL
iAthens = CivilizationTypes.CIVILIZATION_ATHENS
iSparta = CivilizationTypes.CIVILIZATION_SPARTA
iScythia = CivilizationTypes.CIVILIZATION_SCYTHIA
iCarthage = CivilizationTypes.CIVILIZATION_CARTHAGE
iCeltia = CivilizationTypes.CIVILIZATION_CELT
iEtruria = CivilizationTypes.CIVILIZATION_ETRURIA
iNubia = CivilizationTypes.CIVILIZATION_NUBIA
iPersia = CivilizationTypes.CIVILIZATION_PERSIA
iRome = CivilizationTypes.CIVILIZATION_ROME
iMacedonia = CivilizationTypes.CIVILIZATION_MACEDONIA
iIndia = CivilizationTypes.CIVILIZATION_INDIA
iBactria = CivilizationTypes.CIVILIZATION_BACTRIA
iNumidia = CivilizationTypes.CIVILIZATION_NUMIDIA
iGermania = CivilizationTypes.CIVILIZATION_GERMANIA
iSassanid = CivilizationTypes.CIVILIZATION_SASSANID
iByzantium = CivilizationTypes.CIVILIZATION_BYZANTIUM
iHuns = CivilizationTypes.CIVILIZATION_HUNS
iIndependent = CivilizationTypes.CIVILIZATION_INDEPENDENT
iIndependent2 = CivilizationTypes.CIVILIZATION_INDEPENDENT2
iBarbarian = CivilizationTypes.CIVILIZATION_BARBARIAN

iNumPlayers = gc.getMAX_CIV_PLAYERS() - 2 #-2: independent slots

def tech(techName):
	return CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), "TECH_" + techName.upper())

def building(buildingName):
	return CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), "BUILDING_" + buildingName.upper())

def unit(unitName):
	return CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_" + unitName.upper())

def civ2player(civType):
	return gc.getRiseFall().getRFCPlayer(civType).getPlayerType()

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

def bonus(bonusName):
	return CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), "BONUS_" + bonusName.upper())

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
		global i542BC
		global i500BC
		global i450BC
		global i400BC
		global i350BC
		global i330BC
		global i300BC
		global i275BC
		global i270BC
		global i250BC
		global i200BC
		global i100BC
		global i63BC
		global i0AD
		global i10AD
		global i180AD
		global i350AD
		global i400AD
		global i500AD

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
		i1250BC = getTurnForYear(-1250)
		i1200BC = getTurnForYear(-1200)
		i1100BC = getTurnForYear(-1100)
		i1070BC = getTurnForYear(-1070)
		i1000BC = getTurnForYear(-1000)
		i900BC = getTurnForYear(-900)
		i800BC = getTurnForYear(-800)
		i671BC = getTurnForYear(-671)
		i600BC = getTurnForYear(-600)
		i587BC = getTurnForYear(-587)
		i542BC = getTurnForYear(-542)
		i500BC = getTurnForYear(-500)
		i450BC = getTurnForYear(-450)
		i400BC = getTurnForYear(-400)
		i350BC = getTurnForYear(-350)
		i330BC = getTurnForYear(-330)
		i300BC = getTurnForYear(-300)
		i275BC = getTurnForYear(-275)
		i270BC = getTurnForYear(-270)
		i250BC = getTurnForYear(-250)
		i200BC = getTurnForYear(-200)
		i100BC = getTurnForYear(-100)
		i63BC = getTurnForYear(-63)
		i0AD = getTurnForYear(0)
		i10AD = getTurnForYear(10)
		i180AD = getTurnForYear(180)
		i350AD = getTurnForYear(350)
		i400AD = getTurnForYear(400)
		i500AD = getTurnForYear(500)


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
		global provPersia
		global provPeloponnese
		global provAttica
		global provMacedonia
		global provCentralGreece
		global provEuboea
		global provCyclades
		global provAnatolia
		global provCrimea
		global provSarmatia
		global provCaucasus
		global provScythia
		global provSicily
		global provItaly
		global provMessapia
		global provCelticGaul
		global provNorthernIberia
		global provBritannia
		global provRaetia
		global provVenetia
		global provLydia
		global provCorsica
		global provMedia
		global provThracia

		riseFall = CyRiseFall()
		provPalestine = riseFall.getProvince(riseFall.findProvince("PROVINCE_PALESTINE"))
		provPhoenicia = riseFall.getProvince(riseFall.findProvince("PROVINCE_PHOENICIA"))
		provUpperEgypt = riseFall.getProvince(riseFall.findProvince("PROVINCE_UPPER_EGYPT"))
		provLowerEgypt = riseFall.getProvince(riseFall.findProvince("PROVINCE_LOWER_EGYPT"))
		provNubia = riseFall.getProvince(riseFall.findProvince("PROVINCE_NUBIA"))
		provSumer = riseFall.getProvince(riseFall.findProvince("PROVINCE_SUMER"))
		provAkkad = riseFall.getProvince(riseFall.findProvince("PROVINCE_AKKAD"))
		provSubartu = riseFall.getProvince(riseFall.findProvince("PROVINCE_SUBARTU"))
		provKhuzestan = riseFall.getProvince(riseFall.findProvince("PROVINCE_KHUZESTAN"))
		provAfrica = riseFall.getProvince(riseFall.findProvince("PROVINCE_AFRICA"))
		provCyprus = riseFall.getProvince(riseFall.findProvince("PROVINCE_CYPRUS"))
		provSouthernIberia = riseFall.getProvince(riseFall.findProvince("PROVINCE_SOUTHERN_IBERIA"))
		provPersia = riseFall.getProvince(riseFall.findProvince("PROVINCE_PERSIA"))
		provPeloponnese = riseFall.getProvince(riseFall.findProvince("PROVINCE_PELOPONNESE"))
		provAttica = riseFall.getProvince(riseFall.findProvince("PROVINCE_ATTICA"))
		provMacedonia = riseFall.getProvince(riseFall.findProvince("PROVINCE_MACEDONIA"))
		provCentralGreece = riseFall.getProvince(riseFall.findProvince("PROVINCE_CENTRAL_GREECE"))
		provEuboea = riseFall.getProvince(riseFall.findProvince("PROVINCE_EUBOEA"))
		provCyclades = riseFall.getProvince(riseFall.findProvince("PROVINCE_CYCLADES"))
		provAnatolia = riseFall.getProvince(riseFall.findProvince("PROVINCE_ANATOLIA"))
		provCrimea = riseFall.getProvince(riseFall.findProvince("PROVINCE_CRIMEA"))
		provSarmatia = riseFall.getProvince(riseFall.findProvince("PROVINCE_SARMATIA"))
		provCaucasus = riseFall.getProvince(riseFall.findProvince("PROVINCE_CAUCASUS"))
		provScythia = riseFall.getProvince(riseFall.findProvince("PROVINCE_SCYTHIA"))
		provSicily = riseFall.getProvince(riseFall.findProvince("PROVINCE_SICILY"))
		provItaly = riseFall.getProvince(riseFall.findProvince("PROVINCE_ITALY"))
		provMessapia = riseFall.getProvince(riseFall.findProvince("PROVINCE_MESSAPIA"))
		provCelticGaul = riseFall.getProvince(riseFall.findProvince("PROVINCE_CELTIC_GAUL"))
		provNorthernIberia = riseFall.getProvince(riseFall.findProvince("PROVINCE_NORTHERN_IBERIA"))
		provBritannia = riseFall.getProvince(riseFall.findProvince("PROVINCE_BRITANNIA"))
		provRaetia = riseFall.getProvince(riseFall.findProvince("PROVINCE_RAETIA"))
		provVenetia = riseFall.getProvince(riseFall.findProvince("PROVINCE_VENETIA"))
		provLydia = riseFall.getProvince(riseFall.findProvince("PROVINCE_LYDIA"))
		provCorsica = riseFall.getProvince(riseFall.findProvince("PROVINCE_CORSICA"))
		provMedia = riseFall.getProvince(riseFall.findProvince("PROVINCE_MEDIA"))
		provThracia = riseFall.getProvince(riseFall.findProvince("PROVINCE_THRACIA"))

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
		
	def getScythianKilledCivs(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['scythianKilledCivs']

	def setScythianKilledCivs(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['scythianKilledCivs'] = i
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
		return scriptDict['athensHarborBuilt']

	def setAthensHarborBuilt(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['athensHarborBuilt'] = i
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def getHittiteKilledUnits(self):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['hittiteKilledUnits']

	def setHittiteKilledUnits(self, i):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['hittiteKilledUnits'] = i
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

	def getReligionFounded(self, religion):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		return scriptDict['lReligionFounded'][religion]

	def setReligionFounded(self, religion, iNewValue):
		scriptDict = pickle.loads(gc.getGame().getScriptData())
		scriptDict['lReligionFounded'][religion] = iNewValue
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def onLoadGame(self):
		self.initGlobals()

	def onGameStart(self):
		self.initGlobals()

		#init script data
		scriptDict = {
					'lGoals': [[-1 for i in range(iNumCivs)] for j in range(iNumCivs)],
					'iEnslavedUnits': 0,
					'lSumerianTechs': [-1, -1, -1],
					'lAthensTechs': [-1, -1, -1],
					'lWondersBuilt': [0] * iNumCivs,
					'babyloniaKilledCivs': 0,
					'scythianKilledCivs': 0,
					'hittiteKilledUnits': 0,
					'mycenaeTombsBuilt': 0,
					'athensHarborBuilt': 0,
					'lReligionFounded': [-1] * gc.getNumReligionInfos()
		}
		gc.getGame().setScriptData(pickle.dumps(scriptDict))

	def allowEvent(self): #Do not check events until game is loaded
		return gc.getGame().isVictoryValid(7) and len(gc.getGame().getScriptData()) > 0

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
		if not self.allowEvent():
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
					elif iGameTurn >= i1070BC:
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

			if (iGameTurn == i1200BC):
				if (self.getGoal(iIndusValley, 2) == -1): #see onCityAcquired()
					self.setGoal(iIndusValley, 2, 1)

		elif civType == iElam and iGameTurn <= i1000BC:
			if iGameTurn < i1900BC:
				pIndusValley = civ2player(iIndusValley)
				if pIndusValley != PlayerTypes.NO_PLAYER and pPlayer.canContact(pIndusValley) and pPlayer.canTradeNetworkWith(pIndusValley):
					self.setGoal(iElam, 1, 1)
			elif iGameTurn == i1800BC and self.getGoal(iElam, 1) == -1:
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
				pBarbarian = civ2player(iBarbarian)
				pIndependent = civ2player(iIndependent)
				pIndependent2 = civ2player(iIndependent2)
				barbCities = provLydia.getNumCities(pBarbarian) \
				+ provLydia.getNumCities(pIndependent) \
				+ provLydia.getNumCities(pIndependent2) \
				+ provAnatolia.getNumCities(pBarbarian) \
				+ provAnatolia.getNumCities(pIndependent) \
				+ provAnatolia.getNumCities(pIndependent2)

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
							self.setGoal(iAssyria, 1, 1)
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
			if self.getGoal(iAthens, 2) == -1 and iGameTurn > i300BC:
				self.setGoal(iAthens, 2, 0)

			if self.getGoal(iAthens, 1) == -1 and iGameTurn > i450BC:
				self.setGoal(iAthens, 1, 0)

		elif civType == iSparta:
			if (iGameTurn == i400BC):
				bPeloponnese = provPeloponnese.getNumCities(iPlayer) >= 1
				bAttica = provAttica.getNumCities(iPlayer) >= 1
				bMacedonia = provMacedonia.getNumCities(iPlayer) >= 1
				bCentralGreece = provCentralGreece.getNumCities(iPlayer) >= 1
				bEuboea = provEuboea.getNumCities(iPlayer) >= 1
				bCyclades = provCyclades.getNumCities(iPlayer) >= 1
				goalCompleted = controlsProvince(iPlayer, provPeloponnese) and \
						controlsProvince(iPlayer, provAttica) and \
						controlsProvince(iPlayer, provMacedonia) and \
						controlsProvince(iPlayer, provCentralGreece) and \
						controlsProvince(iPlayer, provEuboea) and \
						controlsProvince(iPlayer, provCyclades)
				if bPeloponnese and bAttica and bMacedonia and bCentralGreece and bEuboea and bCyclades:
					self.setGoal(iSparta, 1, 1)
				else:
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
		
		
		elif civType == iScythia:
			if iGameTurn == i100BC:
				bForeignPresence = False
				for i in xrange(CyMap().numPlots()):
					pCurrent = CyMap().plotByIndex(i)
					if provCrimea.isInBorderBounds(pCurrent.getX(), pCurrent.getY()) or \
						provSarmatia.isInBorderBounds(pCurrent.getX(), pCurrent.getY()) or \
						provCaucasus.isInBorderBounds(pCurrent.getX(), pCurrent.getY()) or \
						provScythia.isInBorderBounds(pCurrent.getX(), pCurrent.getY()):
						if not pCurrent.isWater():
							for iLoop in range(iNumPlayers): #no minor civs
								if iLoop != iPlayer:
									if pCurrent.getCulture(iLoop) > 0:
										bForeignPresence = True
										break

				if not bForeignPresence:
					self.setGoal(iScythia, 2, 1)
				else:
					self.setGoal(iScythia, 2, 0)

			if iGameTurn == i500BC:
				if pPlayer.countOwnedBonuses(bonus('Horse')) + pPlayer.getBonusImport(bonus('Horse')) >= 4:
					self.setGoal(iScythia, 0, 1)
				else:
					self.setGoal(iScythia, 0, 0)
											
			if iGameTurn < i300BC:
				if self.getScythianKilledCivs() >= 3:
					self.setGoal(iScythia, 1, 1)
			elif iGameTurn == i300BC:
				if self.getScythianKilledCivs() < 3:
					self.setGoal(iScythia, 1, 0)
				else:
					self.setGoal(iScythia, 1, 1)

		elif civType == iCarthage:
			if (iGameTurn == i0AD):
				if (gc.getGame().getTeamRank(pPlayer.getTeam()) == 0):
					self.setGoal(iCarthage, 2, 1)
				else:
					self.setGoal(iCarthage, 2, 0)
			if iGameTurn < i400BC:
				if pPlayer.countOwnedBonuses(bonus('Dye')) + pPlayer.getBonusImport(bonus('Dye')) >= 3:
					self.setGoal(iCarthage, 0, 1)
			elif iGameTurn == i400BC:
				if pPlayer.countOwnedBonuses(bonus('Dye')) + pPlayer.getBonusImport(bonus('Dye')) < 3:
					self.setGoal(iCarthage, 0, 0)

		elif (civType == iCeltia):
			if (iGameTurn == i0AD):
				if (pPlayer.countTotalCulture() >= 1000):
					self.setGoal(iCeltia, 2, 1)
				else:
					self.setGoal(iCeltia, 2, 0)

			if (iGameTurn == i300BC):
				bCelticGaul = provCelticGaul.getNumCities(iPlayer) >= 2
				bBritannia = provBritannia.getNumCities(iPlayer) >= 1
				bNorthernIberia = provNorthernIberia.getNumCities(iPlayer) >= 1
				bRaetia = provRaetia.getNumCities(iPlayer) >= 1
				bVenetia = provVenetia.getNumCities(iPlayer) >= 1
				if (bCelticGaul and bBritannia and bNorthernIberia and bRaetia and bVenetia):
					self.setGoal(iCeltia, 0, 1)
				elif iGameTurn >= i671BC:
					self.setGoal(iCeltia, 0, 0)
					
		elif (civType == iEtruria):
			if (iGameTurn == i300BC):
				if (pPlayer.getGold() >= 2000):
					self.setGoal(iEtruria, 0, 1)
				else:
					self.setGoal(iEtruria, 0, 0)
					
			if (iGameTurn == i270BC):
				bItaly = provItaly.getNumCities(iPlayer) >= 4
				bCorsica = provCorsica.getNumCities(iPlayer) >= 1
				bVenetia = provVenetia.getNumCities(iPlayer) >= 1
				if (bItaly and bCorsica and bVenetia):
					self.setGoal(iEtruria, 1, 1)
				elif iGameTurn >= i270BC:
					self.setGoal(iEtruria, 1, 0)
			
			if (iGameTurn == i250BC):
				if (pPlayer.countTotalCulture() >= 500):
					self.setGoal(iEtruria, 2, 1)
				else:
					self.setGoal(iEtruria, 2, 0)
					
		elif civType == iNubia:
			if iGameTurn == i542BC:
				if pPlayer.countOwnedBonuses(bonus('Gold')) + pPlayer.getBonusImport(bonus('Gold')) >= 3:
					self.setGoal(iNubia, 0, 1)
				else:
					self.setGoal(iNubia, 0, 0)

			#TODO Nubia's UHV isn't well defined, as Meroe
			# can be on several plots, even at the same time :(
			if self.getGoal(iNubia, 1) == -1:
				# Find Meroe.
				meroeCity = None
				for i in range(pPlayer.getNumCities()):
					city = pPlayer.getCity(i)
					if city.plot().getCityName(iNubia, True) == "Meroe":
						if meroeCity == None or city.getPopulation() > meroeCity.getPopulation():
							meroeCity = city
				hasAllGreatPeople = False
				if meroeCity != None:
					hasAllGreatPeople = True
					for i in range(gc.getNumSpecialistInfos()):
						specialist = gc.getSpecialistInfo(i)
						unitClass = specialist.getGreatPeopleUnitClass()
						if unitClass != -1:
							unit = gc.getUnitInfo(unitClass)
							for j in range(gc.getNumSpecialistInfos()):
								if unit.getGreatPeoples(j) and meroeCity.getFreeSpecialistCount(j) == 0:
									hasAllGreatPeople = False
									break
				if hasAllGreatPeople:
					self.setGoal(iNubia, 1, 1)
				elif iGameTurn > i350AD:
					self.setGoal(iNubia, 1, 0)

			if iGameTurn == i400AD:
				if gc.getGame().getTeamRank(pPlayer.getTeam()) == 0:
					self.setGoal(iNubia, 2, 1)
				else:
					self.setGoal(iNubia, 2, 0)
					
			if iGameTurn == i500AD:
				if gc.getGame().getTeamRank(pPlayer.getTeam()) == 0:
					self.setGoal(iRome, 2, 1)
				else:
					self.setGoal(iRome, 2, 0)

		elif civType == iPersia:
			if iGameTurn == i330BC:
				bLydia = provLydia.getNumCities(iPlayer) >= 2
				bAnatolia = provAnatolia.getNumCities(iPlayer) >= 2
				bMedia = provMedia.getNumCities(iPlayer) >= 2
				bAkkad = provAkkad.getNumCities(iPlayer) >= 1
				if bLydia and bAnatolia and bMedia and bAkkad:
					self.setGoal(iPersia, 0, 1)
				elif iGameTurn >= i330BC:
					self.setGoal(iPersia, 0, 0)

			if self.getGoal(iPersia, 1) == -1:
					iGreatEngineer = gc.getInfoTypeForString("SPECIALIST_GREAT_ENGINEER")
					i2GSCities = 0
					for cCity in PyPlayer(iPlayer).getCityList():
						if cCity.GetCy().getFreeSpecialistCount(iGreatEngineer) >= 1:
							i2GSCities += 1
					if i2GSCities >= 2:
						self.setGoal(iPersia, 1, 1)
					elif iGameTurn > i275BC:
						self.setGoal(iPersia, 1, 0)

			if iGameTurn == i250BC:
				if gc.getGame().getTeamRank(pPlayer.getTeam()) == 0:
					self.setGoal(iPersia, 2, 1)
				else:
					self.setGoal(iPersia, 2, 0)
					
		elif civType == iRome:
			if iGameTurn == i180AD:
				if pPlayer.countOwnedBonuses(bonus('Salt')) + pPlayer.getBonusImport(bonus('Salt')) >= 1 and pPlayer.countOwnedBonuses(bonus('Silver')) + pPlayer.getBonusImport(bonus('Silver')) >= 1:
					self.setGoal(iRome, 1, 1)
				else:
					self.setGoal(iRome, 1, 0)

		elif civType == iMacedonia:
			if self.getGoal(iMacedonia, 0) == -1:
				goalCompleted = controlsProvince(iPlayer, provSubartu) and \
						controlsProvince(iPlayer, provLydia) and \
						controlsProvince(iPlayer, provPhoenicia) and \
						controlsProvince(iPlayer, provThracia)
				if goalCompleted:
					self.setGoal(iMacedonia, 0, 1)
				elif iGameTurn > i300BC:
					self.setGoal(iMacedonia, 0, 0)
					
			if (self.getGoal(iMacedonia, 1) == -1):
					if (iGameTurn <= i200BC):
						Hellenism = gc.getInfoTypeForString("RELIGION_HELLENISM")
						religionPercent = gc.getGame().calculateReligionPercent(Hellenism)
						if (religionPercent >= 30.0):
							self.setGoal(iMacedonia, 1, 1)
					else:
							self.setGoal(iMacedonia, 1, 0)

			if iGameTurn == i10AD:
				if gc.getGame().getTeamRank(pPlayer.getTeam()) == 0:
					self.setGoal(iMacedonia, 2, 1)
				else:
					self.setGoal(iMacedonia, 2, 0)


	def onCityBuilt(self, city):
		if not self.allowEvent():
			return

		iGameTurn = gc.getGame().getGameTurn()

	def onReligionFounded(self, iReligion, iFounder):
		if not self.allowEvent():
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
		if not self.allowEvent():
			return

		iGameTurn = gc.getGame().getGameTurn()
		cityX = city.getX()
		cityY = city.getY()

		ownerType = gc.getPlayer(owner).getCivilizationType()
		attackerType = gc.getPlayer(attacker).getCivilizationType()

		if self.getGoal(iScythia, 1) == -1: # Check if last city
			if attackerType == iScythia:
				if gc.getPlayer(owner).getNumCities() == 0:
					self.setScythianKilledCivs(self.getScythianKilledCivs()+1)

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
					if (iGameTurn <= i1200BC):
						if (attackerType == iBarbarian):
							self.setGoal(iIndusValley, 2, 0)

		if attackerType == iBabylonia:
			if gc.getPlayer(owner).getNumCities() == 0:
				self.setBabyloniaKilledCivs(self.getBabyloniaKilledCivs()+1)
				
		if self.getGoal(iCarthage, 1) == -1 and cityX == 19 and cityY == 30: #Rome captured by Carthage
			if attackerType == iCarthage:
				self.setGoal(iCarthage, 1, 1)
			else:
				self.setGoal(iCarthage, 1, 0)
				
		if self.getGoal(iCeltia, 1) == -1 and cityX == 19 and cityY == 30: #Rome captured by Celts
			if attackerType == iCeltia:
				self.setGoal(iCeltia, 1, 1)
			else:
				self.setGoal(iCeltia, 1, 0)
				
		if self.getGoal(iRome, 1) == -1 and cityX == 15 and cityY == 20: #Carthage captured by Rome
			if attackerType == iRome:
				self.setGoal(iRome, 0, 1)
			else:
				self.setGoal(iRome, 0, 0)


	def onCityRazed(self, city, conqueror, owner):
		if not self.allowEvent():
			return

		if self.getGoal(iScythia, 1) == -1: # Check if last city
			if conqueror == iScythia:
				if gc.getPlayer(owner).getNumCities() == 0:
					self.setScythianKilledCivs(self.getScythianKilledCivs()+1)

		if self.getGoal(iElam, 0) == -1 and city.getX() == 46 and city.getY() == 19: #Ur captured by Elam
			if gc.getPlayer(conqueror).getCivilizationType() == iElam:
				self.setGoal(iElam, 0, 1)
			else:
				self.setGoal(iElam, 0, 0)
				
		if self.getGoal(iCarthage, 1) == -1 and city.getX() == 19 and city.getY() == 30: #Rome captured by Carthage
			if gc.getPlayer(conqueror).getCivilizationType() == iCarthage:
				self.setGoal(iCarthage, 1, 1)
			else:
				self.setGoal(iCarthage, 1, 0)
				
		if self.getGoal(iCeltia, 1) == -1 and city.getX() == 19 and city.getY() == 30: #Rome captured by Celts
			if gc.getPlayer(conqueror).getCivilizationType() == iCeltia:
				self.setGoal(iCeltia, 1, 1)
			else:
				self.setGoal(iCeltia, 1, 0)

	def onTechAcquired(self, iTech, iPlayer):
		if not self.allowEvent():
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
		if not self.allowEvent():
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
				if self.getGoal(iAthens, 1) == -1:
					self.setAthensHarborBuilt(self.getAthensHarborBuilt() + 1)
					if self.getAthensHarborBuilt() >= 5:
						self.setGoal(iAthens, 1, 1)
			if (self.getGoal(iAthens, 2) == -1):
					if (iBuilding == building('Oracle') or iBuilding == building('Colossus') or iBuilding == building('Parthenon') or iBuilding == building('Artemis')):
						self.setWondersBuilt(iAthens, self.getWondersBuilt(iAthens) + 1)
					if (self.getWondersBuilt(iAthens) == 4):
						self.setGoal(iAthens, 2, 1)

	def onCombatResult(self, argsList):
		if not self.allowEvent():
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
