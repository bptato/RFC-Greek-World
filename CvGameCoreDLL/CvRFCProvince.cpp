/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCProvince.h"

CvRFCProvince::CvRFCProvince() {
	reset();
}

CvRFCProvince::~CvRFCProvince() {
	uninit();
}

void CvRFCProvince::init() {
	reset();
}

void CvRFCProvince::reset() {
	uninit();
	bottom = -1;
	right = -1;
	top = -1;
	left = -1;
}

void CvRFCProvince::uninit() {
	name.clear();
	scheduledUnits.clear();
	mercenaries.clear();
}

void CvRFCProvince::setName(const wchar* newName) {
	CvWString cvwNewName(newName);
	name = cvwNewName;
}

void CvRFCProvince::setBounds(int newBottom, int newLeft, int newTop, int newRight) {
	bottom = newBottom;
	left = newLeft;
	top = newTop;
	right = newRight;
}

void CvRFCProvince::scheduleUnit(CvRFCUnit scheduledUnit) {
	scheduledUnits.push_back(scheduledUnit);
}

void CvRFCProvince::addMercenary(CvRFCMercenary mercenary) {
	mercenaries.push_back(mercenary);
}

void CvRFCProvince::checkMercenaries() {
	std::vector<CvUnit*> provinceUnits = getUnits();
	int createdMercs = 0;
	for(std::vector<CvUnit*>::iterator it = provinceUnits.begin(); it != provinceUnits.end(); ++it) {
		CvUnit* unit = *it;
		CvPlayer& unitOwner = GET_PLAYER(unit->getOwner());
		if(!unit->isAnimal() && (unitOwner.isBarbarian() || unitOwner.isMinorCiv())) {
			static int minLastActionDifference = GC.getDefineINT("MERCENARY_MIN_LAST_ACTION_DIFFERENCE");
			if(unit->getLastAction() != 0 && GC.getGame().getGameTurn() - unit->getLastAction() >= minLastActionDifference) {
				static int mercRate = GC.getDefineINT("MERCENARY_CREATION_RATE");
				int mercOdds = mercRate;
				if(createdMercs > 0) {
					mercOdds /= createdMercs;
				}

				if(unit->plot()->isCity()) {
					if(unit->plot()->getNumDefenders(unit->getOwner()) > 1) {
						mercOdds *= unit->plot()->getNumDefenders(unit->getOwner());
						mercOdds /= 4;
					} else {
						mercOdds = 0;
					}
				}

				if(unit->getLeaderUnitType() != NO_UNIT) {
					mercOdds /= 2;
				}

				if(GC.getGame().getSorenRandNum(100, "Mercenary creation roll") < mercOdds) {
					UnitTypes unitType = unit->getUnitType();
					int hireCost = GC.getUnitInfo(unitType).getProductionCost() * (unit->getLevel()+1) + (unit->getLevel()+1) * std::abs(unit->getExperience() - unit->experienceNeeded());

					static int hireCostModifier = GC.getDefineINT("MERCENARY_HIRE_COST_MODIFIER");
					static int baseHireCost = GC.getDefineINT("MERCENARY_BASE_HIRE_COST");
					hireCost *= hireCostModifier;
					hireCost /= 100;

					hireCost += baseHireCost;

					int maintenanceCostModifier = unitOwner.getCurrentEra();
					maintenanceCostModifier *= 30;
					maintenanceCostModifier /= 100;

					int baseMaintenanceCost = 2;

					int maintenanceCost = unit->getLevel() * 3;
					maintenanceCost += hireCost * 5 * maintenanceCostModifier / 100 / 100;
					maintenanceCost += baseMaintenanceCost;
					//maintenance cost modifier
					maintenanceCost *= 15;
					maintenanceCost /= 100;

					CvRFCMercenary mercenary(hireCost, maintenanceCost, unit->getExperience(), unitType);
					for(int i = 0; i<GC.getNumPromotionInfos(); ++i) {
						if(unit->isHasPromotion((PromotionTypes)i)) {
							mercenary.addPromotion((PromotionTypes)i);
						}
					}
					addMercenary(mercenary);
					unit->kill(false);
					++createdMercs;
				}
			}
		}
	}

	for(std::vector<CvRFCMercenary>::iterator it = mercenaries.begin(); it != mercenaries.end();) {
		static int disbandRate = GC.getDefineINT("MERCENARY_DISBAND_RATE");
		static int wanderingRate = GC.getDefineINT("MERCENARY_WANDERING_RATE");
		if(GC.getGame().getSorenRandNum(100, "Mercenary disband roll") < disbandRate) {
			if(GC.getGame().getSorenRandNum(100, "Mercenary wandering roll") < wanderingRate) {
				int borderProvinces = 0;
				for(int i = 0; i<GC.getRiseFall().getNumProvinces(); ++i) {
					if(isBorderProvince(GC.getRiseFall().getRFCProvince(i))) {
						++borderProvinces;
					}
				}
				int rand = 0;
				for(int i = 0; i<GC.getRiseFall().getNumProvinces(); ++i) {
					if(isBorderProvince(GC.getRiseFall().getRFCProvince(i))) {
						rand += 100/borderProvinces;
						if(100/borderProvinces<GC.getGame().getSorenRandNum(rand, "Border province selection roll")) {
							GC.getRiseFall().getRFCProvince(i)->addMercenary(*it);
							break;
						}
					}
				}
			}
			it = mercenaries.erase(it);
		} else {
			++it;
		}
	}
}

