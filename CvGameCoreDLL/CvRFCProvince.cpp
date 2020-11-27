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
	_plots.clear();
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
	GC.logMsg("Province units amount: %d", provinceUnits.size());
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

				GC.logMsg("Mercenary creation odds: %d", mercOdds);
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
				for(int i = 0; i < GC.getRiseFall().getNumProvinces(); ++i) {
					if(isBorderProvince((ProvinceTypes)i)) {
						++borderProvinces;
					}
				}
				int rand = 0;
				for(int i = 0; i < GC.getRiseFall().getNumProvinces(); ++i) {
					if(isBorderProvince((ProvinceTypes)i)) {
						rand += 100/borderProvinces;
						if(100/borderProvinces<GC.getGame().getSorenRandNum(rand, "Border province selection roll")) {
							GC.getRiseFall().getProvince((ProvinceTypes)i).addMercenary(*it);
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

void CvRFCProvince::addPlot(int plotid) {
	FAssert(plotid < GC.getMap().numPlots());
	_plots.push_back(plotid);
}

void CvRFCProvince::removePlot(int plotid) {
	for(std::vector<int>::iterator it = _plots.begin(); it != _plots.end(); ++it) {
		if(*it == plotid) {
			_plots.erase(it);
			return;
		}
	}
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
	for(std::vector<int>::iterator it = _plots.begin(); it != _plots.end(); ++it) {
		CvPlot* plot = GC.getMapINLINE().plotByIndexINLINE(*it);
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

std::vector<int>& CvRFCProvince::getPlots() {
	return _plots;
}

int CvRFCProvince::getNumCities(PlayerTypes playerType) const {
	int i;
	int countedCities = 0;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(city->plot()->getProvinceType() == getProvinceType()) {
			++countedCities;
		}
	}
	return countedCities;
}

CvCity* CvRFCProvince::getFirstCity(PlayerTypes playerType) {
	int i;
	for(CvCity* city = GET_PLAYER(playerType).firstCity(&i); city != NULL; city = GET_PLAYER(playerType).nextCity(&i)) {
		if(city->plot()->getProvinceType() == getProvinceType()) {
			return city;
		}
	}
	return NULL;
}

bool CvRFCProvince::isBorderProvince(ProvinceTypes province) {
	for(std::vector<int>::iterator it = getPlots().begin(); it != getPlots().end(); ++it) {
		if(GC.getMapINLINE().plotByIndexINLINE(*it)->getProvinceType() == getProvinceType()) {
			int x = GC.getMapINLINE().plotByIndexINLINE(*it)->getX();
			int y = GC.getMapINLINE().plotByIndexINLINE(*it)->getY();
			if(GC.getMapINLINE().isPlotINLINE(x, y - 1))
				if(GC.getMapINLINE().plotINLINE(x, y - 1)->getProvinceType() == province)
					return true;
			if(GC.getMapINLINE().isPlotINLINE(x, y + 1))
				if(GC.getMapINLINE().plotINLINE(x, y + 1)->getProvinceType() == province)
					return true;
			if(GC.getMapINLINE().isPlotINLINE(x + 1, y))
				if(GC.getMapINLINE().plotINLINE(x + 1, y)->getProvinceType() == province)
					return true;
			if(GC.getMapINLINE().isPlotINLINE(x - 1, y))
				if(GC.getMapINLINE().plotINLINE(x - 1, y)->getProvinceType() == province)
					return true;
		}
	}
	return false;
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

	{
		uint size = _plots.size();
		stream->Write(size);
		for(std::vector<int>::iterator it = _plots.begin(); it != _plots.end(); ++it) {
			stream->Write(*it);
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

	{
		_plots.clear();
		uint size;
		stream->Read(&size);
		for(uint i = 0; i < size; i++) {
			int plotid;
			stream->Read(&plotid);
			_plots.push_back(plotid);
		}
	}
}
