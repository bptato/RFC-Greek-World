#pragma once
/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"

#define STABILITY_CATEGORIES 5 //cities (0), civics (1), economic (2), expansion (3), foreign (4)

class CvRFCPlayer {
	public:
		CvRFCPlayer();
		~CvRFCPlayer();
		void reset(CivilizationTypes newCivType);

		void setCivilizationType(CivilizationTypes newCivType);
		void scheduleUnit(CvRFCUnit rfcUnit);
		void setEnabled(bool newEnabled);
		void setStartingCivic(CivicOptionTypes civicOptionType, CivicTypes civicType);
		void setStartingYear(int year);
		void setStartingTurn(int turn);
		void setStartingPlotX(int x);
		void setStartingPlotY(int y);
		void setStartingGold(int gold);
		void setMinorCiv(bool newMinor);
		void setHuman(bool newHuman);
		void setSpawned(bool newSpawned);
		void addStartingTech(TechTypes tech);
		void addStartingWar(CivilizationTypes civType);
		void addCoreProvince(const wchar* province);
		void setFlipCountdown(int newFlipCountdown);
		void setTempStability(int category, int newStability);
		void setPermStability(int category, int newStability);
		void setGNP(int newGNP);
		void checkStability(PlayerTypes playerType);
		void setNumPlots(int numPlots);
		void addRelatedLanguage(CivilizationTypes civType);

		void setCompactEmpireModifier(int modifier);
		void setUnitUpkeepModifier(int modifier);
		void setResearchModifier(int modifier);
		void setDistanceMaintenanceModifier(int modifier);
		void setNumCitiesMaintenanceModifier(int modifier);
		void setUnitProductionModifier(int modifier);
		void setCivicUpkeepModifier(int modifier);
		void setHealthBonusModifier(int modifier);
		void setBuildingProductionModifier(int modifier);
		void setWonderProductionModifier(int modifier);
		void setGreatPeopleModifier(int modifier);
		void setInflationModifier(int modifier);
		void setGrowthModifier(int modifier);

		void setNewCityFreePopulation(int population);
		void changeNewCityFreePopulation(int population);

		CivilizationTypes getCivilizationType();
		std::vector<CvRFCUnit>& getScheduledUnits();
		std::vector<CvRFCCity*>& getScheduledCities();
		CvRFCUnit& getScheduledUnit(int i);
		CvRFCCity* getScheduledCity(int i);
		int getNumScheduledUnits() const;
		int getNumScheduledCities() const;
		std::vector<CivilizationTypes>& getRelatedLanguages();
		bool isEnabled() const;
		int getStartingPlotX() const;
		int getStartingPlotY() const;
		CivicTypes getStartingCivic(CivicOptionTypes civicOptionType) const;
		int getStartingYear() const;
		int getStartingTurn() const;
		int getStartingGold() const;
		bool isSpawned() const;
		bool isHuman() const;
		bool isMinor() const;
		std::vector<TechTypes>& getStartingTechs();
		std::vector<CivilizationTypes>& getStartingWars();
		bool isInCoreBounds(int x, int y);
		bool isInBorderBounds(int x, int y);
		int getFlipCountdown() const;
		int getTempStability(int category) const;
		int getPermStability(int category) const;
		int getStability(int category) const;
		int getTotalStability() const;
		int getGNP() const;
		bool isStartingTech(TechTypes tech) const;
		bool isStartingWar(CivilizationTypes civType) const;
		int getNumCoreProvinces() const;
		std::wstring getCoreProvince(int i) const;
		int getNumPlots() const;
		bool isRelatedLanguage(CivilizationTypes civType);

		int getCompactEmpireModifier() const;
		int getUnitUpkeepModifier() const;
		int getResearchModifier() const;
		int getDistanceMaintenanceModifier() const;
		int getNumCitiesMaintenanceModifier() const;
		int getUnitProductionModifier() const;
		int getCivicUpkeepModifier() const;
		int getHealthBonusModifier() const;
		int getBuildingProductionModifier() const;
		int getWonderProductionModifier() const;
		int getGreatPeopleModifier() const;
		int getInflationModifier() const;
		int getGrowthModifier() const;

		bool isVassalBonus() const;
		bool isFoundBonus() const;
		bool isConquestBonus() const;
		bool isCommerceBonus() const;

		int getNewCityFreePopulation() const;

		CvRFCCity* addScheduledCity();

		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);

	protected:
		void applyStability(PlayerTypes playerType, int* num, CivicTypes civicType1, CivicTypes civicType2, int stability);

		CivilizationTypes civilizationType;
		std::vector<CvRFCUnit> scheduledUnits;
		std::vector<CvRFCCity*> scheduledCities;
		int* startingCivics;
		int startingYear;
		int startingTurn;
		int startingPlotX;
		int startingPlotY;
		int startingGold;
		bool enabled;
		bool spawned;
		bool human;
		bool minor;
		std::vector<CvWString> coreProvinces;
		std::vector<TechTypes> startingTechs;
		std::vector<CivilizationTypes> startingWars;
		int tempStability[STABILITY_CATEGORIES];
		int permStability[STABILITY_CATEGORIES];
		int flipCountdown;
		int GNP;
		int numPlots;
		std::vector<CivilizationTypes> relatedLanguages;

		//modifiers
		int compactEmpireModifier;
		int unitUpkeepModifier;
		int researchModifier;
		int distanceMaintenanceModifier;
		int numCitiesMaintenanceModifier;
		int unitProductionModifier;
		int civicUpkeepModifier;
		int healthBonusModifier;
		int buildingProductionModifier;
		int wonderProductionModifier;
		int greatPeopleModifier;
		int inflationModifier;
		int growthModifier;

		//civic stability
		bool vassalBonus;
		bool foundBonus;
		bool conquestBonus;
		bool commerceBonus;

		//misc
		int newCityFreePopulation;
};
