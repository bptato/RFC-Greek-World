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
		void setNumBuilding(int building, int value);
		void setReligion(int religion, bool value);
		void setHolyCityReligion(int religion, bool value);
		void setCulture(int civType, int value);

		int getYear();
		int getX();
		int getY();
		int getPopulation();
		int getNumBuilding(int building);
		bool getReligion(int religion);
		bool getHolyCityReligion(int religion);
		int getCulture(int civType);

	protected:
		CvRFCCity* rfcCity;
};
