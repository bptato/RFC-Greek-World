/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCMercenary.h"

void CyRFCMercenaryInterface() {
	python::class_<CyRFCMercenary>("CyRFCMercenary")
		.def("setHasPromotion", &CyRFCMercenary::setHasPromotion, "void (int i, bool val)")
		.def("getHireCost", &CyRFCMercenary::getHireCost, "int ()")
		.def("getUnitType", &CyRFCMercenary::getUnitType, "int ()")
		.def("hasPromotion", &CyRFCMercenary::hasPromotion, "bool (int i)")
		.def("getExperience", &CyRFCMercenary::getExperience, "int ()")
		.def("getMaintenanceCost", &CyRFCMercenary::getMaintenanceCost, "int ()")
		;
}
