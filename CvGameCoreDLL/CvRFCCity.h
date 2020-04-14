#pragma once
/*
Author: bluepotato
*/

class CvRFCCity {
	public:
		CvRFCCity();
		CvRFCCity(int year, int x, int y, int population);
		~CvRFCCity();

		int getYear() const;
		int getX() const;
		int getY() const;
		int getPopulation() const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int year;
		int x;
		int y;
		int population;
};