# Тема проектной работы: "Расширение сети передачи данных компании,организация вспомогательных сервисов для контроля сетевого оборудования"
## Целью данной проектной работы является:
1. Организовать отказоустойчивую сеть передачи данных компании
2. Разобраться  и интегрировать сервис Netbox в существующую сеть
3. Организовать мониторинг сети на базе Zabbix

 Для реализации данных задач был организован лабараторный стэнд на базе Oracle Virtualbox.
![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/лабораторный%20стенд.jpg)

Для реализации связи между виртуальными машинами необходимо разместить их в одной виртуальной сети, в данном случае Сеть NAT 10.0.2.0/24.
Что бы оборудование в лабораторном стенде имело связь с виртуальными машинами нужно седенить их с сетью Cloud0, и соответсвенно на интерфейсе оборудования прописать статический ip.
## 1. Организация отказоустойчивой сети передачи данных компании.
![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/old%20net1.jpg)

Согласно данной схемы у компании было 3 сервиса:
1. Один критически важный сервис расположенный на удалённой площадке. До него идёт один физический канал связи построенный через одну пару маршрутизаторов
2. Сервис доступа к базе данных офисных сотрудников. Оператор связи предоставлял один L3 канал по средствам оптической линии связи. Данный канал терминировался на маршрутизаторе, проходил преобразование адресов и таким образом предоставлял доступ к сети интернет.
3. Сервис доступа к облачной АТС(VOIP) предоставлялся так же(L3 канал в другом vlan)

Прошло некоторое время и компания расширилась и стала более критически реагировать на отказ в обслуживании данных сервисов.
Было решено расширить сеть передачи данных до следующего вида:
![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/new%20net1.jpg)

**место установки** | **наименование оборудования** | **Интерфейс** | **ip address**
 --- | --- | --- | ---
 Отдел связи | R1 | e0/0 | 15.0.0.1/30 
 Отдел связи | R1 | e0/1 | 30.0.0.1/30
 Отдел связи | R1 | e0/2 | 33.0.0.1/30
 Отдел связи | R1 | e0/3 | 34.0.0.1/30
 Отдел связи | R1 | e1/0 | 10.0.2.10/24
 Отдел связи | R1 | lo0 | 1.1.1.1/32
 Отдел связи | R2 | e0/0.10 | 14.0.0.1/30
 Отдел связи | R2 | e0/1 | 30.0.0.2/30
 Отдел связи | R2 | e0/2 | 31.0.0.1/30
 Отдел связи | R2 | e0/3 | 35.0.0.1/30
 Отдел связи | R2 | e1/0 | 10.0.2.11/24
 Отдел связи | R2 | lo0 | 2.2.2.2/32
 Отдел связи | L3SW_3 | e0/0 | 10.0.0.1/30
 Отдел связи | L3SW_3 | e0/1 | 172.16.0.1/29
 Отдел связи | L3SW_3 | e0/2 | 172.20.0.3/29
 Отдел связи | L3SW_3 | e0/3 | 13.0.0.1/30
 Отдел связи | L3SW_3 | e1/0 | 10.0.2.21/24
 Отдел связи | L3SW_3 | lo0 | 3.3.3.3/32
 Отдел связи | L3SW_4 | e0/0 | 12.0.0.1/30
 Отдел связи | L3SW_4 | e0/1 | 172.20.0.1/29
 Отдел связи | L3SW_4 | e0/2 | 172.16.0.3/29
 Отдел связи | L3SW_4 | e0/3 | 13.0.0.2/30
 Отдел связи | L3SW_4 | e1/0 | 10.0.2.22/24
 Отдел связи | L3SW_4 | lo0 | 4.4.4.4/32
 Отдел связи | SW1_1 | Vlan101 | 10.0.2.17/24
 Отдел связи | SW1_2 | Vlan101 | 10.0.2.18/24
 Отдел связи | SW1_3 | Vlan101 | 10.0.2.16/24
 Отдел связи | SW2_1 | Vlan101 | 10.0.2.14/24
 Отдел связи | SW2_2 | Vlan101 | 10.0.2.13/24
 Отдел связи | SW2_3 | Vlan101 | 10.0.2.12/24
 Отдел связи | VPC15 | e0 | 172.16.0.4/29
 Отдел связи | VPC16 | e0 | 172.20.0.4/29
 Отдел ИТ | SW3_25 | Vlan101 | 10.0.2.8/24
 Отдел ИТ | SW3_26 | Vlan101 | 10.0.2.6/24
 Отдел ИТ | SW3_27 | Vlan101 | 10.0.2.7/24
 Отдел ИТ | R21 | e0/0 | 31.0.0.2/30
 Отдел ИТ | R21 | e0/1 | 34.0.0.2/30
 Отдел ИТ | R21 | e0/2 | 32.0.0.2/30
 Отдел ИТ | R21 | e0/3 | 100.10.0.2/29
 Отдел ИТ | R21 | e1/0 | 200.20.0.2/29
 Отдел ИТ | R21 | e1/1 | 10.0.2.9/24
 Отдел ИТ | R21 | lo0 | 21.21.21.21/32
 Отдел ИТ | R22 | e0/0 | 33.0.0.2/30
 Отдел ИТ | R22 | e0/1 | 35.0.0.2/30
 Отдел ИТ | R22 | e0/2 | 32.0.0.1/30
 Отдел ИТ | R22 | e0/3 | 100.10.0.1/29
 Отдел ИТ | R22 | e1/0 | 200.20.0.1/29
 Отдел ИТ | R22 | e1/1 | 10.0.2.5/24
 Отдел ИТ | R22 | lo0 | 22.22.22.22/32
 Отдел ИТ | LAN | e0 | 200.20.0.4/29
 Отдел ИТ | VOIP | e0 | 100.10.0.4/29
 Удалённая площадка | L3SW_11 | e0/0 | 10.0.0.2/30
 Удалённая площадка | L3SW_11 | e0/1 | 172.16.16.1/30
 Удалённая площадка | L3SW_11 | e0/2 | 11.0.0.1/30
 Удалённая площадка | L3SW_11 | e0/3 | 10.0.2.19/24
 Удалённая площадка | L3SW_11 | lo0 | 11.11.11.11/32
 Удалённая площадка | L3SW_12 | e0/0 | 12.0.0.2/30
 Удалённая площадка | L3SW_12 | e0/1 | 172.20.20.1/30
 Удалённая площадка | L3SW_12 | e0/2 | 11.0.0.2/30
 Удалённая площадка | L3SW_12 | e0/3 | 10.0.2.20/24
 Удалённая площадка | L3SW_12 | lo0 | 12.12.12.12/32
 Удалённая площадка | VPC13 | e0 | 172.16.16.2/30
 Удалённая площадка | VPC14 | e0 | 172.20.20.2/30
 Оператор связи | R17 | e0/0.10 | 14.0.0.2/30
 Оператор связи | R17 | e0/1 | 23.0.0.1/30
 Оператор связи | R17 | e0/2 | 24.0.0.1/30
 Оператор связи | R17 | e0/3 | 20.0.0.1/30
 Оператор связи | R17 | e1/0 | 10.0.2.23/24
 Оператор связи | R17 | lo0 | 17.17.17.17/32
 Оператор связи | R18 | e0/0 | 10.0.2.24/24
 Оператор связи | R18 | e0/1 | 21.0.0.1/30
 Оператор связи | R18 | e0/3 | 20.0.0.2/30
 Оператор связи | R18 | lo0 | 18.18.18.18/32
 Оператор связи | R19 | e0/0 | 100.0.0.1/30
 Оператор связи | R19 | e0/1 | 21.0.0.2/30
 Оператор связи | R19 | e0/2 | 24.0.0.2/30
 Оператор связи | R19 | e0/3 | 22.0.0.1/30
 Оператор связи | R19 | e1/0 | 10.0.2.25/24
 Оператор связи | R19 | lo0 | 19.19.19.19/32
 Оператор связи | R20 | e0/0 | 15.0.0.2/30
 Оператор связи | R20 | e0/1 | 23.0.0.2/30
 Оператор связи | R20 | e0/2 | 200.0.0.1/30
 Оператор связи | R20 | e0/3 | 22.0.0.2/30
 Оператор связи | R20 | e1/0 | 10.0.2.26/24
 Оператор связи | R20 | lo0 | 20.20.20.20/32
 Оператор связи | Asterisk | e0 | 100.0.0.2/30
 Оператор связи | BD | e0 | 200.0.0.2/30
  
