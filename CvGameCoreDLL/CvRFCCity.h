#pragma once
/*
Author: bluepotato
*/

class CvRFCCity {
	public:
		CvRFCCity();
		~CvRFCCity();
		void init();

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setPopulation(int population);
		void setNumBuilding(BuildingTypes building, int value);

		int getYear() const;
		int getX() const;
		int getY() const;
		int getPopulation() const;
		int getNumBuilding(BuildingTypes building) const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int _year;
		int _x;
		int _y;
		int _population;
		int* _buildings;
};
