class Address:
    def __init__(self, id, name, location, count):
        self.id = id
        self.name = name
        self.location = location
        self.count = count
        self.count += 1
        self.location_id = self.count

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def getlocation(self):
        return self.location

    def getlocationid(self):
        return self.location_id

    def setid(self, id):
        self.id = id

    def setname(self, name):
        self.name = name

    def setlocation(self, location):
        self.location = location

    def setlocationid(self, lid):
        self.location_id = lid
