# iptables-to-firewalld

This Python script converts an iptables table file to firewalld-cmd command lines which you can run on your Linux operating system.
It's pretty basic: it only converts -A INPUT lines from the iptables table file.

Example iptables file:

    -A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
    -A INPUT -p tcp -m multiport --dports 1556  -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT
    -A INPUT -m state --state NEW -m udp -p udp --dport 10080 -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 2050 -j ACCEPT
    -A INPUT -p tcp -m state --state NEW -s 1.2.3.4/32 -m tcp --dport 9100 -j ACCEPT

The iptab_conv.py script output using the example iptables file:

    /usr/bin/firewall-cmd --add-port=22/tcp --permanent
    /usr/bin/firewall-cmd --add-port=1556/tcp --permanent
    /usr/bin/firewall-cmd --add-port=21/tcp --permanent
    /usr/bin/firewall-cmd --add-port=10080/udp --permanent
    /usr/bin/firewall-cmd --add-port=2050/tcp --permanent
    /usr/bin/firewall-cmd --new-zone=zone_9100 --permanent
    /usr/bin/firewall-cmd --zone=zone_9100 --add-port=9100/tcp --permanent
    /usr/bin/firewall-cmd --zone=zone_9100 --add-source=1.2.3.4/32 --permanent

**USAGE:**
python iptab_conv.py iptables_file

The iptables_file is usually found as /etc/sysconfig/iptables.

A note of warning:
This is for educational usage only. 
No rights can be derived from this script. If you f# things up, it's your problem.

