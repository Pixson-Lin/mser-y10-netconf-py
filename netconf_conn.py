from ncclient import manager

def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=30,
                           device_params={'name': 'alu'},
                           hostkey_verify=False)
    
    return conn

if __name__ == '__main__':
    host = "172.27.0.41"
    port = 830
    user_name = "netconf"
    pass_word = "Nokia4conf"

    with manager.connect(host=host, port=830, username=user_name, password=pass_word, hostkey_verify=False) as m:
        print(m.connected)
        for s in m.server_capabilities:
            print(s)
#        c = m.get_config(source='running').data_xml
#        print(c)
        