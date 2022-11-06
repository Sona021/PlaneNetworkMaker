class Airport:

    def __init__(self, name):
        self.name = name
        self.connections = {}
        #self.__planes = []

    def add_connection(self, station, distance=0):
        self.connections[station] = distance

    def get_connections(self):
        return list(self.connections.keys())
