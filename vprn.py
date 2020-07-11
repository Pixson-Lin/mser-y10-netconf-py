from ncclient import manager
from lxml import etree
from router import router
from ncclient.xml_ import *

class vprn_endpoint():
    
    def __init__(self, id, name, rd, if_name, if_ip, in_tag, out_tag, sap_port, desc):
        self.data = {}
        self.data['id'] = int(id)
        self.data['name'] = str(name)
        self.data['rd'] = str(rd)
        self.data['if_name'] = str(if_name)
        self.data['if_ip'] = str(if_ip)
        self.data['in_tag'] = int(in_tag)
        self.data['out_tag'] = int(out_tag)
        self.data['sap_port'] = str(sap_port)
        self.data['desc'] = str(desc)
#        print(self.data['route_next_hop'])

    def to_provision_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])

        config  = " configure service vprn " + str(self.data['id']) + " name "+ self.data['name'] + " customer 1 create\n"
        config += "   description " + self.data['desc'] + " \n"
        config += "   route-distinguisher " + self.data['rd'] + " \n"
        config += "   auto-bind-tunnel \n"
        config += "       resolution-filter \n"
        config += "           sr-policy \n"
        config += "       exit \n"
        config += "       resolution filter \n"
        config += "   exit \n"
        config += "   vrf-target target:65001:" + str(self.data['id']) + " \n"
        config += "   interface " + self.data['if_name'] + " \n"
        config += "     address " + self.data['if_ip'] + " \n"
        config += "     sap " + sap_str + " create \n"
        config += "       ingress qos 16 \n"
        config += "       egress qos 16 \n"
        config += "     exit \n"
        config += "   exit \n"
        config += " no shutdown \n"

#        print(config)
        return config

    def to_teardown_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])

        config  = " configure service vprn " + str(self.data['id']) + " \n"
        config += "   interface " + self.data['if_name'] + " sap " + sap_str + " shutdown \n"
        config += "   interface " + self.data['if_name'] + " no sap " + sap_str + " \n"
        config += "   interface " + self.data['if_name'] + " shutdown \n"
        config += "   no interface " + self.data['if_name'] + " \n"
        config += "   shutdown \n"
        config += "   back \n"
        config += " no vprn " + str(self.data['id']) + " \n"

#        print(config)
        return config
'''
            description "TC-01-10(j) CLI VPRN on R1 service id:60003 outter:603 inner:1"
            route-distinguisher 1.1.1.1:60001
            auto-bind-tunnel
                resolution-filter
                    sr-policy
                exit
                resolution filter
            exit
            vrf-target target:65001:60001
            interface "to_tester_603.1" create
                address 192.168.100.1/24
                sap lag-97:603.1 create
                    ingress
                        qos 16
                    exit
                    egress
                        qos 16
                    exit
                exit
            exit
            no shutdown

'''