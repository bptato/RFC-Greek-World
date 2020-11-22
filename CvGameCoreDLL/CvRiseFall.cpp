/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRiseFall.h"
#include "CvPlayer.h"
#include "CvPlot.h"
#include "CvCity.h"
#include "CvGlobals.h"
#include "CvEnums.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvInitCore.h"
#include "CvRFCPlayer.h"
#include "CvRFCProvince.h"

CvRiseFall::CvRiseFall() {
	_rfcPlayers = new CvRFCPlayer[GC.getNumCivilizationInfos()];
}

CvRiseFall::~CvRiseFall() {
	SAFE_DELETE_ARRAY(_rfcPlayers);
	for(std::vector<CvRFCProvince*>::iterator it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_rfcProvinces.clear();
}

void CvRiseFall::reset() {
	GC.logMsg("CvRiseFall::reset");
	for(int i = 0; i < GC.getNumCivilizationInfos(); i++) {
		_rfcPlayers[i].reset((CivilizationTypes)i);
	}
	for(std::vector<CvRFCProvince*>::iterator it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_rfcProvinces.clear();
}

void CvRiseFall::onGameStarted() {
	GC.logMsg("CvRiseFall::onGameStarted");
	CvGame& game = GC.getGameINLINE();

	bool activePlayerSet = false;
	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		if(player.isHuman()) {
			CvRFCPlayer& rfcPlayer = getRFCPlayer(player.getCivilizationType());
			rfcPlayer.setHuman(true);
			CvPlot* startingPlot = GC.getMap().plot(rfcPlayer.getStartingPlotX(), rfcPlayer.getStartingPlotY());
			player.initUnit(((UnitTypes)0), rfcPlayer.getStartingPlotX(), rfcPlayer.getStartingPlotY()); //will be killed as soon as autoplay starts, this is just to reveal the player's starting position like in RFC
			gDLL->getEngineIFace()->cameraLookAt(startingPlot->getPoint());
			if(!activePlayerSet) {
				game.setActivePlayer((PlayerTypes)i); //just to be sure
			}
		}
	}

	game.setAIAutoPlay(1);
	/* TODO: this is ugly. the nicer alternative would be to call this function
	from setFinalInitialized if the value set there is true and CvRiseFall is initialized.
	But this seems to work for now so we'll leave it like that. */
	game.setFinalInitialized(false);
	checkTurn();
	game.setFinalInitialized(true);
	for(int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		GET_PLAYER((PlayerTypes)i).processDynamicNames();
		checkLeader(GET_PLAYER((PlayerTypes)i).getCivilizationType(), (PlayerTypes)i);
	}
}

void CvRiseFall::checkTurn() {
	CvGame& game = GC.getGameINLINE();
	GC.logMsg("CvRiseFall::checkTurn - turn %d", game.getGameTurn());

	for(int i = 0; i<GC.getNumCivilizationInfos(); i++) {
		if(getRFCPlayer((CivilizationTypes)i).isHuman()) {
			int turn = game.getGameTurn();
			turn = turn <= 1 ? turn : turn + 1;
			checkTurnForPlayer((CivilizationTypes)i, turn);
		}
	}

	for(int i = 0; i<GC.getNumCivilizationInfos(); i++) {
		if(!getRFCPlayer((CivilizationTypes)i).isHuman()) {
			checkTurnForPlayer((CivilizationTypes)i, game.getGameTurn());
		}
	}

	for(int i = 0; i<getNumProvinces(); i++) {
		CvRFCProvince* rfcProvince = getRFCProvince(i);
		//Historical barbs
		int numScheduledUnits = rfcProvince->getNumScheduledUnits();
		if(numScheduledUnits>0) {
			std::vector<CvPlot*> plots;
			for(int provX = rfcProvince->getLeft(); provX<=rfcProvince->getRight(); provX++) {
				for(int provY = rfcProvince->getBottom(); provY<=rfcProvince->getTop(); provY++) {
					CvPlot* loopPlot = GC.getMap().plot(provX, provY);
					if(!loopPlot->isWater() && !loopPlot->isPeak() && !loopPlot->isCity() && !loopPlot->isBeingWorked() && !loopPlot->isUnit()) {
						plots.push_back(loopPlot);
					}
				}
			}
			if(plots.size()>0) {
				for(int j = 0; j<numScheduledUnits; j++) {
					CvRFCUnit* rfcUnit = rfcProvince->getScheduledUnit(j);
					if(rfcUnit->getLastSpawned() == -1 || rfcUnit->getLastSpawned() + rfcUnit->getSpawnFrequency()/2 < game.getGameTurn()) {
						if(rfcUnit->getYear() <= game.getGameTurnYear() && rfcUnit->getEndYear() >= game.getGameTurnYear() && game.getSorenRandNum(rfcUnit->getSpawnFrequency()/2, "Unit spawn roll") == 0) {
							CvPlayer& barbPlayer = GET_PLAYER(BARBARIAN_PLAYER); //TODO: different rfcUnit owner civs?
							CvPlot* randomPlot = plots[game.getSorenRandNum(plots.size(), "Barb spawning plot roll")];
							for(int k = 0; k<rfcUnit->getAmount(); k++) {
								barbPlayer.initUnit(rfcUnit->getUnitType(), randomPlot->getX(), randomPlot->getY(), rfcUnit->getUnitAIType(), rfcUnit->getFacingDirection());
							}
							rfcUnit->setLastSpawned(game.getGameTurn());
						}
					}
				}
			}
		}

		//Mercenaries
		if(GC.getGame().getGameTurn() % 5 == 3) {
			rfcProvince->checkMercenaries();
		}
	}
	//Player plot stability
	updatePlayerPlots();
}

void CvRiseFall::checkTurnForPlayer(CivilizationTypes civType, int turn) {
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	if(!rfcPlayer.isEnabled()) {
		return;
	}
	CvGame& game = GC.getGameINLINE();
	PlayerTypes playerType = getPlayerTypeForCiv(civType);

	if(rfcPlayer.getStartingYear() <= game.getTurnYear(turn) || playerType != NO_PLAYER || rfcPlayer.isMinor()) { //barbarians & minors as well
		if(rfcPlayer.isHuman()) {
			GC.logMsg("Checking human at year %d for year %d", game.getGameTurnYear(), game.getTurnYear(turn));
		}
		bool spawnedNow = false;
		if(!rfcPlayer.isSpawned()) {
			//conditional spawns
			if(!rfcPlayer.isHuman() && skipConditionalSpawn(civType)) {
				if(rfcPlayer.getStartingTurn() < 0) {
					rfcPlayer.setStartingTurn(turn);
				} else if(rfcPlayer.getStartingTurn() < turn - 10) {
					rfcPlayer.setSpawned(true);
				}
				return;
			}

			spawnedNow = true; //for unit immobilization

			if(rfcPlayer.isHuman()) { //major human civs
				spawnHumanCivilization(civType);
			} else if(playerType == BARBARIAN_PLAYER) { //barbarian
				rfcPlayer.setSpawned(true);
				CvPlayer& barbPlayer = GET_PLAYER(playerType);
				for (int j = 0; j < MAX_CIV_TEAMS; j++) {
					if ((TeamTypes)j != barbPlayer.getTeam()) {
						GET_TEAM(barbPlayer.getTeam()).declareWar(((TeamTypes)j), false, NO_WARPLAN);
					}
				}
			} else if(rfcPlayer.isMinor()) { //minor civs
				spawnMinorCivilization(civType);
			} else { //major AI civs
				spawnAICivilization(civType);
			}
		}

		playerType = getPlayerTypeForCiv(civType); //refresh playerType as we might've spawned now

		if(playerType != NO_PLAYER) { //if yes, check stability, flipping, scheduled units and cities.
			CvPlayer& player = GET_PLAYER(playerType);

			if(!player.isMinorCiv() && !player.isBarbarian()) {
				checkStabilityEffect(civType, playerType);

				//Flip here because we want the flipped units to be spawned right after flipping the cities
				checkFlip(playerType, civType);
			}

			checkScheduledCities(playerType, civType, turn);
			checkScheduledUnits(playerType, civType, turn, spawnedNow);
		}
	}
}

void CvRiseFall::checkFlip(PlayerTypes playerType, CivilizationTypes civType) {
	int flipCountdown = getRFCPlayer(civType).getFlipCountdown();
	if(flipCountdown>=0) {
		getRFCPlayer(civType).setFlipCountdown(flipCountdown - 1);
		if(flipCountdown==0) {
			std::vector<CvCity*> toFlip;
			for(int j = 0; j<MAX_PLAYERS; ++j) {
				if((PlayerTypes)j != playerType) {
					CvPlayer& loopPlayer = GET_PLAYER((PlayerTypes)j);
					int k;
					for(CvCity* loopCity = loopPlayer.firstCity(&k); loopCity != NULL; loopCity = loopPlayer.nextCity(&k)) {
						if(getRFCPlayer(civType).isInCoreBounds(loopCity->getX(), loopCity->getY()) && !loopCity->isCapital()) {
							toFlip.push_back(loopCity);
						}
					}
				}
			}

			if(toFlip.size()>0) {
				for(std::vector<CvCity*>::iterator it = toFlip.begin(); it != toFlip.end(); ++it) {
					if(!GET_TEAM(GET_PLAYER(playerType).getTeam()).isAtWar(GET_PLAYER((*it)->getOwner()).getTeam())) {
						GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(GET_PLAYER((*it)->getOwner()).getTeam(), true, WARPLAN_TOTAL); //we want new civs to completely destroy older ones
					}
					flipCity(*it, playerType, true);
				}
			}
		}
	}
}

void CvRiseFall::checkScheduledCities(PlayerTypes playerType, CivilizationTypes civType, int turn) {
	std::vector<CvRFCCity*>& scheduledCities = getRFCPlayer(civType).getScheduledCities();
	for(std::vector<CvRFCCity*>::iterator it = scheduledCities.begin(); it != scheduledCities.end();) {
		CvRFCCity* rfcCity = *it;
		if(GC.getGame().getTurnYear(turn) >= rfcCity->getYear()) {
			if(GET_PLAYER(playerType).canFound(rfcCity->getX(), rfcCity->getY())) {
				GET_PLAYER(playerType).initCity(rfcCity->getX(), rfcCity->getY(), true, true);
				CvCity* city = GC.getMap().plot(rfcCity->getX(), rfcCity->getY())->getPlotCity();
				city->setPopulation(rfcCity->getPopulation());
				for(int i = 0; i < GC.getNumBuildingInfos(); ++i) {
					int buildingNum = rfcCity->getNumBuilding((BuildingTypes)i);
					if(buildingNum > 0)
						city->setNumRealBuilding((BuildingTypes)i, buildingNum);
				}
				for(int i = 0; i < GC.getNumReligionInfos(); ++i) {
					if(rfcCity->getReligion((ReligionTypes)i)) {
						city->setHasReligion((ReligionTypes)i, true, false, false);
					}
				}
				for(int i = 0; i < GC.getNumReligionInfos(); ++i) {
					if(rfcCity->getHolyCityReligion((ReligionTypes)i)) {
						GC.getGame().setHolyCity((ReligionTypes)i, city, false);
					}
				}
			}
			SAFE_DELETE(rfcCity);
			it = scheduledCities.erase(it);
		} else {
			++it;
		}
	}
}

void CvRiseFall::checkScheduledUnits(PlayerTypes playerType, CivilizationTypes civType, int turn, bool spawnedNow) {
	std::vector<CvRFCUnit*>& scheduledUnits = getRFCPlayer(civType).getScheduledUnits();
	for(std::vector<CvRFCUnit*>::iterator it = scheduledUnits.begin(); it != scheduledUnits.end();) {
		CvRFCUnit* rfcUnit = *it;
		if(GC.getGame().getTurnYear(turn) >= rfcUnit->getYear()) {
			if(!rfcUnit->isAIOnly() || !getRFCPlayer(civType).isHuman()) {
				int ix = rfcUnit->getX();
				int iy = rfcUnit->getY();
				CvPlot* plot = GC.getMap().plot(ix, iy);
				if(plot->isCity() && rfcUnit->isDeclareWar()) {
					if(plot->getPlotCity()->getOwnerINLINE() != civType) {
						DomainTypes domainType = (DomainTypes)GC.getUnitInfo(rfcUnit->getUnitType()).getDomainType();
						plot = findSpawnPlot(ix, iy, domainType);
						if(plot == NULL) {
							continue;
						}
					}
				}

				if(rfcUnit->isDeclareWar()) {
					PlayerTypes plotOwner = plot->getOwner();
					if(plotOwner != NO_PLAYER) {
						if(!GET_TEAM(GET_PLAYER(playerType).getTeam()).isAtWar(GET_PLAYER(plotOwner).getTeam())) {
							GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(GET_PLAYER(plotOwner).getTeam(), true, WARPLAN_TOTAL);
						}
					}
				}
				for(int j = 0; j < rfcUnit->getAmount(); j++) {
					CvUnit* unit = GET_PLAYER(playerType).initUnit(rfcUnit->getUnitType(), ix, iy, rfcUnit->getUnitAIType(), rfcUnit->getFacingDirection());
					if(unit != NULL && spawnedNow && !getRFCPlayer(civType).isHuman() && GC.getUnitInfo(rfcUnit->getUnitType()).getDefaultUnitAIType() != UNITAI_SETTLE) {
						unit->setImmobileTimer(2);
					}
				}
			}
			SAFE_DELETE(rfcUnit);
			it = scheduledUnits.erase(it);
		} else {
			++it;
		}
	}
}


void CvRiseFall::checkPlayerTurn(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
	CvGame& game = GC.getGame();

	if(!player.isBarbarian() && !player.isMinorCiv()) {
		checkMinorWars(playerType, game.getGameTurn());
		if(game.getGameTurn() % 3 == 2) {
			getRFCPlayer(player.getCivilizationType()).checkStability(playerType);
			if(!player.isHuman()) {
				checkLeader(player.getCivilizationType(), playerType);
			}
		}
	}
}

void CvRiseFall::checkMinorWars(PlayerTypes playerType, int turn) {
	if(turn % 2 == 0) {
		return;
	}

	CvPlayer& player = GET_PLAYER(playerType);

	PlayerTypes minorCivType = NO_PLAYER;

	for(int i = 0; i<MAX_CIV_PLAYERS; i++) {
		CvPlayer& loopCiv = GET_PLAYER((PlayerTypes)i);
		if(loopCiv.isAlive() && loopCiv.isMinorCiv() && !loopCiv.isBarbarian()) {
			if(GC.getGame().getSorenRandNum(100, "Minor civ for checkMinorWars") < 50) {
				minorCivType = (PlayerTypes)i;
			}
		}
	}

	if(minorCivType == NO_PLAYER) {
		return;
	}

	CvPlayer& minorCiv = GET_PLAYER(minorCivType);

	if(GET_TEAM(player.getTeam()).isAtWar(minorCiv.getTeam())) {
		int rand = player.isHuman() ? 30 : 20;
		if(GC.getGame().getSorenRandNum(100, "Peace for checkMinorWars") <= rand) {
			if(!unitsInForeignTerritory(playerType, minorCivType)) {
				GET_TEAM(player.getTeam()).makePeace(minorCiv.getTeam(), false);
			}
		}
	} else if(!player.isHuman()) {
		if(GC.getGame().getSorenRandNum(100, "War for checkMinorWars") <= 10) {
			GET_TEAM(player.getTeam()).declareWar(minorCiv.getTeam(), false, WARPLAN_TOTAL);
		}
	}
}

void CvRiseFall::checkLeader(CivilizationTypes civType, PlayerTypes playerType) {
	LeaderHeadTypes leader = (LeaderHeadTypes)0;
	CvCivilizationInfo& civInfo = GC.getCivilizationInfo(civType);

	int reign = 0;
	bool reignSet = false;
	for(int i = 0; i<GC.getNumLeaderHeadInfos(); i++) {
		if(civInfo.isLeaders(i)) {
			CvLeaderHeadInfo& leaderInfo = GC.getLeaderHeadInfo((LeaderHeadTypes)i);
			if(leaderInfo.getLeaderReign() <= GC.getGameINLINE().getGameTurnYear() && (!reignSet || reign < leaderInfo.getLeaderReign())) {
				reignSet = true;
				reign = leaderInfo.getLeaderReign();
				leader = (LeaderHeadTypes)i;
			}
		}
	}

	if(GC.getInitCore().getLeader(playerType)!=leader) {
		GC.getInitCore().setLeader(playerType, leader);
	}
}

void CvRiseFall::spawnHumanCivilization(CivilizationTypes civType) {
	CvGame& game = GC.getGameINLINE();

	for(int i = 0; i<MAX_CIV_PLAYERS; i++) {
		CvPlayerAI& player = GET_PLAYER((PlayerTypes)i);
		if(player.isHuman() && player.getCivilizationType() == civType) {
			game.setAIAutoPlay(0);

			if(player.getNumUnits() > 0) {
				gDLL->getInterfaceIFace()->selectGroup(player.getUnit(0), false, false, false);
			}

			finishMajorCivSpawn(civType, (PlayerTypes)i);
			GC.logMsg("CvRiseFall::spawnHumanCivilization - Spawned human civ %i", civType);
			return;
		}
	}
	GC.logMsg("CvRiseFall::spawnHumanCivilization - Failed to spawn human civ %i", civType);
}

void CvRiseFall::updatePlayerPlots() {
	int* ownedPlots = new int[GC.getNumCivilizationInfos()];

	for(int i = 0; i<GC.getNumCivilizationInfos(); ++i) {
		ownedPlots[i] = 0;
	}

	for(int x = 0; x<GC.getMap().getGridWidth(); ++x) {
		for(int y = 0; y<GC.getMap().getGridHeight(); ++y) {
			CvPlot* plot = GC.getMap().plot(x, y);
			if(!plot->isWater() && !plot->isPeak() && plot->getOwner() != NO_PLAYER) {
				CivilizationTypes civType = GET_PLAYER(plot->getOwner()).getCivilizationType();
				if(plot->getSettlerValue(civType) < 90) {
					ownedPlots[civType] += 1;
				}
			}
		}
	}

	for(int i = 0; i<GC.getNumCivilizationInfos(); ++i) {
		getRFCPlayer((CivilizationTypes)i).setNumPlots(ownedPlots[i]);
	}

	SAFE_DELETE_ARRAY(ownedPlots);
}

void CvRiseFall::checkStabilityEffect(CivilizationTypes civType, PlayerTypes playerType) {
	CvGame& game = GC.getGameINLINE();
	//we don't want new civs to collapse, nor do we want to check all of this every turn
	if(game.getGameTurn() % 6 != 0) {
		return;
	}
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	if(game.getGameTurn() <= rfcPlayer.getStartingTurn() + 20) {
		return;
	}
	CvPlayer& player = GET_PLAYER(playerType);

	if(rfcPlayer.getTotalStability() < 0) {
		//shaky, risk of city independent secessions
		if(game.getSorenRandNum(100, "Secession roll") <= 5) {
			int j;
			CvCity* chosenCity = NULL;
			int chosenHappiness = 0; //no secessions if all cities are happy.

			for(CvCity* city = player.firstCity(&j); NULL != city; city = player.nextCity(&j)) {
				if(!city->isCapital()) {
					if(city->happyLevel() - city->unhappyLevel() < chosenHappiness) {
						chosenHappiness = city->happyLevel() - city->unhappyLevel();
						chosenCity = city;
					}
				}
			}

			if(chosenCity != NULL) {
				citySecession(chosenCity);

				for(j = 0; j < NUM_STABILITY_CATEGORIES; ++j) {
					int newStability = rfcPlayer.getPermStability(j) / 3;
					newStability *= 2;
					rfcPlayer.setPermStability(j, newStability);
				}
			}
		}
	}
	if(rfcPlayer.getTotalStability() < -20) {
		if(game.getSorenRandNum(100, "Secession roll") <= 10) {
			int j;
			CvCity* chosenCity = NULL;
			int chosenHappiness = 0;

			for(CvCity* city = player.firstCity(&j); NULL != city; city = player.nextCity(&j)) {
				if(!city->isCapital()) {
					if(city->happyLevel() - city->unhappyLevel() < chosenHappiness || chosenCity == NULL) {
						chosenHappiness = city->happyLevel() - city->unhappyLevel();
						chosenCity = city;
					}
				}
			}

			if(chosenCity != NULL) {
				citySecession(chosenCity);
			}

			for(j = 0; j < NUM_STABILITY_CATEGORIES; ++j) {
				int newStability = rfcPlayer.getPermStability(j) / 4;
				newStability *= 3;
				rfcPlayer.setPermStability(j, newStability);
			}
		}
	}
	if(rfcPlayer.getTotalStability() < -40) {
		//collapsing, risk of complete collapse (or collapse to core in case of the human player)
		if(game.getSorenRandNum(100, "Collapse roll") <= 40) {
			if(player.isHuman()) {
				capitalCollapse(playerType);
			} else {
				completeCollapse(playerType);
			}
			for(int j = 0; j < NUM_STABILITY_CATEGORIES; ++j) {
				rfcPlayer.setPermStability(j, 0);
				rfcPlayer.setTempStability(j, 0);
			}
		}
	}
}

void CvRiseFall::spawnAICivilization(CivilizationTypes civType) {
	for (int i = 0; i<MAX_CIV_PLAYERS; i++) {
		CvPlayerAI& player = GET_PLAYER((PlayerTypes)i);
		if(!player.isAlive() && !player.isBarbarian() && !player.isMinorCiv() && !player.isHuman()) { //use slot if it isn't occupied by a human, barbarian or minor civ.
			setupAIPlayer(civType, (PlayerTypes)i);
			finishMajorCivSpawn(civType, (PlayerTypes)i);
			GC.logMsg("CvRiseFall::spawnAICivilization - Spawned ai civ %i", civType);
			return;
		}
	}
	GC.logMsg("CvRiseFall::spawnAICivilization - Failed to spawn ai civ %i", civType);
}

void CvRiseFall::spawnMinorCivilization(CivilizationTypes civType) {
	for (int i = 0; i<MAX_CIV_PLAYERS; i++) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		if(!player.isAlive() && !player.isHuman() && player.isMinorCiv()) { //add minor civ if this is a "minor slot"
			setupAIPlayer(civType, (PlayerTypes)i);
			getRFCPlayer(civType).setSpawned(true);
			return;
		}
	}
}

