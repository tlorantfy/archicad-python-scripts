import os
import tkinter as tk
from archicad import ACConnection
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from threading import Timer

################################ CONFIGURATION #################################
dialogSize = '800x250'
dialogTitle = 'Recurring Publish'
textPublisherSet = 'Publisher Set:'
textOutputPath = 'Output Path:'
textBrowseButton = 'Browse'
textRecur1 = 'Recur every'
textRecur2 = 'minute(s)'
textPublishButton = 'Start Publishing'
textExitButton = 'Stop and Exit'

errorMessageTitleArchicadNotFound = 'Could not find Archicad!'
errorMessageDetailsArchicadNotFound = 'A running Archicad instance is required to initialize the schedule.'

errorMessageTitlePublishCommandNotFound = 'Could not find Publish JSON command!'
errorMessageDetailsPublishCommandNotFound = 'AdditionalJSONCommands Add-On is required.\nDownload it from github: https://github.com/tlorantfy/archicad-additional-json-commands/releases'

errorMessageTitleOutputPathInvalid = 'Invalid output path!'
errorMessageDetailsOutputPathInvalid = 'Please input valid output path.'

errorMessageTitlePublishFailed = 'Publish command failed!'

publishSubfolderPrefix = ''
publishSubfolderDatePostfixFormat = '%Y-%m-%d_%H-%M-%S'
################################################################################

conn = ACConnection.connect ()
if not conn:
	messagebox.showerror (errorMessageTitleArchicadNotFound, errorMessageDetailsArchicadNotFound)
	exit ()

acc = conn.commands
act = conn.types
acu = conn.utilities

publishCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'Publish')
teamworkReceiveCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'TeamworkReceive')

if not acc.IsAddOnCommandAvailable (publishCommandId):
	messagebox.showerror (errorMessageTitlePublishCommandNotFound, errorMessageDetailsPublishCommandNotFound)
	exit ()

app = tk.Tk ()
app.title (dialogTitle)

publisherSetLabel = tk.Label (app, text=textPublisherSet)
publisherSetCombobox = ttk.Combobox (app)
outputPathLabel = tk.Label (app, text=textOutputPath)
outputPathEntry = tk.Entry (app)
recurFrame = tk.Frame (app)
recurLabel1 = tk.Label (recurFrame, text=textRecur1)
recurScale = tk.Scale (recurFrame, from_=1, to_=10080, orient='horizontal', length=400)
recurLabel2 = tk.Label (recurFrame, text=textRecur2)

timer = None

def ExecutePublishCommand ():
	if outputPathEntry.get () and not os.path.isdir (outputPathEntry.get ()):
		messagebox.showerror (errorMessageTitleOutputPathInvalid, errorMessageDetailsOutputPathInvalid)
		return

	executeButton['state'] = tk.DISABLED
	exitButton['state'] = tk.NORMAL

	acc.ExecuteAddOnCommand (teamworkReceiveCommandId)

	parameters = { 'publisherSetName': publisherSetCombobox.get () }
	if outputPathEntry.get ():
		parameters['outputPath'] = os.path.join (
								outputPathEntry.get (),
								f'{publishSubfolderPrefix}{datetime.now ().strftime(publishSubfolderDatePostfixFormat)}'
								)

	response = acc.ExecuteAddOnCommand (publishCommandId, parameters)
	if response:
		messagebox.showerror (errorMessageTitlePublishFailed, response)

	deltaTime = timedelta (minutes = recurScale.get ())

	secs = deltaTime.total_seconds ()

	global timer
	timer = Timer (secs, ExecutePublishCommand)
	timer.daemon = True
	timer.start ()

def BrowseOutputPath ():
	chosenPath = filedialog.askdirectory ()
	if chosenPath:
		outputPathEntry.delete (0, tk.END)
		outputPathEntry.insert (0, chosenPath)

def StopAndExit ():
	global timer
	if timer:
		timer.cancel ()
	exit ()

outputPathBrowseButton = tk.Button (app, text=textBrowseButton, command=BrowseOutputPath)
executeButton = tk.Button (app, text=textPublishButton, command=ExecutePublishCommand)
exitButton = tk.Button (app, text=textExitButton, command=StopAndExit)
exitButton['state'] = tk.DISABLED

publisherSetLabel.grid (column=0, row=0, columnspan=2, padx=10, sticky=tk.W)
publisherSetCombobox.grid (column=0, row=1, columnspan=2, padx=10, sticky=tk.NSEW)
outputPathLabel.grid (column=0, row=2, columnspan=2, padx=10, sticky=tk.W)
outputPathEntry.grid (column=0, row=3, padx=10, sticky=tk.NSEW)
outputPathBrowseButton.grid (column=1, row=3, padx=10, sticky=tk.NSEW)
recurFrame.grid (column=0, row=4, columnspan=2, pady=10, padx=10, sticky=tk.NSEW)
executeButton.grid (column=0, row=5, columnspan=2, pady=5, padx=10, sticky=tk.NSEW)
exitButton.grid (column=0, row=6, columnspan=2, pady=5, padx=10, sticky=tk.NSEW)

recurLabel1.grid (column=0, row=0, padx=10, sticky=tk.W)
recurScale.grid (column=1, row=0, padx=10, sticky=tk.NSEW)
recurLabel2.grid (column=2, row=0, padx=10, sticky=tk.W)

publisherSetNames = acc.GetPublisherSetNames ()
publisherSetNames.sort ()

if publisherSetNames:
	publisherSetCombobox['values'] = publisherSetNames
	publisherSetCombobox.current (0)
else:
    executeButton['state'] = tk.DISABLED

app.columnconfigure (0, weight=1)
app.rowconfigure (5, weight=1)
app.geometry (dialogSize)
app.mainloop ()
