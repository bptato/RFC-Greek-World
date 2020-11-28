/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCMercenary.h"

CvRFCMercenary::CvRFCMercenary() {
	_promotions = new bool[GC.getNumPromotionInfos()];
	reset();
}

CvRFCMercenary::~CvRFCMercenary() {
	SAFE_DELETE_ARRAY(_promotions);
}

void CvRFCMercenary::init() {
}

void CvRFCMercenary::uninit() {
}

void CvRFCMercenary::reset() {
	for(int i = 0; i < GC.getNumPromotionInfos(); ++i) {
		_promotions[i] = false;
	}
	_hireCost = -1;
	_maintenanceCost = -1;
	_experience = -1;
	_unitType = NO_UNIT;
}

CvRFCMercenary* CvRFCMercenary::clone() {
	CvRFCMercenary* clone = new CvRFCMercenary;
	for(int i = 0; i < GC.getNumPromotionInfos(); ++i) {
		clone->setHasPromotion((PromotionTypes)i, _promotions[i]);
	}
	clone->setHireCost(_hireCost);
	clone->setMaintenanceCost(_maintenanceCost);
	clone->setExperience(_experience);
	clone->setUnitType(_unitType);
	return clone;
}


void CvRFCMercenary::setHasPromotion(PromotionTypes promotion, bool val) {
	_promotions[promotion] = val;
}

void CvRFCMercenary::setHireCost(int hireCost) {
	_hireCost = hireCost;
}

void CvRFCMercenary::setExperience(int experience) {
	_experience = experience;
}

void CvRFCMercenary::setUnitType(UnitTypes unitType) {
	_unitType = unitType;
}

void CvRFCMercenary::setMaintenanceCost(int maintenanceCost) {
	_maintenanceCost = maintenanceCost;
}


int CvRFCMercenary::getHireCost() const {
	if(GC.getGame().getActiveCivilizationType() == CIVILIZATION_SUMERIA) { //TODO: does getActiveCivilizationType always work here?
		return _hireCost / 2;
	}
	return _hireCost;
}

int CvRFCMercenary::getExperience() const {
	return _experience;
}

UnitTypes CvRFCMercenary::getUnitType() const {
	return _unitType;
}

bool CvRFCMercenary::hasPromotion(PromotionTypes promotion) const {
	return _promotions[promotion];
}

int CvRFCMercenary::getMaintenanceCost() const {
	if(GC.getGame().getActiveCivilizationType() == CIVILIZATION_SUMERIA) { //TODO: does getActiveCivilizationType always work here?
		return _maintenanceCost / 2;
	}
	return _maintenanceCost;
}


void CvRFCMercenary::write(FDataStreamBase* stream) {
	stream->Write(_hireCost);
	stream->Write(_maintenanceCost);
	stream->Write(_experience);
	stream->Write(_unitType);
	stream->Write(GC.getNumPromotionInfos(), _promotions);
}

void CvRFCMercenary::read(FDataStreamBase* stream) {
	stream->Read(&_hireCost);
	stream->Read(&_maintenanceCost);
	stream->Read(&_experience);
	stream->Read((int*)&_unitType);
	stream->Read(GC.getNumPromotionInfos(), _promotions);
}
