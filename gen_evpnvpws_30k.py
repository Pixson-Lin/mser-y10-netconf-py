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
outter_tag_start = 101
outter_tag_end = 110
inner_tag_start = 1
inner_tag_end = 3000

#the lag for sap to sit on
R1_sap_str = "lag-96"
R3_sap_str = "lag-97"

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

################################################################################
### BEGIN of loop
for service in range (service_start, service_end, 1):
#   R1 service
    service_R1_p_str  = "epipe " + str(service_id) + " name \"TC-01-6_evpnvpws_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R1_p_str += "description \"TC-01-6(e) 30k EVPN VPWS on R1 service_id:" + str(service_id) + " outter:" + str(outter_tag) + " inner:" + str(inner_tag) + "\"\n"
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
###  cancel usage of evi  
#    service_R1_p_str += "        evi " + str(service + evi_start) + "\n"
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
    service_R1_p_str += "        sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_R1_p_str += "            ingress qos 16" + "\n"
    service_R1_p_str += "            egress qos 16" + "\n"
    service_R1_p_str += "        no shutdown" + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "    no shutdown" + "\n"
    service_R1_p_str += "exit" + "\n\n"
#    print(service_str)
    fo_R1_p.write(service_R1_p_str)

# R1 teardown
    service_R1_t_str  = "/configure service epipe " + str(service_id) + " bgp-evpn mpls shutdown \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " no bgp-evpn \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " no sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " shutdown \n"
    service_R1_t_str += "/configure service no epipe " + str(service_id) + " \n\n"
    fo_R1_t.write(service_R1_t_str)

# R3 service
    service_R3_p_str  = "epipe " + str(service_id) + " name \"TC-01-6_evpnvpws_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R3_p_str += "description \"TC-01-6(e) 30k EVPN VPWS on R3 service_id:" + str(service_id) + " outter:" + str(outter_tag) + " inner:" + str(inner_tag) + "\"\n"
    service_R3_p_str += "    bgp" + "\n"
    service_R3_p_str += "        route-distinguisher " + R3_id + ":" + str(service_id) + "\n"
    service_R3_p_str += "        route-target export target:65001:" + str(service_id) + " import target:65001:" + str(service_id) + "\n"
    service_R3_p_str += "    exit" + "\n"
    service_R3_p_str += "    bgp-evpn" + "\n"
    service_R3_p_str += "        local-ac-name \"3\"" + "\n"
    service_R3_p_str += "            eth-tag 3" + "\n"
    service_R3_p_str += "        exit" + "\n"
    service_R3_p_str += "        remote-ac-name \"1\"" + "\n"
    service_R3_p_str += "            eth-tag 1" + "\n"
    service_R3_p_str += "        exit" + "\n"
###  cancel usage of evi  
#    service_R3_p_str += "        evi " + str(service + evi_start) + "\n"
    service_R3_p_str += "        mpls bgp 1" + "\n"
    service_R3_p_str += "            auto-bind-tunnel" + "\n"
    service_R3_p_str += "                resolution-filter" + "\n"
    service_R3_p_str += "                    sr-policy" + "\n"
    service_R3_p_str += "                exit" + "\n"
    service_R3_p_str += "                resolution filter" + "\n"
    service_R3_p_str += "            exit" + "\n"
    service_R3_p_str += "            route-next-hop " + R3_id + "\n"
    service_R3_p_str += "            no shutdown" + "\n"
    service_R3_p_str += "        exit" + "\n"
    service_R3_p_str += "    exit" + "\n"
    service_R3_p_str += "        sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_R3_p_str += "            ingress qos 16" + "\n"
    service_R3_p_str += "            egress qos 16" + "\n"
    service_R3_p_str += "        no shutdown" + "\n"
    service_R3_p_str += "    exit" + "\n"
    service_R3_p_str += "    no shutdown" + "\n"
    service_R3_p_str += "exit" + "\n\n"
#    print(service_str)
    fo_R3_p.write(service_R3_p_str)

# R3 teardown
    service_R3_t_str  = "/configure service epipe " + str(service_id) + " bgp-evpn mpls shutdown \n"
    service_R3_t_str += "/configure service epipe " + str(service_id) + " no bgp-evpn \n"
    service_R3_t_str += "/configure service epipe " + str(service_id) + " sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
    service_R3_t_str += "/configure service epipe " + str(service_id) + " no sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"
    service_R3_t_str += "/configure service epipe " + str(service_id) + " shutdown \n"
    service_R3_t_str += "/configure service no epipe " + str(service_id) + " \n\n"
    fo_R3_t.write(service_R3_t_str)

# handle loop variables
    service_id = service_id + 1
    if inner_tag == inner_tag_end:
        inner_tag = inner_tag_start
        outter_tag = outter_tag + 1
    else:
        inner_tag = inner_tag + 1

### END of loop
################################################################################


fo_R1_p.close
fo_R1_t.close
fo_R3_p.close
fo_R3_t.close
