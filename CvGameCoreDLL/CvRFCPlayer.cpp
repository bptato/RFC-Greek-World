/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCPlayer.h"

CvRFCPlayer::CvRFCPlayer() {
	_startingCivics = new int[GC.getNumCivicOptionInfos()];
	_startingWars = new bool[GC.getNumCivilizationInfos()];
	_startingTechs = new bool[GC.getNumTechInfos()];
	init(NO_CIVILIZATION);
}

CvRFCPlayer::~CvRFCPlayer() {
	uninit();
	SAFE_DELETE_ARRAY(_startingCivics);
	SAFE_DELETE_ARRAY(_startingWars);
	SAFE_DELETE_ARRAY(_startingTechs);
}

void CvRFCPlayer::reset(CivilizationTypes civilizationType) {
	uninit();
	init(civilizationType);
}

void CvRFCPlayer::init(CivilizationTypes civilizationType) {
	_civilizationType = civilizationType;
	_playerType = NO_PLAYER;
	_startingYear = 0;
	_startingTurn = -1;
	_startingPlotX = 0;
	_startingPlotY = 0;
	_startingGold = 0;
	_startingReligion = NO_RELIGION;
	_flipCountdown = 0;
	_GNP = 0;
	_numPlots = 0;

	//modifiers (following values are BTS defaults, though some of them replace handicap values)
	_compactEmpireModifier = 50;
	_unitUpkeepModifier = 100;
	_researchModifier = 100;
	_distanceMaintenanceModifier = 100;
	_numCitiesMaintenanceModifier = 100;
	_unitProductionModifier = 100;
	_civicUpkeepModifier = 100;
	_healthBonusModifier = 0;
	_buildingProductionModifier = 100;
	_wonderProductionModifier = 100;
	_greatPeopleModifier = 100;
	_inflationModifier = 100;
	_growthModifier = 100;

	_enabled = false;
	_spawned = false;
	_minor = false;
	_human = false;
	_flipped = false;

	_vassalBonus = false;
	_foundBonus = false;
	_conquestBonus = false;
	_commerceBonus = false;

	_newCityFreePopulation = 0;

	for(int i = 0; i < GC.getNumCivicOptionInfos(); i++) {
		_startingCivics[i] = NO_CIVIC;
	}

	for(int i = 0; i < NUM_STABILITY_CATEGORIES; i++) {
		_tempStability[i] = 0;
		_permStability[i] = 0;
	}

	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		_startingWars[i] = false;
	}

	for(int i = 0; i < GC.getNumTechInfos(); ++i) {
		_startingTechs[i] = false;
	}

	_coreProvinces.clear();
	_relatedLanguages.clear();
}

