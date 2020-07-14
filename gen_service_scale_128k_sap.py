service_id_start = 300001
service_id_end = 363001
sap1_str = "lag-81"
sap2_str = "lag-82"
outter_tag_start = 1001
outter_tag_end = 10016
inner_tag_start = 1
inner_tag_end = 4000

service_id = service_id_start
outter_tag = outter_tag_start
inner_tag = inner_tag_start

foc = open("service_scale_local_epipe_128k_sap_create.txt", "w")
foc.write("/configure service \n")

fot = open("service_scale_local_epipe_128k_sap_teardown.txt", "w")
fot.write("/configure service \n")

for service in range (service_id_start, service_id_end, 1):
    service_str  = "  epipe " + str(service_id) + " name \"epipe_" + str(service_id) + "\" customer 1 create" + "\n"
    service_str += "    description \"service_scale_local_epipe: " + str(service_id) + " outter_tag:" + str(outter_tag) + " inner_tag:" + str(inner_tag) + "\"" + "\n"
    service_str += "    sap " + sap1_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_str += "      ingress qos 118\n"
    service_str += "      no shutdown" + "\n"
    service_str += "    exit" + "\n"
    service_str += "    sap " + sap2_str + ":" + str(outter_tag) + "." + str(inner_tag) + " create" + "\n"
    service_str += "      ingress qos 118\n"
    service_str += "      no shutdown" + "\n"
    service_str += "    exit" + "\n"
    service_str += "    no shutdown" + "\n"
    service_str += "  exit" + "\n\n"
#    print(service_str)
    foc.write(service_str)

    teardown_str  = "  epipe " + str(service_id) +"\n"
    teardown_str += "    sap " + sap1_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown" + "\n"
    teardown_str += "    no sap " + sap1_str + ":" + str(outter_tag) + "." + str(inner_tag) + "\n"
    teardown_str += "    sap " + sap2_str + ":" + str(outter_tag) + "." + str(inner_tag) + " shutdown" + "\n"
    teardown_str += "    no sap " + sap2_str + ":" + str(outter_tag) + "." + str(inner_tag) + "\n"
    teardown_str += "  shutdown\n"
    teardown_str += "  exit\n"
    teardown_str += "  no epipe " + str(service_id) +"\n\n"
    fot.write(teardown_str)

    service_id = service_id + 1
    if inner_tag == inner_tag_end:
        inner_tag = inner_tag_start
        outter_tag = outter_tag + 1
    else:
        inner_tag = inner_tag + 1
    