#!/usr/bin/python3 
import socket
import signal
import sys
from colored import fg,bg,attr
import click
from threading import Thread


warning = fg('red')
command = fg('green')
command_bg = fg('green')
status  = fg('cyan')
message = fg('blue')
bold = attr("bold")

def receiver(sock,ps,*server_address):
    """Receives conections"""
    data = sock.recv(2048)
    while data:
        print("~> ",data,sep = '')
        print(str(ps).format(*server_address))
        data = sock.recv(2048)
    

def signal_handler(sig, frame):
    print(warning+"\n[Ctrl+C recieved]"+bold)
    print(status+"[Bye]"+bold)
    sys.exit(0)

@click.group()
def cli():
    """
    A netcat alternatives with tonnes of colors and good looking, works in listener mode and 
    connection mode
    """
    signal.signal(signal.SIGINT, signal_handler)
    pass


@cli.command()
@click.option("--lport",default=6969,help = "Set the port to listen on")
def listen(lport):
    "Listener mode: nyacat listen --lport=6969"

    if int(lport) > 65535 or int(lport) < 1 :
        print(warning+"Port invalid. Use a port between 0-65535, also on linux machines you need to be SU for using port < 1000"+bold)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #using 0.0.0.0 allows using ipaddress on lan to connect as well
    server_address = ('0.0.0.0',lport)
    print(command+"[Listener started on {} port {}]".format(*server_address))
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print(status+"[Waiting for connection] ...")
        connection,client_address = sock.accept()
        try:
            print(message+"[Connection received : ",client_address,"]")
            while True:
                data = connection.recv(2048)
                data = data.decode('utf-8')
                print("{!r}".format(data))
                if not data:
                    print(warning+'--> No data from client: ',client_address)
                    print(warning+"[Perhaps client has disconnected]"+bold)
                    break
        finally:
            connection.close()

@cli.command()
@click.option("--host",default="0.0.0.0",help="Remote/Local server address")
@click.option("--port",default=6969,help="Remote/Local port")
def client(host,port):

    "Connection mode: nyacat client --host=0.0.0.0 --port=6969"

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)
    print(command+"[Connecting to {} on port {}] ... ".format(*server_address))
    sock.connect(server_address)
    try:
        ps = command_bg+"[  {}"
        ps+=warning+"@"
        ps+=command_bg+"{} >>>] "
        message = input(str(ps).format(*server_address))
        bgthread = Thread(target=receiver,args=(sock,ps,*server_address,),daemon=True)
        bgthread.start()
        while True:
            sock.sendall(message.encode('utf-8'))
            message = input(str(ps).format(*server_address))



    finally:
        print(warning+"[Closing Socket]\n[Server dead]")
        sock.close()
        


if __name__ == "__main__":
    cli()
