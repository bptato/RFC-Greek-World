#pragma once
/*
Author: bluepotato
*/

class CvRFCMercenary {
	public:
		CvRFCMercenary();
		~CvRFCMercenary();
		void init();
		void uninit();
		void reset();
		CvRFCMercenary* clone();

		void setHasPromotion(PromotionTypes promotion, bool val);
		void setHireCost(int val);
		void setMaintenanceCost(int val);
		void setExperience(int val);
		void setUnitType(UnitTypes val);

		int getHireCost() const;
		int getMaintenanceCost() const;
		int getExperience() const;
		UnitTypes getUnitType() const;
		bool hasPromotion(PromotionTypes promotion) const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int _hireCost;
		int _maintenanceCost;
		int _experience;
		UnitTypes _unitType;
		bool* _promotions;
};
