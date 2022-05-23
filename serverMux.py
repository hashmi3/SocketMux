#!/usr/bin/env python3
import socket

##################################
#
# I have used the idea of time multiplexing for sending
# and receiving int values between different machines.
#
# Muhammad Hashmi
##################################

PORT = 5657
TIMEOUT = 1.0     #timeout value in seconds

def clientcom(c1_ip):
    global PORT, TIMEOUT
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.settimeout(TIMEOUT)
    c2.connect((c1_ip, PORT))                   #CONNECT

    valRecv = c2.recv(1024)                         #receive num
    print("Val received: ",valRecv.decode("utf-8"))
    c2.close()
    return valRecv.decode('utf-8')


if __name__ == "__main__":


    currVal = int(input("Enter an integer for this machine: "))
    print("\nIP of THIS MACHINE ALREADY ACQUIRED !!!! \n\n")
    c1_ip = input('Enter IP address of machine 1: ')
    #c1_ip = 'x12.indstate.edu'
    #c1_port = int(input('Enter port number of machine 1: () '))

    c2_ip = input('Enter IP address of machine 2: ')
    #c2_ip = 'x11.indstate.edu'
    tally = []
    numbertable = {}
    incount = 0
    sent = 0

    #server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), PORT))
    s.listen(5)                             #queue of 5 miscomm
    s.settimeout(TIMEOUT)

    while True:
        try:
            print("Waiting for other Machines ! Press Ctrl+c  to Terminate")
            clientsocket, address = s.accept()        #sockt obj and address
            print(f"Connection from {address}  estblished !")
            clientsocket.send(bytes(str(currVal), 'utf-8'))   #send server number
            clientsocket.close()
            sent += 1
        except KeyboardInterrupt:               # Terminate condition handling
            print("SERVER SHUTTING DOWN ! END")
            break
        except:
            print(f"\nTime out occured, incount:{incount}, sent{sent} \n\n")

            if incount == 2 and sent == 2:
                break

            if c1_ip not in tally:
                tally.append(c1_ip)
                incount += 1
                # get value from Machine 1
                try:
                    print("connecting server at: ", c1_ip)
                    numbertable[c1_ip] = clientcom(c1_ip)
                except:
                    incount -= 1
                    tally.pop()
                    pass

            if c2_ip not in tally:
                tally.append(c2_ip)
                incount += 1
                #get vaue from Machine 2
                try:
                    print("connecting server at: ", c2_ip)
                    numbertable[c2_ip] = clientcom(c2_ip)
                except:
                    incount -= 1
                    tally.pop()
                    pass

    print("Int value of current machine", currVal)
    for i,j in numbertable.items():
        print(f"Int value from {i}: {j} ")
    s.close()
