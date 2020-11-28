#pragma once
/*
Author: bluepotato
*/
class CvRFCMercenary;

class CyRFCMercenary {
	public:
		CyRFCMercenary();
		CyRFCMercenary(CvRFCMercenary* rfcMercenary);

		void setHasPromotion(int i, bool val);

		int getUnitType();
		bool hasPromotion(int i);
		int getHireCost();
		int getExperience();
		int getMaintenanceCost();
	protected:
		CvRFCMercenary* rfcMercenary;
};