### 1. Критически важный сервис расположенный на удалённой площадке.
  Для критически важного сервиса была продложена дополнительная линия связи, установлен второй комплект серверного оборудования.Так же был добавлен второй комплект маршрутизаторов. На данных маршрутизаторах(L3SW(3,4,11,12)) для целей безотказной работы сервиса была настроена динамическая маршруизация OSPF.Со стороны отдела связи так же было добавлено еще 5 коммутатора таким образом чтобы они образовали два отдельных сегмента.Для борьбы с петлями коммутации в каждом сегменте был настроен RSTP. Для того что бы выход из строя маршризатора не повлек бы за собой обрыв канала связи с каждым комплектом серверов был настроен протокол резервирования шлюза VRRP.
```
L3SW3#
L3SW3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                10.0.0.1        YES NVRAM  up                    up      
Ethernet0/1                172.16.0.1      YES NVRAM  up                    up      
Ethernet0/2                172.20.0.3      YES NVRAM  up                    up      
Ethernet0/3                13.0.0.1        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.21       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  3.3.3.3         YES NVRAM  up                    up

L3SW3#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
11.11.11.11       1   FULL/BDR        00:00:33    10.0.0.2        Ethernet0/0
4.4.4.4           1   FULL/BDR        00:00:38    172.20.0.1      Ethernet0/2
4.4.4.4           1   FULL/BDR        00:00:36    172.16.0.3      Ethernet0/1

L3SW3#sh vrrp   
Ethernet0/1 - Group 1  
  State is Master  
  Virtual IP address is 172.16.0.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 255 
  Master Router is 172.16.0.1 (local), priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.003 sec

Ethernet0/2 - Group 2  
  State is Backup  
  Virtual IP address is 172.20.0.1
  Virtual MAC address is 0000.5e00.0102
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 100 
  Master Router is 172.20.0.1, priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.609 sec (expires in 2.792 sec)
```
```
L3SW4#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                12.0.0.1        YES NVRAM  up                    up      
Ethernet0/1                172.20.0.1      YES NVRAM  up                    up      
Ethernet0/2                172.16.0.3      YES NVRAM  up                    up      
Ethernet0/3                13.0.0.2        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.22       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  4.4.4.4         YES NVRAM  up                    up      

L3SW4#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
12.12.12.12       1   FULL/BDR        00:00:36    12.0.0.2        Ethernet0/0
3.3.3.3           1   FULL/DR         00:00:38    172.20.0.3      Ethernet0/1
3.3.3.3           1   FULL/DR         00:00:33    172.16.0.1      Ethernet0/2
L3SW4#sh vrrp
Ethernet0/1 - Group 2  
  State is Master  
  Virtual IP address is 172.20.0.1
  Virtual MAC address is 0000.5e00.0102
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 255 
  Master Router is 172.20.0.1 (local), priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.003 sec

Ethernet0/2 - Group 1  
  State is Backup  
  Virtual IP address is 172.16.0.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 100 
  Master Router is 172.16.0.1, priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.609 sec (expires in 2.969 sec)
```
```
L3SW_11#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                10.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                172.16.16.1     YES NVRAM  up                    up      
Ethernet0/2                11.0.0.1        YES NVRAM  up                    up      
Ethernet0/3                10.0.2.19       YES NVRAM  up                    up      
Loopback0                  11.11.11.11     YES NVRAM  up                    up      
L3SW_11#sh ip ospf nei
L3SW_11#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
3.3.3.3           1   FULL/DR         00:00:38    10.0.0.1        Ethernet0/0
12.12.12.12       1   FULL/DR         00:00:39    11.0.0.2        Ethernet0/2
```
```
L3SW12#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                12.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                172.20.20.1     YES NVRAM  up                    up      
Ethernet0/2                11.0.0.2        YES NVRAM  up                    up      
Ethernet0/3                10.0.2.20       YES NVRAM  up                    up      
Loopback0                  12.12.12.12     YES NVRAM  up                    up

L3SW12#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
4.4.4.4           1   FULL/DR         00:00:36    12.0.0.1        Ethernet0/0
11.11.11.11       1   FULL/BDR        00:00:31    11.0.0.1        Ethernet0/2
```
```
VPC15> ping 172.16.16.2

84 bytes from 172.16.16.2 icmp_seq=1 ttl=62 time=5.354 ms
84 bytes from 172.16.16.2 icmp_seq=2 ttl=62 time=2.364 ms
84 bytes from 172.16.16.2 icmp_seq=3 ttl=62 time=1.528 ms
84 bytes from 172.16.16.2 icmp_seq=4 ttl=62 time=2.214 ms
84 bytes from 172.16.16.2 icmp_seq=5 ttl=62 time=2.785 ms
```
```
VPC16> sh ip

NAME        : VPC16[1]
IP/MASK     : 172.20.0.4/29
GATEWAY     : 172.20.0.1
DNS         : 
MAC         : 00:50:79:66:68:10
LPORT       : 20000
RHOST:PORT  : 127.0.0.1:30000
MTU         : 1500

VPC16> ping 172.20.20.2

84 bytes from 172.20.20.2 icmp_seq=1 ttl=62 time=15.971 ms
84 bytes from 172.20.20.2 icmp_seq=2 ttl=62 time=6.367 ms
84 bytes from 172.20.20.2 icmp_seq=3 ttl=62 time=4.116 ms
84 bytes from 172.20.20.2 icmp_seq=4 ttl=62 time=2.756 ms
84 bytes from 172.20.20.2 icmp_seq=5 ttl=62 time=3.668 ms
```

