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
	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		_rfcPlayers[i].reset((CivilizationTypes)i);
	}
	for(std::vector<CvRFCProvince*>::iterator it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_rfcProvinces.clear();
}

void CvRiseFall::onGameStarted() {
	CvGame& game = GC.getGameINLINE();

	for(int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		if(player.isHuman()) {
			CvRFCPlayer& rfcPlayer = getRFCPlayer(player.getCivilizationType());
			rfcPlayer.setHuman(true);
			CvPlot* startingPlot = GC.getMapINLINE().plotINLINE(rfcPlayer.getStartingPlotX(), rfcPlayer.getStartingPlotY());
			player.initUnit(((UnitTypes)0), rfcPlayer.getStartingPlotX(), rfcPlayer.getStartingPlotY()); //will be killed as soon as autoplay starts, this is just to reveal the player's starting position like in RFC
			gDLL->getEngineIFace()->cameraLookAt(startingPlot->getPoint());
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
		if(GET_PLAYER((PlayerTypes)i).isAlive()) {
			GET_PLAYER((PlayerTypes)i).processDynamicNames();
			if(!GET_PLAYER((PlayerTypes)i).isHuman()) {
				checkLeader(GET_PLAYER((PlayerTypes)i).getCivilizationType(), (PlayerTypes)i);
			}
		}
	}
}

void CvRiseFall::checkTurn() {
	CvGame& game = GC.getGameINLINE();

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		if(getRFCPlayer((CivilizationTypes)i).isHuman()) {
			int turn = game.getGameTurn();
			turn = turn <= 1 ? turn : turn + 1;
			checkTurnForPlayer((CivilizationTypes)i, turn);
		}
	}

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		if(!getRFCPlayer((CivilizationTypes)i).isHuman()) {
			checkTurnForPlayer((CivilizationTypes)i, game.getGameTurn());
		}
	}

	for(int i = 0; i < getNumProvinces(); ++i) {
		//Mercenaries
		if(GC.getGameINLINE().getGameTurn() % 5 == 3) {
			getProvince((ProvinceTypes)i).checkMercenaries();
		}

		//Historical barbs

		int numScheduledUnits = getProvince((ProvinceTypes)i).getNumScheduledUnits();
		if(numScheduledUnits > 0) {
			//skip barb spawning if no plots are owned in province
			if(getProvince((ProvinceTypes)i).canSpawnBarbs() && getProvince((ProvinceTypes)i).getPlots().size() > 0) {
				std::vector<CvPlot*> validPlots;
				bool plotsInit = false;
				std::vector<CvPlot*> validSeaPlots;
				bool seaPlotsInit = false;
				for(int j = 0; j < numScheduledUnits; ++j) {
					CvRFCUnit* rfcUnit = getProvince((ProvinceTypes)i).getScheduledUnit(j);
					DomainTypes domainType = (DomainTypes)GC.getUnitInfo(rfcUnit->getUnitType()).getDomainType();
					if(domainType == DOMAIN_SEA && !seaPlotsInit) {
						for(std::vector<int>::iterator it = getProvince((ProvinceTypes)i).getPlots().begin(); it != getProvince((ProvinceTypes)i).getPlots().end(); ++it) {
							CvPlot* loopPlot = GC.getMapINLINE().plotByIndexINLINE(*it);
							if(loopPlot->isWater()) {
								validSeaPlots.push_back(loopPlot);
							}
						}
						seaPlotsInit = true;
					} else if(domainType != DOMAIN_SEA && !plotsInit) {
						for(std::vector<int>::iterator it = getProvince((ProvinceTypes)i).getPlots().begin(); it != getProvince((ProvinceTypes)i).getPlots().end(); ++it) {
							CvPlot* loopPlot = GC.getMapINLINE().plotByIndexINLINE(*it);
							if(!loopPlot->isCity() && !loopPlot->isWater() && !loopPlot->isPeak()) {
								validPlots.push_back(loopPlot);
							}
						}
						plotsInit = true;
					}
					if(rfcUnit->getLastSpawned() == -1 || rfcUnit->getLastSpawned() + rfcUnit->getSpawnFrequency()/2 < game.getGameTurn()) {
						if(rfcUnit->getYear() <= game.getGameTurnYear() && rfcUnit->getEndYear() >= game.getGameTurnYear() && game.getSorenRandNum(rfcUnit->getSpawnFrequency()/2, "Unit spawn roll") == 0) {
							CvPlot* randomPlot;
							if(domainType != DOMAIN_SEA) {
								randomPlot = validPlots[game.getSorenRandNum(validPlots.size(), "Barb spawning plot roll")];
							} else {
								randomPlot = validSeaPlots[game.getSorenRandNum(validSeaPlots.size(), "Barb spawning plot roll")];
							}

							FAssert(randomPlot != NULL);

							for(int k = 0; k < rfcUnit->getAmount(); ++k) {
								//TODO: different rfcUnit owner civs?
								GET_PLAYER(BARBARIAN_PLAYER).initUnit(rfcUnit->getUnitType(), randomPlot->getX(), randomPlot->getY(), rfcUnit->getUnitAIType(), rfcUnit->getFacingDirection());
							}
							rfcUnit->setLastSpawned(game.getGameTurn());
						}
					}
				}
			}
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
	PlayerTypes playerType = getRFCPlayer(civType).getPlayerType();

	if(rfcPlayer.getStartingYear() <= GC.getGameINLINE().getTurnYear(turn) || playerType != NO_PLAYER || rfcPlayer.isMinor()) { //barbarians & minors as well
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
			} else if(civType == CIVILIZATION_BARBARIAN) { //barbarian
				rfcPlayer.setSpawned(true);
				rfcPlayer.setPlayerType(BARBARIAN_PLAYER);
				for (int j = 0; j < MAX_CIV_TEAMS; j++) {
					if ((TeamTypes)j != GET_PLAYER(BARBARIAN_PLAYER).getTeam()) {
						GET_TEAM(GET_PLAYER(BARBARIAN_PLAYER).getTeam()).declareWar(((TeamTypes)j), false, NO_WARPLAN);
					}
				}
			} else if(rfcPlayer.isMinor()) { //minor civs
				spawnMinorCivilization(civType);
			} else { //major AI civs
				spawnAICivilization(civType);
			}
		}

		playerType = getRFCPlayer(civType).getPlayerType(); //refresh playerType as we might've spawned now

		if(playerType != NO_PLAYER) { //if yes, check stability, flipping, scheduled units and cities.
			CvPlayer& player = GET_PLAYER(playerType);

			if(!player.isMinorCiv() && !player.isBarbarian()) {
				checkStabilityEffect(civType, playerType);

				//Flip here because we want the flipped units to be spawned right after flipping the cities
				checkFlip(civType, playerType);
			}

			checkScheduledCities(civType, playerType, turn);
			checkScheduledUnits(civType, playerType, turn, spawnedNow);
		}
	}
}

