#!/usr/bin/env python

import sys
import cobra.mit.session
import cobra.model.datetime
from cobra.mit.access import MoDirectory
from cobra.mit.request import ConfigRequest
import cobra.mit.naming
import json

from cobra.internal.codec.xmlcodec import toXMLStr

def apic_login(hostname, username, password):
    '''
    Function that creates a session to communicate with the APIC
    '''
    url = "https://" + hostname
    login_session = cobra.mit.session.LoginSession(url, username, password)
    modir = MoDirectory(login_session)
    print 'connecting to ' + hostname
    try:
        modir.login()
    except:
        print 'Login error'
        exit(1)
    return modir

def get_ntp_servers():
    '''
    Function that configures NTP servers
    '''
    ntp_servers = int(raw_input("How many NTP servers would you like to configure (between 1 and 5): "))
    ntp_list=[]
    if ntp_servers > 0 and ntp_servers <= 5:
        pass
    else:
        print 'Please enter  between 1 and 5:'
        exit()
    print 'NTP Server #1 will be configured as the preferred NTP Server'
    for x in range(ntp_servers):
        server_number = str(x+1)
        print "Enter the Hostname or IP address of NTP server #%s"% server_number
        ntp_list.append(raw_input())
    return ntp_list

def conf_NTP(modir , ntp_list):
    '''
    Function that iterates through ntp_list and creates JSON call to configure NTP providers.
    The first NTP server in ntp_list will be the prefered NTP provider.
    '''
    topDn = cobra.mit.naming.Dn.fromString('uni/fabric/time-Best_NTP_Policy')
    topParentDn = topDn.getParent()
    topMo = modir.lookupByDn(topParentDn)
    datetimePol = cobra.model.datetime.Pol(topMo, ownerKey=u'', name=u'Best_NTP_Policy', descr=u'Scripted NTP_Config', adminSt=u'enabled', ownerTag=u'')
    ntp_servers_dict={}
    ntp_prov_dict={}

    for x in range(len(ntp_list)):
        if x == 1:
            ntp_servers_dict['ntp_server_%02d' % x] = cobra.model.datetime.NtpProv(datetimePol, name=ntp_list[x], preferred=u'true')
            ntp_prov_dict['ntp_prov_%02d' % x] = cobra.model.datetime.RsNtpProvToEpg(ntp_servers_dict['ntp_server_%02d' % x], tDn=u'uni/tn-mgmt/mgmtp-default/oob-default')
        else:
            ntp_servers_dict['ntp_server_%02d' % x] = cobra.model.datetime.NtpProv(datetimePol, name=ntp_list[x])
            ntp_prov_dict['ntp_prov_%02d' % x] = cobra.model.datetime.RsNtpProvToEpg(ntp_servers_dict['ntp_server_%02d' % x], tDn=u'uni/tn-mgmt/mgmtp-default/oob-default')


    print toXMLStr(topMo)
    c = ConfigRequest()
    c.addMo(topMo)
    modir.commit(c)


def main():
    '''
    Main python program - execution starts from here.
    '''
    if len(sys.argv) != 4:
        print 'Usage: ntp.py <hostname> <username> <password> '
        sys.exit()
    else:
        hostname, username, password = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        ntp_list = get_ntp_servers()
        conf_NTP(modir, ntp_list)
        modir.logout()

if __name__ == '__main__':
    main()











