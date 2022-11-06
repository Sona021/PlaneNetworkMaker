from Airport import Airport
from random import randint
from Plane import Plane
import shelve
import time


class Network:

    def __init__(self):
        self.airports = {}


    def add_airport(self, airport_name):
        new_Airport = Airport(airport_name)
        self.airports[new_Airport.name] = new_Airport
        

    def add_airport_connection(self, from_airport_name, to_airport_name, distance):
        self.airports[from_airport_name].add_connection(self.airports[to_airport_name], distance)

    def return_airports(self):
        return list(self.airports.keys())
    
    def __string_to_object(self, string):
        for i in self.airports:
            if i == string:
                return self.airports[i]



    def get_path(self, current, target, visited = None, stack = None):
        if isinstance(current, str):
            current = self.__string_to_object(current)

        if isinstance(target, str):
            target = self.__string_to_object(target)

        if not visited:
            visited = []
        
        if not stack:
            stack = [current]

        visited.append(current)

        if current == target:
            return [i.name for i in stack]

        for i in current.get_connections():
            if i not in visited:
                stack.append(i)
                path = self.get_path(i, target, visited, stack)
                if path:
                    return path
                else:
                    stack.pop()
    


    
    def simulate(self):
        current_plane = Plane()
        print("Which path will this plane take? (Pick 2 airports)")
        available = self.return_airports()
        print(available)
        name1 = input()
        name2 = input()

        if name1 not in available:
            print("That airport does not exist!")
            return
        
        if name2 not in available:
            print("That airport does not exist!")
            return

        if name1 == name2:
                print("The plane is already here!")
                time.sleep(3)
                return
        
        path = self.get_path(name1, name2)
       
        
        for i in range(len(path) - 1):
            print(f"The plane is at {path[i]}!\n")
            entered = randint(0, current_plane.get_capacity() - current_plane.get_passengers())
            exited = randint(0, current_plane.get_passengers())
            print(f'{exited} passengers exited the plane!')
            print(f'{entered} passengers entered the plane!\n')
            current_plane.add_passengers(-1 * exited)
            current_plane.add_passengers(entered)
            print(f"The plane is heading to {path[i + 1]}!\n")
            time.sleep(3)
            
        print(f"The plane is at {path[-1]}!")
        print("The plane is at it's final stop!")  
        print(f'{current_plane.get_passengers()} passengers exited the plane!')
        current_plane = None
    


    def dump(self):
        with shelve.open('storage.db') as storage:
            airport_names = [i for i in self.airports.keys()]
            storage['names'] = airport_names

            airport_connections = {}
            for i in self.airports.values():
                airport_connections[i.name] = {i.name:0 for i in i.connections.keys()}
            
            storage['connections'] = airport_connections
       
    def load(self):
        with shelve.open('storage.db') as storage:
            for i in storage['names']:
                new_airport = Airport(i)
                self.airports[new_airport.name] = new_airport
            
            for i in storage['connections']: 
               for j in storage['connections'][i]:
                    self.airports[i].add_connection(self.airports[j], 0)



            
            storage.clear()
