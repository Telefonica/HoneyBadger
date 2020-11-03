import os

class show_help:
    """
        Shows the user all the help available and then exits the program.
    """
    def __init__(self):
        os.system('clear')
        print(
            'This program provides all the tools needed to create a honeypod\n'
            'on the local network through the SSDP and mDNS protocol.\n'
            '\n'
            'Options:\n'
            '\n'
            '-h     --help      Provides all the help available.\n'
            '\n'
            '-l     --list      List in the terminal the most common services\n'
            '                   to allow the user know how to spoof it.\n'
            '\n'
            '-g     --genxml    Allows the creation (Automatic or not) of a\n'
            '                   .xml file which will allow to spoof the\n'
            '                   required device.\n'
            '\n'
            '-s     --server    Starts the server with the .xml found, if no\n'
            '                   .xml available the user will be asked to\n'
            '                   create a new one or exit.\n'
            '\n'
            '-c     --clone     Allows the clonation of a local service in\n'
            '                   the local network to spoof it later.\n'
        )