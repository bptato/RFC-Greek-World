/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCPlayer.h"

CvRFCPlayer::CvRFCPlayer() {
	startingCivics = new int[GC.getNumCivicOptionInfos()];
}

CvRFCPlayer::~CvRFCPlayer() {
	SAFE_DELETE_ARRAY(startingCivics);
	uninit();
}

void CvRFCPlayer::reset(CivilizationTypes newCivType) {
	uninit();
	civilizationType = newCivType;
	startingYear = 0;
	startingTurn = -1;
	startingPlotX = 0;
	startingPlotY = 0;
	startingGold = 0;
	flipCountdown = 0;
	GNP = 0;
	numPlots = 0;

	//modifiers (following values are BTS defaults, though some of them replace handicap values)
	compactEmpireModifier = 50;
	unitUpkeepModifier = 100;
	researchModifier = 100;
	distanceMaintenanceModifier = 100;
	numCitiesMaintenanceModifier = 100;
	unitProductionModifier = 100;
	civicUpkeepModifier = 100;
	healthBonusModifier = 0;
	buildingProductionModifier = 100;
	wonderProductionModifier = 100;
	greatPeopleModifier = 100;
	inflationModifier = 100;
	growthModifier = 100;

	enabled = false;
	spawned = false;
	minor = false;
	human = false;
	flipped = false;

	vassalBonus = false;
	foundBonus = false;
	conquestBonus = false;
	commerceBonus = false;

	newCityFreePopulation = 0;

	for(int i = 0; i < GC.getNumCivicOptionInfos(); i++) {
		startingCivics[i] = NO_CIVIC;
	}

	for(int i = 0; i < NUM_STABILITY_CATEGORIES; i++) {
		tempStability[i] = 0;
		permStability[i] = 0;
	}

	startingTechs.clear();
	coreProvinces.clear();
	startingWars.clear();
	relatedLanguages.clear();
}

void CvRFCPlayer::uninit() {
	for(std::vector<CvRFCUnit*>::iterator it = scheduledUnits.begin(); it != scheduledUnits.end(); ++it) {
		SAFE_DELETE(*it);
	}
	scheduledUnits.clear();
	for(std::vector<CvRFCCity*>::iterator it = scheduledCities.begin(); it != scheduledCities.end(); ++it) {
		SAFE_DELETE(*it);
	}
	scheduledCities.clear();
}

void CvRFCPlayer::setCivilizationType(CivilizationTypes newCivType) {
	civilizationType = newCivType;
}

void CvRFCPlayer::setEnabled(bool newEnabled) {
	enabled = newEnabled;
}

void CvRFCPlayer::setStartingCivic(CivicOptionTypes civicOptionType, CivicTypes civicType) {
	startingCivics[civicOptionType] = civicType;
}

void CvRFCPlayer::setStartingYear(int year) {
	startingYear = year;
}

void CvRFCPlayer::setStartingTurn(int turn) {
	startingTurn = turn;
}

void CvRFCPlayer::setStartingPlotX(int x) {
	startingPlotX = x;
}

void CvRFCPlayer::setStartingPlotY(int y) {
	startingPlotY = y;
}

void CvRFCPlayer::setStartingGold(int gold) {
	startingGold = gold;
}

void CvRFCPlayer::setMinorCiv(bool newMinor) {
	minor = newMinor;
}

void CvRFCPlayer::setHuman(bool newHuman) {
	human = newHuman;
}

void CvRFCPlayer::setSpawned(bool newSpawned) {
	spawned = newSpawned;
}

void CvRFCPlayer::setFlipped(bool newFlipped) {
	flipped = newFlipped;
}

void CvRFCPlayer::addStartingTech(TechTypes tech) {
	if(tech != NO_TECH) {
		startingTechs.push_back(tech);
	}
}

void CvRFCPlayer::addCoreProvince(const wchar* newProvince) {
	coreProvinces.push_back(newProvince);
}

void CvRFCPlayer::setFlipCountdown(int newFlipCountdown) {
	flipCountdown = newFlipCountdown;
}

void CvRFCPlayer::setTempStability(int category, int newStability) {
	tempStability[category] = newStability;
}