void CvRiseFall::checkFlip(CivilizationTypes civType, PlayerTypes playerType) {
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
					FAssert((*it)->getOwnerINLINE() != playerType);
					if(!GET_TEAM(GET_PLAYER(playerType).getTeam()).isAtWar(GET_PLAYER((*it)->getOwnerINLINE()).getTeam())) {
						GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(GET_PLAYER((*it)->getOwnerINLINE()).getTeam(), true, WARPLAN_TOTAL); //we want new civs to completely destroy older ones
					}
					flipCity(*it, playerType, true);
				}
			}
			getRFCPlayer(civType).setFlipped(true);
		}
	}
}

void CvRiseFall::checkScheduledCities(CivilizationTypes civType, PlayerTypes playerType, int turn) {
	std::vector<CvRFCCity*>& scheduledCities = getRFCPlayer(civType).getScheduledCities();
	for(std::vector<CvRFCCity*>::iterator it = scheduledCities.begin(); it != scheduledCities.end();) {
		CvRFCCity* rfcCity = *it;
		if(GC.getGameINLINE().getTurnYear(turn) >= rfcCity->getYear()) {
			if(GET_PLAYER(playerType).canFound(rfcCity->getX(), rfcCity->getY())) {
				GET_PLAYER(playerType).initCity(rfcCity->getX(), rfcCity->getY(), true, true);
				CvCity* city = GC.getMapINLINE().plotINLINE(rfcCity->getX(), rfcCity->getY())->getPlotCity();
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
						GC.getGameINLINE().setHolyCity((ReligionTypes)i, city, false);
					}
				}
				for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
					if(rfcCity->getCulture((CivilizationTypes)i) > 0) {
						PlayerTypes cultureCiv = NO_PLAYER;
						for(int j = 0; j < MAX_PLAYERS; ++j) {
							if(GET_PLAYER((PlayerTypes)j).isAlive() && GET_PLAYER((PlayerTypes)j).getCivilizationType() == (CivilizationTypes)i) {
								cultureCiv = (PlayerTypes)j;
							}
						}
						if(cultureCiv != NO_PLAYER) {
							city->setCulture(cultureCiv, rfcCity->getCulture((CivilizationTypes)i), true, true);
						}
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

void CvRiseFall::checkScheduledUnits(CivilizationTypes civType, PlayerTypes playerType, int turn, bool spawnedNow) {
	std::vector<CvRFCUnit*>& scheduledUnits = getRFCPlayer(civType).getScheduledUnits();
	for(std::vector<CvRFCUnit*>::iterator it = scheduledUnits.begin(); it != scheduledUnits.end();) {
		CvRFCUnit* rfcUnit = *it;
		if(GC.getGameINLINE().getTurnYear(turn) >= rfcUnit->getYear()) {
			if(!rfcUnit->isAIOnly() || !getRFCPlayer(civType).isHuman()) {
				int ix = rfcUnit->getX();
				int iy = rfcUnit->getY();
				CvPlot* plot = GC.getMapINLINE().plotINLINE(ix, iy);
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
					PlayerTypes plotOwner = plot->getOwnerINLINE();
					if(plotOwner != NO_PLAYER && plotOwner != playerType) {
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

	if(!player.isBarbarian() && !player.isMinorCiv()) {
		if(GC.getGameINLINE().getGameTurn() % 2 != 0) {
			checkMinorWars(playerType);
		}
		if(GC.getGameINLINE().getGameTurn() % 3 == 2) {
			getRFCPlayer(player.getCivilizationType()).checkStability(playerType);
			if(!player.isHuman()) {
				checkLeader(player.getCivilizationType(), playerType);
			}
		}
	}
}

void CvRiseFall::checkMinorWars(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);

	PlayerTypes minorCivType = NO_PLAYER;

	for(int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		CvPlayer& loopCiv = GET_PLAYER((PlayerTypes)i);
		if(loopCiv.isAlive() && loopCiv.isMinorCiv() && !loopCiv.isBarbarian()) {
			if(GC.getGameINLINE().getSorenRandNum(100, "Minor civ for checkMinorWars") < 50) {
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
		if(GC.getGameINLINE().getSorenRandNum(100, "Peace for checkMinorWars") <= rand) {
			if(!unitsInForeignTerritory(playerType, minorCivType)) {
				GET_TEAM(player.getTeam()).makePeace(minorCiv.getTeam(), false);
			}
		}
	} else if(!player.isHuman()) {
		if(GC.getGameINLINE().getSorenRandNum(100, "War for checkMinorWars") <= 10) {
			GET_TEAM(player.getTeam()).declareWar(minorCiv.getTeam(), false, WARPLAN_TOTAL);
		}
	}
}

void CvRiseFall::checkLeader(CivilizationTypes civType, PlayerTypes playerType) {
	LeaderHeadTypes leader = NO_LEADER;
	CvCivilizationInfo& civInfo = GC.getCivilizationInfo(civType);
	int reign = 0;

	for(int i = 0; i < GC.getNumLeaderHeadInfos(); ++i) {
		if(!civInfo.isLeaders(i)) {
			continue;
		}
		CvLeaderHeadInfo& leaderInfo = GC.getLeaderHeadInfo((LeaderHeadTypes)i);
		if(leaderInfo.getLeaderReign() <= GC.getGameINLINE().getGameTurnYear()
				&& (leader == NO_LEADER || reign < leaderInfo.getLeaderReign())) {
			reign = leaderInfo.getLeaderReign();
			leader = (LeaderHeadTypes)i;
		}
	}

	FAssert(leader != NO_LEADER);

	if(GC.getInitCore().getLeader(playerType) != leader) {
		GC.getInitCore().setLeader(playerType, leader);
	}
}

void CvRiseFall::spawnHumanCivilization(CivilizationTypes civType) {
	CvGame& game = GC.getGameINLINE();

	for(int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		CvPlayerAI& player = GET_PLAYER((PlayerTypes)i);
		if(player.isHuman() && player.getCivilizationType() == civType) {
			game.setAIAutoPlay(0);

			if(player.getNumUnits() > 0) {
				gDLL->getInterfaceIFace()->selectGroup(player.getUnit(0), false, false, false);
			}

			getRFCPlayer(civType).setPlayerType((PlayerTypes)i);

			finishMajorCivSpawn(civType, (PlayerTypes)i);
			return;
		}
	}
	GC.logMsg("CvRiseFall::spawnHumanCivilization - Failed to spawn human civ %i", civType);
}

void CvRiseFall::updatePlayerPlots() {
	int* ownedPlots = new int[GC.getNumCivilizationInfos()];

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		ownedPlots[i] = 0;
	}

	for(int x = 0; x<GC.getMapINLINE().getGridWidth(); ++x) {
		for(int y = 0; y<GC.getMapINLINE().getGridHeight(); ++y) {
			CvPlot* plot = GC.getMapINLINE().plotINLINE(x, y);
			if(!plot->isWater() && !plot->isPeak() && plot->getOwnerINLINE() != NO_PLAYER) {
				CivilizationTypes civType = GET_PLAYER(plot->getOwnerINLINE()).getCivilizationType();
				if(plot->getSettlerValue(civType) < 90) {
					ownedPlots[civType] += 1;
				}
			}
		}
	}

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		getRFCPlayer((CivilizationTypes)i).setNumPlots(ownedPlots[i]);
	}

	SAFE_DELETE_ARRAY(ownedPlots);
}

void CvRiseFall::checkStabilityEffect(CivilizationTypes civType, PlayerTypes playerType) {
	//we don't want new civs to collapse, nor do we want to check all of this every turn
	if(GC.getGameINLINE().getGameTurn() % 6 != 0) {
		return;
	}
	if(GC.getGameINLINE().getGameTurn() <= getRFCPlayer(civType).getStartingTurn() + 20) {
		return;
	}
	CvPlayer& player = GET_PLAYER(playerType);

	if(getRFCPlayer(civType).getTotalStability() < 0) {
		//shaky, risk of city independent secessions
		if(GC.getGameINLINE().getSorenRandNum(100, "Secession roll") <= 5) {
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
					int newStability = getRFCPlayer(civType).getPermStability(j) / 3;
					newStability *= 2;
					getRFCPlayer(civType).setPermStability(j, newStability);
				}
			}
		}
	}
	if(getRFCPlayer(civType).getTotalStability() < -20) {
		if(GC.getGameINLINE().getSorenRandNum(100, "Secession roll") <= 10) {
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
				int newStability = getRFCPlayer(civType).getPermStability(j) / 4;
				newStability *= 3;
				getRFCPlayer(civType).setPermStability(j, newStability);
			}
		}
	}
	if(getRFCPlayer(civType).getTotalStability() < -40) {
		//collapsing, risk of complete collapse (or collapse to core in case of the human player)
		if(GC.getGameINLINE().getSorenRandNum(100, "Collapse roll") <= 40) {
			if(player.isHuman()) {
				capitalCollapse(playerType);
			} else {
				completeCollapse(playerType);
			}
			for(int j = 0; j < NUM_STABILITY_CATEGORIES; ++j) {
				getRFCPlayer(civType).setPermStability(j, 0);
				getRFCPlayer(civType).setTempStability(j, 0);
			}
		}
	}
}

void CvRiseFall::spawnAICivilization(CivilizationTypes civType) {
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		CvPlayerAI& player = GET_PLAYER((PlayerTypes)i);
		if(!player.isAlive() && !player.isBarbarian() && !player.isMinorCiv() && !player.isHuman()) { //use slot if it isn't occupied by a human, barbarian or minor civ.
			getRFCPlayer(civType).setPlayerType((PlayerTypes)i);
			setupAIPlayer(civType, (PlayerTypes)i);
			finishMajorCivSpawn(civType, (PlayerTypes)i);
			return;
		}
	}
	GC.logMsg("CvRiseFall::spawnAICivilization - Failed to spawn ai civ %i", civType);
}

void CvRiseFall::spawnMinorCivilization(CivilizationTypes civType) {
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i) {
		CvPlayer& player = GET_PLAYER((PlayerTypes)i);
		if(!player.isAlive() && !player.isHuman() && player.isMinorCiv()) { //add minor civ if this is a "minor slot"
			setupAIPlayer(civType, (PlayerTypes)i);
			getRFCPlayer(civType).setSpawned(true);
			getRFCPlayer(civType).setPlayerType((PlayerTypes)i);
			if(!GET_TEAM(player.getTeam()).isAtWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam())) {
				GET_TEAM(player.getTeam()).declareWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam(), true, NO_WARPLAN);
			}
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

	eraseSurroundings(civType, playerType);
	if(GET_PLAYER(playerType).isHuman()) {
		GET_PLAYER(playerType).setAlive(true);
	}
	if(!GET_TEAM(GET_PLAYER(playerType).getTeam()).isAtWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam())) {
		GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(GET_PLAYER(BARBARIAN_PLAYER).getTeam(), true, NO_WARPLAN);
	}
	assignStartingTechs(civType, playerType);
	assignStartingCivics(civType, playerType);
	setupStartingWars(civType, playerType);
	if(!getRFCPlayer(civType).isFlipped()) {
		getRFCPlayer(civType).setFlipCountdown(3);
	}
	getRFCPlayer(civType).setStartingTurn(GC.getGameINLINE().getGameTurn());
	getRFCPlayer(civType).setSpawned(true);
	GET_PLAYER(playerType).setGold(getRFCPlayer(civType).getStartingGold());
	if(getRFCPlayer(civType).getStartingReligion() != NO_RELIGION) {
		GET_PLAYER(playerType).setLastStateReligion(getRFCPlayer(civType).getStartingReligion());
	}
	GET_PLAYER(playerType).processDynamicNames(true);
}

