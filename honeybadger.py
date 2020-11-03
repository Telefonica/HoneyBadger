# Checks for the correct import of all of the required packages, if any is missing or returns an error.
# the user get a message and the program exits.
try:
    import sys, getopt
    from help import *
    from devices import *
    from server import server
    from utils import utils
    from end import BYE
    from gen import genxml
    from clone import clone
except ImportError as text:
    print('There has been and error while importing the required packages:\n')
    print('Error: '+str(text))
    exit()

# Check the version of Python installed, if it is not 3.0+ the user get a message and the program exits.
if sys.version_info < (3, 0):
    print("You need a version of Python 3.0+\n")
    exit()

#Creates a list with all the available arguments for the program
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "hgscl"
long_options = ["help","genxml","server","clone","list"]

def main():
    """
        The main function of the program if an argument is given it will recognize it and execute the proper function.\n

        If no argument is provided it will show a menu with all the available options to the user.
    """
    arguments = len(sys.argv) - 1

    if arguments == 0:
        os.system('clear')
        print('What you want to do?\n'
        '\n1) Generate XML // 2) Start server // 3) Clone // 4) Help // 5) List devices options // 6) Exit\n')
        choose = input("Selection: ")
        os.system('clear')
        if choose == "1":
            genxml()
        elif choose == "2":
            server()
        elif choose == "3":
            clone()
        elif choose == "4":
            show_help()
        elif choose == "5":
            show_devices()
        else:
            BYE()
    else:
        try:
            # Checks the arguments provided to see if are valid.
            arguments, _ = getopt.getopt(argument_list, short_options, long_options)
        except getopt.error:
            exit()
        
        # Loop through the arguments checking for matches if the argument received is not 
        # listed it will return an eror and exit the program
        for current_argument, _ in arguments:
            if current_argument in ("-h", "--help"):
                show_help()
            if current_argument in ("-g", "--genxml"):
                genxml()
            if current_argument in ("-s", "--server"):
                server()
            if current_argument in ("-c", "--clone"):
                clone()
            if current_argument in ("-l", "--list"):
                show_devices()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        BYE()