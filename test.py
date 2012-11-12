__author__ = 'kbourne'
import re
import sys

url = "3.www.6pm.com"
url1 = "www.enzappos.com"
url2 = "www.tasty.com"
url3 = "www.zappos.com"
url4 = "www.ham.com"


def validate(url):
    #Housekeeping

    controlled_strings = set(['zappos', '6pm', 'google'])
    splitdomain =  url.split('.')

    p = re.compile('^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,4}$')
    d = p.match(url)

    if d:
        print 'Match found: ', d.group()
    else:
        print "input fail\n"
        return 1


    print 'Begin domain tests'


    #Making sure it is not one of the controlled domains.

    for dpart in splitdomain:

        if dpart in  controlled_strings:

            print  "domain is controlled and can not be blocked\n"
            return 1
    print "domain is valid\n"

    #Passed sanitization and controlled domain test. Split the domain and make sure there are less then 3 options.

    if len(splitdomain) >= 3:
        #print "domain failed length check\n"
        del splitdomain[0]
        x  ='.'.join(splitdomain)
        return x
    return url


print "Testing " + url
x = validate(url)

print "Testing " + url1
x1 = validate(url1)

print "Testing " + url2
x3 = validate(url2)

print "Testing " + url3
x4 = validate(url3)

print "Testing " + url4
x5 = validate(url4)

print x,x1,x3,x4,x5