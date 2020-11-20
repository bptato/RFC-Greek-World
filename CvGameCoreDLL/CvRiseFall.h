#pragma once
/*
Author: bluepotato
*/
#include "CvGame.h"
#include "CvRFCPlayer.h"
#include "CvRFCProvince.h"
#include "CvRFCUnit.h"
#include "CvRFCCity.h"
#include "CvRFCMercenary.h"

class CvRiseFall {
	public:
		CvRiseFall();
		~CvRiseFall();
		void reset();

		void onGameStarted();
		void checkTurn();
		void checkTurnForPlayer(CivilizationTypes civType, int turn);
		void checkScheduledCities(PlayerTypes playerType, CivilizationTypes civType, int turn);
		void checkScheduledUnits(PlayerTypes playerType, CivilizationTypes civType, int turn, bool spawnedNow);

		void checkPlayerTurn(PlayerTypes playerType);
		void checkLeader(CivilizationTypes civType, PlayerTypes playerType);
		void checkMinorWars(PlayerTypes playerID, int turn);
		void updatePlayerPlots();
		void checkStabilityEffect(CivilizationTypes civType, PlayerTypes playerType);

		void spawnHumanCivilization(CivilizationTypes civType);
		void spawnAICivilization(CivilizationTypes civType);
		void spawnMinorCivilization(CivilizationTypes civType);

		void setupAIPlayer(CivilizationTypes civType, PlayerTypes playerType);
		void finishMajorCivSpawn(CivilizationTypes civType, PlayerTypes playerType);
		void eraseSurroundings(CivilizationTypes civType, PlayerTypes playerType);
		void assignStartingTechs(CivilizationTypes civType, PlayerTypes playerType);
		void assignStartingCivics(CivilizationTypes civType, PlayerTypes playerType);
		void setupStartingWars(CivilizationTypes civType, PlayerTypes playerType);

		void addProvince(const wchar* name, int bottom, int left, int top, int right);
		void citySecession(CvCity* city);
		void flipCity(CvCity* city, PlayerTypes newOwnerType, bool flipAllUnits);
		void flipUnitsInArea(CivilizationTypes newCivType, PlayerTypes newOwnerType, int left, int bottom, int right, int top, PlayerTypes previousOwnerType = NO_PLAYER);
		void capitalCollapse(PlayerTypes playerType);
		void completeCollapse(PlayerTypes playerType);

		void setMapFile(const wchar* newName);

		PlayerTypes getPlayerTypeForCiv(CivilizationTypes civType) const;
		CvRFCPlayer& getRFCPlayer(CivilizationTypes civType) const;
		CvRFCProvince* getRFCProvince(const wchar* provinceName);
		CvRFCProvince* getRFCProvince(int provinceID);
		int getNumProvinces() const;
		CvRFCProvince* getProvinceForPlot(int x, int y);
		bool skipConditionalSpawn(CivilizationTypes civType) const;
		bool unitsInForeignTerritory(PlayerTypes owner, PlayerTypes foreign) const;
		CvPlot* findSpawnPlot(int ix, int iy, DomainTypes domainType) const;
		const wchar* getMapFile() const;

		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);

	protected:
		CvRFCPlayer* _rfcPlayers;
		std::vector<CvRFCProvince*> _rfcProvinces;
		CvWString _mapFile;
};
