#pragma once
/*
Author: bluepotato
*/
class CvRFCPlayer;
class CyRFCUnit;
class CyRFCCity;

class CyRFCPlayer {
	public:
		CyRFCPlayer();
		CyRFCPlayer(CvRFCPlayer* rfcPlayerConst);

		void setStartingYear(int newStartingYear);
		void setStartingCivic(int civicOptionType, int civicType);
		void setStartingTech(int techType, bool value);
		void setStartingWar(int civType, bool startingWar);
		void addRelatedLanguage(int civType);
		void setStartingPlot(int x, int y);
		void setStartingGold(int gold);
		void setStartingReligion(int religion);
		void addCoreProvince(int provinceType);
		void setEnabled(bool newEnabled);
		void setMinorCiv(bool minor);
		void setFlipped(bool flipped);

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
		void removeScheduledUnit(int i);
		void removeScheduledCity(int i);
		void removeCoreProvince(int i);

		int getPlayerType();
		int getStability(int category);
		int getTotalStability();
		int getStartingYear();
		bool isEnabled();
		int getStartingCivic(int civicOptionType);
		int getStartingGold();
		int getStartingReligion();
		bool isStartingTech(int tech);
		bool isStartingWar(int civType);
		bool isRelatedLanguage(int civType);
		int getStartingPlotX();
		int getStartingPlotY();
		bool isMinor();
		bool isSpawned();
		bool isFlipped();

		int getNumScheduledUnits();
		CyRFCUnit* addScheduledUnit();
		CyRFCUnit* getScheduledUnit(int i);
		int getNumScheduledCities();
		CyRFCCity* addScheduledCity();
		CyRFCCity* getScheduledCity(int i);
		int getNumCoreProvinces();
		ProvinceTypes getCoreProvince(int i);

		int getCompactEmpireModifier();
		int getUnitUpkeepModifier();
		int getResearchModifier();
		int getDistanceMaintenanceModifier();
		int getNumCitiesMaintenanceModifier();
		int getUnitProductionModifier();
		int getCivicUpkeepModifier();
		int getHealthBonusModifier();
		int getBuildingProductionModifier();
		int getWonderProductionModifier();
		int getGreatPeopleModifier();
		int getInflationModifier();
		int getGrowthModifier();

	protected:
		CvRFCPlayer* rfcPlayer;
};
