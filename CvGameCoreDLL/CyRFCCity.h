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

		int getYear();
		int getX();
		int getY();
		int getPopulation();
		int getNumBuilding(int building);

	protected:
		CvRFCCity* rfcCity;
};
