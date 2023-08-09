import os, re, platform, subprocess, tkinter as tk
from utilities import *
from archicad import ACConnection
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
from threading import Timer

################################ CONFIGURATION #################################
dialogSize = '800x480'
dialogTitle = 'Recurring Publish'
textProject = 'Project:'
textTeamworkUsername = 'Username:'
textPublisherSets = 'Select Publisher Set(s) to Publish:'
textOutputPath = 'Output Path:'
textBrowseButton = 'Browse'
textRecur1 = 'Recur every'
textRecur2 = 'minute(s)'
textPublishButton = 'Start Publishing'
textExitButton = 'Stop and Exit'

textProgressWaitingForStart = 'Waiting to start...'
textProgressPublishing = 'Publishing...'
textProgressSecsBackTillNextPublishing = ' second(s) till next publishing...'

publishSubfolderPrefix = ''
publishSubfolderDatePostfixFormat = '%Y-%m-%d_%H-%M-%S'
################################################################################

def GetProjectInfo ():
	response = ExecuteAdditionalJSONCommand ('GetProjectInfo')
	ExitIfResponseDoesNotContain (response, ['projectLocation', 'projectPath', 'isTeamwork'])
	return response

archicadLocation = GetArchicadLocation ()
projectInfo = GetProjectInfo ()
taskScheduler = None
publisherSetNames = []

class ProgressUpdater:
	def __init__ (self, secondsToCountBack):
		self.secondsToCountBack = secondsToCountBack
		self.elapsed = 0
		self.timer = Timer (1, self.Tick)
		self.timer.start ()

	def Tick (self):
		self.elapsed += 1
		if self.Remaining () > 0:
			self.UpdateProgress ()
			self.timer = Timer (1, self.Tick)
			self.timer.start ()

	def Remaining (self):
		return self.secondsToCountBack - self.elapsed
	
	def UpdateProgress (self):
		progressLabel.config (text=f'{self.Remaining ()} {textProgressSecsBackTillNextPublishing}')


class RecurringTaskScheduler:
	def __init__ (self, task):
		self.task = task

	def ScheduleNextExecution (self, secsToNextExecution = 1):
		self.timer = Timer (secsToNextExecution, self.Execute)
		self.timer.daemon = True
		self.timer.start ()
		self.progressUpdater = ProgressUpdater (secsToNextExecution)

	def Stop (self):
		if self.timer:
			self.timer.cancel ()
		self.StopArchicad ()

	def Execute (self):
		StartArchicadAndOpenProject (archicadLocation, projectInfo['projectLocation'])
		self.task ()
		StopArchicad ()
		self.ScheduleNextExecution (timedelta (minutes=int (recurEntry.get ())).total_seconds ())

def ExecutePublishCommand ():
	progressLabel.config (text=textProgressPublishing)

	if projectInfo['isTeamwork']:
		response = ExecuteAdditionalJSONCommand ('TeamworkReceive')
		ExitIfResponseIsError (response)

	for publisherSetListIndex in publisherSetList.curselection ():
		publisherSetName = publisherSetNames[publisherSetListIndex]
		parameters = { 'publisherSetName': publisherSetName }
		if outputPathEntry.get ():
			parameters['outputPath'] = os.path.join (
									outputPathEntry.get (),
									publisherSetName,
									f'{publishSubfolderPrefix}{datetime.now ().strftime(publishSubfolderDatePostfixFormat)}'
									)

		response = ExecuteAdditionalJSONCommand ('Publish', parameters)
		ExitIfResponseIsError (response)

def StartRecurringPublishing ():
	executeButton['state'] = tk.DISABLED
	exitButton['state'] = tk.NORMAL

	global taskScheduler
	taskScheduler = RecurringTaskScheduler (ExecutePublishCommand)
	taskScheduler.ScheduleNextExecution ()

def SetEntryValue (entry, text):
	entry.delete (0, tk.END)
	entry.insert (0, text)

def BrowseOutputPath ():
	chosenPath = filedialog.askdirectory ()
	if chosenPath:
		outputPathEntry['state'] = tk.NORMAL
		SetEntryValue (outputPathEntry, chosenPath)
		outputPathEntry['state'] = tk.DISABLED

def GetUsernameFromProjectLocation (projectLocation):
	return re.compile (r'.*://(.*):.*@.*').match (projectLocation).group (1)

