/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCCity.h"

CvRFCCity::CvRFCCity() : //only for reading!
_year(0),
_x(0),
_y(0),
_population(0)
{
}

CvRFCCity::CvRFCCity(int year, int x, int y) :
_year(year),
_x(x),
_y(y),
_population(0)
{
}

CvRFCCity::~CvRFCCity() {
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

void CvRFCCity::write(FDataStreamBase* stream) {
	stream->Write(_year);
	stream->Write(_x);
	stream->Write(_y);
	stream->Write(_population);
}

void CvRFCCity::read(FDataStreamBase* stream) {
	stream->Read(&_year);
	stream->Read(&_x);
	stream->Read(&_y);
	stream->Read(&_population);
}
