from utilities import *
from tkinter import messagebox

acConnection = ConnectArchicad ()

elements = acConnection.commands.GetSelectedElements()

response = ExecuteAdditionalJSONCommand ('GetGDLParametersOfElements', ConvertElementsResponseToInput (elements))
ExitIfResponseDoesNotContain (response, ['gdlParametersOfElements'])

elementIdPropertyId = acConnection.utilities.GetBuiltInPropertyId('General_ElementID')
elementIdPropertiesForElements = acConnection.commands.GetPropertyValuesOfElements(elements, [elementIdPropertyId])

for i in range(len(elements)):
	elementGuid = str (elements[i].elementId.guid)
	parameters = response['gdlParametersOfElements'][i]
	propertyValue = elementIdPropertiesForElements[i].propertyValues[0].propertyValue.value
	messagebox.showinfo ('GDL Parameters of ' + propertyValue + ' (Guid: ' + elementGuid + ')', '\n'.join([name + ' = ' + str (details['value']) for name, details in parameters.items ()]))