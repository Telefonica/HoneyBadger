import socket, os, re, requests
from time import sleep
from utils import utils
from gen import genxml

class clone:
    """
    Allows the clonation of a local device to spoof it by scanning all of the active services in the local
    network and cloning its properties.
    """
    # This is the query needed to multicast and ask for all the available services.
    REQUEST =  (
        'M-SEARCH * HTTP/1.1'
        '\r\nHOST: 239.255.255.250:1900'
        '\r\nMAN: \"ssdp:discover\"\r\n'
        'MX: 2\r\n'
        'ST: ssdp:all\r\n\r\n')
    def __init__(self):
        # Initialize Socket and bind it to address of the machine.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Send the REQUEST to the Broadcast IP and waits 5 seconds for a response of the active services.
        sock.sendto(clone.REQUEST.encode(), ('239.255.255.250',1900))
        sock.settimeout(5)

        UUID_list = []
        os.system('rm -rf ./tmp')
        os.system('mkdir ./tmp')
        counterA = 0
        counterB = 0
        while True:
            try:
                # Start listening to responses from the M-SEARCH query
                data, _ = sock.recvfrom(1024)
                # With the response from all of the ssdp services that have sent a response within the timeout
                incName = data.decode()
                # Searching for the UUID 
                try:
                    uuid = re.search("USN: (.*?)::",incName).group(1)
                except (AttributeError):
                    pass
                # Checks that the UUID is not duplicated, deleting all of the services that are not needed.
                if uuid not in UUID_list:
                    counterB += 1
                    UUID_list.append(uuid)
                    try:
                        location = re.search("LOCATION: (.*?).xml",incName).group(1) + ".xml"
                    except (AttributeError):
                        pass
                    UUID_list.append(location)
                    # Saves the located service xml to parse it more easily.
                    response = requests.get(location)
                    with open('./tmp/ssdp.xml', 'wb') as file:
                        file.write(response.content)
                    # Gets all the info needed from the saved xml and prints it to the user.
                    friendlyname = utils.get_friendlyname_tmp(None)
                    UUID_list.append(friendlyname)
                    service = utils.get_service_tmp(None)
                    UUID_list.append(service)
                    print('--------------------\nService ('+str(counterB)+')')
                    print('Name: '+UUID_list[counterA+2])
                    counterA += 1
                    print('Address: '+UUID_list[counterA])
                    counterA += 1
                    print('UUID: '+UUID_list[counterA-2])
                    counterA += 1
                    print('Service Identificator: '+UUID_list[counterA])
                    TOS = "Unknow"
                    if UUID_list[counterA] == "urn:dial-multiscreen-org:service:dial:1":
                        TOS = "DLNA/Chromecast"
                    elif UUID_list[counterA] == "urn:schemas-upnp-org:service:RenderingControl:1":
                        TOS = "DLNA Receiver"
                    elif UUID_list[counterA] == "urn:schemas-upnp-org:service:PrintBasic:1":
                        TOS = "Printer"
                    print('Service provided: '+TOS+'\n--------------------\n')
                    counterA += 1
                               
            except socket.timeout:
                # Deletes all the temporary files created while parsing the xml
                os.system('rm -rf ./tmp')
                # Ask for the user which service wants and with an algorithm extracts the info of the
                # choosen service.
                print("\nWhich service you want to clone?\n")
                service = input("Write the number of the service: ")
                service = utils.get_service_number(None, service)
                os.system('clear')
                print(
                    'You have selected:\n'
                    'Name: '+UUID_list[service-1]+'\n'
                    'Address: '+UUID_list[service-2]+'\n'
                    'UUID: '+UUID_list[service-3]+'\n'
                    'Service Identificator:'+UUID_list[service]+'\n'
                )
                save = requests.get(UUID_list[service-2])
                print("\nsaving configuration....\n")
                sleep(2)
                with open('./ssdp.xml', 'wb') as file:
                    file.write(save.content)
                os.system('clear')
                genxml.gencloned(None)
