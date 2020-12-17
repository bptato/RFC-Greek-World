/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRFCUnit.h"

void CyRFCUnitInterface() {
	python::class_<CyRFCUnit>("CyRFCUnit")
		.def("setYear", &CyRFCUnit::setYear, "void (int year)")
		.def("setX", &CyRFCUnit::setX, "void (int x)")
		.def("setY", &CyRFCUnit::setY, "void (int y)")
		.def("setUnitType", &CyRFCUnit::setUnitType, "void (int unitType)")
		.def("setUnitAIType", &CyRFCUnit::setUnitAIType, "void (int unitAIType)")
		.def("setFacingDirection", &CyRFCUnit::setFacingDirection, "void (int facingDirection)")
		.def("setAmount", &CyRFCUnit::setAmount, "void (int amount)")
		.def("setEndYear", &CyRFCUnit::setEndYear, "void (int endYear)")
		.def("setSpawnFrequency", &CyRFCUnit::setSpawnFrequency, "void (int spawnFrequency)")
		.def("setAIOnly", &CyRFCUnit::setAIOnly, "void (bool aiOnly)")
		.def("setDeclareWar", &CyRFCUnit::setDeclareWar, "void (bool declareWar)")
		.def("getYear", &CyRFCUnit::getYear, "int ()")
		.def("getX", &CyRFCUnit::getX, "int ()")
		.def("getY", &CyRFCUnit::getY, "int ()")
		.def("getUnitType", &CyRFCUnit::getUnitType, "int ()")
		.def("getUnitAIType", &CyRFCUnit::getUnitAIType, "int ()")
		.def("getFacingDirection", &CyRFCUnit::getFacingDirection, "int ()")
		.def("getAmount", &CyRFCUnit::getAmount, "int ()")
		.def("getEndYear", &CyRFCUnit::getEndYear, "int ()")
		.def("getSpawnFrequency", &CyRFCUnit::getSpawnFrequency, "int ()")
		.def("isAIOnly", &CyRFCUnit::isAIOnly, "bool ()")
		.def("isDeclareWar", &CyRFCUnit::isDeclareWar, "bool ()")
		;
}

