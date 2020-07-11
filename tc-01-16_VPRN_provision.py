from vprn import vprn_endpoint
from router import router
from datetime import datetime
from netconf_conn import connect
from ncclient.xml_ import *


if __name__ == '__main__':
    R1_OOB_ip = "172.27.1.41"
    R1_system_ip = '1.1.1.1'
    R1_port = 830
    R1_username = "netconf"
    R1_password = "Nokia4conf"
    R1_sap_str = "lag-97"

    R3_OOB_ip = "172.27.1.43"
    R3_system_ip = '3.3.3.3'
    R3_port = 830
    R3_username = "netconf"
    R3_password = "Nokia4conf"
    R3_sap_str = "lag-97"

    R1 = router(R1_OOB_ip)
    R1.netconf_port = R1_port
    R1.username = R1_username
    R1.password = R1_password

    R3 = router(R3_OOB_ip)
    R3.netconf_port = R3_port
    R3.username = R3_username
    R3.password = R3_password

    service_id = 60005
    service_name = 'TC-01-16_vprn_' + str(service_id)
    outter_tag = 605
    inner_tag = 1
    R1_if_name = "R1_" + str(service_id) + ":" + str(outter_tag) + ":" + str(inner_tag)
    R1_if_ip = "192.168.100.1/24"
    R1_desc = "TC-01-16_vprn_on_R1_outter:" + str(outter_tag) + "_inner:" + str(inner_tag)
    R3_if_name = "R3_" + str(service_id) + ":" + str(outter_tag) + ":" + str(inner_tag)
    R3_if_ip = "192.168.200.1/24"
    R3_desc = "TC-01-16_vprn_on_R3_outter:" + str(outter_tag) + "_inner:" + str(inner_tag)

    
    service_r1 = vprn_endpoint(service_id, service_name, R1_system_ip+":"+str(service_id), R1_if_name, R1_if_ip, inner_tag, outter_tag, R1_sap_str, R1_desc)

    service_r3 = vprn_endpoint(service_id, service_name, R3_system_ip+":"+str(service_id), R3_if_name, R3_if_ip, inner_tag, outter_tag, R3_sap_str, R3_desc)

    conn_r1 = connect(R1.ip, R1.netconf_port, R1.username, R1.password)
    print("R1 connected: " + str(conn_r1.connected))

    conn_r3 = connect(R3.ip, R3.netconf_port, R3.username, R3.password)
    print("R3 connected: " + str(conn_r3.connected))

    print(str(datetime.now().time()) + " Begin of R1 vprn provision")
    conn_r1.load_configuration(config=service_r1.to_provision_cli(), format='cli')
    print(str(datetime.now().time()) + " End of R1 vprn provision")

    print(str(datetime.now().time()) + " Begin of R3 vprn provision")
    conn_r3.load_configuration(config=service_r3.to_provision_cli(), format='cli')
    print(str(datetime.now().time()) + " End of R3 vprn provision")

