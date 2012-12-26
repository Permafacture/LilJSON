# coding: utf8
"""
Simplification of polygonal lines according to Visvalingam's algorothm:
http://www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html

Copyright 2012 Flávio Codeco Coelho
License: GPL v3
"""

def triangle_area(p1,p2,p3):
    """
    calculates the area of a triangle given its vertices
    """
    return abs(p1[0]*(p2[1]-p3[1])+p2[0]*(p1[1]-p3[1])+p3[0]*(p1[1]-p2[1]))/2.

class JSONSimplify(object):
    def __init__(self, feature_collection):
        self.data = feature_collection
        self.features = feature_collection["features"]


    def simplify(self):
        simplified_features = [self.simplify_geometry(f) for f in self.features]
        self.data["features"] = simplified_features
        return self.data

    def simplify_geometry(self, feature):
        geometry = feature["geometry"]
        assert isinstance(geometry,dict)
        if "type" in geometry and geometry["type"] == "Polygon":
            coordinates = geometry["coordinates"][0]
        else:
            print geometry
            raise TypeError("Invalid Geometry")
        deleted = {}
        areas = {n : triangle_area(coordinates[n-1],coordinates[n],coordinates[n+1]) for n in range(1,len(coordinates)-1)}
        # First, non-destructive elimination of co-linear points
        for n,area in areas.iteritems():
            if area == 0:
                deleted[n] = area

        feature["geometry"]["coordinates"] = [[c for n,c in enumerate(coordinates) if n not in deleted]]
        return feature

if __name__=="__main__":
    import json
    with open('pt.json','r') as f:
        data = json.load(f)
    L = JSONSimplify(data)
    data_s = L.simplify()
    with open('pt_s.json','w') as f:
        json.dump(data_s,f,separators=(',', ':'))


