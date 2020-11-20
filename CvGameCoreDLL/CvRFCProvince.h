#pragma once
/*
Author: bluepotato
*/

class CvRFCProvince {
	public:
		CvRFCProvince();
		~CvRFCProvince();
		void reset();
		void init();
		void uninit();

		void setName(const wchar* newName);
		void setBounds(int newBottom, int newRight, int newTop, int newLeft);
		void addMercenary(CvRFCMercenary mercenary);
		void checkMercenaries();
		void hireMercenary(PlayerTypes playerType, int mercenaryID);

		const wchar* getName() const;
		bool isInBounds(int x, int y) const;
		int getBottom() const;
		int getRight() const;
		int getTop() const;
		int getLeft() const;
		bool isBorderProvince(CvRFCProvince* province) const;
		int getNumScheduledUnits() const;
		CvRFCUnit* addScheduledUnit();
		CvRFCUnit* getScheduledUnit(int i) const;
		std::vector<CvRFCUnit*>& getScheduledUnits();
		int getNumMercenaries() const;
		CvRFCMercenary& getMercenary(int i);
		std::vector<CvRFCMercenary>& getMercenaries();
		std::vector<CvUnit*> getUnits();
		int getNumCities(PlayerTypes playerType) const;
		CvCity* getFirstCity(PlayerTypes);

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		CvWString name;
		int bottom;
		int left;
		int top;
		int right;
		std::vector<CvRFCUnit*> scheduledUnits; //barbs
		std::vector<CvRFCMercenary> mercenaries;
};
