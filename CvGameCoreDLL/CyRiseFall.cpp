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

CyRFCProvince* CyRiseFall::getRFCProvinceByName(std::wstring provinceName) {
	return new CyRFCProvince(riseFall->getRFCProvince(provinceName.c_str()));
}

CyRFCProvince* CyRiseFall::addProvince(std::wstring provinceName, int bottom, int left, int top, int right) {
	return new CyRFCProvince(riseFall->addProvince(provinceName.c_str(), bottom, left, top, right));
}

void CyRiseFall::setMapFile(std::wstring name) {
	riseFall->setMapFile(name.c_str());
}

std::wstring CyRiseFall::getMapFile() {
	return riseFall->getMapFile();
}
