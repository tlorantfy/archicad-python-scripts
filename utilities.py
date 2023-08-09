import platform, subprocess
from archicad import ACConnection
from tkinter import messagebox

################################ CONFIGURATION #################################
errorMessageTitleArchicadNotFound = 'Could not find Archicad!'
errorMessageDetailsArchicadNotFound = 'A running Archicad instance is required to initialize the schedule.'

errorMessageTitleAdditionalCommandsNotFound = 'Could not find the required commands!'
errorMessageDetailsAdditionalCommandsNotFound = 'The below commands are not available:\n{}\n\nThe latest version of AdditionalJSONCommands Add-On is required.\nDownload it from github:\nhttps://github.com/tlorantfy/archicad-additional-json-commands/releases'

errorMessageTitleCommandExecutionFailed = 'Failed to execute Archicad command!'
################################################################################

def ReconnectToArchicad ():
	return ACConnection.connect ()

def ConnectArchicad ():
	conn = ReconnectToArchicad ()
	if not conn:
		messagebox.showerror (errorMessageTitleArchicadNotFound, errorMessageDetailsArchicadNotFound)
		exit ()
	return conn

def CheckCommandsAvailability (acConnection, additionalJSONCommands):
	notAvailableCommands = [commandId.commandName + ' (Namespace: ' + commandId.commandNamespace + ')' for commandId in additionalJSONCommands if not acConnection.commands.IsAddOnCommandAvailable (commandId)]
	if notAvailableCommands:
		messagebox.showerror (errorMessageTitleAdditionalCommandsNotFound, errorMessageDetailsAdditionalCommandsNotFound.format ('\n'.join (notAvailableCommands)))
		exit ()

def ExitIfResponseIsError (response):
	ExitIfResponseDoesNotContain (response)

def ExitIfResponseDoesNotContain (response, requiredFields = None):
	missingFields = []
	if requiredFields:
		for f in requiredFields:
			if f not in response:
				missingFields.append (f)
	if (len(response) > 0 and 'error' in response) or (len(missingFields) > 0):
		messagebox.showerror (errorMessageTitleCommandExecutionFailed, response)
		exit ()

def ConvertElementsResponseToInput (elements):
	return { 'elements' : [ { 'elementId' : { 'guid' : str (e.elementId.guid) } } for e in elements ] }

def IsUsingMacOS ():
	return platform.system () == 'Darwin'

def IsUsingWindows ():
	return platform.system () == 'Windows'

def EscapeSpacesInPath (path):
	if IsUsingWindows ():
		return f'"{path}"'
	else:
		return path.replace (' ', '\\ ')

def StartArchicadAndOpenProject (archicadLocation, projectLocation):
	acConnection = ReconnectToArchicad ()
	if not acConnection:
		subprocess.Popen (f"{EscapeSpacesInPath (archicadLocation)} {EscapeSpacesInPath (projectLocation)}", start_new_session=True, shell=IsUsingMacOS ())
	while not acConnection:
		acConnection = ReconnectToArchicad ()

def ExecuteAdditionalJSONCommand (commandName, inputParameters = None):
	acConnection = ConnectArchicad ()
	command = acConnection.types.AddOnCommandId ('AdditionalJSONCommands', commandName)
	CheckCommandsAvailability (acConnection, [command])
	return acConnection.commands.ExecuteAddOnCommand (command, inputParameters)

def StopArchicad ():
	return ExecuteAdditionalJSONCommand ('Quit')

def GetArchicadLocation ():
	response = ExecuteAdditionalJSONCommand ('GetArchicadLocation')
	ExitIfResponseDoesNotContain (response, ['archicadLocation'])
	if IsUsingMacOS ():
		return f"{response['archicadLocation']}/Contents/MacOS/ARCHICAD"
	return response['archicadLocation']