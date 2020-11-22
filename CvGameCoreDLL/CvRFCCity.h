#pragma once
/*
Author: bluepotato
*/

class CvRFCCity {
	public:
		CvRFCCity();
		~CvRFCCity();
		void init();
		void uninit();
		void reset();

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setPopulation(int population);
		void setNumBuilding(BuildingTypes building, int value);
		void setReligion(ReligionTypes religion, bool value);
		void setHolyCityReligion(ReligionTypes religion, bool value);
		void setCulture(CivilizationTypes civType, int value);

		int getYear() const;
		int getX() const;
		int getY() const;
		int getPopulation() const;
		int getNumBuilding(BuildingTypes building) const;
		bool getReligion(ReligionTypes religion) const;
		bool getHolyCityReligion(ReligionTypes religion) const;
		int getCulture(CivilizationTypes culture) const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int _year;
		int _x;
		int _y;
		int _population;
		int* _buildings;
		bool* _religions;
		bool* _holyCityReligions;
		int* _culture;
};
