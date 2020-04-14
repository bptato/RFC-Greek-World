#pragma once
/*
Author: bluepotato
*/
class CvRFCMercenary;

class CyRFCMercenary {
	public:
		CyRFCMercenary();
		CyRFCMercenary(CvRFCMercenary* rfcMercenary);

		void addPromotion(int i);

		int getUnitType();
		int getNumPromotions();
		int getPromotion(int i);
		int getHireCost();
		int getExperience();
		int getMaintenanceCost();
	protected:
		CvRFCMercenary* rfcMercenary;
};
