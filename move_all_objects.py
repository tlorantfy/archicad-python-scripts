import json
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

moveElementsCommandId = act.AddOnCommandId ('AdditionalJSONCommands', 'MoveElements')

def CheckAdditionalJSONCommands ():
	additionalJSONCommands = [moveElementsCommandId]

	if not all ([acc.IsAddOnCommandAvailable (commandId) for commandId in additionalJSONCommands]):
		messagebox.showerror (errorMessageTitleAdditionalCommandsNotFound, errorMessageDetailsAdditionalCommandsNotFound)
		exit ()

CheckAdditionalJSONCommands ()

objects = acc.GetElementsByType ('Object')
elementsWithMoveVectors = [{'elementId': {'guid': str (object.elementId.guid)}, 'moveVector': {'x': 1.0, 'y': 1.0, 'z': 0.0}} for object in objects]

response = acc.ExecuteAddOnCommand (moveElementsCommandId, { 'elementsWithMoveVectors': elementsWithMoveVectors })
if response:
    messagebox.showerror (errorMessageTitleCommandExecutionFailed, response)