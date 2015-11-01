#!/usr/bin/env python

# Tool to Parse Ansible Facts Json output.
# 
# To Generate json
#
# # ansible -i inventory all -m setup --tree out/
#
# This will Generate files in out/hostname

import json
import sys

#Start Config
enable_cidr = 1
enable_debug = 0

# Allowed Ethernet Interface Names
allowed_ether = ["eth0","eth1","eth2","eth3","eth5","eth6","virbr0","docker0"]

#End Config


_header = ['name','FQDN']
_data = 0
f = open(sys.argv[1],"r")
z = json.loads(f.read())


print "\nServer Information"
print "------------------"
print "System Vendor: %s" % (z['ansible_facts']['ansible_system_vendor'])
print "\nHost Info"
print "  FQDN: %s" % (z['ansible_facts']['ansible_fqdn'])
print "\nOS: %s %s" % (z['ansible_facts']['ansible_system'],z['ansible_facts']['ansible_machine'])
print "  Distribution: %s" % (z['ansible_facts']['ansible_distribution'])
print "  Release: %s" % (z['ansible_facts']['ansible_distribution_major_version'])
print "  Version: %s" % (z['ansible_facts']['ansible_distribution_version'])
print "\nCPU Information"
print "  %s x %s (%s Cores)" % (z['ansible_facts']['ansible_processor_count'],z['ansible_facts']['ansible_processor'][1],z['ansible_facts']['ansible_processor_cores'])
print "\nMemory Information"
print '  %0.fMB (free %0.2fMB)' % ((z['ansible_facts']['ansible_memtotal_mb']),(z['ansible_facts']['ansible_memfree_mb']))
print "\nSystem Mounts"
for _disk in z['ansible_facts']['ansible_mounts']:
    print "uuid: %s" % (_disk['uuid'])
    if _disk['size_total'] >= 1073741824000:
        print "  size: %sTB" % (_disk['size_total']/1073741824000)
        print "  freespace: %sTB" % (_disk['size_available']/1073741824000)
    elif _disk['size_total'] >= 1048576000:
        print "  size: %sGB" % (_disk['size_total']/1048576000)
        print "  freespace: %sGB" % (_disk['size_available']/1048576000)
    else:
        print "  size: %sMB" % (_disk['size_total']/1048576)
        print "  freespace: %sMB" % (_disk['size_available']/1048576)
    print "  mountpoint: %s" % (_disk['mount'])
    print "  fstype: %s" % (_disk['fstype'])

print "\nSystem Drives"
for _device in z['ansible_facts']['ansible_devices']:
    print "device: %s" % (_device)
    print "  sectors: %s" % (z['ansible_facts']['ansible_devices'][_device]['sectors'])
    print "  size: %s" % (z['ansible_facts']['ansible_devices'][_device]['size'])

print "\nIPs"
for _ether in z['ansible_facts']['ansible_interfaces']:
    _interface = _ether.strip()
    _int = "ansible_%s" % (_interface)
    if enable_debug == 1:
        print z['ansible_facts']['ansible_interfaces']
        print _int
        print _ether
    if _interface in allowed_ether:
        if enable_cidr == 1:
            _cidr = sum([bin(int(x)).count('1') for x in z['ansible_facts'][_int]['ipv4']['netmask'].split('.')])
            print "  [%s] %s / %s" % (_ether,z['ansible_facts'][_int]['ipv4']['address'],_cidr)
        else: 
            print "  [%s] %s / %s" % (_ether,z['ansible_facts'][_int]['ipv4']['address'],z['ansible_facts'][_int]['ipv4']['netmask'])
    else:
        exit
print "------------------"