### 2.  Доступа к удалённой базе данных офисными сотрудниками.
  Для целей отказоустойчивого доступа была так же организована дополнительная линия связи,со стороны отдела связи был установлен новый телекомуникационный шкаф ТШ-1, с двумя маршрутизаторами(R1,R2).Со стороны отдела ИТ так же был добавлен один маршрутизатор(R22), а так же добавлен один коммутатор. между оборудование отдела связи(R1,R2) и оборудованием отдела ИТ(R21,R22) было проложено ,по разнесенным трассам, две линии связи. Между маршрутизаторами так же был настроен протокол динамической маршрутизации OSPF. Со стороны отдела ИТ на коммутаторах, для целей борьбы с петлями коммутации, был настроен RSTP. Для того что бы выход из строя маршризатора не повлек бы за собой обрыв канала связи, был настроен протокол резервирования шлюза VRRP.
  Для предоставления отказоустойчивого доступа в сеть интернет оператор связи решил маштабировать свою инфраструктуру. Было добавлено ещё 3 маршрутизатора, для обмена маршрутной информацией был применён протокол динамической маршрутизации EIGRP.
  Для того чтобы обеспечить минимальное время восстановления доступа к базе данных было принято решение организовывать связь по средствам BGP,брать у оператора ASN. Оператор связи в качестве route-reflector поставил R17, чтобы не отдавать лишних сетей через access list и route-map были выделены и анонсированы только нужные сети.Для доступа к сервису облачной АТС был настроен NAT на маршрутизаторах R1 и R2. Приоритетным каналом связи между предприятием и операторм связи является линия между R1 и R20.
