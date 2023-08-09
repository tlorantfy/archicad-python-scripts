from utilities import *

acConnection = ConnectArchicad ()
objects = acConnection.commands.GetElementsByType ('Object')

deltaX = 1.0
deltaY = 1.0
deltaZ = 0.0

elementsWithMoveVectors = [{'elementId': {'guid': str (object.elementId.guid)}, 'moveVector': {'x': deltaX, 'y': deltaY, 'z': deltaZ}} for object in objects]

response = ExecuteAdditionalJSONCommand ('MoveElements', { 'elementsWithMoveVectors': elementsWithMoveVectors })
ExitIfResponseIsError (response)