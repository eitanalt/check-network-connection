import socket, pyping, sys, os, netifaces

def chip():
    ip = s.getsockname()[0]
    if ip == "":
        return 2    # device has no IP
    elif "169.254" in ip:
        return 1    # device gets APIPA
    else:
        return 0    # Device has legal ip address

def ping(host):
    print "Sending ping"

    response = pyping.ping(host)
    print "\n---------------------------------"
    
    if response.ret_code == 0:
        print "ping       -> OK"
        return True
    else:
        print "ping       -> ERROR"
        return False

def checkGW():
    # checks the computer's default gateway and check connection

    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    response = pyping.ping(default_gateway)
    if response.ret_code == 0:
        print "Default GW ->", default_gateway
        print "Ping to GW -> OK"
    else:
        print "Ping to GW -> ERROR"
    
if len(sys.argv) > 1:    # user wants to check a connection to another device
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostname = sys.argv[1]    
    print "********************************************"
    print "[*] Checking connectivity for ",hostname
    print "********************************************"
    try:
        ping(hostname)
    except:
        print "[*] Wrong IP address"
    s.close()
    
else:               # user wants to check the connection for his device
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostname = socket.gethostname()
    print "********************************************"
    print "[*] Checking connectivity for ",hostname
    print "********************************************"
    if ping("8.8.8.8"):
        if chip() == 0:
            print "IP         -> OK:",s.getsockname()[0]
            checkGW()                     #sends ping to Default GateWay
        elif chip() == 1:
            print "IP         -> APIPA"
        elif chip() == 2:
            print "IP         -> NONE"
    
print "---------------------------------"
s.close()
