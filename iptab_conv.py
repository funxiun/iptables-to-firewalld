#!/usr/bin/python3

import os
import re
import socket
import argparse

firewalld_bin = "/usr/bin/firewall-cmd"
firewalld_lines = []
zone_list = []


def get_host_ip (fqdn):
    return socket.gethostbyname(fqdn)

def conv_input (line):

    k = []
    ports = ""
    nic = ""
    nic_param = ""
    port_list = []
    source_list = []

    fwd_list = re.split('-', line.strip())

    # Delete empty list items
    while("" in fwd_list) :
            fwd_list.remove("")

    # Trim list item
    for i in fwd_list:
        j = i.strip()
        k.append(j)
    fwd_list = k

    for i in fwd_list:

        fw_line = re.split(' ',i)

        if 'i' in fw_line:                     # Get network interface
            idx = fw_line.index('i')
            nic = fw_line[idx+1]

        if 'p' in fw_line:                     # Get protocol
           idx = fw_line.index('p')
           port_type = fw_line[idx+1]

        if 's' in fw_line:                     # Get source address
            idx = fw_line.index('s')
            source = fw_line[idx+1]
            source_list = re.split(',', source)
            idx=0
            for s in source_list:             # If source address contains letters, it isn't an IP address
                if s.isalnum():
                    ip=get_host_ip(s)         # Convert FQDN to IP
                    source_list[idx]=ip
                idx=idx+1

        if 'dport' in fw_line:               # Get destination port
            idx = fw_line.index('dport')
            ports = fw_line[idx+1]
            port_list = re.split(',', ports)

        if 'dports' in fw_line:               # Get destination ports
            idx = fw_line.index('dports')
            ports = fw_line[idx+1]
            port_list = re.split(',', ports)

#    if nic:
#        nic_param = " --add-interface="+nic

    if port_list:
        for p in port_list:
            if source_list:  # If there's a source IP we should create a zone
                zone_name='zone_'+p
                if zone_name not in zone_list:
                    zone_list.append(zone_name)
                    firewalld_lines.append ( firewalld_bin+nic_param+' --new-zone='+zone_name+' --permanent')
                    firewalld_lines.append ( firewalld_bin+nic_param+' --zone='+zone_name+' --add-port='+p.replace(":","-")+'/'+port_type+' --permanent')
                for s in source_list:
                  firewalld_lines.append( firewalld_bin+nic_param+' --zone='+zone_name+' --add-source='+s+' --permanent')
            else:
                firewalld_lines.append( firewalld_bin+nic_param+' --add-port='+p.replace(":","-")+'/'+port_type+' --permanent')
    return

def generate_commandline (lines):

    for i in lines:
        print (i)        # Print the firewalld command lines.
#        os.system (i)   # Unremark this to execute the firewalld command line in the OS. !!WARNING!!
    return



parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', type=str,help='filename')
args = parser.parse_args()


with open(args.filename) as f:
    for line in f:
        uline=line.upper()      # Convert line to uppercase to prevent weird camelcase lines.
        if uline.startswith('-A INPUT'):
            conv_input (line)

generate_commandline (firewalld_lines)