```
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                15.0.0.1        YES NVRAM  up                    up      
Ethernet0/1                30.0.0.1        YES NVRAM  up                    up      
Ethernet0/2                33.0.0.1        YES NVRAM  up                    up      
Ethernet0/3                34.0.0.1        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.10       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  1.1.1.1         YES NVRAM  up                    up      
NVI0                       15.0.0.1        YES unset  up                    up      
R1#sh ip ospf neig

Neighbor ID     Pri   State           Dead Time   Address         Interface
21.21.21.21       1   FULL/DR         00:00:37    34.0.0.2        Ethernet0/3
22.22.22.22       1   FULL/DR         00:00:36    33.0.0.2        Ethernet0/2
2.2.2.2           1   FULL/DR         00:00:38    30.0.0.2        Ethernet0/1
R1#sh ip bgp sum
R1#sh ip bgp summary 
BGP router identifier 15.0.0.1, local AS number 65002
BGP table version is 6, main routing table version 6
4 network entries using 560 bytes of memory
6 path entries using 480 bytes of memory
4/3 BGP path/bestpath attribute entries using 576 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1640 total bytes of memory
BGP activity 4/0 prefixes, 7/1 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
15.0.0.2        4        65001     212     209        6    0    0 03:07:36        2
30.0.0.2        4        65002     228     229        6    0    0 03:22:55        2

```
рабочая конфигурация R1:
```
router ospf 1
 router-id 1.1.1.1
 area 3 stub
 redistribute bgp 65002 subnets
 network 1.1.1.1 0.0.0.0 area 0
 network 15.0.0.0 0.0.0.3 area 3
 network 30.0.0.0 0.0.0.3 area 3
 network 33.0.0.0 0.0.0.3 area 0
 network 34.0.0.0 0.0.0.3 area 0
!
router bgp 65002
 bgp router-id 15.0.0.1
 bgp log-neighbor-changes
 redistribute ospf 1 route-map VOIP
 neighbor 15.0.0.2 remote-as 65001
 neighbor 15.0.0.2 next-hop-self
 neighbor 15.0.0.2 route-map MAIN-ROUTE out
 neighbor 30.0.0.2 remote-as 65002
 neighbor 30.0.0.2 next-hop-self
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
ip nat inside source list 3 interface Ethernet0/0 overload
!
ip access-list standard LAN
 permit 100.10.0.0 0.0.0.7
ip access-list standard VOIP
 permit 200.20.0.0 0.0.0.7
!
!
route-map VOIP permit 10
 match ip address LAN VOIP
!
route-map MAIN_ROUTE permit 10
 set local-preference 110
!
snmp-server community public RW
!
access-list 2 permit 200.20.0.0 0.0.0.7
access-list 3 permit 100.10.0.0 0.0.0.7
```
R2:
```
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                unassigned      YES NVRAM  up                    up      
Ethernet0/0.10             14.0.0.1        YES NVRAM  up                    up      
Ethernet0/1                30.0.0.2        YES NVRAM  up                    up      
Ethernet0/2                31.0.0.1        YES NVRAM  up                    up      
Ethernet0/3                35.0.0.1        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.11       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  2.2.2.2         YES NVRAM  up                    up      
NVI0                       14.0.0.1        YES unset  up                    up      
R2#sh ip ospf nei
R2#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
22.22.22.22       1   FULL/DR         00:00:31    35.0.0.2        Ethernet0/3
21.21.21.21       1   FULL/DR         00:00:33    31.0.0.2        Ethernet0/2
1.1.1.1           1   FULL/BDR        00:00:39    30.0.0.1        Ethernet0/1
R2#sh ip bgp sum
BGP router identifier 2.2.2.2, local AS number 65002
BGP table version is 6, main routing table version 6
4 network entries using 560 bytes of memory
8 path entries using 640 bytes of memory
5/2 BGP path/bestpath attribute entries using 720 bytes of memory
2 BGP AS-PATH entries using 64 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1984 total bytes of memory
BGP activity 4/0 prefixes, 8/0 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
14.0.0.2        4        65001     225     229        6    0    0 03:23:18        2
30.0.0.1        4        65002     241     240        6    0    0 03:33:36        4
```
рабочая конфигурация R2:
```
router ospf 1
 router-id 2.2.2.2
 area 3 stub
 redistribute bgp 65002 subnets
 network 2.2.2.2 0.0.0.0 area 0
 network 14.0.0.0 0.0.0.3 area 3
 network 30.0.0.0 0.0.0.3 area 3
 network 31.0.0.0 0.0.0.3 area 0
 network 35.0.0.0 0.0.0.3 area 0
!
router bgp 65002
 bgp router-id 2.2.2.2
 bgp log-neighbor-changes
 redistribute ospf 1 route-map SERVICES
 neighbor 14.0.0.2 remote-as 65001
 neighbor 14.0.0.2 next-hop-self
 neighbor 14.0.0.2 route-map REZERV in
 neighbor 30.0.0.1 remote-as 65002
 neighbor 30.0.0.1 next-hop-self
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server

ip nat inside source list 3 interface Ethernet0/0.10 overload
!
ip access-list standard LAN
 permit 200.20.0.0 0.0.0.7
ip access-list standard VOIP
 permit 100.10.0.0 0.0.0.7
!
!
route-map REZERV permit 10
 set as-path prepend 65002 65002 65002
!
route-map SERVICES permit 10
 match ip address LAN VOIP
!
snmp-server community public RW
!
access-list 2 permit 200.20.0.0 0.0.0.7
access-list 3 permit 100.10.0.0 0.0.0.7
```
R17:
```
R17#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                unassigned      YES NVRAM  up                    up      
Ethernet0/0.10             14.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                23.0.0.1        YES NVRAM  up                    up      
Ethernet0/2                24.0.0.1        YES NVRAM  up                    up      
Ethernet0/3                20.0.0.1        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.23       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  17.17.17.17     YES NVRAM  up                    up      
R17#sh ip eig
R17#sh ip eigrp ne
R17#sh ip eigrp neighbors 
EIGRP-IPv4 VR(OP) Address-Family Neighbors for AS(1)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
2   23.0.0.2                Et0/1                    14 03:22:17    6   150  0  6
1   24.0.0.2                Et0/2                    12 03:24:13   73   438  0  12
0   20.0.0.2                Et0/3                    14 03:25:02   20   120  0  20
R17#sh ip bgp sum
BGP router identifier 17.17.17.17, local AS number 65001
BGP table version is 5, main routing table version 5
4 network entries using 560 bytes of memory
4 path entries using 320 bytes of memory
2/2 BGP path/bestpath attribute entries using 288 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1192 total bytes of memory
BGP activity 4/0 prefixes, 4/0 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
14.0.0.1        4        65002     233     230        5    0    0 03:27:16        2
18.18.18.18     4        65001     228     232        5    0    0 03:25:03        0
19.19.19.19     4        65001     230     233        5    0    0 03:24:17        1
20.20.20.20     4        65001     226     230        5    0    0 03:22:16        1
```
рабочая конфигурация R17:
```
router eigrp OP
 !
 address-family ipv4 unicast autonomous-system 1
  !
  topology base
  exit-af-topology
  network 14.0.0.0 0.0.0.3
  network 17.17.17.17 0.0.0.0
  network 20.0.0.0 0.0.0.3
  network 23.0.0.0 0.0.0.3
  network 24.0.0.0 0.0.0.3
 exit-address-family
!
router bgp 65001
 bgp router-id 17.17.17.17
 bgp log-neighbor-changes
 neighbor IBGP peer-group
 neighbor IBGP remote-as 65001
 neighbor IBGP update-source Loopback0
 neighbor IBGP route-reflector-client
 neighbor IBGP next-hop-self
 neighbor 14.0.0.1 remote-as 65002
 neighbor 14.0.0.1 next-hop-self
 neighbor 18.18.18.18 peer-group IBGP
 neighbor 19.19.19.19 peer-group IBGP
 neighbor 20.20.20.20 peer-group IBGP
 ```
