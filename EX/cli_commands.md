# Packmaster CLI Rules syntax examples

## Show Rules:

```
cc dump-flows br0
```

## Show Ports:

```
cc dump-ports br0 (Shows port stats as well)
```

```
ovs-vsctl show
```

```
ovs-ofctl show br0 (Useful for also getting MAC addresses)
```

## Delete Ports:

```
cv delete-port br0 <port-name>
```

## Rule Output actions

### Example command:

```
cc add-flow br0 in_port=1,priority=32768,actions=output:2
```

### Output to multiple ports

```
actions=output:2,3,4
```

can also be abbreviated as ***actions="2,3,4"***

### Drop all traffic

```
actions=drop
```

### Output to group 100

```
actions=group:100
```

### Modify VLAN ID \

The CLI command requires an offset of 4096 for the VLAN ID; i.e. ***set_field:4196*** is equivalent to setting a VLAN ID of 100

```
actions="set_field:4196->vlan_vid,output:2"
```

### Push VLAN

```
actions="push_vlan:0x8100,set_field:4196->vlan_vid,output:2"
```

### Strip VLAN ID

```
actions="strip_vlan,output:2"
```

### Modify MAC source

```
actions="set_field:10:AB:11:CD:12:EF->eth_src,2"
```

### Modify MAC destination

```
actions="set_field:10:AB:11:CD:12:EF->eth_dst,2"
```

### Push MPLS

```
actions="pop_l2,push_mpls:0x8847,set_field:16->mpls_label,push_l2,set_field:10:AB:11:CD:12:EF->eth_dst,output:2"
```

### Set MPLS Label

```
actions="pop_l2,pop_mpls:0x8847,push_mpls:0x8847,set_field:16->mpls_label,push_l2,set_field:10:AB:11:CD:12:EF->eth_dst,output:2"
```

### Pop MPLS

```
actions="pop_l2,pop_mpls:0,push_l2,set_field:10:AB:11:CD:12:EF->eth_dst,output:2"   
```

## Rule Input Filters

### Filter VLAN ID:

```
cc add-flow br0 in_port=1,priority=32768,dl_vlan=1,actions=output:2
```

### Match only untagged traffic:

``` 
cc add-flow br0 in_port=1,priority=32768,vlan_tci=0x0000/0x1000,actions="2"
```

### Filter by protocol:

```
cc add-flow br0 in_port=1,priority=32768,tcp,actions=output:2
```

```
cc add-flow br0 in_port=1,priority=32768,udp,actions=output:2
```

Protocol options:

- arp

- icmp

- ip

- rarp

- sctp

- tcp

- udp

### IP with protocol number:

```
cc add-flow br0 in_port=1,priority=32768,ip,nw_proto=50,actions="output:2"
```

## Filter MAC source:

```
cc add-flow br0 in_port=1,priority=32768,dl_src=10:AB:11:CD:12:EF,actions=output:2
```

## Filter MAC destination:

```
cc add-flow br0 in_port=1,priority=32768,dl_dst=10:AB:11:CD:12:EF,actions=output:2
```

## Filter MAC source and destination:

```
cc add-flow br0 in_port=1,priority=32768,dl_src=10:AB:11:CD:12:EF,dl_dst=10:AB:11:CD:12:EF,actions=output:2
```

### Filter source IP:

```
cc add-flow br0 in_port=1,priority=32768,ip,nw_src=192.168.0.1,actions=output:2
```

### Filter destination IP:

```
cc add-flow br0 in_port=1,priority=32768,ip,nw_dst=192.168.0.1,actions=output:2
```

### Filter source and destination IP:

```
cc add-flow br0 in_port=1,priority=32768,ip,nw_src=192.168.0.1,nw_dst=192.168.0.1,actions=output:2
```

***nw_src*** & ***nw_dst*** are interchangeable with ***ip_src*** and ***ip_dst***

### Filter source port:

```
cc add-flow br0 in_port=1,priority=32768,tcp,tp_src=443,actions=output:2
```

