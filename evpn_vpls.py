from ncclient import manager
from lxml import etree
from router import router
from ncclient.xml_ import *

class evpnvpls_endpoint():
    
    def __init__(self, id, name, rd, rt_export, rt_import, route_next_hop, in_tag, out_tag, sap_port):
        self.data = {}
        self.data['id'] = int(id)
        self.data['name'] = str(name)
        self.data['rd'] = str(rd)
        self.data['rt_export'] = str(rt_export)
        self.data['rt_import'] = str(rt_import)
        self.data['route_next_hop'] = str(route_next_hop)
        self.data['in_tag'] = int(in_tag)
        self.data['out_tag'] = int(out_tag)
        self.data['sap_port'] = str(sap_port)
#        print(self.data['route_next_hop'])

    def to_alu_r13_xml(self):
        yang_config_root = new_ele('configure', attrs={'xmlns': ALU_CONFIG})
        cfg_service = sub_ele(yang_config_root, 'service')
        cfg_svc_vpls = sub_ele(cfg_service, 'vpls')

        sub_ele(cfg_svc_vpls, 'service-id').text = str(self.data['id'])
        sub_ele(cfg_svc_vpls, 'name').text = str(self.data['name'])
        sub_ele(cfg_svc_vpls, 'customer').text = '1'

        cfg_svc_vpls_description = sub_ele(cfg_svc_vpls, 'description')
        str_description = 'TC-01-10(i) evpn vpls :' + str(self.data['id']) + ' outter: ' + str(self.data['out_tag']) + ' inner:' + str(self.data['in_tag'])
        sub_ele(cfg_svc_vpls_description, 'description-string').text = str_description

        cfg_svc_vpls_fdbsize = sub_ele(cfg_svc_vpls, 'fdb-table-size')
        sub_ele(cfg_svc_vpls_fdbsize, 'table-size').text = '500'

        cfg_svc_vpls_bgp = sub_ele(cfg_svc_vpls, 'bgp')
        cfg_svc_vpls_bgp_rd = sub_ele(cfg_svc_vpls_bgp, 'route-distinguisher')
        sub_ele(cfg_svc_vpls_bgp_rd, 'rd').text = self.data['rd']

        cfg_svc_vpls_bgp_rt= sub_ele(cfg_svc_vpls_bgp, 'route-target')
        sub_ele(cfg_svc_vpls_bgp_rt, 'export').text = self.data['rt_export']
        sub_ele(cfg_svc_vpls_bgp_rt, 'import').text = self.data['rt_import']

        cfg_svc_vpls_bgpevpn = sub_ele(cfg_svc_vpls, 'bgp-evpn')
        cfg_svc_vpls_bgpevpn_mpls = sub_ele(cfg_svc_vpls_bgpevpn, 'mpls')
        sub_ele(cfg_svc_vpls_bgpevpn_mpls, 'bgp').text = '1'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls, 'shutdown').text = 'true'

        cfg_svc_vpls_bgpevpn_mpls_atunl = sub_ele(cfg_svc_vpls_bgpevpn_mpls, 'auto-bind-tunnel')
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl, 'enforce-strict-tunnel-tagging').text ='false'

        cfg_svc_vpls_bgpevpn_mpls_atunl_res = sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl, 'resolution')
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_res, 'disabled-any-filter').text ='filter'

        cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter = sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl, 'resolution-filter')
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'bgp').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'ldp').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'mpls-fwd-policy').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'rib-api').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'rsvp').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'sr-isis').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'sr-ospf').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'sr-ospf3').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'sr-policy').text = 'true'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'sr-te').text = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_atunl_resfilter, 'udp').text = 'false'

        cfg_svc_vpls_bgpevpn_mpls_rnh = sub_ele(cfg_svc_vpls_bgpevpn_mpls, 'route-next-hop')
#        sub_ele(cfg_svc_vpls_bgpevpn_mpls_rnh, 'system-ipv4').text  = 'false'
#        sub_ele(cfg_svc_vpls_bgpevpn_mpls_rnh, 'system-ipv6').text  = 'false'
        sub_ele(cfg_svc_vpls_bgpevpn_mpls_rnh, 'ip-address').text  = self.data['route_next_hop']
        sub_ele(cfg_svc_vpls_bgpevpn_mpls, 'shutdown').text = 'false'

        cfg_svc_vpls_sap = sub_ele(cfg_svc_vpls, 'sap')
        sub_ele(cfg_svc_vpls_sap, 'sap-id').text = self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])
        sub_ele(cfg_svc_vpls_sap, 'shutdown').text = 'false'        

        sub_ele(cfg_svc_vpls, 'shutdown').text = 'false'

        return yang_config_root

    def to_teardown_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])
        config  = " configure service vpls " + str(self.data['id']) + " \n"
        config += "   sap " + sap_str + " shutdown \n"
        config += "   no sap " + sap_str + " \n"
        config += "   bgp-evpn mpls shutdown \n"
        config += "   no bgp-evpn \n"
        config += "   shutdown \n"
        config += "   back \n"
        config += "   no vpls " + str(self.data['id']) + " \n"

        return config


'''
            bgp
                route-distinguisher 65001:1
                route-target export target:65001:66000 import target:65001:66000
            exit
            bgp-evpn
                mpls bgp 1
                    auto-bind-tunnel
                        resolution-filter
                            sr-policy
                        exit
                        resolution filter
                    exit
                    route-next-hop 1.1.1.1
                    no shutdown
                exit
            exit
            stp
                shutdown
            exit
            sap lag-97:660.1 create
                no shutdown
            exit
            no shutdown
'''
