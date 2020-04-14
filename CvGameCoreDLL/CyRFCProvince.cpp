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


void CyRFCProvince::scheduleUnit(int year, int unitID, int unitAI, int facingDirection, int amount, int endYear, int spawnFrequency) {
	CvRFCUnit rfcUnit(year, (UnitTypes)unitID, (UnitAITypes)unitAI, (DirectionTypes)facingDirection, amount, endYear, spawnFrequency);
	rfcProvince->scheduleUnit(rfcUnit);
}

void CyRFCProvince::hireMercenary(int playerType, int mercenaryID) {
	rfcProvince->hireMercenary((PlayerTypes)playerType, mercenaryID);
}


std::wstring CyRFCProvince::getName() {
	return rfcProvince->getName();
}

int CyRFCProvince::getBottom() {
	return rfcProvince->getBottom();
}

int CyRFCProvince::getLeft() {
	return rfcProvince->getLeft();
}

int CyRFCProvince::getTop() {
	return rfcProvince->getTop();
}

int CyRFCProvince::getRight() {
	return rfcProvince->getRight();
}

int CyRFCProvince::getNumScheduledUnits() {
	return rfcProvince->getNumScheduledUnits();
}

CyRFCUnit* CyRFCProvince::getScheduledUnit(int i) {
	return new CyRFCUnit(&rfcProvince->getScheduledUnit(i));
}

int CyRFCProvince::getNumMercenaries() {
	return rfcProvince->getNumMercenaries();
}

CyRFCMercenary* CyRFCProvince::getMercenary(int i) {
	return new CyRFCMercenary(&rfcProvince->getMercenary(i));
}

int CyRFCProvince::getNumCities(int playerType) {
	return rfcProvince->getNumCities((PlayerTypes)playerType);
}