void CvRiseFall::setupAIPlayer(CivilizationTypes civType, PlayerTypes playerType) { //basically the same as CvGame::addPlayer, except we assign the correct leader (and color)
	CvPlayer& player = GET_PLAYER(playerType);
	CvWString emptyString = L"";

	GC.getInitCore().setLeaderName(playerType, emptyString);
	GC.getInitCore().setCivAdjective(playerType, emptyString);
	GC.getInitCore().setCivDescription(playerType, emptyString);
	GC.getInitCore().setCivShortDesc(playerType, emptyString);
	checkLeader(civType, playerType);
	GC.getInitCore().setCiv(playerType, civType);
	GC.getInitCore().setSlotStatus(playerType, SS_COMPUTER);
	GC.getInitCore().setColor(playerType, (PlayerColorTypes)GC.getCivilizationInfo(civType).getDefaultPlayerColor());
	GET_TEAM(player.getTeam()).init(player.getTeam());
	player.init(playerType);
}

void CvRiseFall::finishMajorCivSpawn(CivilizationTypes civType, PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	CvGame& game = GC.getGameINLINE();

	eraseSurroundings(civType, playerType);
	if(player.isHuman()) {
		player.setAlive(true);
	}
	if(!GET_TEAM(player.getTeam()).isAtWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam())) {
		GET_TEAM(player.getTeam()).declareWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam(), true, NO_WARPLAN);
	}
	assignStartingTechs(civType, playerType);
	assignStartingCivics(civType, playerType);
	setupStartingWars(civType, playerType);
	rfcPlayer.setFlipCountdown(3);
	rfcPlayer.setStartingTurn(game.getGameTurn());
	rfcPlayer.setSpawned(true);
	player.setGold(rfcPlayer.getStartingGold());
	player.processDynamicNames(true);
}

