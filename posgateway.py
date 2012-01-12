#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO make sure the HTTPS certificate is verified

import suds

class PosGateway():
    '''a class to talk SOAP to the HPS Exchange POS Gateway'''

    url = 'https://posgateway.cert.secureexchange.net/Hps.Exchange.PosGateway.UAT/PosGatewayService.asmx?wsdl'

    def __init__(self, licenseid, siteid, deviceid,
                 username, password, tokenvalue=None,
                 sitetrace=None, developerid=None, versionnbr=None,
                 clerkid=None):
        if len(username) > 20:
            raise Exception('UserName must be no longer than 20 characters')
        self.client = suds.client.Client(PosGateway.url)
        # required
        self.licenseid = licenseid
        self.siteid = siteid
        self.deviceid = deviceid
        self.username = username
        self.password = password
        # optional
        self.tokenvalue = tokenvalue
        self.sitetrace = sitetrace
        self.developerid = developerid
        self.versionnbr = versionnbr
        self.clerkid = clerkid


    def _newrequest(self):
        '''create a new PosRequest and populate the headers'''
        request = pos.client.factory.create('ns0:PosRequest')
        # required
        request['Ver1.0']['Header']['LicenseId'] = self.licenseid
        request['Ver1.0']['Header']['SiteId'] = self.siteid
        request['Ver1.0']['Header']['DeviceId'] = self.deviceid
        request['Ver1.0']['Header']['UserName'] = self.username
        request['Ver1.0']['Header']['Password'] = self.password
        # optional
        if self.tokenvalue:
            request['Ver1.0']['Header']['TokenValue'] = self.tokenvalue
        if self.sitetrace:
            request['Ver1.0']['Header']['SiteTrace'] = self.sitetrace
        if self.developerid:
            request['Ver1.0']['Header']['DeveloperID'] = self.developerid
        if self.versionnbr:
            request['Ver1.0']['Header']['VersionNbr'] = self.versionnbr
        if self.clerkid:
            request['Ver1.0']['Header']['ClerkID'] = self.clerkid
        return request


    def _dotransaction(self, transaction, value='random garbage'):
        '''run a transaction, some don't have a value but suds needs
        something there to generate the XML properly'''
        request = self._newrequest()
        request['Ver1.0']['Transaction'][transaction] = value
        #print request
        self.client.service.DoTransaction(request['Ver1.0'])


    def testcredentials(self):
        '''test the credentials setup in the object'''
        self._dotransaction('TestCredentials')


    def creditsale(self, carddata, amount, allowdup='N'):
        pass


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)
    #logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
    #logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

    pos = PosGateway('12345', '12345', '12345678', '12345678A', '$password',
                        developerid='012345', versionnbr='1234')
    pos.testcredentials()
    
