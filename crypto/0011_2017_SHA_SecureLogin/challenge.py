import SocketServer,threading
import os

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return x

p = 122393459642722715193508803338542206847651199104157034101901924367393290934998109518127197921357057965651363461495646489924392985126604671445241184587580086506941330238866801122301302482735364698974701123276213503102347555197266179750135524475763752922326614949176378421073363097486484940695242289746980388463
q = 133300336978107715331632886132210333124971739104027612877718732100345095048024966592792491983973801217967424585553062016226983458965633742347459768034630253066926503982017000225921857150785008634550090092282020402493896538543688354044017384128130488713660821776540113235126497327793261484261440017516736459081
n = 16315089414291365072804956105526619397880822648675320383852140885712340615983082870173758725944399423152738344037428151973965538500069936447639534890845531199613678184294237628125057316342510982776407156694815184917000970306121657284237906532814224632215370256293838582309545956565555297923401741307034617986383052120572516847847033937942436031190316937147957112647856482484333571961544221830208413154823809272644578945534650200125045586420565951106372262848424400490694183992092842805959840817463523575339840959190636863559402670693269438649657323364034745897181633739006582260227361430715116697654601217320483982503
e = 65537

d = egcd(e, (p-1)*(q-1))
if d < 0:
	d = d % ((p-1)*(q-1))

f = open("hackability.flag")
flag = f.readline().strip()

# Translate a number to a string (byte array), for example 5678 = 0x162e = \x16\x2e
def num2str(num):
    t = ('%x' % num)
    if len(t) % 2 == 1:
        t = '0' + t
    return t.decode('hex')

# Translate byte array back to number \x16\x2e = 0x162e = 5678
def str2num(s):
    return int(s.encode('hex'),16)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            self.request.sendall("\nWelcome to the secure login server, make your choice from the following options:\n1. Register yourself as a user.\n2. Collect flag\n3. Sign a message\n4. Exit\nChoice: ")
            inp = self.request.recv(1024).strip()
            if inp == '1':
                self.request.sendall("Pick a username: ")
                uname = self.request.recv(1024).strip()
                self.request.sendall("Enter your full name: ")
                full = self.request.recv(1024).strip()
                ticket = 'ticket:user|%s|%s' % (uname,full)
                ticket = pow(str2num(ticket),d,n)
                ticket = num2str(ticket)
                self.request.sendall("Your ticket:\n")
                self.request.sendall(ticket.encode('hex') + "\n")
            elif inp == '2':
                self.request.sendall("Enter your ticket: ")
                ticket = self.request.recv(1024).strip()
                try:
                    ticket = int(ticket,16)
                except:
                    ticket = 0
                ticket = pow(ticket,e,n)
                ticket = num2str(ticket)
                if ticket.startswith('ticket:'):
                    if ticket.startswith('ticket:admin|root|'):
                        self.request.sendall("Here you go!\n")
                        self.request.sendall(flag + "\n")
                        break
                    else:
                        self.request.sendall("Sorry that function is only available to admin user root\n")
                else:
                    self.request.sendall("That doesn't seem to be a valid ticket\n")
            elif inp == '3':
                self.request.sendall("Enter your message, hex encoded (i.e. 4142 for AB): ")
                msg = self.request.recv(1024).strip()
                try:
                    msg = msg.decode('hex')
                except:
                    self.request.sendall("That's not a valid message\n!")
                    continue
                msg = '\xff' + msg # Add some padding at the start so users can't use this to sign a ticket
                if str2num(msg) >= n:
                    self.request.sendall("That's not a valid message\n!")
                    continue
                signed = pow(str2num(msg),d,n)
                signed = num2str(signed)
                self.request.sendall("Your signature:\n")
                self.request.sendall(signed.encode('hex') + "\n")
            elif inp == '4':
                self.request.sendall("Bye!\n")
                break
            else:
                self.request.sendall("Invalid choice!\n")

SocketServer.TCPServer.allow_reuse_address = True
server = ThreadedTCPServer(("0.0.0.0", 12345), MyTCPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
server.serve_forever()
