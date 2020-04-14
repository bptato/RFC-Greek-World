/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCUnit.h"

CvRFCUnit::CvRFCUnit() : //empty constructor, only for reading!
year(0),
x(0),
y(0),
unitType(NO_UNIT),
unitAIType(NO_UNITAI),
facingDirection(NO_DIRECTION),
amount(0),
endYear(0),
spawnFrequency(0),
lastSpawned(0)
{
}

CvRFCUnit::CvRFCUnit(int constYear, int constX, int constY, UnitTypes constUnitType, UnitAITypes constUnitAIType, DirectionTypes constFacingDirection, int constAmount) : //scheduled unit constructor
year(constYear),
x(constX),
y(constY),
unitType(constUnitType),
unitAIType(constUnitAIType),
facingDirection(constFacingDirection),
amount(constAmount),
endYear(0),
spawnFrequency(0),
lastSpawned(0)
{
}

CvRFCUnit::CvRFCUnit(int constYear, UnitTypes constUnitType, UnitAITypes constUnitAIType, DirectionTypes constFacingDirection, int constAmount, int constEndYear, int constSpawnFrequency) : //barb constructor
year(constYear),
x(-1),
y(-1),
unitType(constUnitType),
unitAIType(constUnitAIType),
facingDirection(constFacingDirection),
amount(constAmount),
endYear(constEndYear),
spawnFrequency(constSpawnFrequency),
lastSpawned(0)
{
}

CvRFCUnit::~CvRFCUnit() {

}

void CvRFCUnit::setLastSpawned(int turn) {
	lastSpawned = turn;
}


int CvRFCUnit::getLastSpawned() const {
	return lastSpawned;
}

int CvRFCUnit::getYear() const {
	return year;
}

int CvRFCUnit::getEndYear() const { //only for province barb spawning, returns the end of barb wave
	return endYear;
}

int CvRFCUnit::getX() const {
	return x;
}

int CvRFCUnit::getY() const {
	return y;
}

UnitTypes CvRFCUnit::getUnitType() const {
	return unitType;
}

UnitAITypes CvRFCUnit::getUnitAIType() const {
	return unitAIType;
}

int CvRFCUnit::getAmount() const {
	return amount;
}

int CvRFCUnit::getSpawnFrequency() const { //only for province barb spawning, returns how often barbs are spawned
	return spawnFrequency;
}

DirectionTypes CvRFCUnit::getFacingDirection() const {
	return facingDirection;
}

void CvRFCUnit::write(FDataStreamBase* stream) {
	stream->Write(year);
	stream->Write(x);
	stream->Write(y);
	stream->Write(unitType);
	stream->Write(unitAIType);
	stream->Write(facingDirection);
	stream->Write(amount);
	stream->Write(endYear);
	stream->Write(spawnFrequency);
	stream->Write(lastSpawned);
}

void CvRFCUnit::read(FDataStreamBase* stream) {
	stream->Read(&year);
	stream->Read(&x);
	stream->Read(&y);
	stream->Read((int*)&unitType);
	stream->Read((int*)&unitAIType);
	stream->Read((int*)&facingDirection);
	stream->Read(&amount);
	stream->Read(&endYear);
	stream->Read(&spawnFrequency);
	stream->Read(&lastSpawned);
}