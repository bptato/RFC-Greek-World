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
		CyRFCProvince* getRFCProvinceByName(std::wstring provinceName);
		CyRFCProvince* addProvince(std::wstring provinceName, int bottom, int left, int top, int right);
		void setMapFile(std::wstring name);
		std::wstring getMapFile();
	protected:
		CvRiseFall* riseFall;
};
