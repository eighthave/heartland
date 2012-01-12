#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO make sure the HTTPS certificate is verified

import suds

class PosGateway():
    '''a class to talk SOAP to the HPS Exchange POS Gateway'''

    url = 'https://posgateway.cert.secureexchange.net/Hps.Exchange.PosGateway.UAT/PosGatewayService.asmx?wsdl'

    def __init__(self, licenseid=None, siteid=None, deviceid=None,
                 username=None, password=None, tokenvalue=None,
                 sitetrace=None, developerid=None, versionnbr=None,
                 clerkid=None):
        self.client = suds.client.Client(PosGateway.url)
        self.soapheaders = dict()
        if licenseid:
            self.soapheaders['LicenseId'] = licenseid
        if siteid:
            self.soapheaders['SideId'] = siteid
        if deviceid:
            self.soapheaders['DeviceId'] = deviceid
        if username:
            self.soapheaders['UserName'] = username
        if password:
            self.soapheaders['Password'] = password
        if tokenvalue:
            self.soapheaders['TokenValue'] = tokenvalue
        if sitetrace:
            self.soapheaders['SiteTrace'] = sitetrace
        if developerid:
            self.soapheaders['DeveloperID'] = developerid
        if versionnbr:
            self.soapheaders['VersionNbr'] = versionnbr
        if clerkid:
            self.soapheaders['ClerkID'] = clerkid
        self.client.set_options(soapheaders=self.soapheaders)
        print self.client

    def dotransaction(self, carddata, amount, allowdup='N'):
        '''run a credit card transaction'''
        self.client.service.DoTransaction



if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)

    client = PosGateway()
