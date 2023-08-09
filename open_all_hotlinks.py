from utilities import *

def GetHotlinks ():
	response = ExecuteAdditionalJSONCommand ('GetHotlinks')
	ExitIfResponseDoesNotContain (response, ['hotlinks'])
	return response['hotlinks']

def OpenHotlinkAndDo (hotlink, function):
	archicadLocation = GetArchicadLocation ()
	StopArchicad ()
	StartArchicadAndOpenProject (archicadLocation, hotlink['location'])

	function ()

	if 'children' in hotlink:
		for childHotlink in hotlink['children']:
			OpenHotlinkAndDo (childHotlink, function)

def DummyFunction ():
	print ("Implement here something to be executed for all hotlinks and the main project")

ConnectArchicad ()
DummyFunction ()

for hotlink in GetHotlinks ():
	OpenHotlinkAndDo (hotlink, DummyFunction)

StopArchicad ()