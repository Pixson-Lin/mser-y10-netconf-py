from ncclient.xml_ import *
from router import router

class evpnvpws_endpoint():

    def __init__(self, id, name, evi, rd, rt_export, rt_import, local_ac, remote_ac, route_next_hop, in_tag, out_tag, sap_port):
        self.data = {}
        self.data['id'] = int(id)
        self.data['name'] = str(name)
        self.data['evi'] = int(evi)
        self.data['rd'] = str(rd)
        self.data['rt_export'] = str(rt_export)
        self.data['rt_import'] = str(rt_import)
        self.data['local_ac'] = int(local_ac)
        self.data['remote_ac'] = int(remote_ac)
        self.data['route_next_hop'] = str(route_next_hop)
        self.data['in_tag'] = int(in_tag)
        self.data['out_tag'] = int(out_tag)
        self.data['sap_port'] = str(sap_port)
    
    def to_alu_r13_xml(self):
        yang_config_root = new_ele('configure', attrs={'xmlns': ALU_CONFIG})
        cfg_service = sub_ele(yang_config_root, 'service')
        cfg_svc_epipe = sub_ele(cfg_service, 'epipe')
        
        sub_ele(cfg_svc_epipe, 'service-id').text = str(self.data['id'])

        sub_ele(cfg_svc_epipe, 'customer').text = '1'

        cfg_svc_epipe_description = sub_ele(cfg_svc_epipe, 'description')
        str_description = 'TC-01-10(i) evpn vpws :' + str(self.data['id']) + ' outter: ' + str(self.data['out_tag']) + ' inner:' + str(self.data['in_tag'])
        sub_ele(cfg_svc_epipe_description, 'description-string').text = str_description
        
        cfg_svc_epipe_bgp = sub_ele(cfg_svc_epipe, 'bgp')
        cfg_svc_epipe_bgp_rd = sub_ele(cfg_svc_epipe_bgp, 'route-distinguisher')
        sub_ele(cfg_svc_epipe_bgp_rd, 'rd').text = self.data['rd']

        cfg_svc_epipe_bgp_rt= sub_ele(cfg_svc_epipe_bgp, 'route-target')
        sub_ele(cfg_svc_epipe_bgp_rt, 'export').text = self.data['rt_export']
        sub_ele(cfg_svc_epipe_bgp_rt, 'import').text = self.data['rt_import']

        cfg_svc_epipe_bgpevpn = sub_ele(cfg_svc_epipe, 'bgp-evpn')
        cfg_svc_epipe_bgpevpn_localac = sub_ele(cfg_svc_epipe_bgpevpn, 'local-ac-name')
        sub_ele(cfg_svc_epipe_bgpevpn_localac, 'ac-name').text = "AC-" + str(self.data['local_ac'])
        cfg_svc_epipe_bgpevpn_localac_ethtag = sub_ele(cfg_svc_epipe_bgpevpn_localac, 'eth-tag')
        sub_ele(cfg_svc_epipe_bgpevpn_localac_ethtag, 'tag-value').text = str(self.data['local_ac'])

        cfg_svc_epipe_bgpevpn_remoteac = sub_ele(cfg_svc_epipe_bgpevpn, 'remote-ac-name')
        sub_ele(cfg_svc_epipe_bgpevpn_remoteac, 'ac-name').text = "AC-" + str(self.data['remote_ac'])
        cfg_svc_epipe_bgpevpn_remoteac_ethtag = sub_ele(cfg_svc_epipe_bgpevpn_remoteac, 'eth-tag')
        sub_ele(cfg_svc_epipe_bgpevpn_remoteac_ethtag, 'tag-value').text = str(self.data['remote_ac'])

        cfg_svc_epipe_bgpevpn_mpls = sub_ele(cfg_svc_epipe_bgpevpn, 'mpls')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'bgp').text = '1'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'shutdown').text = 'true'

        cfg_svc_epipe_bgpevpn_mpls_atunl = sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'auto-bind-tunnel')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl, 'enforce-strict-tunnel-tagging').text ='false'

        cfg_svc_epipe_bgpevpn_mpls_atunl_res = sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl, 'resolution')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_res, 'disabled-any-filter').text ='filter'

        cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter = sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl, 'resolution-filter')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'bgp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'ldp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'mpls-fwd-policy').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'rib-api').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'rsvp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'sr-isis').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'sr-ospf').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'sr-ospf3').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'sr-policy').text = 'true'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'sr-te').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_atunl_resfilter, 'udp').text = 'false'

        cfg_svc_epipe_bgpevpn_mpls_rnh = sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'route-next-hop')
#        sub_ele(cfg_svc_epipe_bgpevpn_mpls_rnh, 'system-ipv4').text  = 'false'
#        sub_ele(cfg_svc_epipe_bgpevpn_mpls_rnh, 'system-ipv6').text  = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_rnh, 'ip-address').text  = self.data['route_next_hop']
        sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'shutdown').text = 'false'

        cfg_svc_epipe_sap = sub_ele(cfg_svc_epipe, 'sap')
        sub_ele(cfg_svc_epipe_sap, 'sap-id').text = self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])
        sub_ele(cfg_svc_epipe_sap, 'shutdown').text = 'false'

        sub_ele(cfg_svc_epipe, 'shutdown').text = 'false'

        return yang_config_root

    def to_teardown_cli(self):
        sap_str =  self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])
        config  = " configure service epipe " + str(self.data['id']) + " \n"
        config += "   sap " + sap_str + " shutdown \n"
        config += "   no sap " + sap_str + " \n"
        config += "   bgp-evpn mpls shutdown \n"
        config += "   no bgp-evpn \n"
        config += "   no bgp \n"
        config += "   shutdown \n"
        config += "   back \n"
        config += "   no epipe " + str(self.data['id']) + " \n"

        return config


'''
            description "TC-01-6(e) 30k EVPN VPWS on R3 service_id:30001 outter:101 inner:1"
            bgp
                route-distinguisher 3.3.3.3:30001
                route-target export target:65001:30001 import target:65001:30001
            exit
            bgp-evpn
                local-ac-name "3"
                    eth-tag 3
                exit
                remote-ac-name "1"
                    eth-tag 1
                exit
                mpls bgp 1
                    auto-bind-tunnel
                        resolution-filter
                            sr-policy
                        exit
                        resolution filter
                    exit
                    route-next-hop 3.3.3.3
                    no shutdown
                exit
            exit
            sap lag-97:101.1 create
                ingress
                    qos 16
                exit
                egress
                    qos 16
                exit
                no shutdown
            exit
            no shutdown
'''

