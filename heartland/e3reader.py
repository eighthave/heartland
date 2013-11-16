#!/usr/bin/python
# -*- coding: utf-8 -*-

# this is based on the document "E3 Wedge Reader Programmer's Manual Rev A.7.pdf"
import re

class E3Reader():
    '''class for handling the Heartland E3 credit card reader'''

    FIELD_DELIMITER = chr(0x7C)

    def __init__(self, data):
        '''initialize an instance with a full swipe'''
        if not E3Reader.isvalid(card):
            raise Exception('Not valid card data: ' + card)
        self.data = data
        self._parse()

    @staticmethod
    def isvalid(card):
        '''validate that we got a complete packet'''
        if re.match("^<X1.*\|>$", card):
            # "X1 = Error condition exist"
            return False
        if re.match("^<E1.+\|>$", card):
            # E1 = Regular data output
            if len(card.split('|')) != 11:
                return False
            return True
        return False

    def _parse(self):
        '''given a complete string from a Heartland E3 reader, parse data into a dict'''
        self.fields = card.split('|')
        self.track1 = None
        self.track2 = None
        self.number = None
        self.expirationdate = None
        if len(self.fields[0]) > 9 and self.fields[0][9] == '%':
            self.track1 = '%' + self.fields[0].split('%')[1].split('?')[0] + '?'
            self.track1formatcode = self.track1[1]
            track1data = self.track1.split('^')
            self.number = re.sub('[^0-9]', '', track1data[0][2:])
            self.name = track1data[1]
            self.expirationdate = track1data[2][0:4]
            names = self.name.split('/')
            if len(names) == 2:
                self.lastname = names[0].lstrip().rstrip().capitalize()
                self.firstname = names[1].lstrip().rstrip().capitalize()
            elif len(names) == 1:
                self.firstname = ''
                self.lastname = self.name.lstrip().rstrip().capitalize()
            else:
                self.firstname = ''
                self.lastname = ''
        if len(self.fields[3]) > 2 and self.fields[3][2] == ';':
            self.track2 = ';' + self.fields[3].split(';')[1].split('?')[0] + '?'
            track2data = self.track2.split('=')
            if self.number == None:
                self.number = track2data[0].split(';')[1]
            if self.expirationdate == None:
                self.expirationdate = track2data[1][0:4]
        if re.match('3[08]', self.number[0:2]):
            self.type = 'dinersclub'
        elif self.number[0:2] == '35':
            self.type = 'jcb'
        elif self.number[0:2] == '37':
            self.type = 'americanexpress'
        elif self.number[0] == '4':
            self.type = 'visa'
        elif self.number[0:2] == '50':
            self.type = 'dankort'
        elif re.match('5[1-5]', self.number[0:2]):
            self.type = 'mastercard'
        elif self.number[0:2] == '56':
            self.type = 'australianbankcard'
        elif self.number[0:2] == '60':
            self.type = 'discover'
        elif self.number[0:2] == '63':
            self.type = 'switchsolo'
        elif self.number[0] == '7':
            self.type = 'dankort'
        else:
            self.type = 'UNKNOWN'


