/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCMercenary.h"

CyRFCMercenary::CyRFCMercenary() : rfcMercenary(NULL) {}

CyRFCMercenary::CyRFCMercenary(CvRFCMercenary* rfcMercenaryConst) : rfcMercenary(rfcMercenaryConst) {
}

void CyRFCMercenary::addPromotion(int promotion) {
	rfcMercenary->addPromotion((PromotionTypes)promotion);
}

int CyRFCMercenary::getUnitType() {
	return rfcMercenary->getUnitType();
}

int CyRFCMercenary::getNumPromotions() {
	return rfcMercenary->getNumPromotions();
}

int CyRFCMercenary::getPromotion(int i) {
	return rfcMercenary->getPromotion(i);
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
