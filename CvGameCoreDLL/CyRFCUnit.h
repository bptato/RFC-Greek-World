#pragma once
/*
Author: bluepotato
*/
class CvRFCUnit;

class CyRFCUnit {
	public:
		CyRFCUnit();
		CyRFCUnit(CvRFCUnit* rfcUnit);

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setUnitType(int unitType);
		void setUnitAIType(int unitAIType);
		void setFacingDirection(int facingDirection);
		void setAmount(int amount);
		void setEndYear(int endYear);
		void setSpawnFrequency(int spawnFrequency);
		void setAIOnly(bool aiOnly);
		void setDeclareWar(bool declareWar);

		int getYear();
		int getX();
		int getY();
		int getUnitType();
		int getUnitAIType();
		int getFacingDirection();
		int getAmount();
		int getEndYear();
		int getSpawnFrequency();
		bool isAIOnly();
		bool isDeclareWar();

	protected:
		CvRFCUnit* rfcUnit;
};
