/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CyRiseFall.h"
#include "CyRFCPlayer.h"
#include "CyRFCProvince.h"

CyRiseFall::CyRiseFall() : riseFall(NULL) {
	riseFall = &GC.getRiseFall();
}

CyRiseFall::CyRiseFall(CvRiseFall* riseFallConst) : riseFall(riseFallConst) {
}

CyRFCPlayer* CyRiseFall::getRFCPlayer(int civType) {
	return new CyRFCPlayer(&riseFall->getRFCPlayer((CivilizationTypes)civType));
}

int CyRiseFall::getNumProvinces() {
	return riseFall->getNumProvinces();
}

CyRFCProvince* CyRiseFall::getRFCProvince(int province) {
	return new CyRFCProvince(riseFall->getRFCProvince((ProvinceTypes)province));
}

int CyRiseFall::findRFCProvince(std::string provinceName) {
	return riseFall->findRFCProvince(provinceName.c_str());
}

CyRFCProvince* CyRiseFall::addProvince(std::string provinceType) {
	return new CyRFCProvince(riseFall->addProvince(provinceType.c_str()));
}

void CyRiseFall::setMapFile(std::wstring name) {
	riseFall->setMapFile(name.c_str());
}

std::wstring CyRiseFall::getMapFile() {
	return riseFall->getMapFile();
}