void CvRFCPlayer::uninit() {
	for(std::vector<CvRFCUnit*>::iterator it = _scheduledUnits.begin(); it != _scheduledUnits.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_scheduledUnits.clear();
	for(std::vector<CvRFCCity*>::iterator it = _scheduledCities.begin(); it != _scheduledCities.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_scheduledCities.clear();
}

void CvRFCPlayer::setCivilizationType(CivilizationTypes civilizationType) {
	_civilizationType = civilizationType;
}

void CvRFCPlayer::setPlayerType(PlayerTypes playerType) {
	_playerType = playerType;
}

void CvRFCPlayer::setEnabled(bool enabled) {
	_enabled = enabled;
}

void CvRFCPlayer::setStartingCivic(CivicOptionTypes civicOptionType, CivicTypes civicType) {
	_startingCivics[civicOptionType] = civicType;
}

void CvRFCPlayer::setStartingYear(int startingYear) {
	_startingYear = startingYear;
}

void CvRFCPlayer::setStartingTurn(int startingTurn) {
	_startingTurn = startingTurn;
}

void CvRFCPlayer::setStartingPlotX(int startingPlotX) {
	_startingPlotX = startingPlotX;
}

void CvRFCPlayer::setStartingPlotY(int startingPlotY) {
	_startingPlotY = startingPlotY;
}

void CvRFCPlayer::setStartingGold(int startingGold) {
	_startingGold = startingGold;
}

void CvRFCPlayer::setStartingReligion(ReligionTypes startingReligion) {
	_startingReligion = startingReligion;
}

void CvRFCPlayer::setMinorCiv(bool minor) {
	_minor = minor;
}

void CvRFCPlayer::setHuman(bool human) {
	_human = human;
}

void CvRFCPlayer::setSpawned(bool spawned) {
	_spawned = spawned;
}

void CvRFCPlayer::setFlipped(bool flipped) {
	_flipped = flipped;
}

void CvRFCPlayer::setStartingTech(TechTypes tech, bool value) {
	FAssert(tech != NO_TECH);
	_startingTechs[tech] = value;
}

void CvRFCPlayer::addCoreProvince(const char* province) {
	_coreProvinces.push_back(province);
}

void CvRFCPlayer::setFlipCountdown(int flipCountdown) {
	_flipCountdown = flipCountdown;
}

void CvRFCPlayer::setTempStability(int category, int stability) {
	_tempStability[category] = stability;
}

void CvRFCPlayer::setPermStability(int category, int stability) {
	_permStability[category] = stability;
}

void CvRFCPlayer::setGNP(int GNP) {
	_GNP = GNP;
}

void CvRFCPlayer::setStartingWar(CivilizationTypes civType, bool startingWar) {
	FAssert(civType != NO_CIVILIZATION);
	_startingWars[civType] = startingWar;
}

void CvRFCPlayer::addRelatedLanguage(CivilizationTypes civType) {
	_relatedLanguages.push_back(civType);
}

void CvRFCPlayer::setNumPlots(int numPlots) {
	_numPlots = numPlots;
}

void CvRFCPlayer::checkStability(PlayerTypes playerType) {
	CvPlayer& player = GET_PLAYER(playerType);
	if(player.getNumCities() == 0) {
		return;
	}
	CvTeam& team = GET_TEAM(player.getTeam());
	CvGame& game = GC.getGameINLINE();
	int i;

	int citiesStability = getTempStability(0);
	int civicsStability = getTempStability(1);
	int economicStability = getTempStability(2);
	int expansionStability = getTempStability(3);
	int foreignStability = getTempStability(4);

	int permEconomicStability = getPermStability(2);

	int newCitiesStability = 0;
	int newCivicsStability = 0;
	int newEconomicStability = 0;
	int newExpansionStability = 0;
	int newForeignStability = 0;

	int population = std::max(1, player.getTotalPopulation());
	int eraModifier = player.getCurrentEra(); //can be 0!

	//Civics
	_vassalBonus = false;
	_foundBonus = false;
	_conquestBonus = false;
	_commerceBonus = false;
	for(i = 0; i<GC.getNumCivicOptionInfos(); ++i) {
		CvCivicInfo& civicInfo = GC.getCivicInfo(player.getCivics((CivicOptionTypes)i));
		if(civicInfo.isStabilityVassalBonus()) {
			_vassalBonus = true;
		}
		if(civicInfo.isStabilityFoundBonus()) {
			_foundBonus = true;
		}
		if(civicInfo.isStabilityConquestBonus()) {
			_conquestBonus = true;
		}
		if(civicInfo.isStabilityCommerceBonus()) {
			_commerceBonus = true;
		}
	}

	if(_vassalBonus) {
		for(i = 0; i<MAX_TEAMS; ++i) {
			if(GET_TEAM((TeamTypes)i).isVassal(player.getTeam())) {
				newCivicsStability += 2;
			}
		}
	}

	if(_commerceBonus) {
		if(newEconomicStability<0) {
			newEconomicStability *= 90;
			newEconomicStability /= 100;
		}
	}

	//TODO: do this stuff in a saner way
	int civicCompatibility = 0;

	static CivicTypes tribal_federation = (CivicTypes)GC.getInfoTypeForString("CIVIC_TRIBAL_FEDERATION");
	static CivicTypes monarchy = (CivicTypes)GC.getInfoTypeForString("CIVIC_MONARCHY");
	static CivicTypes oligarchy = (CivicTypes)GC.getInfoTypeForString("CIVIC_OLIGARCHY");
	static CivicTypes absolutism = (CivicTypes)GC.getInfoTypeForString("CIVIC_ABSOLUTISM");
	static CivicTypes aristocracy = (CivicTypes)GC.getInfoTypeForString("CIVIC_ARISTOCRACY");

	static CivicTypes tribal_custom = (CivicTypes)GC.getInfoTypeForString("CIVIC_TRIBAL_CUSTOM");
	static CivicTypes vassalage = (CivicTypes)GC.getInfoTypeForString("CIVIC_VASSALAGE");
	static CivicTypes bureaucracy = (CivicTypes)GC.getInfoTypeForString("CIVIC_BUREAUCRACY");
	static CivicTypes empire = (CivicTypes)GC.getInfoTypeForString("CIVIC_EMPIRE");
	static CivicTypes religious_law = (CivicTypes)GC.getInfoTypeForString("CIVIC_RELIGIOUS_LAW");

	static CivicTypes tribalism = (CivicTypes)GC.getInfoTypeForString("CIVIC_TRIBALISM");
	static CivicTypes slavery = (CivicTypes)GC.getInfoTypeForString("CIVIC_SLAVERY");
	static CivicTypes wage_labor = (CivicTypes)GC.getInfoTypeForString("CIVIC_WAGE_LABOR");
	static CivicTypes caste_system = (CivicTypes)GC.getInfoTypeForString("CIVIC_CASTE_SYSTEM");
	static CivicTypes apprenticeship = (CivicTypes)GC.getInfoTypeForString("CIVIC_APPRENTICESHIP");

	static CivicTypes redistribution = (CivicTypes)GC.getInfoTypeForString("CIVIC_REDISTRIBUTION");
	static CivicTypes isolationism = (CivicTypes)GC.getInfoTypeForString("CIVIC_ISOLATIONISM");
	static CivicTypes trade_economy = (CivicTypes)GC.getInfoTypeForString("CIVIC_TRADE_ECONOMY");
	static CivicTypes temple_economy = (CivicTypes)GC.getInfoTypeForString("CIVIC_TEMPLE_ECONOMY");
	static CivicTypes patronage = (CivicTypes)GC.getInfoTypeForString("CIVIC_PATRONAGE");

	static CivicTypes animism = (CivicTypes)GC.getInfoTypeForString("CIVIC_ANIMISM");
	static CivicTypes deification = (CivicTypes)GC.getInfoTypeForString("CIVIC_DEIFICATION");
	static CivicTypes organized_religion = (CivicTypes)GC.getInfoTypeForString("CIVIC_ORGANIZED_RELIGION");
	static CivicTypes theocracy = (CivicTypes)GC.getInfoTypeForString("CIVIC_THEOCRACY");
	static CivicTypes persecution = (CivicTypes)GC.getInfoTypeForString("CIVIC_PERSECUTION");

	static CivicTypes tribal_warfare = (CivicTypes)GC.getInfoTypeForString("CIVIC_TRIBAL_WARFARE");
	static CivicTypes client_kingdoms = (CivicTypes)GC.getInfoTypeForString("CIVIC_CLIENT_KINGDOMS");
	static CivicTypes resettlement = (CivicTypes)GC.getInfoTypeForString("CIVIC_RESETTLEMENT");
	static CivicTypes occupation = (CivicTypes)GC.getInfoTypeForString("CIVIC_OCCUPATION");
	static CivicTypes colonies = (CivicTypes)GC.getInfoTypeForString("CIVIC_COLONIES");

	/* rfgw 1.8 stability combinations:
			['tribal_federation', 'vassalage', -5],
			['tribal_federation', 'bureaucracy', -10],
			['tribal_federation', 'empire', -15],
			['tribal_federation', 'redistribution', -10],
			['tribal_federation', 'isolationism', 5],
			['tribal_federation', 'animism', 5],
			['monarchy', 'redistribution', 10],
			['oligarchy', 'slavery', 5],
			['oligarchy', 'trade_economy', 10],
			['oligarchy', 'isolationism', -15],
			['oligarchy', 'temple_economy', -10],
			['oligarchy', 'patronage', -5],
			['aristocracy', 'wage_labor', 5],
			['oligarchy', 'redistribution', -15],
			['absolutism', 'slavery', 5],
			['absolutism', 'empire', 10],
			['religious_law', 'animism', -10],
			['religious_law', 'persecution', 5],
			['religious_law', 'deification', -20],
			['temple_economy', 'theocracy', 5],
			['tribal_custom', 'organized_religion', -10],
			['tribal_custom', 'organized_religion', -10],
			['empire', 'occupation', 5],
			['vassalage', 'client_kingdoms', 5]
	 */
	applyStability(playerType, &civicCompatibility, tribal_federation, vassalage, -5);
	applyStability(playerType, &civicCompatibility, tribal_federation, bureaucracy, -10);
	applyStability(playerType, &civicCompatibility, tribal_federation, empire, -15);
	applyStability(playerType, &civicCompatibility, tribal_federation, redistribution, -5);
	applyStability(playerType, &civicCompatibility, tribal_federation, isolationism, 5);
	applyStability(playerType, &civicCompatibility, tribal_federation, animism, 15);
	applyStability(playerType, &civicCompatibility, monarchy, redistribution, 10);
	applyStability(playerType, &civicCompatibility, oligarchy, slavery, 5);
	applyStability(playerType, &civicCompatibility, oligarchy, trade_economy, 10);
	applyStability(playerType, &civicCompatibility, oligarchy, isolationism, -15);
	applyStability(playerType, &civicCompatibility, oligarchy, temple_economy, -10);
	applyStability(playerType, &civicCompatibility, oligarchy, patronage, -5);
	applyStability(playerType, &civicCompatibility, aristocracy, wage_labor, 5);
	applyStability(playerType, &civicCompatibility, oligarchy, redistribution, -15);
	applyStability(playerType, &civicCompatibility, absolutism, slavery, 5);
	applyStability(playerType, &civicCompatibility, absolutism, empire, 15);
	applyStability(playerType, &civicCompatibility, religious_law, animism, -15);
	applyStability(playerType, &civicCompatibility, religious_law, theocracy, 15);
	applyStability(playerType, &civicCompatibility, religious_law, persecution, 15);
	applyStability(playerType, &civicCompatibility, temple_economy, theocracy, 10);
	applyStability(playerType, &civicCompatibility, tribal_custom, organized_religion, -10);
	applyStability(playerType, &civicCompatibility, empire, occupation, 5);
	applyStability(playerType, &civicCompatibility, vassalage, client_kingdoms, 10);

	newCivicsStability += civicCompatibility;

	//Cities
	ReligionTypes stateReligion = player.getStateReligion();
	for(CvCity* loopCity = player.firstCity(&i); loopCity != NULL; loopCity = player.nextCity(&i)) {
		int cityStability = 0;
		if(loopCity->isOccupation() && !_conquestBonus) {
			cityStability -= 3;
		} else {
			cityStability += std::min(2, std::max(-2, loopCity->happyLevel() - loopCity->unhappyLevel()));
		}

		int totalCulture = loopCity->countTotalCultureTimes100();
		int playerCulture = loopCity->getCultureTimes100(playerType);

		if(playerCulture < totalCulture - playerCulture) {
			cityStability -= 2;
		} else if(totalCulture - playerCulture == 0) {
			cityStability += 2;
		}

		if(stateReligion != NO_RELIGION) {
			if(loopCity->isHasReligion(stateReligion)) {
				cityStability += 2;
			} else {
				cityStability -= 1;
			}
		}

		cityStability = std::min(5, cityStability);
		cityStability = std::max(-5, cityStability);
		newCitiesStability += cityStability;
	}

	int force = 0;
	for(CvUnit* loopUnit = player.firstUnit(&i); loopUnit != NULL; loopUnit = player.nextUnit(&i)) {
		force += loopUnit->currHitPoints();
	}

	newCitiesStability += std::max(-1, std::min(1, force - population));

	//Economic
	int commerce = player.calculateTotalYield(YIELD_COMMERCE) - player.calculateInflatedCosts();
	int industry = player.calculateTotalYield(YIELD_PRODUCTION);
	int agriculture = player.calculateTotalYield(YIELD_FOOD);
	int realPopulation = player.getRealPopulation();

	int newGNP = (commerce + 4*industry + 2*agriculture)/7;
	if(game.getGameTurn() > getStartingTurn() + 15) {
		int gnpStability = 0;
		if(newGNP>getGNP()) {
			gnpStability = 3; //growth
		} else if(newGNP<getGNP()) {
			gnpStability = -4; //recession
		} else {
			gnpStability = -2; //stagnation
		}
		permEconomicStability += gnpStability;

		int imports = player.calculateTotalImports(YIELD_COMMERCE);
		int exports = player.calculateTotalExports(YIELD_COMMERCE);
		int importExportStability = std::min(10, (imports + exports) / (2 * eraModifier + 1) - eraModifier);
		newEconomicStability += importExportStability;

		int agricultureStability = std::min(8, std::max(-8, agriculture * 100000 / realPopulation - 8 + (eraModifier - 3) * 2));
		newEconomicStability += agricultureStability;

		int commerceStability = std::min(3, std::max(-3, commerce * 100000 / realPopulation - 5 + (eraModifier - 3) * 2));
		newEconomicStability += commerceStability;

		//GC.logMsg("Civilization %i new economic stability: GNP %i, Imports&Exports %i, Agriculture %i, Commerce %i", getCivilizationType(), gnpStability, importExportStability, agricultureStability, commerceStability);
	}
	setGNP(newGNP);
	if(abs(newEconomicStability)>60) {
		newEconomicStability *= 90;
		newEconomicStability /= 100;
	}

	//Foreign
	if(team.isOpenBordersTrading()) {
		for(i = 0; i < MAX_CIV_PLAYERS; i++) {
			CvPlayerAI& loopPlayer = GET_PLAYER((PlayerTypes)i);
			CvTeam& loopTeam = GET_TEAM(loopPlayer.getTeam());
			if(!loopPlayer.isBarbarian() && !loopPlayer.isMinorCiv() && (PlayerTypes)i!=playerType && loopTeam.isHasMet(player.getTeam()) && !loopPlayer.isMinorCiv() && !loopPlayer.isHuman()) {
				if(loopTeam.isOpenBordersTrading()) {
					if(loopTeam.isOpenBorders(player.getTeam())) {
						newForeignStability += eraModifier*2;
					} else {
						newForeignStability -= eraModifier*2;
					}
				}
				newForeignStability -= team.getWarWeariness(loopPlayer.getTeam()) / 10000;

				if(loopPlayer.getStateReligion() == player.getStateReligion()) {
					newForeignStability += eraModifier;
				} else {
					newForeignStability -= eraModifier;
				}

				switch(loopPlayer.AI_getAttitude(playerType)) {
					case ATTITUDE_FRIENDLY:
						newForeignStability += 5;
						break;
					case ATTITUDE_PLEASED:
						newForeignStability += 2;
						break;
					case ATTITUDE_ANNOYED:
						newForeignStability -= 2;
						break;
					case ATTITUDE_FURIOUS:
						newForeignStability -= 5;
						break;
				}
			}
		}
	}

	//Expansion
	int corePopulation = 0;
	int borderPopulation = 0;
	int peripheryPopulation = 0;

	for(CvCity* loopCity = player.firstCity(&i); loopCity != NULL; loopCity = player.nextCity(&i)) {
		int x = loopCity->getX();
		int y = loopCity->getY();

		if(isInCoreBounds(x, y)) {
			corePopulation += loopCity->getPopulation();
		} else {
			if(isInBorderBounds(x, y)) {
				borderPopulation += loopCity->getPopulation();
			} else {
				peripheryPopulation += loopCity->getPopulation();
			}
		}
	}

	int populationStability = corePopulation * 5 - borderPopulation * 2 - peripheryPopulation * 4;

	populationStability = populationStability*100 / (100 + abs(populationStability));

	newExpansionStability += std::min(5, populationStability);
	newExpansionStability += std::min(5, corePopulation * 5 - getNumPlots());

	//Set new stability
	setTempStability(STABILITY_CITIES, newCitiesStability);
	setTempStability(STABILITY_CIVICS, newCivicsStability);
	setTempStability(STABILITY_ECONOMY, newEconomicStability);
	setTempStability(STABILITY_EXPANSION, newExpansionStability);
	setTempStability(STABILITY_FOREIGN, newForeignStability);

	setPermStability(STABILITY_ECONOMY, permEconomicStability);
}

void CvRFCPlayer::applyStability(PlayerTypes playerType, int* num, CivicTypes civicType1, CivicTypes civicType2, int stability) {
	CivicOptionTypes civicOptionType1 = (CivicOptionTypes)GC.getCivicInfo(civicType1).getCivicOptionType();
	CivicOptionTypes civicOptionType2 = (CivicOptionTypes)GC.getCivicInfo(civicType2).getCivicOptionType();
	CvPlayer& player = GET_PLAYER(playerType);
	if(player.getCivics(civicOptionType1) == civicType1 && player.getCivics(civicOptionType2) == civicType2) {
		*num += stability;
	}
}

void CvRFCPlayer::setCompactEmpireModifier(int modifier) {
	_compactEmpireModifier = modifier;
}

void CvRFCPlayer::setUnitUpkeepModifier(int modifier) {
	_unitUpkeepModifier = modifier;
}

void CvRFCPlayer::setResearchModifier(int modifier) {
	_researchModifier = modifier;
}

void CvRFCPlayer::setDistanceMaintenanceModifier(int modifier) {
	_distanceMaintenanceModifier = modifier;
}

void CvRFCPlayer::setNumCitiesMaintenanceModifier(int modifier) {
	_numCitiesMaintenanceModifier = modifier;
}

void CvRFCPlayer::setUnitProductionModifier(int modifier) {
	_unitProductionModifier = modifier;
}

void CvRFCPlayer::setCivicUpkeepModifier(int modifier) {
	_civicUpkeepModifier = modifier;
}

void CvRFCPlayer::setHealthBonusModifier(int modifier) {
	_healthBonusModifier = modifier;
}

void CvRFCPlayer::setBuildingProductionModifier(int modifier) {
	_buildingProductionModifier = modifier;
}

void CvRFCPlayer::setWonderProductionModifier(int modifier) {
	_wonderProductionModifier = modifier;
}

void CvRFCPlayer::setGreatPeopleModifier(int modifier) {
	_greatPeopleModifier = modifier;
}

void CvRFCPlayer::setInflationModifier(int modifier) {
	_inflationModifier = modifier;
}

void CvRFCPlayer::setGrowthModifier(int modifier) {
	_growthModifier = modifier;
}

void CvRFCPlayer::setNewCityFreePopulation(int population) {
	_newCityFreePopulation = population;
}

void CvRFCPlayer::changeNewCityFreePopulation(int population) {
	_newCityFreePopulation += population;
}

void CvRFCPlayer::removeScheduledUnit(int i) {
	SAFE_DELETE(_scheduledUnits[i]);
	_scheduledUnits.erase(_scheduledUnits.begin() + i);
}

void CvRFCPlayer::removeScheduledCity(int i) {
	SAFE_DELETE(_scheduledCities[i]);
	_scheduledCities.erase(_scheduledCities.begin() + i);
}

void CvRFCPlayer::removeCoreProvince(int i) {
	_coreProvinces.erase(_coreProvinces.begin() + i);
}

void CvRFCPlayer::changeCoreProvince(int i, const char* province) {
	_coreProvinces[i] = province;
}


CivilizationTypes CvRFCPlayer::getCivilizationType() const {
	return _civilizationType;
}

PlayerTypes CvRFCPlayer::getPlayerType() const {
	return _playerType;
}

std::vector<CvRFCUnit*>& CvRFCPlayer::getScheduledUnits() {
	return _scheduledUnits;
}

std::vector<CvRFCCity*>& CvRFCPlayer::getScheduledCities() {
	return _scheduledCities;
}

CvRFCUnit* CvRFCPlayer::addScheduledUnit() {
	CvRFCUnit* rfcUnit = new CvRFCUnit;
	_scheduledUnits.push_back(rfcUnit);
	return rfcUnit;
}

CvRFCUnit* CvRFCPlayer::getScheduledUnit(int i) const {
	return _scheduledUnits[i];
}

CvRFCCity* CvRFCPlayer::addScheduledCity() {
	CvRFCCity* rfcCity = new CvRFCCity;
	_scheduledCities.push_back(rfcCity);
	return rfcCity;
}

CvRFCCity* CvRFCPlayer::getScheduledCity(int i) const {
	return _scheduledCities[i];
}

int CvRFCPlayer::getNumScheduledUnits() const {
	return _scheduledUnits.size();
}

int CvRFCPlayer::getNumScheduledCities() const {
	return _scheduledCities.size();
}

CivicTypes CvRFCPlayer::getStartingCivic(CivicOptionTypes civicOptionType) const {
	return (CivicTypes)_startingCivics[civicOptionType];
}

bool CvRFCPlayer::isEnabled() const {
	return _enabled;
}

int CvRFCPlayer::getStartingPlotX() const {
	return _startingPlotX;
}

int CvRFCPlayer::getStartingPlotY() const {
	return _startingPlotY;
}

int CvRFCPlayer::getStartingYear() const {
	return _startingYear;
}

//WARNING: this is only set after spawning. Use getStartingYear to determine when the player starts.
int CvRFCPlayer::getStartingTurn() const {
	return _startingTurn;
}

int CvRFCPlayer::getStartingGold() const {
	return _startingGold;
}

ReligionTypes CvRFCPlayer::getStartingReligion() const {
	return _startingReligion;
}

bool CvRFCPlayer::isSpawned() const {
	return _spawned;
}

bool CvRFCPlayer::isHuman() const {
	return _human;
}

bool CvRFCPlayer::isMinor() const {
	return _minor;
}

bool CvRFCPlayer::isFlipped() const {
	return _flipped;
}

std::vector<CivilizationTypes>& CvRFCPlayer::getRelatedLanguages() {
	return _relatedLanguages;
}

bool CvRFCPlayer::isStartingTech(TechTypes tech) const {
	FAssert(tech != NO_TECH);
	return _startingTechs[tech];
}

bool CvRFCPlayer::isStartingWar(CivilizationTypes civType) const {
	FAssert(civType != NO_CIVILIZATION);
	return _startingWars[civType];
}

bool CvRFCPlayer::isInCoreBounds(int x, int y) {
	for(uint i = 0; i < _coreProvinces.size(); i++) {
		ProvinceTypes coreProvince = GC.getRiseFall().findRFCProvince(_coreProvinces[i]);
		FAssert(coreProvince != NO_PROVINCE);
		if(GC.getMap().plot(x, y)->getProvinceType() == coreProvince) {
			return true;
		}
	}
	return false;
}

bool CvRFCPlayer::isInBorderBounds(int x, int y) {
	if(GC.getMap().plot(x, y)->getProvinceType() == NO_PROVINCE) {
		return false;
	}
	for(uint i = 0; i < _coreProvinces.size(); ++i) {
		ProvinceTypes provinceType = GC.getRiseFall().findRFCProvince(_coreProvinces[i]);
		if(provinceType == GC.getMap().plot(x, y)->getProvinceType()) {
			continue;
		}
		if(GC.getRiseFall().getProvince(provinceType).isBorderProvince(GC.getMap().plot(x, y)->getProvinceType())) {
			return true;
		}
	}
	return false;
}

int CvRFCPlayer::getFlipCountdown() const {
	return _flipCountdown;
}

int CvRFCPlayer::getTempStability(int category) const {
	return _tempStability[category];
}

int CvRFCPlayer::getPermStability(int category) const {
	return _permStability[category];
}

int CvRFCPlayer::getStability(int category) const {
	return _tempStability[category] + _permStability[category];
}

int CvRFCPlayer::getTotalStability() const {
	int totalStability = 0;
	for(int i = 0; i < NUM_STABILITY_CATEGORIES; i++) {
		totalStability += _tempStability[i];
		totalStability += _permStability[i];
	}
	return totalStability;
}

int CvRFCPlayer::getGNP() const {
	return _GNP;
}

int CvRFCPlayer::getNumCoreProvinces() const {
	return _coreProvinces.size();
}

std::string CvRFCPlayer::getCoreProvince(int i) const {
	return _coreProvinces[i];
}

int CvRFCPlayer::getNumPlots() const {
	return _numPlots;
}

int CvRFCPlayer::getCompactEmpireModifier() const {
	return _compactEmpireModifier;
}

int CvRFCPlayer::getUnitUpkeepModifier() const {
	return _unitUpkeepModifier;
}

int CvRFCPlayer::getResearchModifier() const {
	return _researchModifier;
}

int CvRFCPlayer::getDistanceMaintenanceModifier() const {
	return _distanceMaintenanceModifier;
}

int CvRFCPlayer::getNumCitiesMaintenanceModifier() const {
	return _numCitiesMaintenanceModifier;
}

int CvRFCPlayer::getUnitProductionModifier() const {
	return _unitProductionModifier;
}

int CvRFCPlayer::getCivicUpkeepModifier() const {
	return _civicUpkeepModifier;
}

int CvRFCPlayer::getHealthBonusModifier() const {
	return _healthBonusModifier;
}

int CvRFCPlayer::getBuildingProductionModifier() const {
	return _buildingProductionModifier;
}

int CvRFCPlayer::getWonderProductionModifier() const {
	return _wonderProductionModifier;
}

int CvRFCPlayer::getGreatPeopleModifier() const {
	return _greatPeopleModifier;
}

int CvRFCPlayer::getInflationModifier() const {
	return _inflationModifier;
}

int CvRFCPlayer::getGrowthModifier() const {
	return _growthModifier;
}

bool CvRFCPlayer::isVassalBonus() const {
	return _vassalBonus;
}

bool CvRFCPlayer::isFoundBonus() const {
	return _foundBonus;
}

bool CvRFCPlayer::isConquestBonus() const {
	return _conquestBonus;
}

bool CvRFCPlayer::isCommerceBonus() const {
	return _commerceBonus;
}

bool CvRFCPlayer::isRelatedLanguage(CivilizationTypes civType) {
	for(std::vector<CivilizationTypes>::iterator it = _relatedLanguages.begin(); it != _relatedLanguages.end(); ++it) {
		if(*it == civType) {
			return true;
		}
	}

	for(std::vector<CivilizationTypes>::iterator it = GC.getRiseFall().getRFCPlayer(civType).getRelatedLanguages().begin(); it != GC.getRiseFall().getRFCPlayer(civType).getRelatedLanguages().end(); ++it) {
		if(*it == getCivilizationType()) {
			return true;
		}
	}

	return false;
}

bool CvRFCPlayer::isPlayable() const {
	return _enabled && !_minor;
}

int CvRFCPlayer::getNewCityFreePopulation() const {
	return _newCityFreePopulation;
}


void CvRFCPlayer::read(FDataStreamBase* stream) {
	reset(NO_CIVILIZATION);
	{
		uint size;
		stream->Read(&size);
		for (uint i = 0; i < size; i++)
		{
			CvRFCUnit* scheduledUnit = new CvRFCUnit;
			scheduledUnit->read(stream);
			_scheduledUnits.push_back(scheduledUnit);
		}
	}
	{
		uint size;
		stream->Read(&size);
		for (uint i = 0; i < size; i++)
		{
			CvRFCCity* scheduledCity = new CvRFCCity;
			scheduledCity->read(stream);
			_scheduledCities.push_back(scheduledCity);
		}
	}

	stream->Read((int*)&_civilizationType);
	stream->Read((int*)&_playerType);
	stream->Read(GC.getNumCivicOptionInfos(), _startingCivics);
	stream->Read(GC.getNumCivilizationInfos(), _startingWars);
	stream->Read(GC.getNumTechInfos(), _startingTechs);
	stream->Read(NUM_STABILITY_CATEGORIES, _tempStability);
	stream->Read(NUM_STABILITY_CATEGORIES, _permStability);
	stream->Read(&_startingYear);
	stream->Read(&_startingTurn);
	stream->Read(&_startingPlotX);
	stream->Read(&_startingPlotY);
	stream->Read(&_startingGold);
	stream->Read((int*)&_startingReligion);
	stream->Read(&_enabled);
	stream->Read(&_spawned);
	stream->Read(&_human);
	stream->Read(&_minor);
	stream->Read(&_flipped);
	stream->Read(&_flipCountdown);
	stream->Read(&_GNP);
	stream->Read(&_numPlots);

	stream->Read(&_compactEmpireModifier);
	stream->Read(&_unitUpkeepModifier);
	stream->Read(&_researchModifier);
	stream->Read(&_distanceMaintenanceModifier);
	stream->Read(&_numCitiesMaintenanceModifier);
	stream->Read(&_unitProductionModifier);
	stream->Read(&_civicUpkeepModifier);
	stream->Read(&_healthBonusModifier);
	stream->Read(&_buildingProductionModifier);
	stream->Read(&_wonderProductionModifier);
	stream->Read(&_greatPeopleModifier);
	stream->Read(&_inflationModifier);
	stream->Read(&_growthModifier);

	stream->Read(&_vassalBonus);
	stream->Read(&_foundBonus);
	stream->Read(&_conquestBonus);
	stream->Read(&_commerceBonus);

	stream->Read(&_newCityFreePopulation);

	{
		_coreProvinces.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			CvString coreProvince;
			stream->ReadString(coreProvince);
			_coreProvinces.push_back(coreProvince);
		}
	}

	{
		_relatedLanguages.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int civType;
			stream->Read(&civType);
			_relatedLanguages.push_back((CivilizationTypes)civType);
		}
	}
}

