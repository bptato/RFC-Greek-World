#pragma once
/*
Author: bluepotato
*/
class CvRFCCity;

class CyRFCCity {
	public:
		CyRFCCity();
		CyRFCCity(CvRFCCity* rfcCityConst);

		int getYear();
		int getX();
		int getY();
		int getPopulation();
		int getNumBuilding(int building);
	protected:
		CvRFCCity* rfcCity;
};