void CvRiseFall::assignStartingTechs(CivilizationTypes civType, PlayerTypes playerType) {
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	CvPlayer& player = GET_PLAYER(playerType);

	for(std::vector<TechTypes>::iterator it = rfcPlayer.getStartingTechs().begin(); it != rfcPlayer.getStartingTechs().end(); ++it) {
		GET_TEAM(player.getTeam()).setHasTech((*it), true, playerType, false, false);
	}
}

void CvRiseFall::assignStartingCivics(CivilizationTypes civType, PlayerTypes playerType) {
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	CvPlayer& player = GET_PLAYER(playerType);

	for(int i = 0; i<GC.getNumCivicOptionInfos(); i++) {
		if(rfcPlayer.getStartingCivic((CivicOptionTypes)i) != NO_CIVIC) {
			player.setCivics((CivicOptionTypes)i, rfcPlayer.getStartingCivic((CivicOptionTypes)i), true);
		}
	}
}

void CvRiseFall::setupStartingWars(CivilizationTypes civType, PlayerTypes playerType) {
	CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
	CvPlayer& player = GET_PLAYER(playerType);

	for(std::vector<CivilizationTypes>::iterator it = rfcPlayer.getStartingWars().begin(); it != rfcPlayer.getStartingWars().end(); ++it) {
		PlayerTypes loopPlayerType = getPlayerTypeForCiv(*it);
		if(loopPlayerType != NO_PLAYER) {
			CvPlayer& loopPlayer = GET_PLAYER(loopPlayerType);
			GET_TEAM(player.getTeam()).declareWar(loopPlayer.getTeam(), true, WARPLAN_TOTAL);
			GET_TEAM(loopPlayer.getTeam()).declareWar(player.getTeam(), true, WARPLAN_TOTAL);
		}
	}
}

