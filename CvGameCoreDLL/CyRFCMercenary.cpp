/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCMercenary.h"

CyRFCMercenary::CyRFCMercenary() : rfcMercenary(NULL) {}

CyRFCMercenary::CyRFCMercenary(CvRFCMercenary* rfcMercenaryConst) : rfcMercenary(rfcMercenaryConst) {
}

void CyRFCMercenary::setHasPromotion(int promotion, bool val) {
	rfcMercenary->setHasPromotion((PromotionTypes)promotion, val);
}

int CyRFCMercenary::getUnitType() {
	return rfcMercenary->getUnitType();
}

bool CyRFCMercenary::hasPromotion(int i) {
	return rfcMercenary->hasPromotion((PromotionTypes)i);
}

int CyRFCMercenary::getHireCost() {
	return rfcMercenary->getHireCost();
}

int CyRFCMercenary::getExperience() {
	return rfcMercenary->getExperience();
}

int CyRFCMercenary::getMaintenanceCost() {
	return rfcMercenary->getMaintenanceCost();
}
