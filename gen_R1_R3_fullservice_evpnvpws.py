#This script generate a script to run on SROS that provision 30k evpn vpws
#The lag must encap qinq

#this is the loop count to control total number of service 
service_start = 1
service_end = 25801

#this is the service id of the first vpws service
service_id_start = 200000
service_id_middle = 201899

#this is the qinq vlan tag, must match or be greater than the total number of service
outter_tag_start = 1001
outter_tag_end = 1258
inner_tag_start = 1
inner_tag_end = 100

#the lag for sap to sit on
R1_sap_str = ["lag-96", "lag-97"]
R3_sap_str = ["lag-97", "lag-97"]

if (service_end - service_start) < ((outter_tag_end - outter_tag_start + 1) * (inner_tag_end - inner_tag_start + 1)):
    exit("no enough VLAN tag")

fo_R1_p = open("bmt_fullservice_R1_R3_epipe_provision.txt", "w")
fo_R1_t = open("bmt_fullservice_R1_R3_epipe_teardown.txt", "w")
fo_R3_p = open("bmt_fullservice_R3_R1_epipe_provision.txt", "w")
fo_R3_t = open("bmt_fullservice_R3_R1_epipe_teardown.txt", "w")

service_str  = "/configure service \n"
fo_R1_p.write(service_str)
fo_R3_p.write(service_str)

service_id = service_id_start
outter_tag = outter_tag_start
inner_tag = inner_tag_start
R1_id = "65200"
R3_id = "65201"

################################################################################
### BEGIN of loop
for service in range (service_start, service_end, 1):
#   R1 service
    service_R1_p_str  = "epipe " + str(service_id) + " name \"TC-01-18_fullservice_to_R3_vpws_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R1_p_str += "description \"TC-01-18_fullservice_ EVPN VPWS on R1 service_id:" + str(service_id) + " outter:" + str(outter_tag) + " inner:" + str(inner_tag) + "\"\n"
    service_R1_p_str += "    bgp" + "\n"
    service_R1_p_str += "        route-distinguisher " + R1_id + ":" + str(service_id) + "\n"
    service_R1_p_str += "        route-target export target:" + R3_id + ":" + str(service_id) + " import target:" + R3_id + ":" + str(service_id) + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "    bgp-evpn" + "\n"
    service_R1_p_str += "        local-ac-name 1 eth-tag 1\n"
    service_R1_p_str += "        remote-ac-name 3 eth-tag 3\n"
    service_R1_p_str += "        mpls bgp 1" + "\n"
    service_R1_p_str += "            auto-bind-tunnel" + "\n"
    service_R1_p_str += "                resolution any" + "\n"
    service_R1_p_str += "            exit" + "\n"
    service_R1_p_str += "            no shutdown" + "\n"
    service_R1_p_str += "        exit" + "\n"
    service_R1_p_str += "    exit" + "\n"
    if(service_id < service_id_middle):
        service_R1_p_str += "    sap " + R1_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    else:
        service_R1_p_str += "    sap " + R1_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_R1_p_str += "            ingress qos 118" + "\n"
    service_R1_p_str += "            egress qos 118" + "\n"
    service_R1_p_str += "        no shutdown" + "\n"
    service_R1_p_str += "    exit" + "\n"
    service_R1_p_str += "    no shutdown" + "\n"
    service_R1_p_str += "exit" + "\n\n"
#    print(service_str)
    fo_R1_p.write(service_R1_p_str)

# R1 teardown
    service_R1_t_str  = "/configure service epipe " + str(service_id) + " bgp-evpn mpls shutdown \n"
    service_R1_t_str += "/configure service epipe " + str(service_id) + " no bgp-evpn \n"
    if(service_id < service_id_middle):
        service_R1_t_str += "/configure service epipe " + str(service_id) + " sap " + R1_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
        service_R1_t_str += "/configure service epipe " + str(service_id) + " no sap " + R1_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"
    else:
        service_R1_t_str += "/configure service epipe " + str(service_id) + " sap " + R1_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
        service_R1_t_str += "/configure service epipe " + str(service_id) + " no sap " + R1_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"  
    service_R1_t_str += "/configure service epipe " + str(service_id) + " shutdown \n"
    service_R1_t_str += "/configure service no epipe " + str(service_id) + " \n\n"
    fo_R1_t.write(service_R1_t_str)

#   R3 service
    service_R3_p_str  = "epipe " + str(service_id) + " name \"TC-01-18_fullservice_to_R1_vpws_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R3_p_str += "description \"TC-01-18_fullservice_ EVPN VPWS on R3 service_id:" + str(service_id) + " outter:" + str(outter_tag) + " inner:" + str(inner_tag) + "\"\n"
    service_R3_p_str += "    bgp" + "\n"
    service_R3_p_str += "        route-distinguisher " + R3_id + ":" + str(service_id) + "\n"
    service_R3_p_str += "        route-target export target:" + R3_id + ":" + str(service_id) + " import target:" + R3_id + ":" + str(service_id) + "\n"
    service_R3_p_str += "    exit" + "\n"
    service_R3_p_str += "    bgp-evpn" + "\n"
    service_R3_p_str += "        local-ac-name 3 eth-tag 3\n"
    service_R3_p_str += "        remote-ac-name 1 eth-tag 1\n"
    service_R3_p_str += "        mpls bgp 1" + "\n"
    service_R3_p_str += "            auto-bind-tunnel" + "\n"
    service_R3_p_str += "                resolution any" + "\n"
    service_R3_p_str += "            exit" + "\n"
    service_R3_p_str += "            no shutdown" + "\n"
    service_R3_p_str += "        exit" + "\n"
    service_R3_p_str += "    exit" + "\n"
    if(service_id < service_id_middle):
        service_R3_p_str += "    sap " + R3_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    else:
        service_R3_p_str += "    sap " + R3_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_R3_p_str += "            ingress qos 118" + "\n"
    service_R3_p_str += "            egress qos 118" + "\n"
    service_R3_p_str += "        no shutdown" + "\n"
    service_R3_p_str += "    exit" + "\n"
    service_R3_p_str += "    no shutdown" + "\n"
    service_R3_p_str += "exit" + "\n\n"
#    print(service_str)
    fo_R3_p.write(service_R3_p_str)

# R1 teardown
    service_R3_t_str  = "/configure service epipe " + str(service_id) + " bgp-evpn mpls shutdown \n"
    service_R3_t_str += "/configure service epipe " + str(service_id) + " no bgp-evpn \n"
    if(service_id < service_id_middle):
        service_R3_t_str += "/configure service epipe " + str(service_id) + " sap " + R3_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
        service_R3_t_str += "/configure service epipe " + str(service_id) + " no sap " + R3_sap_str[0] + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"
    else:
        service_R3_t_str += "/configure service epipe " + str(service_id) + " sap " + R3_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown \n"
        service_R3_t_str += "/configure service epipe " + str(service_id) + " no sap " + R3_sap_str[1] + ":" + str(outter_tag) + "." + str(inner_tag) + " \n"  
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







'''
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

### TO go to LAG-97 for 23900 epipes

#this is the loop count to control total number of service 
service_start = 1
service_end = 23901

#this is the service id of the first vpws service
service_id_start = 201900

#this is the qinq vlan tag, must match or be greater than the total number of service
outter_tag_start = 1020
outter_tag_end = 1259
inner_tag_start = 1
inner_tag_end = 100

'''