void CvRFCPlayer::setPermStability(int category, int newStability) {
	permStability[category] = newStability;
}

void CvRFCPlayer::setGNP(int newGNP) {
	GNP = newGNP;
}

void CvRFCPlayer::addStartingWar(CivilizationTypes civType) {
	if(civType != NO_CIVILIZATION) {
		startingWars.push_back(civType);
	}
}

void CvRFCPlayer::addRelatedLanguage(CivilizationTypes civType) {
	relatedLanguages.push_back(civType);
}

void CvRFCPlayer::setNumPlots(int newNumPlots) {
	numPlots = newNumPlots;
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
	vassalBonus = false;
	foundBonus = false;
	conquestBonus = false;
	commerceBonus = false;
	for(i = 0; i<GC.getNumCivicOptionInfos(); ++i) {
		CvCivicInfo& civicInfo = GC.getCivicInfo(player.getCivics((CivicOptionTypes)i));
		if(civicInfo.isStabilityVassalBonus()) {
			vassalBonus = true;
		}
		if(civicInfo.isStabilityFoundBonus()) {
			foundBonus = true;
		}
		if(civicInfo.isStabilityConquestBonus()) {
			conquestBonus = true;
		}
		if(civicInfo.isStabilityCommerceBonus()) {
			commerceBonus = true;
		}
	}

	if(vassalBonus) {
		for(i = 0; i<MAX_TEAMS; ++i) {
			if(GET_TEAM((TeamTypes)i).isVassal(player.getTeam())) {
				newCivicsStability += 2;
			}
		}
	}

	if(commerceBonus) {
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
		if(loopCity->isOccupation() && !conquestBonus) {
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
		for(i = 0; i<MAX_CIV_PLAYERS; i++) {
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
						newForeignStability += 8;
						break;
					case ATTITUDE_PLEASED:
						newForeignStability += 4;
						break;
					case ATTITUDE_ANNOYED:
						newForeignStability -= 4;
						break;
					case ATTITUDE_FURIOUS:
						newForeignStability -= 8;
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
	compactEmpireModifier = modifier;
}

void CvRFCPlayer::setUnitUpkeepModifier(int modifier) {
	unitUpkeepModifier = modifier;
}

void CvRFCPlayer::setResearchModifier(int modifier) {
	researchModifier = modifier;
}

void CvRFCPlayer::setDistanceMaintenanceModifier(int modifier) {
	distanceMaintenanceModifier = modifier;
}

void CvRFCPlayer::setNumCitiesMaintenanceModifier(int modifier) {
	numCitiesMaintenanceModifier = modifier;
}

void CvRFCPlayer::setUnitProductionModifier(int modifier) {
	unitProductionModifier = modifier;
}

void CvRFCPlayer::setCivicUpkeepModifier(int modifier) {
	civicUpkeepModifier = modifier;
}

void CvRFCPlayer::setHealthBonusModifier(int modifier) {
	healthBonusModifier = modifier;
}

void CvRFCPlayer::setBuildingProductionModifier(int modifier) {
	buildingProductionModifier = modifier;
}

void CvRFCPlayer::setWonderProductionModifier(int modifier) {
	wonderProductionModifier = modifier;
}

void CvRFCPlayer::setGreatPeopleModifier(int modifier) {
	greatPeopleModifier = modifier;
}

void CvRFCPlayer::setInflationModifier(int modifier) {
	inflationModifier = modifier;
}

void CvRFCPlayer::setGrowthModifier(int modifier) {
	growthModifier = modifier;
}

void CvRFCPlayer::setNewCityFreePopulation(int population) {
	newCityFreePopulation = population;
}

void CvRFCPlayer::changeNewCityFreePopulation(int population) {
	newCityFreePopulation += population;
}


CivilizationTypes CvRFCPlayer::getCivilizationType() {
	return civilizationType;
}

std::vector<CvRFCUnit*>& CvRFCPlayer::getScheduledUnits() {
	return scheduledUnits;
}

std::vector<CvRFCCity*>& CvRFCPlayer::getScheduledCities() {
	return scheduledCities;
}

CvRFCUnit* CvRFCPlayer::addScheduledUnit() {
	CvRFCUnit* rfcUnit = new CvRFCUnit();
	scheduledUnits.push_back(rfcUnit);
	return rfcUnit;
}

CvRFCUnit* CvRFCPlayer::getScheduledUnit(int i) const {
	return scheduledUnits[i];
}

CvRFCCity* CvRFCPlayer::addScheduledCity() {
	CvRFCCity* rfcCity = new CvRFCCity();
	scheduledCities.push_back(rfcCity);
	return rfcCity;
}

CvRFCCity* CvRFCPlayer::getScheduledCity(int i) const {
	return scheduledCities[i];
}

int CvRFCPlayer::getNumScheduledUnits() const {
	return scheduledUnits.size();
}

int CvRFCPlayer::getNumScheduledCities() const {
	return scheduledCities.size();
}

CivicTypes CvRFCPlayer::getStartingCivic(CivicOptionTypes civicOptionType) const {
	return (CivicTypes)startingCivics[civicOptionType];
}

bool CvRFCPlayer::isEnabled() const {
	return enabled;
}

int CvRFCPlayer::getStartingPlotX() const {
	return startingPlotX;
}

int CvRFCPlayer::getStartingPlotY() const {
	return startingPlotY;
}

int CvRFCPlayer::getStartingYear() const {
	return startingYear;
}

//WARNING: this is only set after spawning. Use getStartingYear to determine when the player starts.
int CvRFCPlayer::getStartingTurn() const {
	return startingTurn;
}

int CvRFCPlayer::getStartingGold() const {
	return startingGold;
}

bool CvRFCPlayer::isSpawned() const {
	return spawned;
}

bool CvRFCPlayer::isHuman() const {
	return human;
}

bool CvRFCPlayer::isMinor() const {
	return minor;
}

bool CvRFCPlayer::isFlipped() const {
	return flipped;
}

std::vector<TechTypes>& CvRFCPlayer::getStartingTechs() {
	return startingTechs;
}

std::vector<CivilizationTypes>& CvRFCPlayer::getStartingWars() {
	return startingWars;
}

std::vector<CivilizationTypes>& CvRFCPlayer::getRelatedLanguages() {
	return relatedLanguages;
}

bool CvRFCPlayer::isStartingTech(TechTypes tech) const {
	if(std::find(startingTechs.begin(), startingTechs.end(), tech) != startingTechs.end()) {
		return true;
	}
	return false;
}

bool CvRFCPlayer::isStartingWar(CivilizationTypes civType) const {
	if(std::find(startingWars.begin(), startingWars.end(), civType) != startingWars.end()) {
		return true;
	}
	return false;
}

bool CvRFCPlayer::isInCoreBounds(int x, int y) {
	for(uint i = 0; i<coreProvinces.size(); i++) {
		CvRFCProvince* coreProvince = GC.getRiseFall().getRFCProvince(coreProvinces[i]);
		FAssert(coreProvince != NULL);
		if(coreProvince->isInBounds(x, y)) {
			return true;
		}
	}
	return false;
}

bool CvRFCPlayer::isInBorderBounds(int x, int y) {
	CvRFCProvince* borderProvince = GC.getRiseFall().getProvinceForPlot(x, y);
	if(borderProvince == NULL) {
		return false;
	}
	for(uint i = 0; i<coreProvinces.size(); i++) {
		CvRFCProvince* coreProvince = GC.getRiseFall().getRFCProvince(coreProvinces[i]);
		if(coreProvince->isBorderProvince(borderProvince)) {
			return true;
		}
	}
	return false;
}

int CvRFCPlayer::getFlipCountdown() const {
	return flipCountdown;
}

int CvRFCPlayer::getTempStability(int category) const {
	return tempStability[category];
}

int CvRFCPlayer::getPermStability(int category) const {
	return permStability[category];
}

int CvRFCPlayer::getStability(int category) const {
	return tempStability[category] + permStability[category];
}

int CvRFCPlayer::getTotalStability() const {
	int totalStability = 0;
	for(int i = 0; i < NUM_STABILITY_CATEGORIES; i++) {
		totalStability += tempStability[i];
		totalStability += permStability[i];
	}
	return totalStability;
}

int CvRFCPlayer::getGNP() const {
	return GNP;
}

int CvRFCPlayer::getNumCoreProvinces() const {
	return coreProvinces.size();
}

std::wstring CvRFCPlayer::getCoreProvince(int i) const {
	return coreProvinces[i];
}

int CvRFCPlayer::getNumPlots() const {
	return numPlots;
}

int CvRFCPlayer::getCompactEmpireModifier() const {
	return compactEmpireModifier;
}

int CvRFCPlayer::getUnitUpkeepModifier() const {
	return unitUpkeepModifier;
}

int CvRFCPlayer::getResearchModifier() const {
	return researchModifier;
}

int CvRFCPlayer::getDistanceMaintenanceModifier() const {
	return distanceMaintenanceModifier;
}

int CvRFCPlayer::getNumCitiesMaintenanceModifier() const {
	return numCitiesMaintenanceModifier;
}

int CvRFCPlayer::getUnitProductionModifier() const {
	return unitProductionModifier;
}

int CvRFCPlayer::getCivicUpkeepModifier() const {
	return civicUpkeepModifier;
}

int CvRFCPlayer::getHealthBonusModifier() const {
	return healthBonusModifier;
}

int CvRFCPlayer::getBuildingProductionModifier() const {
	return buildingProductionModifier;
}

int CvRFCPlayer::getWonderProductionModifier() const {
	return wonderProductionModifier;
}

int CvRFCPlayer::getGreatPeopleModifier() const {
	return greatPeopleModifier;
}

int CvRFCPlayer::getInflationModifier() const {
	return inflationModifier;
}

int CvRFCPlayer::getGrowthModifier() const {
	return growthModifier;
}

bool CvRFCPlayer::isVassalBonus() const {
	return vassalBonus;
}

bool CvRFCPlayer::isFoundBonus() const {
	return foundBonus;
}

bool CvRFCPlayer::isConquestBonus() const {
	return conquestBonus;
}

bool CvRFCPlayer::isCommerceBonus() const {
	return commerceBonus;
}

bool CvRFCPlayer::isRelatedLanguage(CivilizationTypes civType) {
	for(std::vector<CivilizationTypes>::iterator it = relatedLanguages.begin(); it != relatedLanguages.end(); ++it) {
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

int CvRFCPlayer::getNewCityFreePopulation() const {
	return newCityFreePopulation;
}


void CvRFCPlayer::read(FDataStreamBase* stream) {
	{
		scheduledUnits.clear();
		uint size;
		stream->Read(&size);
		for (uint i = 0; i < size; i++)
		{
			CvRFCUnit* scheduledUnit = new CvRFCUnit();
			scheduledUnit->read(stream);
			scheduledUnits.push_back(scheduledUnit);
		}
	}
	{
		scheduledCities.clear();
		uint size;
		stream->Read(&size);
		for (uint i = 0; i < size; i++)
		{
			CvRFCCity* scheduledCity = new CvRFCCity();
			scheduledCity->read(stream);
			scheduledCities.push_back(scheduledCity);
		}
	}

	stream->Read((int*)&civilizationType);
	stream->Read(GC.getNumCivicOptionInfos(), startingCivics);
	stream->Read(NUM_STABILITY_CATEGORIES, tempStability);
	stream->Read(NUM_STABILITY_CATEGORIES, permStability);
	stream->Read(&startingYear);
	stream->Read(&startingTurn);
	stream->Read(&startingPlotX);
	stream->Read(&startingPlotY);
	stream->Read(&startingGold);
	stream->Read(&enabled);
	stream->Read(&spawned);
	stream->Read(&human);
	stream->Read(&minor);
	stream->Read(&flipped);
	stream->Read(&flipCountdown);
	stream->Read(&GNP);
	stream->Read(&numPlots);

	stream->Read(&compactEmpireModifier);
	stream->Read(&unitUpkeepModifier);
	stream->Read(&researchModifier);
	stream->Read(&distanceMaintenanceModifier);
	stream->Read(&numCitiesMaintenanceModifier);
	stream->Read(&unitProductionModifier);
	stream->Read(&civicUpkeepModifier);
	stream->Read(&healthBonusModifier);
	stream->Read(&buildingProductionModifier);
	stream->Read(&wonderProductionModifier);
	stream->Read(&greatPeopleModifier);
	stream->Read(&inflationModifier);
	stream->Read(&growthModifier);

	stream->Read(&vassalBonus);
	stream->Read(&foundBonus);
	stream->Read(&conquestBonus);
	stream->Read(&commerceBonus);

	stream->Read(&newCityFreePopulation);

	{
		startingTechs.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int techID;
			stream->Read(&techID);
			startingTechs.push_back((TechTypes)techID);
		}
	}

	{
		coreProvinces.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			CvWString coreProvince;
			stream->ReadString(coreProvince);
			coreProvinces.push_back(coreProvince);
		}
	}

	{
		startingWars.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int civType;
			stream->Read(&civType);
			startingWars.push_back((CivilizationTypes)civType);
		}
	}

	{
		relatedLanguages.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int civType;
			stream->Read(&civType);
			relatedLanguages.push_back((CivilizationTypes)civType);
		}
	}
}

void CvRFCPlayer::write(FDataStreamBase* stream) {
	{
		uint size = scheduledUnits.size();
		stream->Write(size);
		for(std::vector<CvRFCUnit*>::iterator it = scheduledUnits.begin(); it != scheduledUnits.end(); ++it) {
			(*it)->write(stream);
		}
	}
	{
		uint size = scheduledCities.size();
		stream->Write(size);
		for(std::vector<CvRFCCity*>::iterator it = scheduledCities.begin(); it != scheduledCities.end(); ++it) {
			(*it)->write(stream);
		}
	}

	stream->Write(civilizationType);
	stream->Write(GC.getNumCivicOptionInfos(), startingCivics);
	stream->Write(NUM_STABILITY_CATEGORIES, tempStability);
	stream->Write(NUM_STABILITY_CATEGORIES, permStability);
	stream->Write(startingYear);
	stream->Write(startingTurn);
	stream->Write(startingPlotX);
	stream->Write(startingPlotY);
	stream->Write(startingGold);
	stream->Write(enabled);
	stream->Write(spawned);
	stream->Write(human);
	stream->Write(minor);
	stream->Write(flipped);
	stream->Write(flipCountdown);
	stream->Write(GNP);
	stream->Write(numPlots);

	stream->Write(compactEmpireModifier);
	stream->Write(unitUpkeepModifier);
	stream->Write(researchModifier);
	stream->Write(distanceMaintenanceModifier);
	stream->Write(numCitiesMaintenanceModifier);
	stream->Write(unitProductionModifier);
	stream->Write(civicUpkeepModifier);
	stream->Write(healthBonusModifier);
	stream->Write(buildingProductionModifier);
	stream->Write(wonderProductionModifier);
	stream->Write(greatPeopleModifier);
	stream->Write(inflationModifier);
	stream->Write(growthModifier);

	stream->Write(vassalBonus);
	stream->Write(foundBonus);
	stream->Write(conquestBonus);
	stream->Write(commerceBonus);

	stream->Write(newCityFreePopulation);

	{
		uint size = startingTechs.size();
		stream->Write(size);
		for(std::vector<TechTypes>::iterator it = startingTechs.begin(); it != startingTechs.end(); ++it) {
			stream->Write(*it);
		}
	}

	{
		uint size = coreProvinces.size();
		stream->Write(size);
		for(std::vector<CvWString>::iterator it = coreProvinces.begin(); it != coreProvinces.end(); ++it) {
			stream->WriteString(*it);
		}
	}

	{
		uint size = startingWars.size();
		stream->Write(size);
		for(std::vector<CivilizationTypes>::iterator it = startingWars.begin(); it != startingWars.end(); ++it) {
			stream->Write(*it);
		}
	}

	{
		uint size = relatedLanguages.size();
		stream->Write(size);
		for(std::vector<CivilizationTypes>::iterator it = relatedLanguages.begin(); it != relatedLanguages.end(); ++it) {
			stream->Write(*it);
		}
	}
}
