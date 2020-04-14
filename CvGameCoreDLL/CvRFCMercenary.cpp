/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCMercenary.h"

CvRFCMercenary::CvRFCMercenary() : //empty constructor, only for reading!
hireCost(-1),
maintenanceCost(-1),
experience(-1),
unitType(NO_UNIT)
{
}

CvRFCMercenary::CvRFCMercenary(int constHireCost, int constMaintenanceCost, int constExperience, UnitTypes constUnitType) :
hireCost(constHireCost),
maintenanceCost(constMaintenanceCost),
experience(constExperience),
unitType(constUnitType)
{
}

CvRFCMercenary::~CvRFCMercenary() {
	promotions.clear();
}


void CvRFCMercenary::addPromotion(PromotionTypes promotion) {
	promotions.push_back(promotion);
}


int CvRFCMercenary::getHireCost() const {
	if(GC.getGame().getActiveCivilizationType() == CIVILIZATION_SUMERIA) { //TODO: does getActiveCivilizationType always work here?
		return hireCost/2;
	}
	return hireCost;
}

int CvRFCMercenary::getExperience() const {
	return experience;
}

UnitTypes CvRFCMercenary::getUnitType() const {
	return unitType;
}

int CvRFCMercenary::getNumPromotions() const {
	return promotions.size();
}

PromotionTypes CvRFCMercenary::getPromotion(int i) const {
	return promotions[i];
}

int CvRFCMercenary::getMaintenanceCost() const {
	if(GC.getGame().getActiveCivilizationType() == CIVILIZATION_SUMERIA) { //TODO: does getActiveCivilizationType always work here?
		return maintenanceCost/2;
	}
	return maintenanceCost;
}


void CvRFCMercenary::write(FDataStreamBase* stream) {
	stream->Write(hireCost);
	stream->Write(maintenanceCost);
	stream->Write(experience);
	stream->Write(unitType);

	{
		uint size = promotions.size();
		stream->Write(size);
		for(std::vector<PromotionTypes>::iterator it = promotions.begin(); it != promotions.end(); ++it) {
			stream->Write((*it));
		}
	}
}

void CvRFCMercenary::read(FDataStreamBase* stream) {
	stream->Read(&hireCost);
	stream->Read(&maintenanceCost);
	stream->Read(&experience);
	stream->Read((int*)&unitType);

	{
		promotions.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i<size; i++) {
			int promotionType;
			stream->Read(&promotionType);
			promotions.push_back((PromotionTypes)promotionType);
		}
	}
}