R18:
```
R18#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                10.0.2.24       YES NVRAM  up                    up      
Ethernet0/1                21.0.0.1        YES NVRAM  up                    up      
Ethernet0/2                unassigned      YES NVRAM  administratively down down    
Ethernet0/3                20.0.0.2        YES NVRAM  up                    up      
Ethernet1/0                unassigned      YES NVRAM  administratively down down    
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  18.18.18.18     YES NVRAM  up                    up      

R18#sh ip eigrp neighbors 
EIGRP-IPv4 VR(OP) Address-Family Neighbors for AS(1)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
1   21.0.0.2                Et0/1                    12 03:26:39   10   100  0  13
0   20.0.0.1                Et0/3                    13 03:27:28  341  2046  0  19
R18#sh ip bgp sum
BGP router identifier 18.18.18.18, local AS number 65001
BGP table version is 5, main routing table version 5
4 network entries using 560 bytes of memory
4 path entries using 320 bytes of memory
2/2 BGP path/bestpath attribute entries using 288 bytes of memory
2 BGP rrinfo entries using 48 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1240 total bytes of memory
BGP activity 4/0 prefixes, 4/0 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
17.17.17.17     4        65001     234     231        5    0    0 03:27:25        4
```
рабочая конфигурация R18:
```
router eigrp OP
 !
 address-family ipv4 unicast autonomous-system 1
  !
  topology base
  exit-af-topology
  network 18.18.18.18 0.0.0.0
  network 20.0.0.0 0.0.0.3
  network 21.0.0.0 0.0.0.3
 exit-address-family
!
router bgp 65001
 bgp router-id 18.18.18.18
 bgp log-neighbor-changes
 neighbor 17.17.17.17 remote-as 65001
 neighbor 17.17.17.17 update-source Loopback0
 neighbor 17.17.17.17 next-hop-self
 ```
