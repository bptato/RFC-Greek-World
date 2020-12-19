#pragma once
/*
Author: bluepotato
*/

class CvRFCProvince {
	public:
		CvRFCProvince(ProvinceTypes provinceType);
		~CvRFCProvince();
		void init(ProvinceTypes provinceType);
		void reset(ProvinceTypes provinceType);
		void uninit();

		void setType(CvString type);
		void setProvinceType(ProvinceTypes provinceType);
		void checkMercenaries();
		void hireMercenary(PlayerTypes playerType, int mercenaryID);
		void addPlot(int plotid);
		void removePlot(int plotid);
		void removeScheduledUnit(int i);

		void addMercenary(CvRFCMercenary* mercenary);
		CvRFCMercenary* addMercenary();
		CvRFCUnit* addScheduledUnit();

		const char* getType() const;
		ProvinceTypes getProvinceType() const;
		const wchar* getName() const;
		int getNumScheduledUnits() const;
		CvRFCUnit* getScheduledUnit(int i) const;
		std::vector<CvRFCUnit*>& getScheduledUnits();
		int getNumMercenaries() const;
		CvRFCMercenary* getMercenary(int i);
		std::vector<CvUnit*> getUnits();
		std::vector<int>& getPlots();
		int getNumCities(PlayerTypes playerType) const;
		int getNumPlots() const;
		CvCity* getFirstCity(PlayerTypes);
		bool isBorderProvince(ProvinceTypes province);
		bool canSpawnBarbs();
		bool isInBorderBounds(int x, int y);

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		CvString _type;
		CvWString _name;
		ProvinceTypes _provinceType;
		std::vector<CvRFCUnit*> _scheduledUnits; //barbs
		std::vector<CvRFCMercenary*> _mercenaries;
		std::vector<int> _plots;
};
