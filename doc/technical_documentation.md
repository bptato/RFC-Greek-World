# Technical documentation of the RFGW engine

Table of contents:

- [Overview](#overview)
	- [About this mod](#about-this-mod)
	- [About this documentation](#about-this-documentation)
- [Code Description](#code-description)
	- [Python](#python)
		- [RFGWB](#rfgwb)
		- [Victory](#victory)
		- [Miscellaneous](#miscellaneous-python)
	- [XML](#xml)
		- [GlobalDefines](#globaldefines)
		- [CIV4CivilizationInfos](#civ4civilizationinfos)
		- [Miscellaneous](#miscellaneous-xml)
	- [DLL](#dll)
		- [CvEnums](#cvenums)
		- [CvRiseFall](#cvrisefall)
		- [CvRFCPlayer](#cvrfcplayer)
		- [CvRFCProvince](#cvrfcprovince)
		- [CvRFCUnit](#cvrfcunit)
		- [CvRFCCity](#cvrfccity)
		- [CvRFCMercenary](#cvrfcmercenary)
		- [CvGame](#cvgame)
		- [CvPlayer](#cvplayer)
		- [CvUnit](#cvunit)
		- [CvEventReporter](#cveventreporter)
		- [CvCity](#cvcity)
		- [CvPlayerAI](#cvplayerai)
		- [CvPlot](#cvplot)
		- [Miscellaneous](#miscellaneous-dll)

## Overview
While the RFGW engine is in a way far simpler than the original Rhye's and Fall engine (or its derivatives), it's also completely different in almost every aspect. RFC has tons of resources on how to modify it, but RFGW 2.0 has been until now almost completely undocumented. Therefore I'm creating this documentation to help future me and potentially others understand how this thing can be modified.  
Note that this isn't a tutorial or manual, just a short documentation of the code (similar to that of SoI, albeit a bit more detailed).

## About this mod
After working with the old RFGW code for a while, it slowly became clear to me that trying to fix it was a futile effort. It had way too many arcane mechanisms that didn't even work correctly, and inherited quite a few of bugs and poorly maintainable features from RFC. Therefore I decided to rewrite the entire RFC engine from the ground up, which made my plans like merging PlatyBuilder, decoupling civ slots from civ types, merging common scenario data, improving the painful process of editing city names and settler maps, etc. far easier to achieve.

My intentions when designing RFGW 2.0 were:

1. To make as few assumptions as possible (i.e. very few hardcoded values), making it easier to reuse.
2. To do as little work as possible (and by extension be faster than RFC), by calculating and storing most values and objects at the beginning of the game and doing most logic in the DLL.
3. To interfere with the game's code as little as possible, making it relatively easier to merge with other mods.

## About this documentation
The Description texts detail _how_ things work, the What to change texts detail _what_ one should change when creating a new mod based on RFGW. Former is mainly useful for merging, maintenance and regular development, the latter for modmods.

### Python
#### RFGWB
Location: `Assets/Python/pyWB/RFGWB.py`

Description:  
`RFGWB.py` replaces the BtS scenario parser. It can load regular Civ4 scenarios (albeit only the terrain), and RFGW scenarios. It can also save RFGW scenarios by creating an internal JSON representation of the current game and dumping it into different files.

RFGW scenarios are regular JSON files, with the string `application/json` on the first line. They consist of two files: the map file, which may be shared between scenarios (see `GreekWorld` in RFGW), and the scenario file (see `4400 BC[...].CivBeyondSwordSave`).

Map files store general data about the map (size etc.), terrain data, and province data.

Scenario files store everything else that shouldn't be shared between scenarios: game-options, civilization-specific data (modifiers, starting year, starting techs, starting wars, core provinces), unit data (when and where units should be spawned), city data (when and where cities should be spawned), and barbarian unit data (units tied to specific provinces instead of plots).

`RFGWB.py` works by first loading the scenario selected in the main menu. Then it is determined whether the loaded file is a RFGWB scenario file or a regular scenario file; if it's the latter, the legacy wbSave parser is used. Otherwise, the scenario and map files are loaded using simplejson. In the end, all values are stored in Python dictionaries.

Then, the `buildMap` function calls all required DLL functions to build a map based on the dictionary's values. This mostly consists of RFGW-specific functions, but also includes a few regular BtS ones. Note that no players, units, cities, etc. are spawned yet, those are handled later by the DLL.

#### Victory
Location: `Assets/Python/Victory.py`

What to change:  
Whatever you would change in RFC (`checkPlayerTurn`, etc.), global variables in initGlobals, and civilization types on the top of the file.

Description:  
In RFC, calling gc.getPlayer(iEgypt) (where iEgypt is 0 due to Egypt being the first player) is guaranteed to result in a player representing Egypt; in RFGW, this is **not** the case.

If Egypt is destroyed, another civilization may occupy its slot; in this example, you may be unpleasantly surprised when gc.getPlayer(iEgypt) returns the Assyrian player. Therefore it is important to always identify civilizations by their type, using `gc.getPlayer(iPlayer).getCivilizationType()` or the equivalent helper function `player2civ`. Conversely, the player type of a civilization type may be retrieved with `civ2player`; this will return `PlayerTypes.NO_PLAYER` (-1) if the player is not alive.

Other differences are that years are calculated dynamically as in SoI; however, that is only done once every game (or reload) in the initGlobals function, where province pointers are also retrieved and stored.

#### Miscellaneous Python
Location: `Assets/Python/`

Description:  
There are a few miscellaneous Python modifications and additions that don't warrant their own section:

- `CvEventManager.py`: free Hunnic and Germanic units, `Victory.py` event triggers
- `CvGameUtils.py`: getSettlerValueDescription function
- `simplejson.py`: JSON parser
- `OrderedDict.py`: Backport of OrderedDict, to allow saving JSON attributes in a consistent order
- `EntryPoints/CvWBInterface.py`: adjusted to cooperate with `RFGWB.py`; also calls `setupEnabled` to notify the DLL when civilization descriptions should be faked
- `EntryPoints/CvScreensInterface.py`: some functions that need to be exposed to the DLL
- `EntryPoints/CvRandomEventInterface.py`: some random events were removed/modified
- `StringUtils.py`: functions related to strings
- `Screens/CvDawnOfMan.py`: a slightly different Dawn of Man slider implementation
- `Screens/CvMercenariesScreen.py`: mercenaries
- `Screens/CvMainInterface.py`: mercenaries
- PlatyBuilder: some parts of it were modified, but its files remain in the same place

### XML
#### GlobalDefines
Location: `Assets/XML/GlobalDefines.xml`

What to change:  
Everything from `MERCENARY_DISBAND_RATE` is RFGW-specific and may be changed.

Description:

- `MERCENARY_DISBAND_RATE`: chance for mercenaries to be disbanded
- `MERCENARY_WANDERING_RATE`: chance for mercenaries to move to another province instead of being disbanded
- `MERCENARY_CREATION_RATE`: chance for creation of new mercenaries from barbarians
- `MERCENARY_BASE_HIRE_COST`: minimum cost of hiring a mercenary
- `MERCENARY_HIRE_COST_MODIFIER`: a modifier for calculating the cost of hiring a mercenary
- `MERCENARY_MIN_LAST_ACTION_DIFFERENCE`: how many turns a barbarian has to spend idle in order to have a chance of become a mercenary
- `HOLY_CITY_RELOCATION_RATE`: the chance of a holy city being relocated every time a religion is spread by a missionary


#### CIV4CivilizationInfos
Location: `Assets/XML/Civilizations/CIV4CivilizationInfos.xml`

What to change:  
It is important that civilizations here are added in the same order as in `CvEnums.h`. They should always be in a chronological order, so that they are displayed correctly in the main menu.

#### Miscellaneous XML
Location: `Assets/XML`

Description:  
There's not much to say here, of course there's a bunch of RFGW XML and some modifications to XML Schemas. The easiest way to find those is to search for bluepotato in `CvGameCoreDLL/CvInfos.cpp`.


### DLL
#### CvEnums
Location: `CvGameCoreDLL/CvEnums.h`

What to change:  
The absolute minimum one has to change when adding new civs is adding the civ to the `CivilizationTypes` enum. This should also be done in `CyEnumsInterface.cpp`, so that it's exposed to Python (and can be added to `Victory.py`).

#### CvRiseFall
Location: `CvGameCoreDLL/CvRiseFall.cpp`

What to change:  
Here the only hardcoded thing one would definitely want to change in a new mod is the `skipConditionalSpawn` function.

Description:  
The main function here is `checkTurn`, called every turn, which manages player stability (see also: CvRFCPlayer), city and unit spawning, provinces, etc. Understanding how the implementation works is only necessary if something breaks in it, since all these functions are abstracted away and manageable in scenario files.

#### CvRFCPlayer
Location: `CvGameCoreDLL/CvRFCPlayer.cpp`

What to change:  
Civic compatibility is hardcoded in the `checkStability` function, which one would definitely want to change in a new mod.

Description:  
All playable civilization types on a map receive a CvRFCPlayer object. They store the civilization's human/minor civilization status, modifiers, unit and city spawns, stability, starting turn, etc. These are all exposed to Python so that the scenario parser can send them to the DLL.

Additionally, `checkStability` calculates the player's stability. It is called by CvRiseFall every third turn.

#### CvRFCProvince
Location: `CvGameCoreDLL/CvRFCProvince.cpp`

Description:  
Provinces are loaded at the beginning of the game, and stay the same for the entire game.

Provinces may contain CvRFCUnits and CvRFCMercenaries. The former is currently used for spawning barbarians, the latter for storing mercenaries available for hire in the province.

#### CvRFCUnit
Location: `CvGameCoreDLL/CvRFCUnit.cpp`

Description:  
Internal representation of units spawned throughout the game.

#### CvRFCCity
Location: `CvGameCoreDLL/CvRFCCity.cpp`

Description:  
Internal representation of cities spawned throughout the game.

#### CvRFCMercenary
Location: `CvGameCoreDLL/CvRFCMercenary.cpp`

What to change:  
The Sumerian unique power is hardcoded here. Search for `CIVILIZATION_SUMERIA` to find it.

Description:  
Internal representation of mercenaries available for hire.

#### CvGame
Location: `CvGameCoreDLL/CvGame.cpp`

Description:  
Numerous changes have been made here for RFC-style autoplay to work.

#### CvPlayer
Location: `CvGameCoreDLL/CvPlayer.cpp`

What to change:  
Some unique powers are hardcoded here. Search for `CIVILIZATION_` to find them.

Description:  
Besides the addition of UPs, trading with independents is disabled here. Dynamic names, civilization modifiers and inflation are also implemented here.

#### CvUnit
Location: `CvGameCoreDLL/CvUnit.cpp`

What to change:  
Some unique powers are hardcoded here. Search for `CIVILIZATION_` to find them.

Description:  
Modifications here are mostly for UPs, plus the change allowing players without cities to enter neutral territory.

#### CvEventReporter
Location: `CvGameCoreDLL/CvEventReporter.cpp`

What to change:  
The Persian unique power is hardcoded here. Search for `CIVILIZATION_PERSIA` to find it.

Description:  
Besides UPs, `CvRiseFall::onGameStarted` is also called from here.

#### CvCity
Location: `CvGameCoreDLL/CvCity.cpp`

What to change:  
Some unique powers are hardcoded here. Search for `CIVILIZATION_` to find them.

Description:  
Besides UPs, some modifiers are also implemented here.

#### CvPlayerAI
Location: `CvGameCoreDLL/CvPlayerAI.cpp`

What to change:  
The Hittite unique power is hardcoded here. Search for `CIVILIZATION_HITTITE` to find it.

Description:  
Besides UPs, mercenary logic and some modifiers are also implemented here.

#### CvPlot
Location: `CvGameCoreDLL/CvPlot.cpp`

What to change:  
Some unique powers are hardcoded here. Search for `CIVILIZATION_` to find them.

Description:
Besides UPs, province types and city names of plots are stored here.

#### Miscellaneous DLL
Location: `CvGameCoreDLL/`

Description:  
Again there are some things that don't warrant their own section:

- `CvGameTextMgr.cpp`: modifications to show correct game text
- `CvInfos.cpp`: XML stuff + a hack for displaying civilizations in the correct order
- `CvReplayInfo.cpp`, `CvReplayMessage.cpp`: hacks for displaying replay colors correctly
- `CvGlobals.cpp`: Utility functions and functions for loading CvRiseFall
- `CvInitCore.cpp`: Loads CvRiseFall
- `CvDLLButtonPopup.cpp`: UI stuff
- `Cy*.cpp`: boilerplate functions for communication with Python