void CvRiseFall::assignStartingTechs(CivilizationTypes civType, PlayerTypes playerType) {
	for(int i = 0; i < GC.getNumTechInfos(); ++i) {
		GET_TEAM(GET_PLAYER(playerType).getTeam()).setHasTech((TechTypes)i, getRFCPlayer(civType).isStartingTech((TechTypes)i), playerType, false, false);
	}
}

void CvRiseFall::assignStartingCivics(CivilizationTypes civType, PlayerTypes playerType) {
	for(int i = 0; i < GC.getNumCivicOptionInfos(); ++i) {
		if(getRFCPlayer(civType).getStartingCivic((CivicOptionTypes)i) != NO_CIVIC) {
			GET_PLAYER(playerType).setCivics((CivicOptionTypes)i,
					getRFCPlayer(civType).getStartingCivic((CivicOptionTypes)i),
					true);
		}
	}
}

void CvRiseFall::setupStartingWars(CivilizationTypes civType, PlayerTypes playerType) {
	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		if(getRFCPlayer(civType).isStartingWar((CivilizationTypes)i)) {
			PlayerTypes loopPlayerType = getRFCPlayer((CivilizationTypes)i).getPlayerType();
			if(loopPlayerType != NO_PLAYER) {
				FAssert(loopPlayerType != playerType);
				CvPlayer& loopPlayer = GET_PLAYER(loopPlayerType);
				GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(loopPlayer.getTeam(), true, WARPLAN_TOTAL);
			}
		}
	}
}

