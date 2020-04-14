/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCCity.h"

CvRFCCity::CvRFCCity() : //only for reading!
year(0),
x(0),
y(0),
population(0)
{
}

CvRFCCity::CvRFCCity(int constYear, int constX, int constY, int constPopulation) :
year(constYear),
x(constX),
y(constY),
population(constPopulation)
{
}

CvRFCCity::~CvRFCCity() {
}

int CvRFCCity::getYear() const {
	return year;
}

int CvRFCCity::getX() const {
	return x;
}

int CvRFCCity::getY() const {
	return y;
}

int CvRFCCity::getPopulation() const {
	return population;
}

void CvRFCCity::write(FDataStreamBase* stream) {
	stream->Write(year);
	stream->Write(x);
	stream->Write(y);
	stream->Write(population);
}

void CvRFCCity::read(FDataStreamBase* stream) {
	stream->Read(&year);
	stream->Read(&x);
	stream->Read(&y);
	stream->Read(&population);
}