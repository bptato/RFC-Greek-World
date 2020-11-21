#pragma once
/*
Author: bluepotato
*/
class CvRFCCity;

class CyRFCCity {
	public:
		CyRFCCity();
		CyRFCCity(CvRFCCity* rfcCityConst);

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setPopulation(int population);
		void setNumBuilding(int building, int num);
		void setReligion(int religion, bool num);
		void setHolyCityReligion(int religion, bool num);

		int getYear();
		int getX();
		int getY();
		int getPopulation();
		int getNumBuilding(int building);
		bool getReligion(int religion);
		bool getHolyCityReligion(int religion);

	protected:
		CvRFCCity* rfcCity;
};