if __name__ == '__main__':

    # data I faked so it has full names
    fakedata = '''<E1050811%B4888900000008888^STEINER/HANS-CHRISTO^131100000000000000000?|qwt0+QpJUgQvcVlI9MimCLW0KUcBV7ccf/qTg8/qh3NY4D1sx53if4AASd/r|+++++++EeBFsgfSl|11;4888900000008888=131100000000000?|6rc8dpYmsFHtpIgTyLLpmbWxF2M|+++++++EeBFosfSl|00|||/wECAQECAoFGsgEH3AELTDT6jRZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0u5elwS+b/8HwW7RluF6gIRs447/4SXo0sSw27V1SFOC90dVWpOuB7CgsQ4ERzyhvCA8+/IUmvqsaJK2E+qSHOSGk4XFnysGeiZlSo2jCuc0gvamjjMXrvtlPByXonqwpjJVtFQTOFIxGXpSxOoqr/Sq/gJbb5jCanA4ZiDYVXjgAjhg0+iAJRwUOzCgT+Urq+PMKoYMK5BTyCh0e/jb6oboOJnOq|>'''
    morefakedata = '''<E1052411%B4588240000002202^STEINER/CHRIS ^1211000000000000000000000000000?|vIKypvzcmTtYme8w6bCg12BxsjuzYO5zs56r+tWy7maokt6j5gnzI/XtTv8Fdf4ViE6E|+++++++7SspSskLx|11;4588240000002202=121100000000000?|AY+qjai0Wv6Dm4NwFmwanUmm7Wu|+++++++7SspSjkLx|00|||/wECAQECAoFGAgEH3AELTsT6jRZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0u5elwS+b/8HwW7RluF6gIRs447/4SXo0fSw27V1SFOC90dVWpOuB7CgcQ4ERzyhvCA8+/IUmvqsaJK2E+qSHOSGk4XFnysGeiZlSo2jCuc0gvamjjMXrvtlPByXonqspjJVtFQTOFIxGXpSxOoqr/Sq/gJbb5jCanA4ZiDYVXjgAjhg0+iAJRwUOzCgT+Urq+PMKoYMK5BTyCh0e/jb6oboOJnOq|>'''
    notevenacreditcard = '''<E1033600|||20;813631526=3227?|7ehyjRUBc6p2Ckr3l44OUqhjkCx||00|||/wECAQECAoFGAgEH3QsPTDT6jRZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0lAym4RaaasMpmwHUjeEhbcq+EIMVG8+xo+/YVzU2h3CF25CF7+L/DqELzZYl9m9Y4JJtZ2vsMeRkdk6u6W4t3AG1HHS2fU08eMQeaUv77+t0aT1zDaQAaGfIodBDOpDXksU0EP3an5H59Uikg/T8dzbOm/I+bRbYcalObc3g7I8AGoYvWFvAYtNfzPYcXbu5V+BDqoXUnfPl3Z/wX7yj53t8lAd1|>'''
    frommanualpdf = '''<E1051910%B1234120000001234^CARDUSER/JOHN^030500000000000000000000000000000?|9SzzRL+ST/5gZ/u7nijpodPzZLs3BA6Hkauy1Mjpenl97Q8heL/ZQvwDPveolHY3i|+++++++3HlMzHk5a|10;1234120000001234=0305000000000000?|9eryKeDXdk/cnN8HMxC0HPpB7+q|+++++++3HlMzHk5a|00|||/wECAQECAoFGAgEH1AIBSkFvYxZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0iIXVzitSbjk2AARLlFE7CvsTb/ZgpUPTjtuAG6OWzlBbsAZCbe7SHIU06j+baz4UrkF2JE2U0O0wwiZuN9eOMl5AWFvnLp9aNNRORots7jrjjxT8owbXjZdp3BXSjnnXdgaVEzKC6uU16wDAFmV6GzrkOMUNpYKcpaEPv2Ekt1cA/sO9AyVfLV5e9VfQ6R/zIhMLTkYEh0xWSk8q1oZtCE9yEG7/|>'''

    cards = []
    cards.append(fakedata)
    cards.append(morefakedata)
    cards.append(notevenacreditcard)
    cards.append(frommanualpdf)

    f = open('../testdata.txt', 'r')
    lines = f.readlines()
    for line in lines:
        cards.append(line.rstrip('\n'))

    for card in cards:
        if E3Reader.isvalid(card):
            print('-----------------------------------')
            e = E3Reader(card)
            print(e.number)
            if e.track1 != None:
                print('track1'),
                print(e.firstname + " " + e.lastname + ": " + '(' + e.type + ') '),
                print(' exp: ' + e.expirationdate)
            if e.track2 != None:
                print('track2'),
                print(e.track2)
