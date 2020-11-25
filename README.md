# HoneyBadger

This project has as function the creation of a Honeypot through the SDDP and mDNS protocols to improve the security in the local network.

To do this it uses a discovery service to clone local devices, or creates it from zero for later create a spoof server that works as a honeypot 
for the attackers.

## Prerequisites

The program needs some packages that need to be installed in order to work, to do this use this command:

```console
pip install -r requirements.txt
```

If you get an error is possible that the 'pip' command needs to be 'pip3', try this command:

```console
pip3 install -r requirements.txt
```

If is still not working probably your python installation is not working properly, try the following command to see if now works:

```console
python -m pip install -r requirements.txt
```

or

```console
python3 -m pip install -r requirements.txt
```

## Options

HoneyBadger has a variety of options which can be accessed through arguments or from the menu.

### Functions

- #### Clone (-c --clone)

    The clone function allows the user to scan the local network looking for devices using the SSDP protocol, then
    it list the compatible devices, allowing the user to save its information for a later use while spoofing.

- #### XML gen (-g --genxml)

    The XML generator allows the user to create autonomously a service, this process can be fully automated or
    the user will be asked for the different options he wants to use allowing the personalization of every parameter.

- #### Server (-s --server)

    This option generates a server in the local network, which uses the SSDP protocol and uses the parameter found in the ssdp.xml file.


### Help and info

- #### Help (-h --help)
    Shows every argument available with a short description of each.

- #### List (-l --list)
    Shows to the use a list with the most common services as reference.

# License

This project is licensed under the GNU General Public License - see the LICENSE file for details

# Contact

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This software doesn't have a QA Process. This software is a Proof of Concept.

If you have any problems, you can contact:

<ideaslocas@telefonica.com> - *Ideas Locas CDCO - Telefónica*

For more information please visit [https://www.elevenpaths.com](https://www.elevenpaths.com).

# Disclaimer

In many places it can be a crime to install software on a computer that does not belong to you, without the owner's consent. We do not approve the use of HoneyBadger for any illegal purpose.  To download or use our software in any way, you must acknowledge and approve the following:

1 - You declare that HoneyBadger will be used exclusively in a legal manner. If you are in doubt as to the legality, consult a licensed attorney in the jurisdiction where you will be using HoneyBadger.

2 - You acknowledge that the computer on which the software is to be installed is yours or you have the owner's consent to manage and install the software on it.
