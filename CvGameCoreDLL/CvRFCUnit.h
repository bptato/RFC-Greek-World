#pragma once
/*
Author: bluepotato
*/

class CvRFCUnit {
	public:
		CvRFCUnit();
		~CvRFCUnit();

		void setYear(int year);
		void setX(int x);
		void setY(int y);
		void setUnitType(UnitTypes unitType);
		void setUnitAIType(UnitAITypes unitType);
		void setFacingDirection(DirectionTypes facingDirection);
		void setAmount(int amount);
		void setEndYear(int endYear);
		void setSpawnFrequency(int spawnFrequency);
		void setLastSpawned(int lastSpawned);
		void setAIOnly(bool aiOnly);
		void setDeclareWar(bool declareWar);

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
		bool isAIOnly() const;
		bool isDeclareWar() const;

		void write(FDataStreamBase* stream);
		void read(FDataStreamBase* stream);

	protected:
		int _year;
		int _x;
		int _y;
		UnitTypes _unitType;
		UnitAITypes _unitAIType;
		DirectionTypes _facingDirection;
		int _amount;
		int _endYear;
		int _spawnFrequency;
		int _lastSpawned;
		bool _aiOnly;
		bool _declareWar;
};
