from vpls import vpls_endpoint
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
    R1_sap_str = "lag-96"
    R1_sdp = "3"

    R3_OOB_ip = "172.27.1.43"
    R3_system_ip = '3.3.3.3'
    R3_port = 830
    R3_username = "netconf"
    R3_password = "Nokia4conf"
    R3_sap_str = "lag-97"
    R3_sdp = "1"

    R1 = router(R1_OOB_ip)
    R1.netconf_port = R1_port
    R1.username = R1_username
    R1.password = R1_password

    R3 = router(R3_OOB_ip)
    R3.netconf_port = R3_port
    R3.username = R3_username
    R3.password = R3_password

    service_id = 60004
    service_name = 'TC-01-10(i)_EVPN_VPLS'
    outter_tag = 604
    inner_tag = 1
    
    service_r1 = vpls_endpoint(service_id, service_name, R1_sdp, inner_tag, outter_tag, R1_sap_str)

    service_r3 = vpls_endpoint(service_id, service_name, R3_sdp, inner_tag, outter_tag, R3_sap_str)
    
    conn_r1 = connect(R1.ip, R1.netconf_port, R1.username, R1.password)
    print("R1 connected: " + str(conn_r1.connected))

    conn_r3 = connect(R3.ip, R3.netconf_port, R3.username, R3.password)
    print("R3 connected: " + str(conn_r3.connected))

    print(str(datetime.now().time()) + " Begin of R1 vpws provision")
    conn_r1.load_configuration(config=service_r1.to_provision_cli(), format='cli')
    print(str(datetime.now().time()) + " End of R1 vpws provision")

    print(str(datetime.now().time()) + " Begin of R3 vpws provision")
    conn_r3.load_configuration(config=service_r3.to_provision_cli(), format='cli')
    print(str(datetime.now().time()) + " End of R3 vpws provision")
