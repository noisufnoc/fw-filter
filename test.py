__author__ = 'kbourne'
import re
import sys

url = "www.6pm.com"
url1 = "www.enzappos.com"
url2 = "www.tasty.com"
url3 = "www.zappos.com"
url4 = "www.ham.com"


def validate(url):
    controlled_strings = set(['zappos', '6pm', 'google'])

    p = re.compile('^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,4}$')
    d = p.match(url)
    #print d
    #print url.split('.')

    #could not find a good way to test for the prefixed www. so i test for length
    #and reject if it is not in the correct format so lazy am i
    print 'Begin domain tests'

    if len(url.rsplit('.')) >3:
        print "domain failed length check"

        sys.exit(1)
    #Making sure it is not one of the controlled domains.
    for dpart in url.rsplit('.'):
        #print dpart +"hello"
        if dpart in  controlled_strings:

            print  "domain is controlled and can not be blocked\n"
            return 1
    print "domain is valid\n"


print "Testing " + url
validate(url)

print "Testing " + url1
validate(url1)

print "Testing " + url2
validate(url2)

print "Testing " + url3
validate(url3)

print "Testing " + url4
validate(url4)

