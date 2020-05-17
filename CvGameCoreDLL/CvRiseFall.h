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
		void checkPlayerTurn(PlayerTypes playerID);

		void checkLeader(CivilizationTypes civType, PlayerTypes playerType);
		void checkMinorWars(PlayerTypes playerID, int turn);
		bool checkUnitsInForeignTerritory(PlayerTypes owner, PlayerTypes foreign);

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

		PlayerTypes getPlayerTypeForCiv(CivilizationTypes civType);
		CvRFCPlayer& getRFCPlayer(CivilizationTypes civType);
		CvRFCProvince* getRFCProvince(const wchar* provinceName);
		CvRFCProvince* getRFCProvince(int provinceID);
		int getNumProvinces();
		CvRFCProvince* getProvinceForPlot(int x, int y);

		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);

	protected:
		CvRFCPlayer* rfcPlayers;
		std::vector<CvRFCProvince> rfcProvinces;
};
