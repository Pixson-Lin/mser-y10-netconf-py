from ncclient.xml_ import *
from router import router

class evpnvpws_endpoint():
    data = {}

    def __init__(self, id, name, evi, rd, rt_export, rt_import, local_ac, remote_ac, in_tag, out_tag, sap_port):
        self.data['id'] = int(id)
        self.data['name'] = str(name)
        self.data['evi'] = int(evi)
        self.data['rd'] = str(rd)
        self.data['rt_export'] = str(rt_export)
        self.data['rt_import'] = str(rt_import)
        self.data['local_ac'] = int(local_ac)
        self.data['remote_ac'] = int(remote_ac)
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
        str_description = 'tc-01-10 netconf epipe :' + str(self.data['id'])
        sub_ele(cfg_svc_epipe_description, 'description-string').text = str_description
       
        sub_ele(cfg_svc_epipe, 'shutdown').text = 'false'
        
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

        cfg_svc_epipe_bgpevpn_evi = sub_ele(cfg_svc_epipe_bgpevpn, 'evi')
        sub_ele(cfg_svc_epipe_bgpevpn_evi, 'value').text = str(self.data['evi'])

        cfg_svc_epipe_bgpevpn_mpls = sub_ele(cfg_svc_epipe_bgpevpn, 'mpls')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'bgp').text = '1'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'shutdown').text = 'false'
        cfg_svc_epipe_bgpevpn_mpls_tunnel = sub_ele(cfg_svc_epipe_bgpevpn_mpls, 'auto-bind-tunnel')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel, 'enforce-strict-tunnel-tagging').text ='true'
        cfg_svc_epipe_bgpevpn_mpls_tunnel_resolution = sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel, 'resolution')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolution, 'disabled-any-filter').text ='filter'

        cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter = sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel, 'resolution-filter')
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'sr-te').text = 'true'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'bgp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'ldp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'mpls-fwd-policy').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'rib-api').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'rsvp').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'sr-isis').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'sr-ospf').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'sr-policy').text = 'false'
        sub_ele(cfg_svc_epipe_bgpevpn_mpls_tunnel_resolutionfilter, 'udp').text = 'false'

        cfg_svc_epipe_sap = sub_ele(cfg_svc_epipe, 'sap')
        sub_ele(cfg_svc_epipe_sap, 'sap-id').text = self.data['sap_port'] + ":" + str(self.data['out_tag']) + "." + str(self.data['in_tag'])
        sub_ele(cfg_svc_epipe_sap, 'shutdown').text = 'false'

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

