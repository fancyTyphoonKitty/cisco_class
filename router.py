def getRouter(rtr):
    router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
    router2 = {'os_version':'3.2.1', 'hostname':'rtp_router2', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.12'}
    router3 = {'os_version':'3.1.1', 'hostname':'Router3', 'model':'nexus 9504', 'domain':'lab.cisco.com', 'mgmt_ip':'10.1.50.13'}
 
    if rtr == 'router1': 
        return router1
    elif rtr == 'router2':
        return router2
    elif rtr == 'router3':
        return router3 
 
    return 'no router found.'