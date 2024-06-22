from utilities import *

acConnection = ConnectArchicad ()

origo = {'x': 0, 'y': 0, 'z': 0}
storyHeight = 3.0
slabWidth = 8.0
slabHoleWidth = 4.0
columnOffset = 0.3

slabPolygonCoordinates     = GetRectangleCoordinates (origo['x'], origo['y'],
                                                      slabWidth, slabWidth)
slabHolePolygonCoordinates = GetRectangleCoordinates (origo['x'], origo['y'],
                                                      slabHoleWidth, slabHoleWidth)
columnOrigo2DCoordinates   = GetRectangleCoordinates (origo['x'], origo['y'],
                                                      slabWidth-columnOffset, slabWidth-columnOffset)
columnOrigo2DCoordinates  += GetRectangleCoordinates (origo['x'], origo['y'],
                                                      slabHoleWidth+columnOffset, slabHoleWidth+columnOffset)
slabs = [{
    'level': origo['z'] + i * storyHeight,
    'polygonCoordinates': slabPolygonCoordinates,
    'holes': [{'polygonCoordinates': slabHolePolygonCoordinates}]
} for i in range(5)]

columnCoordinates = [{
    'x': coord2D['x'], 'y': coord2D['y'], 'z': i * storyHeight
} for coord2D in columnOrigo2DCoordinates for i in range(4)]

response = ExecuteAdditionalJSONCommand ('CreateSlabs', { 'slabs': slabs })
ExitIfResponseIsError (response)
response = ExecuteAdditionalJSONCommand ('CreateColumns', { 'coordinates': columnCoordinates })
ExitIfResponseIsError (response)

treeParameters = [{'name': 'Tree Model Detailed 26',
                    'coordinate': {
                        'x': origo['x'], 'y': origo['y'], 'z': origo['z']
                    },
                    'dimensions': {
                        'x': slabHoleWidth, 'y': slabHoleWidth, 'z': storyHeight*5
}}]

response = ExecuteAdditionalJSONCommand ('CreateObjects', { 'objects': treeParameters })
ExitIfResponseIsError (response)