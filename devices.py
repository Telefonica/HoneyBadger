import os

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