void CvRiseFall::eraseSurroundings(CivilizationTypes civType, PlayerTypes playerType) {
	int startingX = getRFCPlayer(civType).getStartingPlotX();
	int startingY = getRFCPlayer(civType).getStartingPlotY();
	CvPlot* startingPlot = GC.getMapINLINE().plotINLINE(startingX, startingY);

	//erase removable features (=forests)
	FeatureTypes featureType = startingPlot->getFeatureType();
	if(featureType != NO_FEATURE) {
		for (int i = 0; i < GC.getNumBuildInfos(); ++i) {
			if(GC.getBuildInfo((BuildTypes)i).isFeatureRemove(featureType)) {
				startingPlot->setFeatureType(NO_FEATURE);
			}
		}
	}

	if(startingPlot->getOwnerINLINE() != NO_PLAYER) {
		FAssert(startingPlot->getOwnerINLINE() != playerType);
		GET_TEAM(GET_PLAYER(playerType).getTeam()).declareWar(GET_PLAYER(startingPlot->getOwnerINLINE()).getTeam(), true, WARPLAN_TOTAL);
	}

	startingPlot->setImprovementType(NO_IMPROVEMENT);
	for(int i = startingX-1; i < startingX+2; ++i) {
		for(int j = startingY-1; j<startingY+2; ++j) {
			if(GC.getMapINLINE().isPlotINLINE(i, j)) {
				CvPlot* plot = GC.getMapINLINE().plotINLINE(i, j);
				plot->eraseAIDevelopment();
				for(int k = 0; k < GC.getMAX_PLAYERS(); ++k) {
					plot->setCulture((PlayerTypes)k, 0, false, false);
				}
				plot->setOwner(NO_PLAYER, false, false);
			}
		}
	}
}