void CvRiseFall::eraseSurroundings(CivilizationTypes civType, PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);

	int startingX = getRFCPlayer(civType).getStartingPlotX();
	int startingY = getRFCPlayer(civType).getStartingPlotY();
	CvPlot* startingPlot = GC.getMap().plot(startingX, startingY);

	//erase removable features (=forests)
	FeatureTypes featureType = startingPlot->getFeatureType();
	if(featureType!=NO_FEATURE) {
		for (int i = 0; i<GC.getNumBuildInfos(); i++) {
			if(GC.getBuildInfo((BuildTypes)i).isFeatureRemove(featureType)) {
				startingPlot->setFeatureType(NO_FEATURE);
			}
		}
	}

	if(startingPlot->getOwner() != NO_PLAYER) {
		GET_TEAM(player.getTeam()).declareWar(GET_PLAYER(startingPlot->getOwner()).getTeam(), true, WARPLAN_TOTAL);
	}

	for(int i = startingX-1; i<startingX+2; i++) {
		for(int j = startingY-1; j<startingY+2; j++) {
			CvPlot* plot = GC.getMap().plot(i, j);
			if(plot != NULL) {
				plot->eraseAIDevelopment();
				for(int k = 0; k<GC.getMAX_PLAYERS(); k++) {
					plot->setCulture((PlayerTypes)k, 0, false, false);
				}
				plot->setOwner(NO_PLAYER, false, false);
			}
		}
	}
}

