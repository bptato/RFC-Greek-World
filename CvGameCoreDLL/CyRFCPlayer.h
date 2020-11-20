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
		void addStartingTech(int techType);
		void addStartingWar(int civType);
		void addRelatedLanguage(int civType);
		void setStartingPlot(int x, int y);
		void setStartingGold(int gold);
		void addCoreProvince(std::wstring provinceName);
		void setEnabled(bool newEnabled);
		void setMinorCiv(bool minor);

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

		int getStability(int category);
		int getTotalStability();
		int getStartingYear();
		bool isEnabled();
		int getStartingCivic(int civicOptionType);
		int getStartingGold();
		bool isStartingTech(int tech);
		bool isStartingWar(int civType);
		bool isRelatedLanguage(int civType);
		int getStartingPlotX();
		int getStartingPlotY();
		bool isMinor();
		bool isSpawned();

		int getNumScheduledUnits();
		CyRFCUnit* addScheduledUnit();
		CyRFCUnit* getScheduledUnit(int i);
		int getNumScheduledCities();
		CyRFCCity* addScheduledCity();
		CyRFCCity* getScheduledCity(int i);
		int getNumCoreProvinces();
		std::wstring getCoreProvince(int i);

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
