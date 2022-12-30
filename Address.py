from geopy.geocoders import ArcGIS
from geopy.exc import GeopyError
from flask import flash


class Address:
    def __init__(self, name, location):
        try:
            geoLocater = ArcGIS(user_agent="TimeVault")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = 0
            self.longitude = 0
            flash("Error finding the location provided. Please provide a valid address.", category="Error")
        else:
            self.latitude = geoLocation.latitude
            self.longitude = geoLocation.longitude
        finally:
            self.name = name
            self.location = location

    def getname(self):
        return self.name

    def getlocation(self):
        return self.location

    def getlatitude(self):
        return self.latitude

    def getlongitude(self):
        return self.longitude

    def setname(self, name):
        self.name = name

    def setLocation(self, location):
        self.location = location
        try:
            geoLocater = ArcGIS(user_agent="TimeVault")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = 0
            self.longitude = 0
        else:
            self.latitude = geoLocation.latitude
            self.longitude = geoLocation.longitude