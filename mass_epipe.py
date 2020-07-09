from vpws import evpnvpws_endpoint
from router import router
from ncclient import manager
from ncclient.xml_ import *
from datetime import datetime
from netconf_conn import connect

def create_vpws(conn, service_list):
    for service_xml in service_list:
#        print(str(datetime.now().time()) + " begin to load vpws config" + to_xml(service_xml))
        conn.load_configuration(config=service_xml, format='xml')
#        print(str(datetime.now().time()) + " done ")


if __name__ == '__main__':
    R1_ip = "172.27.1.41"
    R1_port = 830
    R1_username = "netconf"
    R1_password = "Nokia4conf"

    R1 = router(R1_ip)
    R1.netconf_port = R1_port
    R1.username = R1_username
    R1.password = R1_password

############################################
s_tag_start = 101
s_tag_end = 102
i_tag_start = 1
i_tag_end = 1001
service_id_shift = 10000

count = 0
R1_service_array = []

route_target = "target:65001:51000"

conn1 = connect(R1.ip, R1.netconf_port, R1.username, R1.password)

print(str(datetime.now().time()) + " begin to prepare vpws config")

for s_tag in range (s_tag_start, s_tag_end, 1):
    for i_tag in range(i_tag_start, i_tag_end, 1) :
        service = (s_tag - s_tag_start) * i_tag_end + i_tag + service_id_shift
        service1_rd = str(R1.ip) + ":" + str(service)
        service1 = evpnvpws_endpoint(service, service, service, service1_rd, route_target, route_target, 1, 2, i_tag, s_tag, 'lag-1')
        R1_service_array.append(service1.to_alu_r13_xml())
        count = count + 1
#        print(to_xml(service1.to_alu_r13_xml()))

print(str(datetime.now().time()) + " "+ str(count) + " vpws prepared")


create_vpws(conn1, R1_service_array)

print(str(datetime.now().time()) + " "+ str(count) + " vpws deployed")