R19:
```
R19#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                100.0.0.1       YES NVRAM  up                    up      
Ethernet0/1                21.0.0.2        YES NVRAM  up                    up      
Ethernet0/2                24.0.0.2        YES NVRAM  up                    up      
Ethernet0/3                22.0.0.1        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.25       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  19.19.19.19     YES NVRAM  up                    up      
R19#sh ip eigr
R19#sh ip eigrp nei
R19#sh ip eigrp neighbors 
EIGRP-IPv4 VR(OP) Address-Family Neighbors for AS(1)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
2   22.0.0.2                Et0/3                    12 03:27:06   15   100  0  5
1   21.0.0.1                Et0/1                    11 03:29:02   28   168  0  19
0   24.0.0.1                Et0/2                    12 03:29:02   10   100  0  20
R19#sh ip bgp sum
BGP router identifier 19.19.19.19, local AS number 65001
BGP table version is 5, main routing table version 5
4 network entries using 560 bytes of memory
4 path entries using 320 bytes of memory
3/3 BGP path/bestpath attribute entries using 432 bytes of memory
1 BGP rrinfo entries using 24 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1360 total bytes of memory
BGP activity 4/0 prefixes, 4/0 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
17.17.17.17     4        65001     238     235        5    0    0 03:29:07        3
```
рабочая конфигурация R19:
```
router eigrp OP
 !
 address-family ipv4 unicast autonomous-system 1
  !
  topology base
  exit-af-topology
  network 19.19.19.19 0.0.0.0
  network 21.0.0.0 0.0.0.3
  network 22.0.0.0 0.0.0.3
  network 24.0.0.0 0.0.0.3
  network 100.0.0.0 0.0.0.7
 exit-address-family
!
router bgp 65001
 bgp router-id 19.19.19.19
 bgp log-neighbor-changes
 redistribute connected route-map VOIP
 neighbor 17.17.17.17 remote-as 65001
 neighbor 17.17.17.17 update-source Loopback0
 neighbor 17.17.17.17 next-hop-self
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
ip access-list standard VOIP
 permit 100.0.0.0 0.0.0.7
!
!
route-map VOIP permit 10
 match ip address VOIP
 ```
R20:
```
R20#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                15.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                23.0.0.2        YES NVRAM  up                    up      
Ethernet0/2                200.0.0.1       YES NVRAM  up                    up      
Ethernet0/3                22.0.0.2        YES NVRAM  up                    up      
Ethernet1/0                10.0.2.26       YES NVRAM  up                    up      
Ethernet1/1                unassigned      YES NVRAM  administratively down down    
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  20.20.20.20     YES NVRAM  up                    up      
R20#sh ip ei
R20#sh ip eigrp nei
EIGRP-IPv4 VR(OP) Address-Family Neighbors for AS(1)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
1   22.0.0.1                Et0/3                    13 03:29:46    7   100  0  14
0   23.0.0.1                Et0/1                    13 03:29:46 1594  5000  0  18
R20#sh ip bgp sum
BGP router identifier 20.20.20.20, local AS number 65001
BGP table version is 5, main routing table version 5
4 network entries using 560 bytes of memory
4 path entries using 320 bytes of memory
3/3 BGP path/bestpath attribute entries using 432 bytes of memory
1 BGP rrinfo entries using 24 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1360 total bytes of memory
BGP activity 4/0 prefixes, 4/0 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
15.0.0.1        4        65002     233     236        5    0    0 03:29:41        0
17.17.17.17     4        65001     238     234        5    0    0 03:29:41        3
```
рабочая конфигурация R20:
```
router eigrp OP
 !
 address-family ipv4 unicast autonomous-system 1
  !
  topology base
   redistribute bgp 65001
  exit-af-topology
  network 15.0.0.0 0.0.0.3
  network 20.20.20.16 0.0.0.7
  network 20.20.20.20 0.0.0.0
  network 22.0.0.0 0.0.0.3
  network 23.0.0.0 0.0.0.3
  network 200.0.0.0 0.0.0.7
 exit-address-family
!
router bgp 65001
 bgp router-id 20.20.20.20
 bgp log-neighbor-changes
 redistribute eigrp 1 metric 20 route-map BD
 neighbor 15.0.0.1 remote-as 65002
 neighbor 15.0.0.1 next-hop-self
 neighbor 17.17.17.17 remote-as 65001
 neighbor 17.17.17.17 update-source Loopback0
 neighbor 17.17.17.17 next-hop-self
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
ip access-list standard BD
 permit 200.0.0.0 0.0.0.3
!         
!
route-map BD permit 10
 match ip address BD
```
R21:
```
R21#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                31.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                34.0.0.2        YES NVRAM  up                    up      
Ethernet0/2                32.0.0.2        YES NVRAM  up                    up      
Ethernet0/3                100.10.0.2      YES NVRAM  up                    up      
Ethernet0/3.11             unassigned      YES unset  administratively down down    
Ethernet0/3.111            unassigned      YES unset  administratively down down    
Ethernet1/0                200.20.0.2      YES NVRAM  up                    up      
Ethernet1/1                10.0.2.9        YES NVRAM  up                    up      
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  21.21.21.21     YES NVRAM  up                    up      
R21#sh ip ospf nei
R21#sh ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
1.1.1.1           1   FULL/BDR        00:00:38    34.0.0.1        Ethernet0/1
22.22.22.22       1   FULL/BDR        00:00:32    32.0.0.1        Ethernet0/2
2.2.2.2           1   FULL/BDR        00:00:38    31.0.0.1        Ethernet0/0
22.22.22.22       1   FULL/DR         00:00:38    200.20.0.1      Ethernet1/0
22.22.22.22       1   FULL/DR         00:00:35    100.10.0.1      Ethernet0/3
R21#sh vrrp
Ethernet0/3 - Group 1  
  State is Backup  
  Virtual IP address is 100.10.0.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 100 
  Master Router is 100.10.0.1, priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.609 sec (expires in 2.776 sec)

Ethernet1/0 - Group 2  
  State is Backup  
  Virtual IP address is 200.20.0.1
  Virtual MAC address is 0000.5e00.0102
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 100 
  Master Router is 200.20.0.1, priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.609 sec (expires in 3.306 sec)
  ```
