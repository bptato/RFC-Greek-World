/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCPlayer.h"
#include "CyRFCUnit.h"
#include "CyRFCCity.h"

CyRFCPlayer::CyRFCPlayer() : rfcPlayer(NULL) {}

CyRFCPlayer::CyRFCPlayer(CvRFCPlayer* rfcPlayerConst) : rfcPlayer(rfcPlayerConst) {
}

void CyRFCPlayer::setStartingYear(int newStartingYear) {
	rfcPlayer->setStartingYear(newStartingYear);
}

void CyRFCPlayer::scheduleUnit(int year, int unitType, int x, int y, int unitAIType, int facingDirection, int amount) {
	CvRFCUnit rfcUnit;
	rfcUnit.setYear(year);
	rfcUnit.setUnitType((UnitTypes)unitType);
	rfcUnit.setX(x);
	rfcUnit.setY(y);
	rfcUnit.setUnitAIType((UnitAITypes)unitAIType);
	rfcUnit.setFacingDirection((DirectionTypes)facingDirection);
	rfcUnit.setAmount(amount);
	rfcPlayer->scheduleUnit(rfcUnit);
}

void CyRFCPlayer::scheduleCity(int year, int x, int y, int population) {
	CvRFCCity rfcCity;
	rfcCity.setYear(year);
	rfcCity.setX(x);
	rfcCity.setY(y);
	rfcCity.setPopulation(population);
	rfcPlayer->scheduleCity(rfcCity);
}

int CyRFCPlayer::getNumScheduledUnits() {
	return rfcPlayer->getNumScheduledUnits();
}

CyRFCUnit* CyRFCPlayer::getScheduledUnit(int i) {
	return new CyRFCUnit(&(rfcPlayer->getScheduledUnits()[i]));
}

int CyRFCPlayer::getNumScheduledCities() {
	return rfcPlayer->getNumScheduledCities();
}

CyRFCCity* CyRFCPlayer::getScheduledCity(int i) {
	return new CyRFCCity(&(rfcPlayer->getScheduledCity(i)));
}

void CyRFCPlayer::setStartingCivic(int civicOptionType, int civicType) {
	rfcPlayer->setStartingCivic((CivicOptionTypes)civicOptionType, (CivicTypes)civicType);
}

void CyRFCPlayer::addStartingTech(int techType) {
	rfcPlayer->addStartingTech((TechTypes)techType);
}

void CyRFCPlayer::addStartingWar(int civType) {
	rfcPlayer->addStartingWar((CivilizationTypes)civType);
}

void CyRFCPlayer::addRelatedLanguage(int civType) {
	rfcPlayer->addRelatedLanguage((CivilizationTypes)civType);
}

void CyRFCPlayer::setStartingPlot(int x, int y) {
	rfcPlayer->setStartingPlotX(x);
	rfcPlayer->setStartingPlotY(y);
}

void CyRFCPlayer::setStartingGold(int gold) {
	rfcPlayer->setStartingGold(gold);
}

void CyRFCPlayer::addCoreProvince(std::wstring provinceName) {
	rfcPlayer->addCoreProvince(provinceName.c_str());
}

void CyRFCPlayer::setEnabled(bool newEnabled) {
	rfcPlayer->setEnabled(newEnabled);
}

void CyRFCPlayer::setMinorCiv(bool minor) {
	rfcPlayer->setMinorCiv(minor);
}

void CyRFCPlayer::setCompactEmpireModifier(int modifier) {
	rfcPlayer->setCompactEmpireModifier(modifier);
}

void CyRFCPlayer::setUnitUpkeepModifier(int modifier) {
	rfcPlayer->setUnitUpkeepModifier(modifier);
}

void CyRFCPlayer::setResearchModifier(int modifier) {
	rfcPlayer->setResearchModifier(modifier);
}

void CyRFCPlayer::setDistanceMaintenanceModifier(int modifier) {
	rfcPlayer->setDistanceMaintenanceModifier(modifier);
}

void CyRFCPlayer::setNumCitiesMaintenanceModifier(int modifier) {
	rfcPlayer->setNumCitiesMaintenanceModifier(modifier);
}

void CyRFCPlayer::setUnitProductionModifier(int modifier) {
	rfcPlayer->setUnitProductionModifier(modifier);
}

