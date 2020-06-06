#pragma once
/*
Author: bluepotato
*/
class CvRFCUnit;

class CyRFCUnit {
	public:
		CyRFCUnit();
		CyRFCUnit(CvRFCUnit* rfcUnit);


		int getYear();
		int getX();
		int getY();
		int getUnitType();
		int getUnitAIType();
		int getFacingDirection();
		int getAmount();
		int getEndYear();
		int getSpawnFrequency();

	protected:
		CvRFCUnit* rfcUnit;
};