void CvRiseFall::citySecession(CvCity* city) {
	int minorCivs = 0;
	for(int i = 0; i<MAX_PLAYERS; i++) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		if(player.isMinorCiv() || player.isBarbarian()) {
			minorCivs++;
		}
	}

	PlayerTypes minorCiv = NO_PLAYER;

	int acceptThreshold = 0;
	if(minorCivs>0) {
		for(int i = 0; i<MAX_PLAYERS; i++) {
			CvPlayer& player = GET_PLAYER((PlayerTypes)i);
			if(player.isMinorCiv() || player.isBarbarian()) {
				acceptThreshold += 100/minorCivs+1;
				if(GC.getGame().getSorenRandNum(100, "Minor civ roll") < acceptThreshold) {
					minorCiv = (PlayerTypes)i;
					break;
				}
			}
		}
	}

	if(minorCiv != NO_PLAYER) {
		flipCity(city, minorCiv, false);
	} else {
		city->kill(true);
	}
}

void CvRiseFall::flipCity(CvCity* city, PlayerTypes newOwnerType, bool flipAllUnits) {
	CvPlayer& newOwner = GET_PLAYER(newOwnerType);

	PlayerTypes previousOwnerType = flipAllUnits ? NO_PLAYER : city->getOwner();
	flipUnitsInArea(newOwner.getCivilizationType(), newOwnerType, city->getX()-1, city->getY()-1, city->getX()+1, city->getY()+1, previousOwnerType);
	newOwner.acquireCity(city, false, true, true);
}

