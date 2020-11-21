/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCCity.h"

CyRFCCity::CyRFCCity() : rfcCity(NULL) {}

CyRFCCity::CyRFCCity(CvRFCCity* rfcCityConst) : rfcCity(rfcCityConst) {
}


void CyRFCCity::setYear(int year) {
	rfcCity->setYear(year);
}

void CyRFCCity::setX(int x) {
	rfcCity->setX(x);
}

void CyRFCCity::setY(int y) {
	rfcCity->setY(y);
}

void CyRFCCity::setPopulation(int population) {
	rfcCity->setPopulation(population);
}

void CyRFCCity::setNumBuilding(int building, int num) {
	rfcCity->setNumBuilding((BuildingTypes)building, num);
}

void CyRFCCity::setReligion(int religion, bool value) {
	rfcCity->setReligion((ReligionTypes)religion, value);
}

void CyRFCCity::setHolyCityReligion(int religion, bool value) {
	rfcCity->setHolyCityReligion((ReligionTypes)religion, value);
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

bool CyRFCCity::getReligion(int religion) {
	return rfcCity->getReligion((ReligionTypes)religion);
}

bool CyRFCCity::getHolyCityReligion(int religion) {
	return rfcCity->getHolyCityReligion((ReligionTypes)religion);
}