### Filter destination port:

```
cc add-flow br0 in_port=1,priority=32768,tcp,tp_dst=443,actions=output:2
```

### Filter source and destination port:

```
cc add-flow br0 in_port=1,priority=32768,udp,tp_src=80,tp_dst=80,actions=output:2
```

***tp_src*** and ***tp_dst*** deprecated. use ***tcp_src***, ***tcp_dst***, ***udp_src***, ***udp_dst***, ***sctp_src***, ***sctp_dst***

### Filter ICMP:

```
cc add-flow br0 in_port=1,priority=32758,icmp,actions="output:2"
```

### Filter ICMP by ICMP type:

```
cc add-flow br0 in_port=1,priority=32758,icmp,icmp_type=3,actions="output:2"
```

### Filter ICMP by ICMP type and ICMP code (3,3):

```
cc add-flow br0 in_port=1,priority=32758,icmp,icmp_type=3,icmp_code=3,actions="output:2"
```

### Filtering on TCP Flags:

### In GUI:

- Set Add Rule > Protocol to "IP/TCP"

- Use "Extra Custom Match" for filtering fields 

- Example custom match entry: ***tcp_flags=+fin***     

- Use '+' to include a flag and '-' to exclude a flag.  Unspecified tags are wildcards. e.g. ***tcp_flags=+syn-ack***

Flag options:

- ack

- cwr

- ece

- ns

- psh

- rst

- syn

- urg


### In CLI:

```
cc add-flow br0 in_port=1,tcp,tcp_flags=+syn-ack,actions=output:2
```

# IPV6 Filtering:

- Set DB Mode to IPV6 in settings

## In GUI:

- Set Add Rule > Protocol to "Custom"

- Set Ether Type to "0x86dd"

- Use "Extra Custom Match" for filtering fields

## In CLI:

```
cc add-flow br0 ipv6,in_port=1,ipv6_src=::1,ipv6_dst=::1,actions=2
```

```
cc add-flow br0 tcp6,in_port=1,tcp_src=80,tcp_dst=80,actions=2
```

or

```
cc add-flow br0 tcp6,in_port=1,tp_src=80,tp_dst=80,actions=2
```

```
cc add-flow br0 udp6,in_port=1,udp_src=80,udp_dst=80,actions=2
```

or

```
cc add-flow br0 udp6,in_port=1,tp_src=80,tp_dst=80,actions=2
```

### with IP and Port:

``` 
cc add-flow br0 ipv6,in_port=1,ipv6_src=::1,ipv6_dst=::1,tp_src=80,tp_dst=80,actions=2
```

## Delete rule: (the behavior of deleting rules can be unexpected.  deleting a rule that matches destination port 80 will delete ALL rules that could potentially go to port 80 not rules that specifically go to port 80)

```
cc del-flows br0 in_port=1
```

```
cc del-flows br0 <matching criteria>  delete all matching flows
```

```
cc del-flows br0 tcp
```

```
cc del-flows br0 tp_dst=80
```

```
cc del-flows br0 dl_src=10:AB:11:CD:12:EF
```

```
cc del-flows br0 nw_src=192.168.0.1
```

```
cc del-flows br0 cookie=<cookie> #Only way to delete a single specific flow
```

## Delete ALL rules:

```
cc del-flows br0
```

## Timeout of rules:

```
cc add-flow br0 in_port=1,hard_timeout=5,priority=32768,actions=output:2
```

timeout number is seconds

```
cc add-flow br0 in_port=1,idle_timeout=5,priority=32768,actions=output:2
```

## Port Groups

### Show Groups:

```
cc dump-groups br0
```

### Add Group:

#### All (Traffic Replication):

- The ***bucket*** parameter takes the same options as ***actions*** above

```
cc add-group br0 group_id=100,type=all,bucket=output:5,bucket=output:6
```    

#### Select (Load Balancing):

```
cc add-group br0 group_id=100,type=select,bucket=output:5,bucket=output:6,bucket=output:7
```

