# coding: utf8
"""
Simplification of polygonal lines according to Visvalingam's algorithm:
http://www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html

Copyright 2012 Flávio Codeco Coelho
License: GPL v3
"""
import copy

def triangle_area(p1,p2,p3):
    """
    calculates the area of a triangle given its vertices
    """
    return abs(p1[0]*(p2[1]-p3[1])+p2[0]*(p1[1]-p3[1])+p3[0]*(p1[1]-p2[1]))/2.

class JSONSimplify(object):
    def __init__(self, feature_collection):
        self.data = feature_collection
        self.features = feature_collection["features"]


    def simplify(self,threshold=0):
        """
        Simplifies polygons by eliminating points which form with neighboring points a triangle of area less than threshold
        with threshold = 0, the simplification is non-destructive. Use with care for values above 0.
        """
        simplified_features = [self._simplify_geometry(f,threshold) for f in self.features]
        self.data["features"] = simplified_features
        return self.data

    def _simplify_geometry(self, feature,threshold=0):
        """
        Simplifies polygons in a feature and returns
        """
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
        # now, sequentially remove triangles with areas less than threshold
        for n in deleted.iterkeys():
            del areas[n]
        filtered_areas = copy.deepcopy(areas)
        while area < threshold:
            if len(filtered_areas) < 25: break

            area = min(filtered_areas.values())
            if area > threshold: break
            for n,a in areas.iteritems():
                if n not in filtered_areas: continue
                if a == area:
                    deleted[n] = a
                    del filtered_areas[n]

        feature["geometry"]["coordinates"] = [[c for n,c in enumerate(coordinates) if n not in deleted]]
        return feature

if __name__=="__main__":
    import json
    with open('data.json','r') as f:
        data = json.load(f)
    L = JSONSimplify(data)
    data_s = L.simplify(0.001)
    with open('data_s.json','w') as f:
        json.dump(data_s,f,separators=(',', ':'))


