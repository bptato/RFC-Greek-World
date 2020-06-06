/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCUnit.h"

CyRFCUnit::CyRFCUnit() : rfcUnit(NULL) {}

CyRFCUnit::CyRFCUnit(CvRFCUnit* rfcUnitConst) : rfcUnit(rfcUnitConst) {
}


int CyRFCUnit::getYear() {
	return rfcUnit->getYear();
}

int CyRFCUnit::getX() {
	return rfcUnit->getX();
}

int CyRFCUnit::getY() {
	return rfcUnit->getY();
}

int CyRFCUnit::getUnitType() {
	return rfcUnit->getUnitType();
}

int CyRFCUnit::getUnitAIType() {
	return rfcUnit->getUnitAIType();
}

int CyRFCUnit::getFacingDirection() {
	return rfcUnit->getFacingDirection();
}

int CyRFCUnit::getAmount() {
	return rfcUnit->getAmount();
}

int CyRFCUnit::getEndYear() {
	return rfcUnit->getEndYear();
}

int CyRFCUnit::getSpawnFrequency() {
	return rfcUnit->getSpawnFrequency();
}