рабочая конфигурация R21:
```
interface Loopback0
 ip address 21.21.21.21 255.255.255.255
!
interface Ethernet0/0
 ip address 31.0.0.2 255.255.255.252
!
interface Ethernet0/1
 ip address 34.0.0.2 255.255.255.252
!
interface Ethernet0/2
 ip address 32.0.0.2 255.255.255.252
!
interface Ethernet0/3
 ip address 100.10.0.2 255.255.255.248
 vrrp 1 ip 100.10.0.1
!         
interface Ethernet0/3.11
 encapsulation dot1Q 11
 shutdown
!
interface Ethernet0/3.111
 encapsulation dot1Q 111
 shutdown
!
interface Ethernet1/0
 ip address 200.20.0.2 255.255.255.248
 vrrp 2 ip 200.20.0.1
!
interface Ethernet1/1
 ip address 10.0.2.9 255.255.255.0
!
interface Ethernet1/2
 no ip address
 shutdown
!
interface Ethernet1/3
 no ip address
 shutdown
 !         
router ospf 1
 router-id 21.21.21.21
 area 4 stub
 network 21.21.21.21 0.0.0.0 area 0
 network 31.0.0.0 0.0.0.3 area 0
 network 32.0.0.0 0.0.0.3 area 0
 network 34.0.0.0 0.0.0.3 area 0
 network 100.10.0.0 0.0.0.7 area 4
 network 200.20.0.0 0.0.0.7 area 4
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
snmp-server community public RW
!
!
!
!
control-plane
!
!
!
!
!
!
!
!
line con 0
 logging synchronous
line aux 0
line vty 0 4
 privilege level 15
 transport input ssh
 ```
R22:
```
R22#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                33.0.0.2        YES NVRAM  up                    up      
Ethernet0/1                35.0.0.2        YES NVRAM  up                    up      
Ethernet0/2                32.0.0.1        YES NVRAM  up                    up      
Ethernet0/3                100.10.0.1      YES NVRAM  up                    up      
Ethernet0/3.11             unassigned      YES unset  up                    up      
Ethernet0/3.111            unassigned      YES unset  up                    up      
Ethernet1/0                200.20.0.1      YES NVRAM  up                    up      
Ethernet1/1                10.0.2.5        YES NVRAM  up                    up      
Ethernet1/2                unassigned      YES NVRAM  administratively down down    
Ethernet1/3                unassigned      YES NVRAM  administratively down down    
Loopback0                  22.22.22.22     YES NVRAM  up                    up      
R22#sh ip ospf nei

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           1   FULL/BDR        00:00:39    35.0.0.1        Ethernet0/1
1.1.1.1           1   FULL/BDR        00:00:30    33.0.0.1        Ethernet0/0
21.21.21.21       1   FULL/DR         00:00:35    32.0.0.2        Ethernet0/2
21.21.21.21       1   FULL/BDR        00:00:31    200.20.0.2      Ethernet1/0
21.21.21.21       1   FULL/BDR        00:00:38    100.10.0.2      Ethernet0/3
R22#sh vrrp
Ethernet0/3 - Group 1  
  State is Master  
  Virtual IP address is 100.10.0.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 255 
  Master Router is 100.10.0.1 (local), priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.003 sec

Ethernet1/0 - Group 2  
  State is Master  
  Virtual IP address is 200.20.0.1
  Virtual MAC address is 0000.5e00.0102
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 255 
  Master Router is 200.20.0.1 (local), priority is 255 
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.003 sec
  
  ```
