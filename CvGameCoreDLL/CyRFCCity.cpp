/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCCity.h"

CyRFCCity::CyRFCCity() : rfcCity(NULL) {}

CyRFCCity::CyRFCCity(CvRFCCity* rfcCityConst) : rfcCity(rfcCityConst) {
}

int CyRFCCity::getYear() {
	return rfcCity->getYear();
}

int CyRFCCity::getX() {
	return rfcCity->getX();
}

int CyRFCCity::getY() {
	return rfcCity->getY();
}

int CyRFCCity::getPopulation() {
	return rfcCity->getPopulation();
}

int CyRFCCity::getNumBuilding(int building) {
	return rfcCity->getNumBuilding((BuildingTypes)building);
}
