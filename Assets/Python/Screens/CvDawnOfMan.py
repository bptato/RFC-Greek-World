## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import CvUtil
from CvPythonExtensions import *
import StringUtils
import math

ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()

class CvDawnOfMan:
	"Dawn of man screen"
	def __init__(self, iScreenID):
		self.iScreenID = iScreenID
		
		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.X_MAIN_PANEL = 250
		self.Y_MAIN_PANEL = 190
		self.W_MAIN_PANEL = 550
		self.H_MAIN_PANEL = 350
		
		self.iMarginSpace = 15
		
		self.X_TEXT_PANEL = self.X_MAIN_PANEL + self.iMarginSpace * 2
		self.Y_TEXT_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace - 10
		self.W_TEXT_PANEL = int(self.H_MAIN_PANEL * (2.0 / 5.0))
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 3) + 10
		self.iTEXT_PANEL_MARGIN = 35
		
		self.W_EXIT = 120
		self.H_EXIT = 30
		
		self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2)
		self.Y_EXIT = self.Y_MAIN_PANEL + 440
		self.endTurn = 0
				
				
	def interfaceScreen(self):
		'Use a popup to display the opening text'
		if (CyGame().isPitbossHost()):
			return
		
		self.calculateSizesAndPositions()
		
		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())
		
		# Create screen
		
		screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)		
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground(False)
		screen.setDimensions(self.X_SCREEN, screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		screen.enableWorldSounds(false)
		
		# Create panels
		
		# Main
		szMainPanel = "DawnOfManMainPanel"
		screen.addPanel(szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN)

		# Text panel
		szTextPanel = "DawnOfManTextPanel"
		screen.addPanel(szTextPanel, "", "", true, true,
			self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM)
		
		# Add contents

		# Main Body text
		szDawnTitle = u"<font=3>" + localText.getText("TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE", ()).upper() + u"</font>"
		screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY,
				self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		bodyString = localText.getText("TXT_KEY_DAWN_OF_MAN_TEXT", (StringUtils.getStrForYear(CyRiseFall().getRFCPlayer(self.player.getCivilizationType()).getStartingYear()), self.player.getCivilizationAdjectiveKey(), self.player.getNameKey()))
		screen.addMultilineText("BodyText", bodyString, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN, self.W_TEXT_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.hide("Exit")
		
		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))
		
		screen.addStackedBarGFC("ProgressBar", self.X_MAIN_PANEL + 60, 400, 435, 40, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_PLAYER_GREEN"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
		self.endTurn = getTurnForYear(CyRiseFall().getRFCPlayer(self.player.getCivilizationType()).getStartingYear())
		
	def handleInput(self, inputClass):
		return 0
	
	def update(self, fDelta):
		gameTurn = CyGame().getGameTurn()
		screen = CyGInterfaceScreen("CvLoadingScreen", self.iScreenID)
		screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, float(max(1, gameTurn))/float(max(1, self.endTurn)))
		screen.setLabel("Text", "", CyTranslator().getText("TXT_KEY_AUTOPLAY_TURNS_REMAINING", (self.endTurn - gameTurn,)), CvUtil.FONT_CENTER_JUSTIFY, self.X_MAIN_PANEL + self.W_MAIN_PANEL/2, 445, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if self.endTurn - gameTurn <= 0:
			screen.show("Exit")
		return
		
	def onClose(self):
		CyInterface().setSoundSelectionReady(true)		
		return 0
			
	def calculateSizesAndPositions(self):
		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		
		screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)
		
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.X_MAIN_PANEL = (self.W_SCREEN/2) - (self.W_MAIN_PANEL/2)
		self.Y_MAIN_PANEL = 190
		
		self.iMarginSpace = 15
		
		self.X_TEXT_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace * 2 - 10
		self.W_TEXT_PANEL = self.W_MAIN_PANEL - self.iMarginSpace * 2
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 3) + 10
		self.iTEXT_PANEL_MARGIN = 35

		
		self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2)
		self.Y_EXIT = self.Y_TEXT_PANEL + self.H_TEXT_PANEL - (self.iMarginSpace * 3)
