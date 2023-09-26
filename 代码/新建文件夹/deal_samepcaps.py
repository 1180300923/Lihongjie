# -*- coding: utf-8 -*-
from scapy.all import *

total_valid_ip = []

'''
获得文件夹下的文件夹名
'''


def get_dir_name(path):
    return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]

# 判断是否是TCP协议
def is_TCP_packet(pkt):
    try:
        pkt['IP']
    except:
        return False  # drop the packet which is not IP packet
    if "TCP" not in pkt:
        return False
    return True

'''
获得文件夹下的文件名
'''
def get_file_name(path,str):
    return [i for i in os.listdir(path) if i.endswith(str)]

'''
读取文件的每一行，并打印a和list b ，格式是   a:['b','c'] 
'''
def read_file_line(file):
    global total_valid_ip
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.replace('\'','')
            line = line.split(':')
            print(line)
            line[1] = line[1].strip('[')
            line[1] = line[1].strip(']')
            print(line[1])
            ips = line[1].split(',')
            print(ips)
            # print(line[0])
            # print(line[1])
            # print(ips)
            if ('amazon.cn' in line[0] or 'amazon.com' in line[0]) and 'adsystem' not in line[0]:
                print(line[0])
                print(ips)
                total_valid_ip = total_valid_ip+ips
                print(total_valid_ip)

# 根据规则区分服务器和客户端
def NormalizationSrcDst(src, sport, dst, dport):
    if sport < dport:
        Client_IP = dst
        return (dst, dport, src, sport, -1)
    elif sport == dport:
        src_ip = "".join(src.split('.'))
        dst_ip = "".join(dst.split('.'))
        if int(src_ip) < int(dst_ip):
            Client_IP = dst
            return (dst, dport, src, sport, -1)
        else:
            Client_IP = src
            return (src, sport, dst, dport, 1)
    else:
        Client_IP = src
        return (src, sport, dst, dport, 1)

# 预处理pcap
def deal(filename):
    read_pkts = rdpcap(dir+filename)
    valid_pkts = []
    for pkt in read_pkts:
        if is_TCP_packet(pkt) == False:
            continue
        proto = "TCP"
        src, sport, dst, dport, updown = NormalizationSrcDst(pkt['IP'].src, pkt[proto].sport,
                                                             pkt['IP'].dst, pkt[proto].dport)

        if dst in total_valid_ip or src in total_valid_ip:
            valid_pkts.append(pkt)
    #  写入pcaps
    wrpcap(dir+filename, valid_pkts)
# 读取pcaps

dirs = get_dir_name('pcaps/')
for dir in dirs:
    dir = 'pcaps/'+dir+'/'
    dns_files = get_file_name(dir,'.txt')
    for temp in dns_files:
        print(temp)
        read_file_line(dir + temp)
    print(total_valid_ip)
    pcap_files = get_file_name(dir,'.pcap')
    for temp in pcap_files:
        print(temp)
        deal(temp)