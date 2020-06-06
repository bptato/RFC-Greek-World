/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCUnit.h"

CvRFCUnit::CvRFCUnit() :
_year(0),
_x(0),
_y(0),
_unitType(NO_UNIT),
_unitAIType(NO_UNITAI),
_facingDirection(NO_DIRECTION),
_amount(0),
_endYear(0),
_spawnFrequency(0),
_lastSpawned(0)
{
}

CvRFCUnit::~CvRFCUnit() {

}

void CvRFCUnit::setYear(int year) {
	_year = year;
}

void CvRFCUnit::setX(int x) {
	_x = x;
}

void CvRFCUnit::setY(int y) {
	_y = y;
}

void CvRFCUnit::setUnitType(UnitTypes unitType) {
	_unitType = unitType;
}

void CvRFCUnit::setUnitAIType(UnitAITypes unitAIType) {
	_unitAIType = unitAIType;
}

void CvRFCUnit::setFacingDirection(DirectionTypes facingDirection) {
	_facingDirection = facingDirection;
}

void CvRFCUnit::setAmount(int amount) {
	_amount = amount;
}

void CvRFCUnit::setEndYear(int endYear) {
	_endYear = endYear;
}

void CvRFCUnit::setSpawnFrequency(int spawnFrequency) {
	_spawnFrequency = spawnFrequency;
}

void CvRFCUnit::setLastSpawned(int turn) {
	_lastSpawned = turn;
}


int CvRFCUnit::getLastSpawned() const {
	return _lastSpawned;
}

int CvRFCUnit::getYear() const {
	return _year;
}

int CvRFCUnit::getEndYear() const { //only for province barb spawning, returns the end of barb wave
	return _endYear;
}

int CvRFCUnit::getX() const {
	return _x;
}

int CvRFCUnit::getY() const {
	return _y;
}

UnitTypes CvRFCUnit::getUnitType() const {
	return _unitType;
}

UnitAITypes CvRFCUnit::getUnitAIType() const {
	return _unitAIType;
}

int CvRFCUnit::getAmount() const {
	return _amount;
}

int CvRFCUnit::getSpawnFrequency() const { //only for province barb spawning, returns how often barbs are spawned
	return _spawnFrequency;
}

DirectionTypes CvRFCUnit::getFacingDirection() const {
	return _facingDirection;
}

void CvRFCUnit::write(FDataStreamBase* stream) {
	stream->Write(_year);
	stream->Write(_x);
	stream->Write(_y);
	stream->Write(_unitType);
	stream->Write(_unitAIType);
	stream->Write(_facingDirection);
	stream->Write(_amount);
	stream->Write(_endYear);
	stream->Write(_spawnFrequency);
	stream->Write(_lastSpawned);
}

void CvRFCUnit::read(FDataStreamBase* stream) {
	stream->Read(&_year);
	stream->Read(&_x);
	stream->Read(&_y);
	stream->Read((int*)&_unitType);
	stream->Read((int*)&_unitAIType);
	stream->Read((int*)&_facingDirection);
	stream->Read(&_amount);
	stream->Read(&_endYear);
	stream->Read(&_spawnFrequency);
	stream->Read(&_lastSpawned);
}