void CvRFCPlayer::write(FDataStreamBase* stream) {
	{
		uint size = _scheduledUnits.size();
		stream->Write(size);
		for(std::vector<CvRFCUnit*>::iterator it = _scheduledUnits.begin(); it != _scheduledUnits.end(); ++it) {
			(*it)->write(stream);
		}
	}
	{
		uint size = _scheduledCities.size();
		stream->Write(size);
		for(std::vector<CvRFCCity*>::iterator it = _scheduledCities.begin(); it != _scheduledCities.end(); ++it) {
			(*it)->write(stream);
		}
	}

	stream->Write(_civilizationType);
	stream->Write(_playerType);
	stream->Write(GC.getNumCivicOptionInfos(), _startingCivics);
	stream->Write(GC.getNumCivilizationInfos(), _startingWars);
	stream->Write(GC.getNumTechInfos(), _startingTechs);
	stream->Write(NUM_STABILITY_CATEGORIES, _tempStability);
	stream->Write(NUM_STABILITY_CATEGORIES, _permStability);
	stream->Write(_startingYear);
	stream->Write(_startingTurn);
	stream->Write(_startingPlotX);
	stream->Write(_startingPlotY);
	stream->Write(_startingGold);
	stream->Write(_startingReligion);
	stream->Write(_enabled);
	stream->Write(_spawned);
	stream->Write(_human);
	stream->Write(_minor);
	stream->Write(_flipped);
	stream->Write(_flipCountdown);
	stream->Write(_GNP);
	stream->Write(_numPlots);

	stream->Write(_compactEmpireModifier);
	stream->Write(_unitUpkeepModifier);
	stream->Write(_researchModifier);
	stream->Write(_distanceMaintenanceModifier);
	stream->Write(_numCitiesMaintenanceModifier);
	stream->Write(_unitProductionModifier);
	stream->Write(_civicUpkeepModifier);
	stream->Write(_healthBonusModifier);
	stream->Write(_buildingProductionModifier);
	stream->Write(_wonderProductionModifier);
	stream->Write(_greatPeopleModifier);
	stream->Write(_inflationModifier);
	stream->Write(_growthModifier);

	stream->Write(_vassalBonus);
	stream->Write(_foundBonus);
	stream->Write(_conquestBonus);
	stream->Write(_commerceBonus);

	stream->Write(_newCityFreePopulation);

	{
		uint size = _coreProvinces.size();
		stream->Write(size);
		for(std::vector<CvString>::iterator it = _coreProvinces.begin(); it != _coreProvinces.end(); ++it) {
			stream->WriteString(*it);
		}
	}

	{
		uint size = _relatedLanguages.size();
		stream->Write(size);
		for(std::vector<CivilizationTypes>::iterator it = _relatedLanguages.begin(); it != _relatedLanguages.end(); ++it) {
			stream->Write(*it);
		}
	}
}
