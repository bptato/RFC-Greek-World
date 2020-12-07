/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCProvince.h"
#include "CyRFCUnit.h"
#include "CyRFCMercenary.h"

CyRFCProvince::CyRFCProvince() : rfcProvince(NULL) {}

CyRFCProvince::CyRFCProvince(CvRFCProvince* rfcProvinceConst) : rfcProvince(rfcProvinceConst) {
}


void CyRFCProvince::hireMercenary(int playerType, int mercenaryID) {
	rfcProvince->hireMercenary((PlayerTypes)playerType, mercenaryID);
}

void CyRFCProvince::removeScheduledUnit(int i) {
	rfcProvince->removeScheduledUnit(i);
}


std::string CyRFCProvince::getType() {
	return rfcProvince->getType();
}

int CyRFCProvince::getProvinceType() {
	return rfcProvince->getProvinceType();
}

std::wstring CyRFCProvince::getName() {
	return rfcProvince->getName();
}

int CyRFCProvince::getNumScheduledUnits() {
	return rfcProvince->getNumScheduledUnits();
}

CyRFCUnit* CyRFCProvince::addScheduledUnit() {
	return new CyRFCUnit(rfcProvince->addScheduledUnit());
}

CyRFCUnit* CyRFCProvince::getScheduledUnit(int i) {
	return new CyRFCUnit(rfcProvince->getScheduledUnit(i));
}

int CyRFCProvince::getNumMercenaries() {
	return rfcProvince->getNumMercenaries();
}

CyRFCMercenary* CyRFCProvince::getMercenary(int i) {
	return new CyRFCMercenary(rfcProvince->getMercenary(i));
}

int CyRFCProvince::getNumCities(int playerType) {
	return rfcProvince->getNumCities((PlayerTypes)playerType);
}

int CyRFCProvince::getNumPlots() {
	return rfcProvince->getNumPlots();
}