void CvRiseFall::flipUnitsInArea(CivilizationTypes newCivType, PlayerTypes newOwnerType, int left, int bottom, int right, int top, PlayerTypes previousOwnerType) {
	CvUnit* loopUnit;
	for(int x = left; x<=right; x++) {
		for(int y = bottom; y<=top; y++) {
			CLLNode<IDInfo>* unitNode = GC.getMap().plot(x, y)->headUnitNode();
			static std::vector<IDInfo> oldUnits;
			oldUnits.clear();

			while (unitNode != NULL) {
				loopUnit = ::getUnit(unitNode->m_data);

				if(loopUnit->getOwner() != newOwnerType && (previousOwnerType==NO_PLAYER || previousOwnerType==loopUnit->getOwner())) {
					CvRFCUnit* scheduledUnit = getRFCPlayer(newCivType).addScheduledUnit();
					scheduledUnit->setYear(GC.getGame().getGameTurnYear());
					scheduledUnit->setX(x);
					scheduledUnit->setY(y);
					scheduledUnit->setUnitType(loopUnit->getUnitType());
					scheduledUnit->setUnitAIType(NO_UNITAI);
					scheduledUnit->setFacingDirection(DIRECTION_SOUTH);
					scheduledUnit->setAmount(1);
					oldUnits.push_back(unitNode->m_data);
				}
				unitNode = GC.getMap().plot(x, y)->nextUnitNode(unitNode);
			}

			for (uint i = 0; i<oldUnits.size(); i++) {
				loopUnit = ::getUnit(oldUnits[i]);
				if (loopUnit != NULL) {
					loopUnit->kill(false);
				}
			}
		}
	}
}