рабочая конфигурация R22:
```
interface Loopback0
 ip address 22.22.22.22 255.255.255.255
!
interface Ethernet0/0
 ip address 33.0.0.2 255.255.255.252
!
interface Ethernet0/1
 ip address 35.0.0.2 255.255.255.252
!
interface Ethernet0/2
 ip address 32.0.0.1 255.255.255.252
!
interface Ethernet0/3
 ip address 100.10.0.1 255.255.255.248
 vrrp 1 ip 100.10.0.1
!
interface Ethernet0/3.11
 encapsulation dot1Q 11
!
interface Ethernet0/3.111
 encapsulation dot1Q 111
!
interface Ethernet1/0
 ip address 200.20.0.1 255.255.255.248
 vrrp 2 ip 200.20.0.1
!
interface Ethernet1/1
 ip address 10.0.2.5 255.255.255.0
!
interface Ethernet1/2
 no ip address
 shutdown
!
interface Ethernet1/3
 no ip address
 shutdown
!
router ospf 1
 router-id 22.22.22.22
 area 4 stub
 network 22.22.22.22 0.0.0.0 area 0
 network 32.0.0.0 0.0.0.3 area 0
 network 33.0.0.0 0.0.0.3 area 0
 network 35.0.0.0 0.0.0.3 area 0
 network 100.10.0.0 0.0.0.7 area 4
 network 200.20.0.0 0.0.0.7 area 4
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!         
!
snmp-server community public RW
!
```
проверка связи ПК LAN С BD:
```
LAN> sh ip

NAME        : LAN[1]
IP/MASK     : 200.20.0.4/29
GATEWAY     : 200.20.0.1
DNS         : 
MAC         : 00:50:79:66:68:1d
LPORT       : 20000
RHOST:PORT  : 127.0.0.1:30000
MTU         : 1500

LAN> ping 200.0.0.2

84 bytes from 200.0.0.2 icmp_seq=1 ttl=61 time=6.931 ms
84 bytes from 200.0.0.2 icmp_seq=2 ttl=61 time=14.286 ms
84 bytes from 200.0.0.2 icmp_seq=3 ttl=61 time=6.024 ms
84 bytes from 200.0.0.2 icmp_seq=4 ttl=61 time=45.268 ms
84 bytes from 200.0.0.2 icmp_seq=5 ttl=61 time=4.043 ms
LAN> trace 200.0.0.2
trace to 200.0.0.2, 8 hops max, press Ctrl+C to stop
 1   200.20.0.1   5.165 ms  2.857 ms  6.074 ms
 2   33.0.0.1   5.679 ms  4.880 ms  4.392 ms
 3   15.0.0.2   16.046 ms  6.970 ms  8.973 ms
 4   *200.0.0.2   9.061 ms (ICMP type:3, code:3, Destination port unreachable
```
проверка связи VOIP с Asterisk
```
VOIP> sh ip

NAME        : VOIP[1]
IP/MASK     : 100.10.0.4/29
GATEWAY     : 100.10.0.1
DNS         : 
MAC         : 00:50:79:66:68:1c
LPORT       : 20000
RHOST:PORT  : 127.0.0.1:30000
MTU         : 1500

VOIP> ping 100.0.0.1

84 bytes from 100.0.0.1 icmp_seq=1 ttl=252 time=8.215 ms
84 bytes from 100.0.0.1 icmp_seq=2 ttl=252 time=38.825 ms
84 bytes from 100.0.0.1 icmp_seq=3 ttl=252 time=20.452 ms
84 bytes from 100.0.0.1 icmp_seq=4 ttl=252 time=5.279 ms
84 bytes from 100.0.0.1 icmp_seq=5 ttl=252 time=5.203 ms

VOIP> trace 100.0.0.1
trace to 100.0.0.1, 8 hops max, press Ctrl+C to stop
 1   100.10.0.1   4.119 ms  5.108 ms  4.927 ms
 2   33.0.0.1   5.258 ms  5.368 ms  9.677 ms
 3   15.0.0.2   6.860 ms  6.513 ms  8.951 ms
 4   *22.0.0.1   9.329 ms (ICMP type:3, code:3, Destination port unreachable)  
 
 ```

## 2. Разобраться  и интегрировать сервис Netbox в существующую сеть

В качестве дистрибутива был выбран Ubuntu server 24.04. был установлен docker.
Netbox собирался согласно инструкции на официальном сайте: https://netboxlabs.com/docs/netbox/en/stable/installation/
Netbox представляет из себя большую БД C APi на доступ к ней,но к сожелению не имеет ни каких встроенных средств для автоматизации заполнения.
Так как узлов в сети было много, а руками заполнять не хотелось мой выбор пал на сервис device auto-discovery SlurpIT.
Я собирал SlurpIT по средствам docker compose.Для того чтобы залогигится в окне аутентификации SLurpIT после деплоя, надо конектится ровно к той строке адреса которая указана в docker-compose.yaml(В моём случае http://localhost:81(при попытке набрать http://127.0.0.1:81 я не мог пройти аутентификацию!!!!))
SlurpIT определяет доступность устройства в сети по средствам доступа по 22порту(ssh), собирает информацию о нем по snmp.
Для того что бы SlurpIT передавал информацию в Netbox нужно сопрячь их.Чтобы это сделать необходимо установить модуль Slurpit в Netbox.

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/slurpit.jpg)

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/netbox_slurpit_int.jpg)

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/netbox_devices.jpg)

Для того что бы созданная сети была наглядной в Netbox,установил модуль topology-view

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/netbox_topology.jpg)

## 3. Организовать мониторинг сети на базе Zabbix
В качестве дистрибутива был выбран Ubuntu server 24.04. был установлен docker последней версии.
скачал и установил следующий репозиторий: https://github.com/zabbix/zabbix-docker 
добавил все устройства в мониторинг по SNMP

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/zabbix.jpg)

![alt text](https://github.com/vk1391/OTUS_NE_DPLM/blob/main/zabbix2.jpg)


