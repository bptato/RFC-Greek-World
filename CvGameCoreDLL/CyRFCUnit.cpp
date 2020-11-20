/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCUnit.h"

CyRFCUnit::CyRFCUnit() : rfcUnit(NULL) {}

CyRFCUnit::CyRFCUnit(CvRFCUnit* rfcUnitConst) : rfcUnit(rfcUnitConst) {
}

void CyRFCUnit::setYear(int year) {
	return rfcUnit->setYear(year);
}

void CyRFCUnit::setX(int x) {
	return rfcUnit->setX(x);
}

void CyRFCUnit::setY(int y) {
	return rfcUnit->setY(y);
}

void CyRFCUnit::setUnitType(int unitType) {
	return rfcUnit->setUnitType((UnitTypes)unitType);
}

void CyRFCUnit::setUnitAIType(int unitAIType) {
	return rfcUnit->setUnitAIType((UnitAITypes)unitAIType);
}

void CyRFCUnit::setFacingDirection(int facingDirection) {
	return rfcUnit->setFacingDirection((DirectionTypes)facingDirection);
}

void CyRFCUnit::setAmount(int amount) {
	return rfcUnit->setAmount(amount);
}

void CyRFCUnit::setEndYear(int endYear) {
	return rfcUnit->setEndYear(endYear);
}

void CyRFCUnit::setSpawnFrequency(int spawnFrequency) {
	return rfcUnit->setSpawnFrequency(spawnFrequency);
}

void CyRFCUnit::setAIOnly(bool aiOnly) {
	return rfcUnit->setAIOnly(aiOnly);
}

void CyRFCUnit::setDeclareWar(bool declareWar) {
	return rfcUnit->setDeclareWar(declareWar);
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

bool CyRFCUnit::isAIOnly() {
	return rfcUnit->isAIOnly();
}

bool CyRFCUnit::isDeclareWar() {
	return rfcUnit->isDeclareWar();
}
