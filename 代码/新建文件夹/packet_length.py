# -*- coding: utf-8 -*-
import math, decimal, hashlib, csv, uuid, time, os
import configparser
import scapy
from scapy.all import *
from scapy.utils import PcapReader

Client_IP = str
pcapname = '1.pcap'
web_sequence = {}


# 判断是否是TCP协议
def is_TCP_packet(pkt):
    try:
        pkt['IP']
    except:
        return False  # drop the packet which is not IP packet
    if "TCP" not in pkt:
        return False
    return True


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


def readpcap(webpage, pcapname):
    List = []
    length_list = []
    try:
        # It is possible that scapy can not read the pcap
        packets = rdpcap(pcapname)
    except Exception as e:
        print(" read {} ERROR:{} ".format(pcapname, e))
        exit(1)
    this_flow = None
    # 只取前100个数据包
    packets = packets[:100]
    for pkt in packets:
        if is_TCP_packet(pkt) == False:
            continue
        proto = "TCP"
        src, sport, dst, dport, updown = NormalizationSrcDst(pkt['IP'].src, pkt[proto].sport,
                                                             pkt['IP'].dst, pkt[proto].dport)
        List.append((src, sport, dst, dport))
        if src != '172.20.233.27':
            print("Client Error", src, sport, dst, dport)
            exit(1)
        length_list.append(updown * len(pkt))
        # hash_key = tuple2hash(src,sport,dst,dport,proto)
        # 输出包长度
        # print(pkt.__len__())
        # print(len(pkt))
    # for i in List:
    #     print(i)

    # print(len(List))
    print(length_list)
    web_sequence[webpage] = length_list


'''
获得文件夹下的文件夹名
'''


def get_dir_name(path):
    return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]


'''
获得文件夹下的文件名
'''


def get_file_name(path):
    return [i for i in os.listdir(path) if i.endswith('.pcap')]


'''
将list画成折线图
'''


def draw_line(dict):
    count = 0
    colors = ['green', 'red', 'skyblue', 'blue', 'black','#33CCCC','yellow']
    plt.xlabel('')
    plt.ylabel('')
    for i in dict:
        plt.plot(dict[i], color=colors[count], label=i)
        count = count + 1
    plt.show()

'''
将一个list中的负数全置为0
'''


def zero_neg(lst):
    return [0 if i < 0 else i for i in lst]


'''
输入一个list，输出一个list，其中每个元素是累加的值
'''


def sum_list(lst):
    return [sum(lst[:i + 1]) for i in range(len(lst))]


weblist = get_dir_name('testpcaps')
for web in weblist:
    temp = get_file_name('testpcaps/' + web + '/')[0]
    readpcap(web, 'testpcaps/' + web + '/' + temp)
print(web_sequence)
for web in web_sequence:
    web_sequence[web] = zero_neg(web_sequence[web])
    web_sequence[web] = sum_list(web_sequence[web])
    print(web, web_sequence[web])

draw_line(web_sequence)