void CvRiseFall::capitalCollapse(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
	GC.logMsg("CvRiseFall::capitalCollapse %i", player.getCivilizationType());
	int i;
	for(CvCity* city = player.firstCity(&i); NULL != city; city = player.nextCity(&i)) {
		if(!city->isCapital()) {
			citySecession(city);
		}
	}
}

void CvRiseFall::completeCollapse(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
	GC.logMsg("CvRiseFall::completeCollapse %i", player.getCivilizationType());
	int i;
	for(CvCity* city = player.firstCity(&i); NULL != city; city = player.nextCity(&i)) {
		citySecession(city);
	}
	player.killUnits();
}

void CvRiseFall::setMapFile(const wchar* mapFile) {
	CvWString cwvMapFile(mapFile);
	_mapFile = cwvMapFile;
}


CvRFCProvince* CvRiseFall::addProvince(const wchar* name, int bottom, int left, int top, int right) {
	CvRFCProvince* province = new CvRFCProvince();
	province->setName(name);
	province->setBounds(bottom, left, top, right);
	_rfcProvinces.push_back(province);
	return province;
}

PlayerTypes CvRiseFall::getPlayerTypeForCiv(CivilizationTypes civType) const {
	for(int i = 0; i<MAX_PLAYERS; i++) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
		if(!rfcPlayer.isMinor() && GC.getGame().getGameTurn()==GC.getGame().getStartTurn() && rfcPlayer.getStartingYear() > GC.getGame().getGameTurnYear()) {
			continue;
		}
		if((rfcPlayer.getFlipCountdown() == 3 || player.isAlive() || player.isMinorCiv() || player.isBarbarian()) && player.getCivilizationType() == civType) {
			return (PlayerTypes)i;
		}
	}
	return NO_PLAYER;
}

