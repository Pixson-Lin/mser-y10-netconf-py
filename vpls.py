from ncclient import manager
from lxml import etree
from router import router
from ncclient.xml_ import *

class vpls_endpoint():
    
    def __init__(self, id, name, sdp, in_tag, out_tag, sap_port):
        self.data = {}
        self.data['id'] = int(id)
        self.data['name'] = str(name)
        self.data['sdp'] = str(sdp)
        self.data['in_tag'] = int(in_tag)
        self.data['out_tag'] = int(out_tag)
        self.data['sap_port'] = str(sap_port)
    
    def to_provision_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])

        config  = " configure service vpls " + str(self.data['id']) + " name "+ self.data['name'] + ":" + str(self.data['id']) + " customer 1 create\n"
        config += "   fdb-table-size 500 \n"
        config += "   sap " + sap_str + " create \n"
        config += "     ingress qos 16 \n"
        config += "     egress qos 16 \n"
        config += "     no shutdown \n"
        config += "   exit \n"
        config += "   spoke-sdp " + self.data['sdp'] + ":" + str(self.data['id']) + " create \n"
        config += "     no shutdown \n"
        config += "   exit \n"
        config += "   no shutdown \n"
        config += " exit \n"

#        print(config)
        return config
        
    def to_teardown_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])

        config  = " configure service vpls " + str(self.data['id']) + " \n"
        config += "   sap " + sap_str + " shutdown \n"
        config += "   no sap " + sap_str + " \n"
        config += "   spoke-sdp " + self.data['sdp'] + ":" + str(self.data['id']) + " shutdown \n"
        config += "   no spoke-sdp " + self.data['sdp'] + ":" + str(self.data['id']) + " \n"
        config += "   shutdown \n"
        config += "   back \n"
        config += "   no vpls " + str(self.data['id']) + " \n"

#        print(config)
        return config
'''
            fdb-table-size 500
            stp
                shutdown
            exit
            sap lag-96:604.1 create
                ingress
                    qos 16
                exit
                egress
                    qos 16
                exit
                no shutdown
            exit
            sap lag-97:604.1 create
                ingress
                    qos 16
                exit
                egress
                    qos 16
                exit
                no shutdown
            exit
            spoke-sdp 3:60004 create
                no shutdown
            exit
            no shutdown

'''