from ncclient import manager
from netconf_conn import connect
from ncclient.xml_ import *
import xml.dom.minidom


def test_get_vpls(host, port, user_name, pass_word, servicename):
    conn = connect(host, port, user_name, pass_word)
    print(conn.connected)

#    config = new_ele('configure', attrs={'xmlns': ALU_CONFIG})
    config_filter = new_ele('configure', attrs={'xmlns': "urn:nokia.com:sros:ns:yang:sr:conf"})
    cfg_service = sub_ele(config_filter, 'service')
    cfg_service_vpls =  sub_ele(cfg_service, 'vpls')
    sub_ele(cfg_service_vpls, 'service-id').text = str(servicename)

    print(to_xml(config_filter))
    result = conn.get_configuration(filter=config_filter)
    print(result)


def test_conf_sysname(host, port, user_name, pass_word):
    conn = connect(host, port, user_name, pass_word)
    print(conn.connected)

    config = new_ele('configure', attrs={'xmlns': ALU_CONFIG})
#    config = new_ele('configure', attrs={'xmlns': "urn:nokia.com:sros:ns:yang:sr:conf"})
    cfg_system = sub_ele(config, 'system')
    cfg_sys_name = sub_ele(cfg_system, 'name')
    cfg_sys_sysname = sub_ele(cfg_sys_name, 'system-name')
    cfg_sys_sysname.text = 'BMT_R1'
#    cfg_sys_name_sysname = sub_ele(cfg_sys_name, 'system-name')
#    cfg_sys_name_sysname.text = 'SR-2e_'
#    cfg_sys_name_systemname = sub_ele(cfg_sys_name, 'system_name')
#    sub_ele(cfg_sys_name_systemname, 'long-description-string').text = 'mini_mser_R1_n1'
    
    print(to_xml(config))

    conn.load_configuration(config=config, format='xml')
#    conn.commit()

    conn.close_session()

def test_nokia_yang(host, port, user_name, pass_word):
    with manager.connect(host=host, port=830, username=user_name, password=pass_word, hostkey_verify=False) as m:
        print(m.connected)
        for s in m.server_capabilities:
            print(s)


if __name__ == '__main__':
    host = "172.27.1.41"
    port = 830
    username = "netconf"
    password = "Nokia4conf"

#    test_nokia_yang(host, port, username, password)

    test_conf_sysname(host, port, username, password)

#    test_get_vpls(host, port, username, password, 66000)