def InitPublisherSetList ():
	global publisherSetNames
	publisherSetNames = ConnectArchicad ().commands.GetPublisherSetNames ()
	publisherSetNames.sort ()

	if publisherSetNames:
		for publisherSetName in publisherSetNames:
			publisherSetList.insert (tk.END, publisherSetName)
		publisherSetList.select_set (0)
		publisherSetList.event_generate ("<<ListboxSelect>>")

def InitControls ():
	InitPublisherSetList ()
	SetEntryValue (projectEntry, projectInfo['projectPath'])
	if projectInfo['isTeamwork']:
		SetEntryValue (projectEntry, f'{projectEntry.get ()} (Teamwork project)')
		SetEntryValue (teamworkUsernameEntry, GetUsernameFromProjectLocation (projectInfo['projectLocation']))
	SetEntryValue (recurEntry, '1')
	projectEntry['state'] = tk.DISABLED
	outputPathEntry['state'] = tk.DISABLED
	exitButton['state'] = tk.DISABLED
	teamworkUsernameEntry['state'] = tk.DISABLED


app = tk.Tk ()
app.title (dialogTitle)

def IntegerValidator (value):
	return str.isdigit (value)

integerValidator = (app.register (IntegerValidator))

projectLabel = tk.Label (app, text=textProject)
projectEntry = tk.Entry (app)
teamworkUsernameLabel = tk.Label (app, text=textTeamworkUsername)
teamworkUsernameEntry = tk.Entry (app)
publisherSetLabel = tk.Label (app, text=textPublisherSets)
publisherSetList = tk.Listbox (app, selectmode=tk.MULTIPLE)
outputPathLabel = tk.Label (app, text=textOutputPath)
outputPathEntry = tk.Entry (app)
recurFrame = tk.Frame (app)
recurLabel1 = tk.Label (recurFrame, text=textRecur1)
recurEntry = tk.Entry (recurFrame, validate='all', validatecommand=(integerValidator, '%P'))
recurLabel2 = tk.Label (recurFrame, text=textRecur2)
progressLabel = tk.Label (app, text=textProgressWaitingForStart)
outputPathBrowseButton = tk.Button (app, text=textBrowseButton, command=BrowseOutputPath)
executeButton = tk.Button (app, text=textPublishButton, command=StartRecurringPublishing)
exitButton = tk.Button (app, text=textExitButton, command=exit)

projectLabel.grid (column=0, row=0, padx=10, sticky=tk.W)
projectEntry.grid (column=1, row=0, columnspan=2, padx=10, sticky=tk.NSEW)
teamworkUsernameLabel.grid (column=0, row=1, padx=10, sticky=tk.W)
teamworkUsernameEntry.grid (column=1, row=1, columnspan=2, padx=10, sticky=tk.NSEW)
publisherSetLabel.grid (column=0, row=2, columnspan=3, padx=10, sticky=tk.W)
publisherSetList.grid (column=0, row=3, columnspan=3, padx=10, sticky=tk.NSEW)
outputPathLabel.grid (column=0, row=4, columnspan=3, padx=10, sticky=tk.W)
outputPathEntry.grid (column=0, row=5, padx=10, columnspan=2, sticky=tk.NSEW)
outputPathBrowseButton.grid (column=2, row=5, padx=10, sticky=tk.NSEW)
recurFrame.grid (column=0, row=6, columnspan=3, pady=10, padx=10, sticky=tk.NSEW)
progressLabel.grid (column=0, row=7, columnspan=3, pady=10, padx=10, sticky=tk.W)
executeButton.grid (column=0, row=8, columnspan=3, pady=5, padx=10, sticky=tk.NSEW)
exitButton.grid (column=0, row=9, columnspan=3, pady=5, padx=10, sticky=tk.NSEW)

recurLabel1.grid (column=0, row=0, padx=10, sticky=tk.W)
recurEntry.grid (column=1, row=0, padx=10, sticky=tk.NSEW)
recurLabel2.grid (column=2, row=0, padx=10, sticky=tk.W)

app.columnconfigure (0, weight=1)
app.columnconfigure (1, weight=8)
app.rowconfigure (8, weight=1)
app.geometry (dialogSize)

InitControls ()

app.mainloop ()