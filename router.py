class router():

    netconf_port = int(830)
    username = 'netconf'
    password = 'Nokia4conf'
    system_ip = '1.1.1.1'
    
    def __init__(self, ip):
        self.ip = ip
        self.netconf_port = 830
        self.username = 'netconf'
        self.password = 'Nokia4conf'

    def set_port(self, port):
        i_port = int(port)
        if i_port > 0 and i_port < 65535 :
            self.netconf_port = i_port

    def set_username(self, username):
        self.username = str(username)

    def set_password(self, password):
        self.password = str(password)

    def set_system_ip(self, system_ip):
        self.system_ip = str(system_ip)
        