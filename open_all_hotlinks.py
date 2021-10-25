import json, platform, subprocess
from archicad import ACConnection
from tkinter import messagebox

################################ CONFIGURATION #################################
errorMessageTitleArchicadNotFound = 'Could not find Archicad!'
errorMessageDetailsArchicadNotFound = 'A running Archicad instance is required to initialize the schedule.'

errorMessageTitleAdditionalCommandsNotFound = 'Could not find the required additional JSON commands!'
errorMessageDetailsAdditionalCommandsNotFound = 'The latest version of AdditionalJSONCommands Add-On is required.\nDownload it from github:\nhttps://github.com/tlorantfy/archicad-additional-json-commands/releases'

errorMessageTitleCommandExecutionFailed = 'Failed to execute Archicad command!'
################################################################################

conn = ACConnection.connect ()
if not conn:
	messagebox.showerror (errorMessageTitleArchicadNotFound, errorMessageDetailsArchicadNotFound)
	exit ()

acc = conn.commands
act = conn.types
acu = conn.utilities

def IsUsingMacOS ():
	return platform.system () == 'Darwin'

def IsUsingWindows ():
	return platform.system () == 'Windows'

def EscapeSpacesInPath (path):
	if IsUsingWindows ():
		return f'"{path}"'
	else:
		return path.replace (' ', '\\ ')

def CheckAdditionalJSONCommands ():
	getArchicadLocationCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'GetArchicadLocation')
	getHotlinksCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'GetHotlinks')
	quitCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'Quit')
	additionalJSONCommands = [getHotlinksCommandId, getArchicadLocationCommandId, quitCommandId]

	if not all ([acc.IsAddOnCommandAvailable (commandId) for commandId in additionalJSONCommands]):
		messagebox.showerror (errorMessageTitleAdditionalCommandsNotFound, errorMessageDetailsAdditionalCommandsNotFound)
		exit ()

def GetArchicadLocation ():
	response = acc.ExecuteAddOnCommand (act.AddOnCommandId ('AdditionalJSONCommands', 'GetArchicadLocation'))
	if not response or 'archicadLocation' not in response:
		messagebox.showerror (errorMessageTitleCommandExecutionFailed, response)
	if IsUsingMacOS ():
		return f"{response['archicadLocation']}/Contents/MacOS/ARCHICAD"
	return response['archicadLocation']

def GetHotlinks ():
	response = acc.ExecuteAddOnCommand (act.AddOnCommandId ('AdditionalJSONCommands', 'GetHotlinks'))
	if not response or 'hotlinks' not in response:
		messagebox.showerror (errorMessageTitleCommandExecutionFailed, response)
	return response['hotlinks']

def ReconnectToArchicad ():
	global conn
	global acc
	global act
	global acu
	conn = ACConnection.connect ()
	if conn:
		acc = conn.commands
		act = conn.types
		acu = conn.utilities

def StartArchicadAndOpenProject (archicadLocation, projectLocation):
	global conn
	subprocess.Popen (f"{EscapeSpacesInPath (archicadLocation)} {EscapeSpacesInPath (projectLocation)}", start_new_session=True, shell=IsUsingMacOS ())
	ReconnectToArchicad ()
	while not conn:
		ReconnectToArchicad ()

def StopArchicad ():
	acc.ExecuteAddOnCommand (act.AddOnCommandId ('AdditionalJSONCommands', 'Quit'))

def OpenHotlinkAndDo (hotlink, function):
	StopArchicad ()
	StartArchicadAndOpenProject (archicadLocation, hotlink['location'])

	function ()

	if 'children' in hotlink:
		for childHotlink in hotlink['children']:
			OpenHotlinkAndDo (childHotlink, function)

def DummyFunction ():
	print ("Implement here something to be executed for all hotlinks and the main project")

CheckAdditionalJSONCommands ()

archicadLocation = GetArchicadLocation ()

DummyFunction ()

for hotlink in GetHotlinks ():
	OpenHotlinkAndDo (hotlink, DummyFunction)

StopArchicad ()