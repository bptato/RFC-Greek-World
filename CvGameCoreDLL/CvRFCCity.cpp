/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCCity.h"

CvRFCCity::CvRFCCity() {
	init();
}

CvRFCCity::~CvRFCCity() {
	uninit();
}

void CvRFCCity::reset() {
	uninit();
	init();
}

void CvRFCCity::init() {
	_year = 0;
	_y = 0;
	_x = 0;
	_population = 0;
	_buildings = new int[GC.getNumBuildingInfos()];
	for(int i = 0; i < GC.getNumBuildingInfos(); ++i) {
		_buildings[i] = 0;
	}
	_religions = new bool[GC.getNumReligionInfos()];
	for(int i = 0; i < GC.getNumReligionInfos(); ++i) {
		_religions[i] = 0;
	}
	_holyCityReligions = new bool[GC.getNumReligionInfos()];
	for(int i = 0; i < GC.getNumReligionInfos(); ++i) {
		_holyCityReligions[i] = 0;
	}
	_culture = new int[GC.getNumCivilizationInfos()];
	for(int i = 0; i < GC.getNumCivilizationInfos(); ++i) {
		_culture[i] = 0;
	}
}

void CvRFCCity::uninit() {
	SAFE_DELETE_ARRAY(_buildings);
	SAFE_DELETE_ARRAY(_religions);
	SAFE_DELETE_ARRAY(_holyCityReligions);
	SAFE_DELETE_ARRAY(_culture);
}

void CvRFCCity::setYear(int year) {
	_year = year;
}

void CvRFCCity::setX(int x) {
	_x = x;
}

void CvRFCCity::setY(int y) {
	_y = y;
}

void CvRFCCity::setPopulation(int population) {
	_population = population;
}

void CvRFCCity::setNumBuilding(BuildingTypes building, int value) {
	FAssert(building >= 0);
	FAssert(building < GC.getNumBuildingInfos());
	_buildings[building] = value;
}

void CvRFCCity::setReligion(ReligionTypes religion, bool value) {
	FAssert(religion >= 0);
	FAssert(religion < GC.getNumReligionInfos());
	_religions[religion] = value;
}

void CvRFCCity::setHolyCityReligion(ReligionTypes religion, bool value) {
	FAssert(religion >= 0);
	FAssert(religion < GC.getNumReligionInfos());
	_holyCityReligions[religion] = value;
}

void CvRFCCity::setCulture(CivilizationTypes civType, int value) {
	FAssert(civType >= 0);
	FAssert(civType < GC.getNumCivilizationInfos());
	_culture[civType] = value;
}


int CvRFCCity::getYear() const {
	return _year;
}

int CvRFCCity::getX() const {
	return _x;
}

int CvRFCCity::getY() const {
	return _y;
}

int CvRFCCity::getPopulation() const {
	return _population;
}

int CvRFCCity::getNumBuilding(BuildingTypes building) const {
	FAssert(building >= 0);
	FAssert(building < GC.getNumBuildingInfos());
	return _buildings[building];
}

bool CvRFCCity::getReligion(ReligionTypes religion) const {
	FAssert(religion >= 0);
	FAssert(religion < GC.getNumReligionInfos());
	return _religions[religion];
}

bool CvRFCCity::getHolyCityReligion(ReligionTypes religion) const {
	FAssert(religion >= 0);
	FAssert(religion < GC.getNumReligionInfos());
	return _holyCityReligions[religion];
}

int CvRFCCity::getCulture(CivilizationTypes civType) const {
	FAssert(civType >= 0);
	FAssert(civType < GC.getNumCivilizationInfos());
	return _culture[civType];
}


void CvRFCCity::write(FDataStreamBase* stream) {
	stream->Write(_year);
	stream->Write(_x);
	stream->Write(_y);
	stream->Write(_population);
	stream->Write(GC.getNumBuildingInfos(), _buildings);
	stream->Write(GC.getNumReligionInfos(), _religions);
	stream->Write(GC.getNumReligionInfos(), _holyCityReligions);
	stream->Write(GC.getNumCivilizationInfos(), _culture);
}

void CvRFCCity::read(FDataStreamBase* stream) {
	reset();
	stream->Read(&_year);
	stream->Read(&_x);
	stream->Read(&_y);
	stream->Read(&_population);
	stream->Read(GC.getNumBuildingInfos(), _buildings);
	stream->Read(GC.getNumReligionInfos(), _religions);
	stream->Read(GC.getNumReligionInfos(), _holyCityReligions);
	stream->Read(GC.getNumCivilizationInfos(), _culture);
}
