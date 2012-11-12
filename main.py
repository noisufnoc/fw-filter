__author__ = 'eknegg'

#import clint
import pexpect
import sys
from getpass import getpass
import re


USAGE = '''fw-url_filter user url'''
COMMAND_PROMPT = '[$#] '
TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'
SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'


#settings are stored i lists  name,ip,prompt,webfilter,vdom_state,enabled
#0name is Fw-working name
#1 ip
#2Device base prompt
#3webfilter in fortinet are broken into id's
#4vdom state = 1 for vdoms enbled , 0 for non vdom
#5device enabled status
firewall =[["core1","192.168.1.1","core-1",1,"0",1],
          ["core2","192.168.1.1","core-1",3,"0",1],
          ["core1","192.168.1.1","core-8",4,"0",0]]



def Login(host,user,password):
    child = pexpect.spawn('ssh -l %s %s '%(user, host))
    child.logfile = sys.stdout

    i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, '[Pp]assword:'])
    if i == 0: #zomg timeout
        print 'Error!'
        print child.before, child.after
        sys.exit (1)

    if i == 1: #Why hello. This seems to be our first meetings(accept)
        child.sendline ('yes')
        child.expect ('[Pp]assword: ')
    child.sendline(password)
    print "pass sent"
    # Now we are either at the command prompt or
    # the login process is asking for our terminal type.
    i = child.expect (['Permission denied', TERMINAL_PROMPT, COMMAND_PROMPT])
    if i == 0:
        print 'Permission denied on host:', host
        sys.exit (1)
    if i == 1:
        child.sendline (TERMINAL_TYPE)
        child.expect (COMMAND_PROMPT)
    return child

def UrlUpdate(url,settings):
    if url == 1:
        Do


    #are we working with a vdom enabled firewall?
    if settings[4] == 1:
        child.sendline('config vdom')
        child.sendline('edit root')
        i = child.expect('something')
        if 0 != i:
            print "This is the place where we bail out if things are not going well"
            return child.after

    #i = child.expect(['command parse error',COMMAND_PROMPT] )
    child.sendline('config webfilter urlfilter')
    i = child.expect('urlfilter')
    if 0 != i:
        print "config webfilter urlfilter failed"
        return child.after

    child.sendline('edit'+settings[3])
    i = child.expect(settings[3])
    if  0 != i:
        print "url filter edit failed"
        return child.after

    child.sendline('config entries')
    i = child.expect('entries')
    if 0 != i:
        print "config entries  failed"
        return child.after

    child.sendline('edit .*'+ url +'.*')
    i = child.expect(url)
    if 0 != 1:
        print "url filter edit failed"
        return child.after

    child.sendline('set thing')
    child.sendline('set otherthing')


def UrlFix(url):
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


#check the url, destry or validate

safeurl = UrlFix(sys.argv[2])

if safeurl == 1:
     print "Url is fail."
     sys.exit(1)
else:


#get pass is in the loop host for loop due to rsa /differeing credentials per host.

    for host in firewall[0:]:
        if host[5] == 0:
            print host[0] + "is disabled."
            continue
        print "Logging into  "+ host[0]
        password = getpass(prompt="Password please")
        child = Login(host[1],sys.argv[1],password)
        if child == None:
            print 'Could not login to host:', sys.argv[1]
            sys.exit(1)


    print 'updating url'
    p = UrlUpdate (safeurl,host)

print "done"
