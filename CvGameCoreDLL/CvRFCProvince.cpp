/*
Author: bluepotato
*/
#include "CvGameCoreDLL.h"
#include "CvRFCProvince.h"
#include "CvDLLInterfaceIFaceBase.h"

CvRFCProvince::CvRFCProvince() {
	reset(NO_PROVINCE);
}

CvRFCProvince::~CvRFCProvince() {
	uninit();
}

void CvRFCProvince::init(ProvinceTypes provinceType) {
	_provinceType = provinceType;
}

void CvRFCProvince::reset(ProvinceTypes provinceType) {
	uninit();
	init(provinceType);
	_mercenaries.clear();
	_type.clear();
	_name.clear();
}

void CvRFCProvince::uninit() {
	for(std::vector<CvRFCUnit*>::iterator it = _scheduledUnits.begin(); it != _scheduledUnits.end(); ++it) {
		SAFE_DELETE(*it);
	}
	_scheduledUnits.clear();
}

void CvRFCProvince::setType(CvString type) {
	CvWStringBuffer tmp;
	_type = type;
	tmp.assign("TXT_KEY_");
	tmp.append(type);
	_name = gDLL->getText(tmp.getCString());
}

void CvRFCProvince::setProvinceType(ProvinceTypes provinceType) {
	_provinceType = provinceType;
}

void CvRFCProvince::addMercenary(CvRFCMercenary mercenary) {
	_mercenaries.push_back(mercenary);
}

void CvRFCProvince::checkMercenaries() {
	std::vector<CvUnit*> provinceUnits = getUnits();
	int createdMercs = 0;
	for(std::vector<CvUnit*>::iterator it = provinceUnits.begin(); it != provinceUnits.end(); ++it) {
		CvUnit* unit = *it;
		CvPlayer& unitOwner = GET_PLAYER(unit->getOwner());
		if(!unit->isAnimal() && (unitOwner.isBarbarian() || unitOwner.isMinorCiv())) {
			static int minLastActionDifference = GC.getDefineINT("MERCENARY_MIN_LAST_ACTION_DIFFERENCE");
			if(GC.getGame().getGameTurn() - unit->getLastAction() >= minLastActionDifference) {
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
					if(!createdMercs) {
						for(int i = 0; i<MAX_CIV_PLAYERS; ++i) {
							CvPlayer& player = GET_PLAYER((PlayerTypes)i);
							if(player.isHuman()) {
								if(getNumCities((PlayerTypes)i)>0) {
									CvWString msg = gDLL->getText("TXT_KEY_NEW_MERCENARIES", getName());
									gDLL->getInterfaceIFace()->addMessage((PlayerTypes)i, true, GC.getEVENT_MESSAGE_TIME(), msg, "", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"));
								}
							}
						}
					}
					++createdMercs;
				}
			}
		}
	}

	for(std::vector<CvRFCMercenary>::iterator it = _mercenaries.begin(); it != _mercenaries.end();) {
		static int disbandRate = GC.getDefineINT("MERCENARY_DISBAND_RATE");
		static int wanderingRate = GC.getDefineINT("MERCENARY_WANDERING_RATE");
		if(GC.getGame().getSorenRandNum(100, "Mercenary disband roll") < disbandRate) {
			if(GC.getGame().getSorenRandNum(100, "Mercenary wandering roll") < wanderingRate) {
				int borderProvinces = 0;
				for(int i = 0; i<GC.getRiseFall().getNumProvinces(); ++i) {
					if(GC.getRiseFall().isBorderProvince(getProvinceType(), (ProvinceTypes)i)) {
						++borderProvinces;
					}
				}
				int rand = 0;
				for(int i = 0; i<GC.getRiseFall().getNumProvinces(); ++i) {
					if(GC.getRiseFall().isBorderProvince(getProvinceType(), (ProvinceTypes)i)) {
						rand += 100/borderProvinces;
						if(100/borderProvinces<GC.getGame().getSorenRandNum(rand, "Border province selection roll")) {
							GC.getRiseFall().getRFCProvince((ProvinceTypes)i)->addMercenary(*it);
							break;
						}
					}
				}
			}
			it = _mercenaries.erase(it);
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

	_mercenaries.erase(_mercenaries.begin() + mercenaryID);
}


const char* CvRFCProvince::getType() const {
	return _type;
}

ProvinceTypes CvRFCProvince::getProvinceType() const {
	return _provinceType;
}

const wchar* CvRFCProvince::getName() const {
	return _name;
}

int CvRFCProvince::getNumScheduledUnits() const {
	return _scheduledUnits.size();
}

CvRFCUnit* CvRFCProvince::addScheduledUnit() {
	CvRFCUnit* rfcUnit = new CvRFCUnit();
	_scheduledUnits.push_back(rfcUnit);
	return rfcUnit;
}

CvRFCUnit* CvRFCProvince::getScheduledUnit(int i) const {
	return _scheduledUnits[i];
}

std::vector<CvRFCUnit*>& CvRFCProvince::getScheduledUnits() {
	return _scheduledUnits;
}

int CvRFCProvince::getNumMercenaries() const {
	return _mercenaries.size();
}

CvRFCMercenary& CvRFCProvince::getMercenary(int i) {
	return _mercenaries[i];
}

std::vector<CvRFCMercenary>& CvRFCProvince::getMercenaries() {
	return _mercenaries;
}

std::vector<CvUnit*> CvRFCProvince::getUnits() {
	std::vector<CvUnit*> units;
	for(int i = 0; i < GC.getMap().numPlots(); ++i) {
		CvPlot* plot = GC.getMap().plotByIndex(i);
		if(plot->isUnit()) {
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

	return units;
}

int CvRFCProvince::getNumCities(PlayerTypes playerType) const {
	int i;
	int countedCities = 0;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(GC.getRiseFall().getRFCProvince(city->plot()->getProvinceType()) == this) {
			++countedCities;
		}
	}
	return countedCities;
}

CvCity* CvRFCProvince::getFirstCity(PlayerTypes playerType) {
	int i;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(GC.getRiseFall().getRFCProvince(city->plot()->getProvinceType()) == this) {
			return city;
		}
	}
	return NULL;
}


void CvRFCProvince::write(FDataStreamBase* stream) {
	stream->WriteString(_type);
	stream->Write(_provinceType);
	stream->WriteString(_name);

	{
		uint size = _scheduledUnits.size();
		stream->Write(size);
		for(std::vector<CvRFCUnit*>::iterator it = _scheduledUnits.begin(); it != _scheduledUnits.end(); ++it) {
			(*it)->write(stream);
		}
	}

	{
		uint size = _mercenaries.size();
		stream->Write(size);
		for(std::vector<CvRFCMercenary>::iterator it = _mercenaries.begin(); it != _mercenaries.end(); ++it) {
			it->write(stream);
		}
	}
}

void CvRFCProvince::read(FDataStreamBase* stream) {
	reset(NO_PROVINCE);
	stream->ReadString(_type);
	stream->Read((int*)&_provinceType);
	stream->ReadString(_name);

	{
		_scheduledUnits.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; i++) {
			CvRFCUnit* scheduledUnit = new CvRFCUnit();
			scheduledUnit->read(stream);
			_scheduledUnits.push_back(scheduledUnit);
		}
	}

	{
		_mercenaries.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; i++) {
			CvRFCMercenary mercenary;
			mercenary.read(stream);
			_mercenaries.push_back(mercenary);
		}
	}
}
