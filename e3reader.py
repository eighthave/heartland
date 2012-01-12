#!/usr/bin/python
# -*- coding: utf-8 -*-


class E3Reader():
    '''class for handling the Heartland E3 credit card reader'''

    @staticmethod
    def parsename(card):
        '''given a complete string from a Heartland E3 reader, return the firstname and lastname'''
        if card[0] != '<' or card[-1] != '>':
            print 'Not valid card data: ' + card
            return
        name = card.split('|')[0].split('^')[1].lower()
        names = name.split('/')
        if len(names) == 2:
            lastname = names[0].lstrip().rstrip().capitalize()
            firstname = names[1].lstrip().rstrip().capitalize()
        elif len(names) == 1:
            firstname = ''
            lastname = name.lstrip().rstrip().capitalize()
        else:
            firstname = ''
            lastname = ''
        return firstname, lastname


if __name__ == '__main__':

    # data I faked so it has full names
    fakedata = '''<E1050811%B4888900000008888^STEINER/HANS-CHRISTO^131100000000000000000?|qwt0+QpJUgQvcVlI9MimCLW0KUcBV7ccf/qTg8/qh3NY4D1sx53if4AASd/r|+++++++EeBFsgfSl|11;4888900000008888=131100000000000?|6rc8dpYmsFHtpIgTyLLpmbWxF2M|+++++++EeBFosfSl|00|||/wECAQECAoFGsgEH3AELTDT6jRZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0u5elwS+b/8HwW7RluF6gIRs447/4SXo0sSw27V1SFOC90dVWpOuB7CgsQ4ERzyhvCA8+/IUmvqsaJK2E+qSHOSGk4XFnysGeiZlSo2jCuc0gvamjjMXrvtlPByXonqwpjJVtFQTOFIxGXpSxOoqr/Sq/gJbb5jCanA4ZiDYVXjgAjhg0+iAJRwUOzCgT+Urq+PMKoYMK5BTyCh0e/jb6oboOJnOq|>'''
    morefakedata = '''<E1052411%B4588240000002202^STEINER/CHRIS ^1211000000000000000000000000000?|vIKypvzcmTtYme8w6bCg12BxsjuzYO5zs56r+tWy7maokt6j5gnzI/XtTv8Fdf4ViE6E|+++++++7SspSskLx|11;4588240000002202=121100000000000?|AY+qjai0Wv6Dm4NwFmwanUmm7Wu|+++++++7SspSjkLx|00|||/wECAQECAoFGAgEH3AELTsT6jRZwb3NAc2VjdXJlZXhjaGFuZ2UubmV0u5elwS+b/8HwW7RluF6gIRs447/4SXo0fSw27V1SFOC90dVWpOuB7CgcQ4ERzyhvCA8+/IUmvqsaJK2E+qSHOSGk4XFnysGeiZlSo2jCuc0gvamjjMXrvtlPByXonqspjJVtFQTOFIxGXpSxOoqr/Sq/gJbb5jCanA4ZiDYVXjgAjhg0+iAJRwUOzCgT+Urq+PMKoYMK5BTyCh0e/jb6oboOJnOq|>'''

    cards = []
    cards.append(fakedata)
    cards.append(morefakedata)

    f = open('testdata.txt', 'r')
    lines = f.readlines()
    for line in lines:
        cards.append(line.rstrip('\n'))

    for card in cards:
        firstname, lastname = E3Reader.parsename(card)
        print '"first: "' + firstname + '" last: "' + lastname + '"'