#### Fast Failover:

```
cc add-group br0 group_id=100,type=ff,bucket=watch_port:7,output:7,bucket=watch_port:8,output:7
```

### Delete All Groups:

```
cc del-groups br0
```

### Delete Group:

#### Delete only group 100

```
cc del-groups br0 group_id=100   
```

# MPLS:  (EX2 does not support pop_all_mpls command. The user must specify each MPLS tag to pop)

```
ovs-ofctl add-flow br0 in_port=1,mpls,actions=output:2 -O openflow13 
```

- MPLS labeled packets pass through, non-MPLS tagged traffic does not

```
ovs-ofctl add-flow br0 in_port=1,mpls,actions="pop_l2,pop_all_mpls,push_l2,set_field:00:00:00:00:00:AA->eth_dst,output:2" -O openflow13
```

- drop MPLS label(s) of ipv4 and ipv6, unlabeled traffic is not forwarded 
- requires a 2nd rule with lower priority


## Filtering on MPLS labeled traffic:
 
- Filtering on MPLS labeled packets does not work - requires strip of MPLS label and a Hardware loop

## Multiple Outputs with MPLS pop command

```
ovs-ofctl add-flow br0 in_port=1,mpls,actions="pop_l2,pop_all_mpls,push_l2,set_field:00:00:00:00:00:AA->eth_dst,output:2,pop_l2,pop_all_mpls,push_l2,set_field:00:00:00:00:00:BB->eth_dst,output:3" -O openflow13
```

## MPLS pop

```
ovs-ofctl add-flow br0 "in_port=1,dl_type=0x0800,actions=pop_l2,push_mpls:0x8847,set_field:16->mpls_label,push_l2,set_field:00:1e:08:00:02:01->eth_dst,output:2" -O openflow13 
```

 - add MPLS label 16


## MPLS change label

```
ovs-ofctl add-flow br0 "dl_type=0x8847,mpls_label=300,actions=pop_l2,pop_mpls:0x8847,push_mpls:0x8847,set_field:400->mpls_label,push_l2,set_field:00:1e:08:00:03:01->eth_dst,output:2" -O openflow13
```
- changes MPLS label from 300 to 400

# GRE: (non-G4 uses different syntax, see below.  EX2 will automatically untunnel any GRE traffic received)

## CLI Config: (G4 units)
	
### Encapsulating Packetmaster

	config

	configure terminal
        
	openflow tunnel local_vtep_ip 10.0.0.1
	
	end
	
	write 
	
Verify with > show running-config | include tunnel
	
	exit
	
	cv add-port br0 l2gre1 -- set interface l2gre1 type=l2gre options:remote_ip=10.0.0.2 options:bind_port=eth-0-1 options:nexthop_mac=00:1e:08:0b:36:c9


### Decapsulating Packetmaster

	config

	configure terminal

	openflow tunnel local_vtep_ip 10.0.0.2
	
	end
	
	exit
	
	cv add-port br0 l2gre1 -- set interface l2gre1 type=l2gre options:remote_ip=10.0.0.1 options:bind_port=eth-0-1 options:nexthop_mac=70:b3:d5:01:a7:c8

## CLI Config: (EX2)

	cv add-port br0 gre1 -- set interface gre1 type=gre options:remote_ip=10.0.0.2 options:local_ip=10.0.0.1 options:bind_port=eth-0-4 options:nexthop_mac=00:00:00:00:00:02

### Flows:
	
### Encap (Encap PM)

	cc add-flow br0 in_port=2,actions=output:201

### Decap (Decap PM)

	cc add-flow br0 in_port=4,gre,actions=gre_decap -O openflow13
	
	cc add-flow br0 in_port=201,actions=output:2
	
### Verify logical interfaces/tunnels
	
	cc dump-ports br0 ( | grep <interface number> i.e. grep 201)
	
	ovs-ofctl show br0
	
	config menu> show interface tunnel brief
