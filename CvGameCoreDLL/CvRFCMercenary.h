#pragma once
/*
Author: bluepotato
*/

class CvRFCMercenary {
	public:
		CvRFCMercenary();
		CvRFCMercenary(int hireCost, int maintenanceCost, int experience, UnitTypes unitType);
		~CvRFCMercenary();

		void addPromotion(PromotionTypes promotion);

		int getHireCost() const;
		int getMaintenanceCost() const;
		int getExperience() const;
		UnitTypes getUnitType() const;
		int getNumPromotions() const;
		PromotionTypes getPromotion(int i) const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int hireCost;
		int maintenanceCost;
		int experience;
		UnitTypes unitType;
		std::vector<PromotionTypes> promotions;
};
