#pragma once
/*
Author: bluepotato
*/

class CvRFCCity {
	public:
		CvRFCCity();
		CvRFCCity(int year, int x, int y);
		~CvRFCCity();

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setPopulation(int population);

		int getYear() const;
		int getX() const;
		int getY() const;
		int getPopulation() const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int _year;
		int _x;
		int _y;
		int _population;
};
