from utilities import *

acConnection = ConnectArchicad ()

origo = {'x': 0, 'y': 0, 'z': 0}
storyHeight = 3.0
slabWidth = 8.0
slabHoleWidth = 4.0
columnOffset = 0.3

slabPolygonCoordinates     = GetRectangleCoordinates (origo['x'], origo['y'], slabWidth, slabWidth)
slabHolePolygonCoordinates = GetRectangleCoordinates (origo['x'], origo['y'], slabHoleWidth, slabHoleWidth)
columnOrigo2DCoordinates   = GetRectangleCoordinates (origo['x'], origo['y'], slabWidth-columnOffset, slabWidth-columnOffset)
columnOrigo2DCoordinates  += GetRectangleCoordinates (origo['x'], origo['y'], slabHoleWidth+columnOffset, slabHoleWidth+columnOffset)

slabs = [{
    'level': origo['z'] + i * storyHeight,
    'polygonCoordinates': slabPolygonCoordinates,
    'holes': [{'polygonCoordinates': slabHolePolygonCoordinates}] if i != 0 else []
} for i in range(5)]

columnCoordinates = [{
    'x': coord2D['x'], 'y': coord2D['y'], 'z': i * storyHeight
} for coord2D in columnOrigo2DCoordinates for i in range(4)]

response = ExecuteAdditionalJSONCommand ('CreateSlabs', { 'slabs': slabs })
ExitIfResponseIsError (response)
response = ExecuteAdditionalJSONCommand ('CreateColumns', { 'coordinates': columnCoordinates })
ExitIfResponseIsError (response)