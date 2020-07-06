#This script generate a script to run on SROS that provision 8k evpn vpws
#The lag must encap qinq

#this is the loop count to control total number of service 
service_start = 1
service_end = 8001

#this is the service id of the first vprn service
service_id_start = 20001

#this is the qinq vlan tag, must match or be greater than the total number of service
outter_tag_start = 301
outter_tag_end = 340
inner_tag_start = 501
inner_tag_end = 700

#the lag for sap to sit on
R1_sap_str = "lag-97"
R3_sap_str = "lag-97"

if (service_end - service_start) < ((outter_tag_end - outter_tag_start + 1) * (inner_tag_end - inner_tag_start + 1)):
    exit("no enough VLAN tag")

fo_R1_p = open("bmt_8k_vprn_R1_provision.txt", "w")
fo_R1_t = open("bmt_8k_vprn_R1_teardown.txt", "w")
fo_R3_p = open("bmt_8k_vprn_R3_provision.txt", "w")
fo_R3_t = open("bmt_8k_vprn_R3_teardown.txt", "w")

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
    service_R1_p_str  = "vprn " + str(service_id) + " name \"TC-01-6_vprn_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R1_p_str += "    description \"TC-01-6(e) 8k VPRN on R1 service id:" + str(service_id) + " outter:" + str(outter_tag) +  " inner:" + str(inner_tag) + "\"\n"
    service_R1_p_str += "    route-distinguisher " + R1_id + ":" + str(service_id) + "\n"
    service_R1_p_str += "    auto-bind-tunnel\n"
    service_R1_p_str += "        resolution-filter\n"
    service_R1_p_str += "            sr-policy\n"
    service_R1_p_str += "        exit\n"
    service_R1_p_str += "        resolution filter\n"
    service_R1_p_str += "    exit\n"
    service_R1_p_str += "    vrf-target target:65001:" + str(service_id) + "\n"
    service_R1_p_str += "    interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" create\n"
    service_R1_p_str += "        address 192.168.100.1/24\n"
    service_R1_p_str += "        sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create\n"
    service_R1_p_str += "            ingress qos 16" + "\n"
    service_R1_p_str += "            egress qos 16" + "\n"
    service_R1_p_str += "        exit\n"
    service_R1_p_str += "    exit\n"
    service_R1_p_str += "    no shutdown\n"
    service_R1_p_str += "exit\n\n"
    fo_R1_p.write(service_R1_p_str)

# R1 teardown
    service_R1_t_str  = "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown\n"
    service_R1_t_str += "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" no sap " + R1_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + "\n"
    service_R1_t_str += "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" shutdown\n"
    service_R1_t_str += "/configure service vprn " + str(service_id) + " no interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\"\n"
    service_R1_t_str += "/configure service vprn " + str(service_id) + " shutdown \n"
    service_R1_t_str += "/configure service no vprn " + str(service_id) + " \n\n"
    fo_R1_t.write(service_R1_t_str)

#   R3 service
    service_R3_p_str  = "vprn " + str(service_id) + " name \"TC-01-6_vprn_" + str(service_id) + "\" customer 1 create" + "\n"
    service_R3_p_str += "    description \"TC-01-6(e) 8k VPRN on R3 service id:" + str(service_id) + " outter:" + str(outter_tag) +  " inner:" + str(inner_tag) + "\"\n"
    service_R3_p_str += "    route-distinguisher " + R3_id + ":" + str(service_id) + "\n"
    service_R3_p_str += "    auto-bind-tunnel\n"
    service_R3_p_str += "        resolution-filter\n"
    service_R3_p_str += "            sr-policy\n"
    service_R3_p_str += "        exit\n"
    service_R3_p_str += "        resolution filter\n"
    service_R3_p_str += "    exit\n"
    service_R3_p_str += "    vrf-target target:65001:" + str(service_id) + "\n"
    service_R3_p_str += "    interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" create\n"
    service_R3_p_str += "        address 192.168.200.1/24\n"
    service_R3_p_str += "        sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create\n"
    service_R3_p_str += "            ingress qos 16" + "\n"
    service_R3_p_str += "            egress qos 16" + "\n"
    service_R3_p_str += "        exit\n"
    service_R3_p_str += "    exit\n"
    service_R3_p_str += "    no shutdown\n"
    service_R3_p_str += "exit\n\n"
    fo_R3_p.write(service_R3_p_str)

# R3 teardown
    service_R3_t_str  = "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown\n"
    service_R3_t_str += "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" no sap " + R3_sap_str + ":" + str(outter_tag) + "." + str(inner_tag) + "\n"
    service_R3_t_str += "/configure service vprn " + str(service_id) + " interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\" shutdown\n"
    service_R3_t_str += "/configure service vprn " + str(service_id) + " no interface \"to_tester_" + str(outter_tag) + "." + str(inner_tag) + "\"\n"
    service_R3_t_str += "/configure service vprn " + str(service_id) + " shutdown \n"
    service_R3_t_str += "/configure service no vprn " + str(service_id) + " \n\n"
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