void CvRiseFall::citySecession(CvCity* city) {
	int minorCivs = 0;
	for(int i = 0; i < MAX_PLAYERS; ++i) {
		if(GET_PLAYER((PlayerTypes)i).isMinorCiv() || GET_PLAYER((PlayerTypes)i).isBarbarian()) {
			++minorCivs;
		}
	}

	PlayerTypes minorCiv = NO_PLAYER;

	int acceptThreshold = 0;
	if(minorCivs > 0) {
		for(int i = 0; i < MAX_PLAYERS; ++i) {
			if(GET_PLAYER((PlayerTypes)i).isMinorCiv() || GET_PLAYER((PlayerTypes)i).isBarbarian()) {
				acceptThreshold += 100/minorCivs+1;
				if(GC.getGameINLINE().getSorenRandNum(100, "Minor civ roll") < acceptThreshold) {
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

	PlayerTypes previousOwnerType = flipAllUnits ? NO_PLAYER : city->getOwnerINLINE();
	flipUnitsInArea(newOwner.getCivilizationType(), newOwnerType, city->getX()-1, city->getY()-1, city->getX()+1, city->getY()+1, previousOwnerType);
	newOwner.acquireCity(city, false, true, true);
}

void CvRiseFall::flipUnitsInArea(CivilizationTypes newCivType, PlayerTypes newOwnerType, int left, int bottom, int right, int top, PlayerTypes previousOwnerType) {
	CvUnit* loopUnit;
	for(int x = left; x<=right; x++) {
		for(int y = bottom; y<=top; y++) {
			if(!GC.getMapINLINE().isPlotINLINE(x, y)) {
				return;
			}
			CLLNode<IDInfo>* unitNode = GC.getMapINLINE().plotINLINE(x, y)->headUnitNode();
			static std::vector<IDInfo> oldUnits;
			oldUnits.clear();

			while (unitNode != NULL) {
				loopUnit = ::getUnit(unitNode->m_data);

				if(loopUnit->getOwnerINLINE() != newOwnerType && (previousOwnerType==NO_PLAYER || previousOwnerType==loopUnit->getOwnerINLINE())) {
					CvRFCUnit* scheduledUnit = getRFCPlayer(newCivType).addScheduledUnit();
					scheduledUnit->setYear(GC.getGameINLINE().getGameTurnYear());
					scheduledUnit->setX(x);
					scheduledUnit->setY(y);
					scheduledUnit->setUnitType(loopUnit->getUnitType());
					scheduledUnit->setUnitAIType(NO_UNITAI);
					scheduledUnit->setFacingDirection(DIRECTION_SOUTH);
					scheduledUnit->setAmount(1);
					oldUnits.push_back(unitNode->m_data);
				}
				unitNode = GC.getMapINLINE().plotINLINE(x, y)->nextUnitNode(unitNode);
			}

			for (uint i = 0; i < oldUnits.size(); ++i) {
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
	int i;
	for(CvCity* city = player.firstCity(&i); NULL != city; city = player.nextCity(&i)) {
		if(!city->isCapital()) {
			citySecession(city);
		}
	}
}

void CvRiseFall::completeCollapse(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
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

void CvRiseFall::removeProvince(ProvinceTypes provinceType) {
	for(int i = 0; i < GC.getMapINLINE().numPlotsINLINE(); ++i) {
		if(GC.getMapINLINE().plotByIndexINLINE(i)->getProvinceType() == provinceType) {
			GC.getMapINLINE().plotByIndexINLINE(i)->setProvinceType(NO_PROVINCE);
		} else if(GC.getMapINLINE().plotByIndexINLINE(i)->getProvinceType() > provinceType) {
			GC.getMapINLINE().plotByIndexINLINE(i)->setProvinceType((ProvinceTypes)
				(GC.getMapINLINE().plotByIndexINLINE(i)->getProvinceType() - 1));
		}
	}

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		for(int j = getRFCPlayer((CivilizationTypes)i).getNumCoreProvinces() - 1; j >= 0; --j) {
			ProvinceTypes coreProvince = getRFCPlayer((CivilizationTypes)i).getCoreProvince(j);
			if(coreProvince == provinceType) {
				getRFCPlayer((CivilizationTypes)i).removeCoreProvince(j);
			} else if(coreProvince > provinceType) {
				getRFCPlayer((CivilizationTypes)i).changeCoreProvince(j, (ProvinceTypes)(coreProvince - 1));
			}
		}
	}

	SAFE_DELETE(_rfcProvinces[provinceType]);
	_rfcProvinces.erase(_rfcProvinces.begin() + provinceType);
}


CvRFCProvince* CvRiseFall::addProvince(CvString type) {
	CvRFCProvince* province = new CvRFCProvince((ProvinceTypes)_rfcProvinces.size());
	province->setType(type);
	_rfcProvinces.push_back(province);
	return province;
}

ProvinceTypes CvRiseFall::findProvince(const char* provinceType) const {
	for (int i = 0; i < getNumProvinces(); ++i) {
		if(strcmp(provinceType, getProvince((ProvinceTypes)i).getType()) == 0) {
			return (ProvinceTypes)i;
		}
	}
	return NO_PROVINCE;
}

int CvRiseFall::getNumProvinces() const {
	return _rfcProvinces.size();
}

bool CvRiseFall::unitsInForeignTerritory(PlayerTypes owner, PlayerTypes foreign) const {
	int i;
	for(CvUnit* unit = GET_PLAYER(owner).firstUnit(&i); unit != NULL; unit = GET_PLAYER(owner).nextUnit(&i)) {
		if(unit->plot()->getOwnerINLINE() == foreign) {
			return true;
		}
	}
	return false;
}

bool CvRiseFall::skipConditionalSpawn(CivilizationTypes civType) const {
	switch(civType) {
		case CIVILIZATION_SASSANID:
			if(getRFCPlayer(CIVILIZATION_PERSIA).getPlayerType() != NO_PLAYER || getRFCPlayer(CIVILIZATION_ELAM).getPlayerType() != NO_PLAYER) {
				return true;
			}
			break;
		case CIVILIZATION_BYZANTIUM:
			PlayerTypes romePlayer = getRFCPlayer(CIVILIZATION_ROME).getPlayerType();
			if(romePlayer == NO_PLAYER || getRFCPlayer(civType).getStartingPlot()->getOwnerINLINE() != romePlayer) {
				return true;
			} else if(getRFCPlayer(CIVILIZATION_ROME).getTotalStability() >= 40) {
				return true;
			}
			break;
	}
	return false;
}

CvPlot* CvRiseFall::findSpawnPlot(int ix, int iy, DomainTypes domainType) const {
	for(int i = NO_DIRECTION; i < NUM_DIRECTION_TYPES; ++i) {
		CvPlot* plot = ::plotDirection(ix, iy, (DirectionTypes)i);
		if(plot != NULL) {
			if((plot->isWater() && domainType == DOMAIN_SEA || !plot->isWater() && domainType != DOMAIN_SEA) && !plot->isPeak()) {
				return plot;
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
	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		_rfcPlayers[i].read(stream);
	}

	{
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; ++i) {
			CvRFCProvince* rfcProvince = new CvRFCProvince(NO_PROVINCE);
			rfcProvince->read(stream);
			_rfcProvinces.push_back(rfcProvince);
		}
	}
	stream->ReadString(_mapFile);
}


void CvRiseFall::write(FDataStreamBase* stream) {
	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		_rfcPlayers[i].write(stream);
	}

	{
		uint size = _rfcProvinces.size();
		stream->Write(size);
		for(std::vector<CvRFCProvince*>::iterator it = _rfcProvinces.begin(); it != _rfcProvinces.end(); ++it) {
			(*it)->write(stream);
		}
	}
	stream->WriteString(_mapFile);
}