void CvRFCProvince::hireMercenary(PlayerTypes playerType, int mercenaryID) {
	CvPlayer& player = GET_PLAYER(playerType);
	CvRFCMercenary& mercenary = getMercenary(mercenaryID);
	FAssert(player.getGold() >= mercenary.getHireCost());


	CvCity* city = getFirstCity(playerType);
	FAssert(city != NULL);

	player.changeGold(-mercenary.getHireCost());
	CvUnit* mercUnit = player.initUnit(mercenary.getUnitType(), city->getX(), city->getY(), NO_UNITAI, DIRECTION_SOUTH, mercenary.getMaintenanceCost());
	mercUnit->setExperience(mercenary.getExperience());
	for(int i = 0; i<mercenary.getNumPromotions(); ++i) {
		mercUnit->setHasPromotion(mercenary.getPromotion(i), true);
	}
	mercUnit->setHasPromotion((PromotionTypes)GC.getInfoTypeForString("PROMOTION_MERCENARY"), true);

	mercenaries.erase(mercenaries.begin() + mercenaryID);
}


const wchar* CvRFCProvince::getName() const {
	return name;
}

bool CvRFCProvince::isInBounds(int x, int y) const {
	return x >= left && x <= right && y >= bottom && y <= top;
}

bool CvRFCProvince::isBorderProvince(CvRFCProvince* province) const { //check if another province overlaps or neighbors this province.
	if(province == this) {
		return false;
	}

	for(int x = left-1; x<=right+1; x++) {
		for(int y = bottom-1; y<=top+1; y++) {
			if(province->isInBounds(x, y)) {
				return true;
			}
		}
	}
	return false;
}

int CvRFCProvince::getBottom() const {
	return bottom;
}

int CvRFCProvince::getLeft() const {
	return left;
}

int CvRFCProvince::getTop() const {
	return top;
}

int CvRFCProvince::getRight() const {
	return right;
}

int CvRFCProvince::getNumScheduledUnits() const {
	return scheduledUnits.size();
}

CvRFCUnit& CvRFCProvince::getScheduledUnit(int i) {
	return scheduledUnits[i];
}

std::vector<CvRFCUnit>& CvRFCProvince::getScheduledUnits() {
	return scheduledUnits;
}

int CvRFCProvince::getNumMercenaries() const {
	return mercenaries.size();
}

CvRFCMercenary& CvRFCProvince::getMercenary(int i) {
	return mercenaries[i];
}

std::vector<CvRFCMercenary>& CvRFCProvince::getMercenaries() {
	return mercenaries;
}

std::vector<CvUnit*> CvRFCProvince::getUnits() {
	std::vector<CvUnit*> units;
	CLinkList<IDInfo> plotUnits;
	for(int x = left; x<=right; ++x) {
		for(int y = bottom; y<=top; ++y) {
			CvPlot* plot = GC.getMap().plot(x, y);
			if(plot->isUnit()) {
				plotUnits.clear();

				CLLNode<IDInfo>* unitNode = plot->headUnitNode();
				while(unitNode != NULL) {
					CvUnit* loopUnit = ::getUnit(unitNode->m_data);
					if(loopUnit != NULL) {
						units.push_back(loopUnit);
					}
					unitNode = plot->nextUnitNode(unitNode);
				}
			}
		}
	}

	return units;
}

int CvRFCProvince::getNumCities(PlayerTypes playerType) const {
	int i;
	int countedCities = 0;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(isInBounds(city->getX(), city->getY())) {
			countedCities++;
		}
	}
	return countedCities;
}

CvCity* CvRFCProvince::getFirstCity(PlayerTypes playerType) {
	int i;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(isInBounds(city->getX(), city->getY())) {
			return city;
		}
	}
	return NULL;
}


void CvRFCProvince::write(FDataStreamBase* stream) {
	stream->WriteString(name);
	stream->Write(bottom);
	stream->Write(left);
	stream->Write(top);
	stream->Write(right);

	{
		uint size = scheduledUnits.size();
		stream->Write(size);
		for(std::vector<CvRFCUnit>::iterator it = scheduledUnits.begin(); it != scheduledUnits.end(); ++it) {
			it->write(stream);
		}
	}

	{
		uint size = mercenaries.size();
		stream->Write(size);
		for(std::vector<CvRFCMercenary>::iterator it = mercenaries.begin(); it != mercenaries.end(); ++it) {
			it->write(stream);
		}
	}
}

void CvRFCProvince::read(FDataStreamBase* stream) {
	stream->ReadString(name);
	stream->Read(&bottom);
	stream->Read(&left);
	stream->Read(&top);
	stream->Read(&right);

	{
		scheduledUnits.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; i++) {
			CvRFCUnit scheduledUnit;
			scheduledUnit.read(stream);
			scheduledUnits.push_back(scheduledUnit);
		}
	}

	{
		mercenaries.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; i++) {
			CvRFCMercenary mercenary;
			mercenary.read(stream);
			mercenaries.push_back(mercenary);
		}
	}
}
