#pragma once
/*
Author: bluepotato
*/

class CvRFCUnit {
	public:
		CvRFCUnit();
		CvRFCUnit(int year, int x, int y, UnitTypes unitType, UnitAITypes unitAIType, DirectionTypes facingDirection, int amount);
		CvRFCUnit(int year, UnitTypes unitType, UnitAITypes unitAIType, DirectionTypes facingDirection, int amount, int endYear, int spawnFrequency);
		~CvRFCUnit();

		void setLastSpawned(int lastSpawned);

		int getYear() const;
		int getX() const;
		int getY() const;
		UnitTypes getUnitType() const;
		UnitAITypes getUnitAIType() const;
		DirectionTypes getFacingDirection() const;
		int getAmount() const;
		int getEndYear() const;
		int getSpawnFrequency() const;
		int getLastSpawned() const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int year;
		int x;
		int y;
		UnitTypes unitType;
		UnitAITypes unitAIType;
		DirectionTypes facingDirection;
		int amount;
		int endYear;
		int spawnFrequency;
		int lastSpawned;
};