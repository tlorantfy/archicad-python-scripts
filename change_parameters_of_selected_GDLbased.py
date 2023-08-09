from utilities import *

acConnection = ConnectArchicad ()

elements = acConnection.commands.GetSelectedElements()

elementsWithGDLParameters = [ { 'elementId' : { 'guid' : str (e.elementId.guid) }, 'gdlParameters' : { 'gs_cont_pen' : { 'value' : 95 } } } for e in elements ]

response = ExecuteAdditionalJSONCommand ('ChangeGDLParametersOfElements', { 'elementsWithGDLParameters' : elementsWithGDLParameters })
ExitIfResponseIsError (response)