from twisted.internet.protocol import ClientFactory
from twisted.internet import ssl
from twisted.internet import reactor
from imgur import grab_image
from janecore.ircbot.ansible.protocol import AnsibleClientProtocol
from janecore.ircbot.ansible import commands
import re
import pickle

JANES_NAME = 'Jane(OfTheJungle)?' 
test_dict = {r'^%s(\s.*)?\sping' % JANES_NAME: 'Go Away!!',
             r'.*bug.*(\d{7})( .*)?': ['https://code.launchpad.net/bugs/%s', 0],
             r'.*BD-(\d{1,5})( .*)?': ['https://support.tfoundry.com/browse/BD-%s', 0],
             r'.*OC-(\d{1,5})( .*)?': ['https://support.tfoundry.com/browse/OC-%s', 0],
             r'.*FS-(\d{1,5})( .*)?': ['https://support.tfoundry.com/browse/FS-%s', 0],
            }

def test_data(data):
    for tests in test_dict.keys():
        match_obj = re.match(tests, data[-1])
        if match_obj:
            if type(test_dict[tests]) == str:
                new_data = [data[1], test_dict[tests]]
            else:
                replace = match_obj.groups()[test_dict[tests][1]]
                new_data = [data[1], test_dict[tests][0] % replace]
            return new_data

class DittoRemote(AnsibleClientProtocol):
    EVENTS=["ircPrivmsg", "ircKickedFrom"]

    def ircPrivmsgCallback(self, data):
        new_data = test_data(data)
        if new_data:
            self.callRemote(commands.DispatchEvent, event_name="ircDoMsg", data=pickle.dumps(new_data))
        elif None:
            imgs = grab_image()
            if imgs:
                data = [data[1], str(imgs[0]['src']) + ' --- ' + str(imgs[0]['title'])]
                self.callRemote(commands.DispatchEvent, event_name="ircDoMsg", data=pickle.dumps(data))

    def ircKickedFromCallback(self, data):
        self.callRemote(commands.DispatchEvent, event_name="ircDoJoin", data=pickle.dumps([data[0], data[2]]))
        self.callRemote(commands.DispatchEvent, event_name="ircDoKick", data=pickle.dumps([data[0], data[1]]))

class AnsibleClientFactory(ClientFactory):
    protocol = DittoRemote

factory = AnsibleClientFactory()
reactor.connectSSL("localhost", 1677, factory, ssl.ClientContextFactory())
reactor.run()
