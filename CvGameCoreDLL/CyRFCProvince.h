#pragma once
/*
Author: bluepotato
*/
class CvRFCProvince;
class CyRFCUnit;
class CyRFCMercenary;

class CyRFCProvince {
	public:
		CyRFCProvince();
		CyRFCProvince(CvRFCProvince* rfcProvinceConst);

		void hireMercenary(int playerType, int mercenaryID);

		std::wstring getName();
		int getBottom();
		int getLeft();
		int getTop();
		int getRight();
		int getNumScheduledUnits();
		CyRFCUnit* addScheduledUnit();
		CyRFCUnit* getScheduledUnit(int i);
		int getNumMercenaries();
		CyRFCMercenary* getMercenary(int i);
		int getNumCities(int playerType);
	protected:
		CvRFCProvince* rfcProvince;
};
