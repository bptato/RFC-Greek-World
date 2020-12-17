/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRiseFall.h"
#include "CyRFCPlayer.h"
#include "CyRFCProvince.h"

void CyRiseFallInterface() {
	python::class_<CyRiseFall>("CyRiseFall")
		.def("getRFCPlayer", &CyRiseFall::getRFCPlayer, python::return_value_policy<python::reference_existing_object>(), "(int civType)")
		.def("getNumProvinces", &CyRiseFall::getNumProvinces, "int ()")
		.def("findProvince", &CyRiseFall::findProvince, "int (str provinceName)")
		.def("getProvince", &CyRiseFall::getProvince, python::return_value_policy<python::reference_existing_object>(), "(int province)")
		.def("addProvince", &CyRiseFall::addProvince, python::return_value_policy<python::reference_existing_object>(), "(str name)")
		.def("setMapFile", &CyRiseFall::setMapFile, "void (str name)")
		.def("getMapFile", &CyRiseFall::getMapFile, "str ()")
		.def("removeProvince", &CyRiseFall::removeProvince, "void (int province)")
		;
}
