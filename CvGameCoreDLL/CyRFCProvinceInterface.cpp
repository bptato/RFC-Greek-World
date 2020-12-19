/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCProvince.h"
#include "CyRFCUnit.h"
#include "CyRFCMercenary.h"

void CyRFCProvinceInterface() {
	python::class_<CyRFCProvince>("CyRFCProvince")
		.def("getType", &CyRFCProvince::getType, "str ()")
		.def("getProvinceType", &CyRFCProvince::getProvinceType, "int ()")
		.def("getName", &CyRFCProvince::getName, "str ()")
		.def("getNumScheduledUnits", &CyRFCProvince::getNumScheduledUnits, "int ()")
		.def("addScheduledUnit", &CyRFCProvince::addScheduledUnit, python::return_value_policy<python::reference_existing_object>(), "()")
		.def("getScheduledUnit", &CyRFCProvince::getScheduledUnit, python::return_value_policy<python::reference_existing_object>(), "(int i)")
		.def("getNumMercenaries", &CyRFCProvince::getNumMercenaries, "int ()")
		.def("getMercenary", &CyRFCProvince::getMercenary, python::return_value_policy<python::reference_existing_object>(), "(int i)")
		.def("getNumCities", &CyRFCProvince::getNumCities, "int (int playerType)")
		.def("getNumPlots", &CyRFCProvince::getNumPlots, "int ()")
		.def("hireMercenary", &CyRFCProvince::hireMercenary, "void (int playerType, int mercenaryID)")
		.def("removeScheduledUnit", &CyRFCProvince::removeScheduledUnit, "void (int i)")
		.def("isInBorderBounds", &CyRFCProvince::isInBorderBounds, "bool (int x, int y)")
		;
}
