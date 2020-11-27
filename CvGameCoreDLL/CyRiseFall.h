#pragma once
/*
Author: bluepotato
*/
class CvRiseFall;
class CyRFCPlayer;
class CyRFCProvince;

class CyRiseFall {
	public:
		CyRiseFall();
		CyRiseFall(CvRiseFall* riseFallConst);

		CyRFCPlayer* getRFCPlayer(int civType);
		int getNumProvinces();
		CyRFCProvince* getRFCProvince(int province);
		int findRFCProvince(std::string provinceType);
		CyRFCProvince* addProvince(std::string provinceType);
		void setMapFile(std::wstring name);
		std::wstring getMapFile();
	protected:
		CvRiseFall* riseFall;
};