CvRFCPlayer& CvRiseFall::getRFCPlayer(CivilizationTypes civType) const {
	return _rfcPlayers[civType];
}

CvRFCProvince* CvRiseFall::getRFCProvince(const wchar* provinceName) {
	std::vector<CvRFCProvince*>::iterator it;
	for (it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
		if(wcscmp(provinceName, (*it)->getName()) == 0) {
			return (*it);
		}
	}
	return NULL;
}

CvRFCProvince* CvRiseFall::getRFCProvince(int provinceID) const {
	return _rfcProvinces[provinceID];
}

int CvRiseFall::getNumProvinces() const {
	return _rfcProvinces.size();
}

CvRFCProvince* CvRiseFall::getProvinceForPlot(int x, int y) {
	std::vector<CvRFCProvince*>::iterator it;
	for (it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
		if((*it)->isInBounds(x, y)) {
			return (*it);
		}
	}
	return NULL;
}

bool CvRiseFall::unitsInForeignTerritory(PlayerTypes owner, PlayerTypes foreign) const {
	int i;
	for(CvUnit* unit = GET_PLAYER(owner).firstUnit(&i); unit != NULL; unit = GET_PLAYER(owner).nextUnit(&i)) {
		if(unit->plot()->getOwner() == foreign) {
			return true;
		}
	}
	return false;
}

bool CvRiseFall::skipConditionalSpawn(CivilizationTypes civType) const {
	switch(civType) {
		case CIVILIZATION_SASSANID:
			if(getPlayerTypeForCiv(CIVILIZATION_PERSIA) != NO_PLAYER || getPlayerTypeForCiv(CIVILIZATION_ELAM) != NO_PLAYER) {
				return true;
			}
			break;
		case CIVILIZATION_BYZANTIUM:
			PlayerTypes romePlayer = getPlayerTypeForCiv(CIVILIZATION_ROME);
			CvRFCPlayer& rfcPlayer = getRFCPlayer(civType);
			CvPlot* startingPlot = GC.getMap().plot(rfcPlayer.getStartingPlotX(), rfcPlayer.getStartingPlotY());
			if(romePlayer == NO_PLAYER || startingPlot->getOwner() != romePlayer || getRFCPlayer(GET_PLAYER(romePlayer).getCivilizationType()).getTotalStability() >= 40) {
				return true;
			}
			break;
	}
	return false;
}

CvPlot* CvRiseFall::findSpawnPlot(int ix, int iy, DomainTypes domainType) const {
	for(int x = ix - 1; x < ix + 1; ++x) {
		for(int y = iy - 1; y < iy + 1; ++y) {
			if(GC.getMap().isPlot(x, y)) {
				CvPlot* plot = GC.getMap().plot(x, y);
				if(!plot->isCity()) {
					if((plot->isWater() && domainType == DOMAIN_SEA || !plot->isWater() && domainType != DOMAIN_SEA) && !plot->isPeak()) {
						return plot;
					}
				}
			}
		}
	}
	return NULL;
}

const wchar* CvRiseFall::getMapFile() const {
	return _mapFile;
}


//read & write
void CvRiseFall::read(FDataStreamBase* stream) {
	reset();
	for(int i = 0; i<GC.getNumCivilizationInfos(); i++) {
		_rfcPlayers[i].read(stream);
	}

	{
		_rfcProvinces.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			CvRFCProvince* rfcProvince = new CvRFCProvince();
			rfcProvince->read(stream);
			_rfcProvinces.push_back(rfcProvince);
		}
	}
}


void CvRiseFall::write(FDataStreamBase* stream) {
	for(int i = 0; i<GC.getNumCivilizationInfos(); i++) {
		_rfcPlayers[i].write(stream);
	}

	{
		uint size = _rfcProvinces.size();
		stream->Write(size);
		for(std::vector<CvRFCProvince*>::iterator it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
			(*it)->write(stream);
		}
	}
}
