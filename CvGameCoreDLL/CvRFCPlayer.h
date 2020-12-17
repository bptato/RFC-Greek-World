#pragma once
/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"

#define NUM_STABILITY_CATEGORIES 5
#define STABILITY_CITIES 0
#define STABILITY_CIVICS 1
#define STABILITY_ECONOMY 2
#define STABILITY_EXPANSION 3
#define STABILITY_FOREIGN 4

class CvRFCPlayer {
	public:
		CvRFCPlayer();
		~CvRFCPlayer();
		void reset(CivilizationTypes civilizationType);
		void init(CivilizationTypes civilizationType);
		void uninit();

		void setCivilizationType(CivilizationTypes civilizationType);
		void setPlayerType(PlayerTypes playerType);
		void setEnabled(bool newEnabled);
		void setStartingCivic(CivicOptionTypes civicOptionType, CivicTypes civicType);
		void setStartingYear(int year);
		void setStartingTurn(int turn);
		void setStartingPlotX(int x);
		void setStartingPlotY(int y);
		void setStartingGold(int gold);
		void setStartingReligion(ReligionTypes startingReligion);
		void setMinorCiv(bool minor);
		void setHuman(bool human);
		void setSpawned(bool spawned);
		void setFlipped(bool flipped);
		void setStartingTech(TechTypes tech, bool val);
		void setStartingWar(CivilizationTypes civType, bool startingWar);
		void addCoreProvince(ProvinceTypes provinceType);
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

		void removeScheduledUnit(int i);
		void removeScheduledCity(int i);
		void removeCoreProvince(int i);
		void changeCoreProvince(int i, ProvinceTypes provinceType);

		CivilizationTypes getCivilizationType() const;
		PlayerTypes getPlayerType() const;
		std::vector<CvRFCUnit*>& getScheduledUnits();
		std::vector<CvRFCCity*>& getScheduledCities();
		CvRFCUnit* addScheduledUnit();
		CvRFCUnit* getScheduledUnit(int i) const;
		CvRFCCity* addScheduledCity();
		CvRFCCity* getScheduledCity(int i) const;
		int getNumScheduledUnits() const;
		int getNumScheduledCities() const;
		std::vector<CivilizationTypes>& getRelatedLanguages();
		bool isEnabled() const;
		int getStartingPlotX() const;
		int getStartingPlotY() const;
		inline CvPlot* getStartingPlot() const {
			return GC.getMapINLINE().plotINLINE(_startingPlotX, _startingPlotY);
		};
		CivicTypes getStartingCivic(CivicOptionTypes civicOptionType) const;
		int getStartingYear() const;
		int getStartingTurn() const;
		int getStartingGold() const;
		ReligionTypes getStartingReligion() const;
		bool isSpawned() const;
		bool isHuman() const;
		bool isMinor() const;
		bool isFlipped() const;
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
		ProvinceTypes getCoreProvince(int i) const;
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

		bool isPlayable() const;

		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);

	protected:
		void applyStability(PlayerTypes playerType, int* num, CivicTypes civicType1, CivicTypes civicType2, int stability);

		CivilizationTypes _civilizationType;
		PlayerTypes _playerType;
		std::vector<CvRFCUnit*> _scheduledUnits;
		std::vector<CvRFCCity*> _scheduledCities;
		int* _startingCivics;
		bool* _startingWars;
		bool* _startingTechs;
		int _startingYear;
		int _startingTurn;
		int _startingPlotX;
		int _startingPlotY;
		int _startingGold;
		ReligionTypes _startingReligion;
		bool _enabled;
		bool _spawned;
		bool _human;
		bool _minor;
		bool _flipped;
		std::vector<ProvinceTypes> _coreProvinces;
		int _tempStability[NUM_STABILITY_CATEGORIES];
		int _permStability[NUM_STABILITY_CATEGORIES];
		int _flipCountdown;
		int _GNP;
		int _numPlots;
		std::vector<CivilizationTypes> _relatedLanguages; //TODO this should be in XML

		//modifiers
		int _compactEmpireModifier;
		int _unitUpkeepModifier;
		int _researchModifier;
		int _distanceMaintenanceModifier;
		int _numCitiesMaintenanceModifier;
		int _unitProductionModifier;
		int _civicUpkeepModifier;
		int _healthBonusModifier;
		int _buildingProductionModifier;
		int _wonderProductionModifier;
		int _greatPeopleModifier;
		int _inflationModifier;
		int _growthModifier;

		//civic stability
		bool _vassalBonus;
		bool _foundBonus;
		bool _conquestBonus;
		bool _commerceBonus;

		//misc
		int _newCityFreePopulation;
};
