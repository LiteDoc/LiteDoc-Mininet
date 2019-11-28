#!/usr/bin/python

from functools import partial
from os import system
from sys import argv
from time import sleep
import atexit
from threading import Thread

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

short_sleep = 3
long_sleep = 5
num_of_cass = 3
num_of_client = 3


class CassTopo(Topo):
    """
        build a network with a single switch,
        and each host is connected to the switch.
        h1 - h{num_of_cass}: Cassandra servers
        h{num_of_cass+1} - h{num_of_cass+num_of_client}: simulated clients
    """

    def build(self):
        switch = self.addSwitch('s1')
        for i in range(num_of_cass):
            host = self.addHost('h{0}'.format(i + 1))
            self.addLink(host, switch)
        for i in range(num_of_cass, num_of_cass + num_of_client):
            host = self.addHost('h{0}'.format(i + 1))
            self.addLink(host, switch, delay='0ms')


def startMini():
    """
    Start Mininet with mounted directories
    :return:
    """
    setLogLevel('info')
    topo = CassTopo()
    privateDirs = [('~/raft/data', '~/raft/data/%(name)s')]
    host = partial(Host, privateDirs=privateDirs)
    # net = Mininet(topo=topo, host=host)
    net = Mininet(topo=topo, host=host, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()

    hs = [net.get('h{0}'.format(i + 1)) for i in range(num_of_cass + num_of_client)]

    # change network interface cards' names to suit cassandra.yaml
    for i in range(num_of_cass):
        hs[i].intf('h{0}-eth0'.format(i + 1)).rename('eth0')

    dumpNodeConnections(net.hosts)
    # net.stop()
    return net, hs


def startEtcd(hs):
    print "starting instances, may take a while..."
    for i in range(num_of_cass):
        # if not redirect output, cass may stuck at bootstrap
        hs[i].cmd(". ~/etcd/etcdConfig.sh")
        # hs[i].cmdPrint("echo ~/raft/etcdServer{0}.sh".format(i + 1))
        hs[i].cmd(". ~/etcd/etcdServer{0}.sh &".format(i + 1))
        sleep(short_sleep)
        print "cass node h{0} is alive".format(i + 1)
    for i in range(num_of_cass, num_of_cass + num_of_client):
        hs[i].cmd(". ~/etcd/etcdctl.sh")

    print "wait the system to stabilize..."
    sleep(long_sleep)
    o1 = hs[3].cmdPrint("ETCDCTL_API=3 etcdctl -w table --endpoints=$ENDPOINTS endpoint status")
    o1 = hs[3].cmdPrint("cd ~/GoBenchmark && ls")
    o1 = hs[3].cmdPrint("go run *.go")

def clean():
    system("mn --clean")  # perform Mininet clean
    system("rm *.etcd -rf")


def main():
    clean()
    if '-t' in argv or '--topo' in argv:
        net, hs = startMini()
        atexit.register(clean)
        if '-s' in argv or '--start' in argv:
            startEtcd(hs)
        CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
                -s
                -c -s -t
              """
    else:
        system("clear")
        print "switches are: ", argv[1:]
        main()

# ~/cassandra/bin/nodetool --host 10.0.0.1ms
# ~/cassandra/bin/cqlsh 10.0.0.1ms
# ssh -i ~/mgmt/init/id simulator-2 ~/mininet/mininet/util/m h3 ifconfig

# h4 ETCDCTL_API=3 etcdctl -w table --endpoints=$ENDPOINTS endpoint status
# h4 etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
# h4 etcdctl --endpoints=$ENDPOINTS get foo
# h4 etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