void CyRFCPlayer::setCivicUpkeepModifier(int modifier) {
	rfcPlayer->setCivicUpkeepModifier(modifier);
}

void CyRFCPlayer::setHealthBonusModifier(int modifier) {
	rfcPlayer->setHealthBonusModifier(modifier);
}

void CyRFCPlayer::setBuildingProductionModifier(int modifier) {
	rfcPlayer->setBuildingProductionModifier(modifier);
}

void CyRFCPlayer::setWonderProductionModifier(int modifier) {
	rfcPlayer->setWonderProductionModifier(modifier);
}

void CyRFCPlayer::setGreatPeopleModifier(int modifier) {
	rfcPlayer->setGreatPeopleModifier(modifier);
}

void CyRFCPlayer::setInflationModifier(int modifier) {
	rfcPlayer->setInflationModifier(modifier);
}

void CyRFCPlayer::setGrowthModifier(int modifier) {
	rfcPlayer->setGrowthModifier(modifier);
}


int CyRFCPlayer::getStability(int category) {
	return rfcPlayer->getStability(category);
}

int CyRFCPlayer::getTotalStability() {
	return rfcPlayer->getTotalStability();
}

int CyRFCPlayer::getStartingYear() {
	return rfcPlayer->getStartingYear();
}

bool CyRFCPlayer::isEnabled() {
	return rfcPlayer->isEnabled();
}

int CyRFCPlayer::getStartingCivic(int civicOptionType) {
	return rfcPlayer->getStartingCivic((CivicOptionTypes)civicOptionType);
}

int CyRFCPlayer::getStartingGold() {
	return rfcPlayer->getStartingGold();
}

bool CyRFCPlayer::isStartingTech(int tech) {
	return rfcPlayer->isStartingTech((TechTypes)tech);
}

bool CyRFCPlayer::isStartingWar(int civType) {
	return rfcPlayer->isStartingWar((CivilizationTypes)civType);
}

bool CyRFCPlayer::isRelatedLanguage(int civType) {
	return rfcPlayer->isRelatedLanguage((CivilizationTypes)civType);
}

int CyRFCPlayer::getStartingPlotX() {
	return rfcPlayer->getStartingPlotX();
}

int CyRFCPlayer::getStartingPlotY() {
	return rfcPlayer->getStartingPlotY();
}

int CyRFCPlayer::getNumCoreProvinces() {
	return rfcPlayer->getNumCoreProvinces();
}

std::wstring CyRFCPlayer::getCoreProvince(int i) {
	return rfcPlayer->getCoreProvince(i);
}

bool CyRFCPlayer::isMinor() {
	return rfcPlayer->isMinor();
}

bool CyRFCPlayer::isSpawned() {
	return rfcPlayer->isSpawned();
}

int CyRFCPlayer::getCompactEmpireModifier() {
	return rfcPlayer->getCompactEmpireModifier();
}

int CyRFCPlayer::getUnitUpkeepModifier() {
	return rfcPlayer->getUnitUpkeepModifier();
}

int CyRFCPlayer::getResearchModifier() {
	return rfcPlayer->getResearchModifier();
}

int CyRFCPlayer::getDistanceMaintenanceModifier() {
	return rfcPlayer->getDistanceMaintenanceModifier();
}

int CyRFCPlayer::getNumCitiesMaintenanceModifier() {
	return rfcPlayer->getNumCitiesMaintenanceModifier();
}

int CyRFCPlayer::getUnitProductionModifier() {
	return rfcPlayer->getUnitProductionModifier();
}

int CyRFCPlayer::getCivicUpkeepModifier() {
	return rfcPlayer->getCivicUpkeepModifier();
}

int CyRFCPlayer::getHealthBonusModifier() {
	return rfcPlayer->getHealthBonusModifier();
}

int CyRFCPlayer::getBuildingProductionModifier() {
	return rfcPlayer->getBuildingProductionModifier();
}

int CyRFCPlayer::getWonderProductionModifier() {
	return rfcPlayer->getWonderProductionModifier();
}

int CyRFCPlayer::getGreatPeopleModifier() {
	return rfcPlayer->getGreatPeopleModifier();
}

int CyRFCPlayer::getInflationModifier() {
	return rfcPlayer->getInflationModifier();
}

int CyRFCPlayer::getGrowthModifier() {
	return rfcPlayer->getGrowthModifier();
}
