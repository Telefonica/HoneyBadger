import os
from time import sleep

def BYE():
    """
        This function is executed when the user wants to leave the server.
    """
    os.system('clear')
    print("BYE")
    sleep(2)
    os.system('clear')
    exit()