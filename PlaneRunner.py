from Airport import Airport
from Network import Network
import time
import shelve




def initiate():
    '''
    This function is called at the start of the program
    returns True if user wants to use program
    returns False if user doesn't want to use program
    '''
  
                                                                      


    print("""
  _____  _                    _   _      _                      _      __  __       _             
 |  __ \| |                  | \ | |    | |                    | |    |  \/  |     | |            
 | |__) | | __ _ _ __   ___  |  \| | ___| |___      _____  _ __| | __ | \  / | __ _| | _____ _ __ 
 |  ___/| |/ _` | '_ \ / _ \ | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ / | |\/| |/ _` | |/ / _ \ '__|
 | |    | | (_| | | | |  __/ | |\  |  __/ |_ \ V  V / (_) | |  |   <  | |  | | (_| |   <  __/ |   
 |_|    |_|\__,_|_| |_|\___| |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |_|  |_|\__,_|_|\_\___|_|   
                                                                                                  
                                                                                                   
                                                                                              
    """)

    time.sleep(2)
    print("Say hello to your own personal plane network!\nWould you like to build a network?")
    print("Y/N")
    choice = input()
    if choice.lower() == "n":
        return False
    else:
        print("I'll take that as a yes.")
        return True
    


def show_choices(network):

    '''
    Prompts the user to pick a choise from stuff to modify their plane network
    This will run infinitely until the user picks choice 5
    If the user mistypes, then they will be prompted again
    '''

    choices = [
        '1. Add an airport',
        '2. Add a connection',
        '3. Print a list of airports',
        '4. Get a path between airports',
        '5. Nothing else, I\'m finished'
    ]
    print("\n\nWhat would you like to do?")
    for i in choices:
        print(i)
    choice = input()
    match choice:
        case '1':
            print("What is the airport\'s name?")
            name = input()
            network.add_airport(name)


        case '2':
            available = network.return_airports()
            print(f"Here are your airports:\n{available}")
            print("What is the starting airport name?")
            name1 = input()
            if name1 not in available:
                print("That's not an availabe airport!")
                time.sleep(2)
                return True


            print("What is the ending airport name?")
            name2 = input()
            if name2 not in available:
                print("That's not an availabe airport!")
                time.sleep(2)
                return True
            
            if name1 == name2:
                print("A plane's path cannot connect to itself!")
                time.sleep(3)
                return

            network.add_airport_connection(name1, name2, 0) #distance = 0; i never implemented it


        case '3':
            available = network.return_airports()
            print(available)
            time.sleep(2)


        case '4':
            available = network.return_airports()
            print(available)
            print("What is the starting airport name?")
            name1 = input()
            if name1 not in available:
                print("That's not an availabe airport!")
                time.sleep(2)
                return True
            print("What is the ending airport name?")


            name2 = input()
            if name2 not in available:
                print("That's not an availabe airport!")
                time.sleep(2)
                return True
            path = network.get_path(name1, name2)
            if not path:
                print("There is no path!")
                time.sleep(2)
            else:
                print("The path goes from left to right!")
                print(path)


        case '5':
            return False
        case _:
            print("Sorry, that'ss not an option. Please try again")
            time.sleep(2)
    return True




def main():
    """
    Runs on the start of the program
    If there is a save, it will prompt the user
    Calls initiate()
    After initiated is done running, the user will be asked if they would like to simulate a plane
    After the plane is simulated, the user is asked if they would like to delete their save
    
    *IMPORTANT*
    The program's save file will corrupt if program ends early
    
    """
    if not initiate():
        print("Come again next time!")
        return
    else:
        stop = False

    plane_network = Network()


    with shelve.open('storage.db') as storage:
        if storage:
            print("\nYou have a save on file!")
            print("Would you like to reload it?\nY/N")
            choice = input()
            if choice.lower() == "n":
                stop = True
            else:
                print("I'll take that as a yes.")
                plane_network.load()
                


    while not stop:
        if not show_choices(plane_network):
            stop = True

    if not plane_network.airports:
        stop = True
    else:
        stop = False

    while not stop:
        print("Would you like to simulate a plane on your railway?\nY/N")
        choice = input()
        if choice.lower() == "n":
            stop = True
        else:
            print("I'll take that as a yes!")
            plane_network.simulate()
        
    print("Would you like to clear this file\nY/N")
    choice = input()
    if choice.lower() == 'y':
        print("Are you sure? Data cannot be retrieved once lost!")
        choice = input()
        if choice.lower() == 'y':
            with shelve.open('storage.db') as storage:
                storage.clear()
                print("Data Cleared!")
    else:
        print("Saving...")
        print("Save successful!")
    print("Come again next time!")
    plane_network.dump()




if __name__ == '__main__':
    main()

