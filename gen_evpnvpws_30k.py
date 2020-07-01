#This script generate a script to run on SROS that provision 30k evpn vpws
#The lag must encap qinq

#this is the loop count to control total number of service 
#and this is also for EVI !!!
service_start = 1
service_end = 30001

#this is the service id of the first vpws service
service_id_start = 30001

#EVI shiftter
evi_start = 1000

#this is the qinq vlan tag, must match or be greater than the total number of service
outter_tag_start = 601
outter_tag_end = 610
inner_tag_start = 1
inner_tag_end = 3000

#the lag for sap to sit on
sap_str = "lag-99"

if (service_end - service_start) < ((outter_tag_end - outter_tag_start + 1) * (inner_tag_end - inner_tag_start + 1)):
    exit("no enough VLAN tag")

fo_R1_p = open("bmt_30k_evpn_R1_provision.txt", "w")
fo_R1_t = open("bmt_30k_evpn_R1_teardown.txt", "w")
fo_R3_p = open("bmt_30k_evpn_R3_provision.txt", "w")
fo_R3_t = open("bmt_30k_evpn_R3_teardown.txt", "w")

service_str  = "/configure service \n"
fo_R1_p.write(service_str)
fo_R3_p.write(service_str)

service_id = service_id_start
outter_tag = outter_tag_start
inner_tag = inner_tag_start
R1_id = "1.1.1.1"
R3_id = "3.3.3.3"

for service in range (service_start, service_end, 1):
#   R1 service
    service_R1_p_str  = "epipe " + str(service_id) + " name \"tc-01-6_evpnvpws" + str(service_id) + "\" customer 1 create" + "\n"
    service_R1_p_str += "description \"TC-01-6 (e) 30k EVPN VPWS on R1 service_id:" + str(service_id) + " outter_tag:" + str(outter_tag) + " inner_tag:" + str(inner_tag) + "\"" + "\n"
    service_R1_p_str += "    bgp" + "\n"
    service_R1_p_str += "        route-distinguisher " + R1_id + ":" + str(service_id) + "\n"
    service_R1_p_str += "        route-target export target:65001:" + str(service_id) + " import target:65001:" + str(service_id) + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "    bgp-evpn" + "\n"
    service_R1_p_str += "        local-ac-name \"1\"" + "\n"
    service_R1_p_str += "            eth-tag 1" + "\n"
    service_R1_p_str += "        exit" + "\n"
    service_R1_p_str += "        remote-ac-name \"3\"" + "\n"
    service_R1_p_str += "            eth-tag 3" + "\n"
    service_R1_p_str += "        exit" + "\n"
    service_R1_p_str += "        evi " + str(service + evi_start) + "\n"
    service_R1_p_str += "        mpls bgp 1" + "\n"
    service_R1_p_str += "            auto-bind-tunnel" + "\n"
    service_R1_p_str += "                resolution-filter" + "\n"
    service_R1_p_str += "                    sr-policy" + "\n"
    service_R1_p_str += "                exit" + "\n"
    service_R1_p_str += "                resolution filter" + "\n"
    service_R1_p_str += "            exit" + "\n"
    service_R1_p_str += "            route-next-hop " + R1_id + "\n"
    service_R1_p_str += "            no shutdown" + "\n"
    service_R1_p_str += "        exit" + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "        sap " + sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_R1_p_str += "        no shutdown" + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "    no shutdown" + "\n"
    service_R1_p_str += "exit" + "\n\n"
#    print(service_str)
    fo_R1_p.write(service_R1_p_str)

    service_R1_t_str  = "/configure service epipe " + str(service_id) + " bgp-evpn mpls shutdown \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " no bgp-evpn \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " sap " + sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " no sap " + sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " shutdown \n"
    service_R1_t_str += "/configure service no epipe " + str(service_id) + " \n\n"
    fo_R1_t.write(service_R1_t_str)


#   R3 service


    service_id = service_id + 1
    if inner_tag == inner_tag_end:
        inner_tag = inner_tag_start
        outter_tag = outter_tag + 1
    else:
        inner_tag = inner_tag + 1

fo_R1_p.close
fo_R1_t.close
fo_R3_p.close
fo_R3_t.close
