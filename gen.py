import os, random, uuid
from utils import utils
from end import *
from server import server

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
