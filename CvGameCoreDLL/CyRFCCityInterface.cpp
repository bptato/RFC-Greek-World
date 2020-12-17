/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCCity.h"

void CyRFCCityInterface() {
	python::class_<CyRFCCity>("CyRFCCity")
		.def("setYear", &CyRFCCity::setYear, "void (int year)")
		.def("setX", &CyRFCCity::setX, "void (int x)")
		.def("setY", &CyRFCCity::setY, "void (int y)")
		.def("setPopulation", &CyRFCCity::setPopulation, "void (int population)")
		.def("setNumBuilding", &CyRFCCity::setNumBuilding, "void (int building, int num)")
		.def("setReligion", &CyRFCCity::setReligion, "void (int religion, bool value)")
		.def("setHolyCityReligion", &CyRFCCity::setHolyCityReligion, "void (int religion, bool value)")
		.def("setCulture", &CyRFCCity::setCulture, "void (int civType, bool value)")
		.def("getYear", &CyRFCCity::getYear, "int ()")
		.def("getX", &CyRFCCity::getX, "int ()")
		.def("getY", &CyRFCCity::getY, "int ()")
		.def("getPopulation", &CyRFCCity::getPopulation, "int ()")
		.def("getNumBuilding", &CyRFCCity::getNumBuilding, "int (int building)")
		.def("getReligion", &CyRFCCity::getReligion, "bool (int religion)")
		.def("getHolyCityReligion", &CyRFCCity::getHolyCityReligion, "bool (int religion)")
		.def("getCulture", &CyRFCCity::getCulture, "int (int civType)")
		;
}

