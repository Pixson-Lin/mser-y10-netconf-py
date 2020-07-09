from evpn_vpws import evpnvpws_endpoint
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

    R3_OOB_ip = "172.27.1.43"
    R3_system_ip = '3.3.3.3'
    R3_port = 830
    R3_username = "netconf"
    R3_password = "Nokia4conf"

    R1 = router(R1_OOB_ip)
    R1.netconf_port = R1_port
    R1.username = R1_username
    R1.password = R1_password

    R3 = router(R3_OOB_ip)
    R3.netconf_port = R3_port
    R3.username = R3_username
    R3.password = R3_password

    service_id = 60002
    service_name = 'TC-01-10(i)_EVPN_VPWS'
    outter_tag = 602
    inner_tag = 1
    route_target = "target:65300:60002"
    sap_str = "lag-97"

    service_r1_rd = str(R1_system_ip) + ":" + str(service_id)
    service_r1 = evpnvpws_endpoint(service_id, service_id, service_id, service_r1_rd, route_target, route_target, 1, 3, R1_system_ip, inner_tag, outter_tag, sap_str)
#    print(to_xml(service_r1.to_alu_r13_xml()))

    service_r3_rd = str(R3_system_ip) + ":" + str(service_id)
    service_r3 = evpnvpws_endpoint(service_id, service_id, service_id, service_r3_rd, route_target, route_target, 3, 1, R3_system_ip, inner_tag, outter_tag, sap_str)
#    print(to_xml(service_r3.to_alu_r13_xml()))

    conn_r1 = connect(R1.ip, R1.netconf_port, R1.username, R1.password)
    print("R1 connected: " + str(conn_r1.connected))

    conn_r3 = connect(R3.ip, R3.netconf_port, R3.username, R3.password)
    print("R3 connected: " + str(conn_r3.connected))

    print(str(datetime.now().time()) + " Begin of R1 vpws provision")
    conn_r1.load_configuration(config=service_r1.to_alu_r13_xml(), format='xml')
    print(str(datetime.now().time()) + " End of R1 vpws provision")

    print()

    print(str(datetime.now().time()) + " Begin of R3 vpws provision")
    conn_r3.load_configuration(config=service_r3.to_alu_r13_xml(), format='xml')
    print(str(datetime.now().time()) + " End of R3 vpws provision")

