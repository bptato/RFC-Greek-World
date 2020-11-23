/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCMercenary.h"

CvRFCMercenary::CvRFCMercenary() : //empty constructor, only for reading!
_hireCost(-1),
_maintenanceCost(-1),
_experience(-1),
_unitType(NO_UNIT)
{
}

CvRFCMercenary::CvRFCMercenary(int hireCost, int maintenanceCost, int experience, UnitTypes unitType) :
_hireCost(hireCost),
_maintenanceCost(maintenanceCost),
_experience(experience),
_unitType(unitType)
{
}

CvRFCMercenary::~CvRFCMercenary() {
	_promotions.clear();
}


void CvRFCMercenary::addPromotion(PromotionTypes promotion) {
	_promotions.push_back(promotion);
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

int CvRFCMercenary::getNumPromotions() const {
	return _promotions.size();
}

PromotionTypes CvRFCMercenary::getPromotion(int i) const {
	return _promotions[i];
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

	{
		uint size = _promotions.size();
		stream->Write(size);
		for(std::vector<PromotionTypes>::iterator it = _promotions.begin(); it != _promotions.end(); ++it) {
			stream->Write(*it);
		}
	}
}

void CvRFCMercenary::read(FDataStreamBase* stream) {
	stream->Read(&_hireCost);
	stream->Read(&_maintenanceCost);
	stream->Read(&_experience);
	stream->Read((int*)&_unitType);

	{
		_promotions.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int promotionType;
			stream->Read(&promotionType);
			_promotions.push_back((PromotionTypes)promotionType);
		}
	}
}
