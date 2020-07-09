from ncclient import manager
from netconf_conn import connect
from ncclient.xml_ import *
import xml.dom.minidom

def get_conf(host, port, username, password):
    conn = connect(host, port, username, password)
    print(conn.connected)
    conn.async_mode = False
    conn.timeout = 600

#    filter_configure = new_ele('configure', attrs={'xmlns': ALU_CONFIG})
    filter_configure = new_ele('configure', attrs={'xmlns': "urn:nokia.com:sros:ns:yang:sr:conf"})

    filter_system = sub_ele(filter_configure, 'system')
#    sub_ele(filter_epipe, 'service-id').text = "50000"
#    filter_epipe = sub_ele(filter_service, 'epipe')

    print(to_xml(filter_configure))

    result = conn.get_configuration(filter=filter_configure)
    print(result)


if __name__ == '__main__':
    host = "172.27.1.41"
    port = 830
    username = "netconf"
    password = "Nokia4conf"

    get_conf(host, port, username, password)