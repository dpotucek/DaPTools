#!/usr/bin/python 3
# -*- coding: utf-8 -*-
'''
Implements spherical geodetic calculations.
Negative coordinates are west/south.

Created on 31/01/2018, 10:14

@author: David Potucek
'''

def parse_coordinates(coordinate):
    """posles koordinat ve formatu 50°19'9.652"E a vrati to cislo 50.319348
    Negative coordinates are west/south.
    Doesn't check input format."""
    import re
    import mathPhys
    parts = re.split('[°\'"]+', coordinate) # TODO - dodelat vstupni kontroly
    coord = mathPhys.degree2decimal(parts[0], parts[1], parts[2], parts[3])
    return coord


def format_degrees_tuple(degrees, kategorie ='NA'):
    """posles tuple stupne, minuty, sekundy a optional kategorie(lat, lon, NA), vrati string
    reprezentaci."""
    if len(degrees) == 1:           # validace na pocet parametru
        stupne = degrees[0]
        minuty = 0
        sec = 0
    elif len(degrees) == 2:
        stupne = degrees[0]
        minuty = degrees[1]
        sec = 0
    elif len(degrees) == 3:
        stupne = degrees[0]
        minuty = degrees[1]
        sec = degrees[2]
    else:
        raise ValueError("incorrect number of arguments")
    return format_degrees(stupne, minuty, sec, kategorie)

def format_degrees(stupne, minuty, vteriny, kategorie ='NA'):
    """Negative coordinates are west/south."""
    if kategorie == 'long':
        if stupne <= 0: direction = 'W'
        else: direction = 'E'
    elif kategorie == 'lat':
        if stupne <= 0: direction = 'S'
        else: direction = 'N'
    elif kategorie == 'NA':
        direction = ''
    else: raise ValueError("unknown parameter of latitude/longitude")
    return """{}°{}\'{:.2f}\"{}""".format(stupne, minuty, vteriny, direction)


class GreatCircleTrackSpherical:
    """Class representing a path from one point on earth to another on spherical Earth.
    Both points are defined as pair of coordinates.
    All these formulae are for calculations on the basis of a spherical earth (ignoring
    ellipsoidal effects) – which is accurate enough for most purposes. In fact, the
    earth is very slightly ellipsoidal; using a spherical model gives errors typically
    up to 0.3%.
    """

    def __init__(self, lat1, lon1, lat2, lon2):
        import mathPhys as tools
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.lat1r = tools.deg2rad(lat1)
        self.lat2r = tools.deg2rad(lat2)
        self.lon1r = tools.deg2rad(lon1)
        self.lon2r = tools.deg2rad(lon2)
        self.delta_lat = tools.deg2rad(lat2 - lat1)
        self.delta_lon = tools.deg2rad(lon2 - lon1)

    def calculate_distance(self):
        """uses the ‘haversine’ formula to calculate the great-circle distance between two points in km
            a = sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)
            c = 2*atan2(√a, √(1−a) )
            d = R*c
            where 	φ is latitude, λ is longitude, R is earth’s radius
            @:return distance
            """
        import math
        from mathPhys import EARTH_RADIUS_KM

        a = (math.sin(self.delta_lat / 2)) ** 2 + math.cos(self.lat1r) * math.cos(self.lat2r) \
            * (math.sin(self.delta_lon / 2)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = EARTH_RADIUS_KM * 1000 * c
        return d/1000

    def get_bearings(self):          # TODO nechodi, opravit!!
        init_bearing = self.__initial_bearing(self.lat1r, self.lat2r, self.delta_lon)
        print('init  data {}, {}, delta longitude: {}'.format(self.lat1r, self.lat2r, self.delta_lon))
        print('final data {}, {}, delta longitude: {}'.format(self.lat2r, self.lat1r, self.delta_lon))
        final_bearing = self.__initial_bearing(self.lat2r, self.lat1r, self.delta_lon)
        return init_bearing, final_bearing

    def __initial_bearing(self, l1r, l2r, d_lon):
        """service method for greatCircleTrack.
        Uses formula: θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
            where φ1,λ1 is the start point, φ2,λ2 the end point (Δλ is the difference in longitude)
        """
        import mathPhys as tools
        import math

        y = math.sin(d_lon) * math.cos(l2r)
        x = (math.cos(l1r) * math.sin(l2r)) - (math.sin(l1r) * math.cos(l2r) * math.cos(d_lon))
        result = math.atan2(y, x)
        result_dgr = tools.rad2deg(result)
        result_dgr = (result_dgr + 360) % 360
        return result_dgr

    def midpoint(self):
        """ This is the half-way point along a great circle path between the two points.1
            Formula:
            Bx = cos φ2 ⋅ cos Δλ
            By = cos φ2 ⋅ sin Δλ
            φm = atan2( sin φ1 + sin φ2, √(cos φ1 + Bx)² + By² )
            λm = λ1 + atan2(By, cos(φ1)+Bx)"""
        import math
        bx = math.cos(self.lat2r) * math.cos(self.delta_lon)
        by = math.cos(self.lat2r) * math.sin(self.delta_lon)
        lat_m = math.atan2(math.sin(self.lat1r) + math.sin(self.lat2r),
                          math.sqrt((math.cos(self.lat1r) + bx) ** 2 + by ** 2))
        lon_m = self.lon1r + math.atan2(by, math.cos(self.lat1r) + bx)
        return lat_m, lon_m

    def __str__(self):
        import mathPhys
        temp = self.get_bearings()
        midpoint = self.midpoint()
        stredobod = []
        for m in midpoint:
            temp = mathPhys.decimal2degree(m)
            stredobod.append(format_degrees_tuple(temp))
        return('Great circle track from [{}, {}] to [{}, {}];\n'
               'distance = {:.2f}km, initial bearing = {}, final bearing = {}\n'
               'midpoint = [{}, {}]'.
            format(self.lat1, self.lon1, self.lat2, self.lon2,
                   self.calculate_distance(), format_degrees_tuple(mathPhys.decimal2degree(temp[0])),
                   format_degrees_tuple(mathPhys.decimal2degree(temp[1])),
                   stredobod[0], stredobod[1]))


if __name__ == '__main__':
    pass