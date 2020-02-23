import requests as req
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import random
import matplotlib.pyplot as plt
import os
import re
import fake_useragent
from fake_useragent import UserAgent
from lxml import etree

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

main_path='/home/database/data'
IP_path = '/home/database/data/IPData'


class getIPTool():
    '''
    get xxx net IP
    '''
    IPPool = []

    def __init__(self):
        self.getIP()

    def getIP(self):

        ip_dir = IP_path + '/ipPool_' + time.strftime('%Y%m%d') + '.txt'
        if os.path.exists(ip_dir + '.txt'):
            with open(ip_dir + '.txt') as f:
                for i in f.readlines():
                    self.IPPool.append(i.strip('\n'))
                print("IP库已经是最新并且已经加载成功！")
        else:
            print('IP库已近过期，刷新中......')
            self.xici_IP()
            self.ip_891()
            self.list_write_to_txt(self.IPPool, ip_dir)
            print('IP库刷新完成，可用IP：%d个' % len(self.IPPool))

    def list_write_to_txt(self, List, dir_fileName):
        '''
        传进 一个列表，然后以追加的方式将列表中中的信息写入TXT文件
        '''
        if dir_fileName.find('.txt'):
            dir_fileName = dir_fileName + '.txt'
        if not os.path.exists(dir_fileName):
            f = open(dir_fileName, 'w')
            f.close()
        with open(dir_fileName, 'a') as f:
            for i in List:
                print('*', end='')
                f.write(str(i) + '\n')

    def verify_ip(self, ip, port):

        proxies = {
            'http': 'https://' + str(ip) + ':' + str(port)
        }
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        url = 'https://www.baidu.com'
        try:
            ip_response = req.get(url, proxies=proxies, headers=header, timeout=5)
        except:
            print('代理IP超时不可用!')
            return False
        # print(type(ip_response.status_code))
        # print(ip_response.status_code)
        if ip_response.status_code == 200:
            print('\r IP可用:%s' % ip, end='')
            return True
        else:
            print('代理IP无法访问')
            return False

    def deal_tr(self, tag_tr):
        IPPool = []
        if len(tag_tr) <= 0:
            print('页面IP信息为空，获取IP失败。')
            return self.IPPool
        for tr in tag_tr:
            ip_info = {
                'ip1': '',
                'port2': '',
                'location3': '',
                'type5': '',
                'speed6': '',
                'link_time7': '',
                'live_time8': '',
                'verify_time9': ''
            }
            ip_td = tr.find_all('td')
            if len(ip_td) == 10:
                try:
                    re_panter = r'<div class="bar" title="(.*)秒">'
                    # print(ip_td[9].text.strip())
                    ip_info['ip1'] = ip_td[1].contents[0]
                    ip_info['port2'] = tr.find_all('td')[2].contents[0]
                    ip_info['location3'] = ip_td[3].select('a')[0].text.strip()
                    ip_info['type5'] = tr.find_all('td')[5].contents[0]
                    ip_info['speed6'] = re.match(re_panter, str(ip_td[6].find_all('div', class_='bar')[0])).group(1)
                    ip_info['link_time7'] = re.match(re_panter, str(ip_td[7].find_all('div', class_='bar')[0])).group(1)
                    ip_info['live_time8'] = str(ip_td[8].text.split('分')[0])
                    ip_info['verify_time9'] = ip_td[9].text.strip()
                    if not self.verify_ip(ip_info['ip1'], ip_info['port2']):
                        print(ip_info['ip1'], 'IP不可用，舍弃！')
                        continue
                except Exception as e:
                    print(e)
                IPPool.append(ip_info)
        return IPPool

    def deal_891_tr(self, tag_tr):
        ip_pool = []
        if len(tag_tr) <= 0:
            print('页面IP信息为空，获取IP失败。')
            return ip_pool
        for tr in tag_tr:
            ip_info = {
                'ip1': '',
                'port2': '',
                'location3': '',
                'type5': '',
                'speed6': '',
                'link_time7': '',
                'live_time8': '',
                'verify_time9': ''
            }
            ip_td = tr.find_all('td')
            if len(ip_td) == 5:
                try:
                    # re_panter = r'<div class="bar" title="(.*)秒">'
                    # print(ip_td[9].text.strip())
                    ip_info['ip1'] = ip_td[0].text.strip()
                    ip_info['port2'] = ip_td[1].text.strip()
                    ip_info['location3'] = ip_td[2].text.strip()
                    # ip_info['speed6'] = re.match(re_panter, str(ip_td[6].find_all('div', class_='bar')[0])).group(1)
                    # ip_info['link_time7'] = re.match(re_panter, str(ip_td[7].find_all('div', class_='bar')[0])).group(1)
                    # ip_info['live_time8'] = str(ip_td[8].text.split('分')[0])
                    # ip_info['verify_time9'] = ip_td[9].text.strip()
                    # if float(ip_info['speed6']) > 0.5:
                    #     print(ip_info['ip1'], 'IP延时较长，舍弃！')
                    #     continue
                    if not self.verify_ip(ip_info['ip1'], ip_info['port2']):
                        print(ip_info['ip1'], 'IP不可用，舍弃！')
                        continue
                    # print(ip_info)
                    ip_pool.append(ip_info)
                except Exception as e:
                    print(e)
        return ip_pool

    def xici_IP(self):
        ip_url_list = ['https://www.xicidaili.com/nn/', 'https://www.xicidaili.com/nt/', \
                       'https://www.xicidaili.com/wn/']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        page_num = 5
        for ip_url in ip_url_list:
            for i in range(page_num):
                if i == 0:
                    continue
                url = ip_url + '/' + str(i)
                try:
                    ip_response = req.get(url, headers=headers).text
                    ip_soup = BeautifulSoup(ip_response, 'lxml')
                    tag_tr = ip_soup.find_all('tr')
                    self.IPPool += (self.deal_tr(tag_tr=tag_tr))
                except:
                    print(url, '无法访问')
                time.sleep(3)
                # print(len(IPPool))

    def ip_891(self):
        ip_url_list = ['http://www.89ip.cn/index.html']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        # IPPool = []
        page_num = 5
        for ip_url in ip_url_list:
            for i in range(page_num):
                if i == 0:
                    continue
                url = 'http://www.89ip.cn/index_' + str(i) + '.html'
                try:
                    ip_response = req.get(url, headers=headers).text
                    ip_soup = BeautifulSoup(ip_response, 'lxml')
                    tag_tr = ip_soup.find_all('tr')
                    self.IPPool += (self.deal_891_tr(tag_tr=tag_tr))
                    # print('*****')
                    # print(self.IPPool)
                except:
                    print(url, '无法访问')
                time.sleep(3)

    def random_ip(self):
        ip = random.choice(self.IPPool)
        print(' 获取随机IP地址：%s' % ip['ip1'])
        return ip


class getBeikeData(UserAgent):
    '''
    获取各个网站的房价信息
    '''
    beike_citys_urls_list = []
    beike_regions_urls_list = []
    beike_regions_urls_err1 = []

    def __init__(self, IPPool):
        self.IPPool = IPPool
        self.city_url_init()
        self.region_url_init(self.beike_citys_urls_list)
        # self.getRegion_URL(self.beike_citys_urls_list)

    def city_url_init(self):
        '''定期刷新IP地址'''
        city_url_dir = r'F:\python\housePrice\data\city_url_' + time.strftime('%Y%m%d')
        if os.path.exists(city_url_dir + '.txt'):
            with open(city_url_dir + '.txt') as f:
                for i in f.readlines():
                    self.beike_citys_urls_list.append(i.strip('\n'))
                print("城市地址已经存在库已经是最新并且已经加载成功！")
        else:
            print('城市地址已近过期，刷新中......')
            self.getCity_URL()
            self.list_write_to_txt(self.beike_citys_urls_list, city_url_dir)
            print('城市地址刷新成功：%d个城市地址' % len(self.beike_citys_urls_list))

    def region_url_init(self, url_list):
        '''刷区域URL'''
        city_region_url_dir = main_path + 'houseData/city_region_url_' + time.strftime('%Y%m%d')
        if os.path.exists(city_region_url_dir + '.txt'):
            with open(city_region_url_dir + '.txt') as f:
                for i in f.readlines():
                    self.beike_regions_urls_list.append(i.strip('\n'))
                print("城市区域地址已经存在库已经是最新并且已经加载成功！")
        else:
            print('城市区域地址已近过期，刷新中......')
            self.getRegion_URL(url_list)
            self.list_write_to_txt(self.beike_regions_urls_list, city_region_url_dir)
            print('城市地址刷新成功：%d个城市地址' % len(self.beike_regions_urls_list))

    def list_write_to_txt(self, List, dir_fileName):
        '''
        传进 一个列表，然后以追加的方式将列表中中的信息写入TXT文件
        '''
        if dir_fileName.find('.txt'):
            dir_fileName = dir_fileName + '.txt'
        if not os.path.exists(dir_fileName):
            f = open(dir_fileName, 'w')
            f.close()
        with open(dir_fileName, 'a') as f:
            for i in List:
                print('*', end='')
                f.write(str(i) + '\n')

    def random_ip_proxies(self):
        if len(self.IPPool) != 0:
            rand_IP_info = eval(random.choice(self.IPPool))
            # print(rand_IP_info['ip1'])
            proxies = {
                'http': 'https://' + str(rand_IP_info['ip1']) + ':' + str(rand_IP_info['port2'])
            }
            return proxies
        else:
            return False

    def getCity_URL(self):
        beike_url = 'https://www.ke.com/city/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        # header = {'User-Agent': UserAgent().random}
        try:
            beike_citys_response = req.get(beike_url, proxies=self.random_ip_proxies(), headers=header, timeout=5)
            beike_citys_soup = BeautifulSoup(beike_citys_response.text, 'lxml')
            provience_city_list = beike_citys_soup.find_all('ul', class_='city_list_ul')[0].find_all('div',
                                                                                                     class_='city_province')
            for i in provience_city_list:
                i_provience_name = i.find_all('div', class_='city_list_tit c_b')[0].text.strip()
                for city in i.find_all('a'):
                    self.beike_citys_urls_list.append(
                        i_provience_name + '-' + city.text.strip() + '#' + 'https:' + city['href'])
        except:
            print('获取贝壳城市名称与URL失败!')

    def getRegion_URL(self, citys_url_list):
        '''
        获取每个城市城市在售二手房数量，城市每个区的名称和URL！
        :param citys_url_list: 传入城市名称与URL信息，列表形式；每个元素格式如：安徽-合肥#https://hf.ke.com
        :return: city_ershoufang_num,city_region_nameUrl_list
        '''
        if len(citys_url_list) <= 0:
            print('传入的城市名称与URL信息列表为空,getRegion_url')
            return False

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        for city_name_url in citys_url_list:
            city_url = city_name_url.split('#')[1]
            print(city_url)
            city_name = city_name_url.split('#')[0]
            print(city_name)
            rand_proxies = self.random_ip_proxies()
            print(rand_proxies)
            try:
                print(city_url + '/ershoufang/')
                citys_region_url_response = req.get(city_url + '/ershoufang/', proxies=rand_proxies, headers=header,
                                                    timeout=5)
                citys_region_soup = BeautifulSoup(citys_region_url_response.text, 'lxml')
                region_info_list = citys_region_soup.find_all('div', class_='position')[0].find_all('a',
                                                                                                    class_=' CLICKDATA')
                if len(region_info_list) <= 0:
                    print('解析城市区域名称与URL失败', city_name)
                    continue
                for region_info in region_info_list:
                    region_name = city_name + '-' + region_info.text
                    region_url = city_url + region_info['href']
                    print('\r' + region_name + '#' + region_url, end='')
                    self.beike_regions_urls_list.append(region_name + '#' + region_url)
            except Exception as e:
                print(e)
                print('出错，位置在：getRegionUrl:', city_name)
                self.beike_regions_urls_err1.append(city_name_url)
                continue

    def get_sell_url_list(self, page_url):
        '''
        返回每一页面的房屋的url信息
        page_url:传入每一个页面的URL
        '''
        proxies = self.random_ip_proxies()
        # print(proxies)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        try:
            region_er_house_info_response = req.get(page_url, proxies=proxies, headers=header,
                                                    timeout=5)
            # print(region_er_house_info_response.status_code)
            region_er_house_info_soup = BeautifulSoup(region_er_house_info_response.text, 'lxml')
            sell_list_soup = region_er_house_info_soup.select('ul.sellListContent')[0].select('div.title > a.VIEWDATA')
            # print(len(sell_list_soup))
            sell_url_list = [sell_soup.get('href') for sell_soup in sell_list_soup]
            # print(sell_url_list)
            return sell_url_list
        except:
            print('获取页面房屋URL list失败，位置，url_list,URL:%s' % page_url)
            return False

    def get_house_url_list(self, region_name_url):
        '''
        region_name_url:包含区域名字和城市url的字符串并以‘#’作为分割符，如：‘安徽-合肥-包河#https://hf.ke.com/ershoufang/baohe/’
        '''
        region_name = region_name_url.split('#')[0]
        region_url = region_name_url.split('#')[1]
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }
        proxies = self.random_ip_proxies()
        # print(proxies)

        # 以下代码为获取一个区域的二手房屋页面总数
        try:
            region_er_house_info_response = req.get(region_url, proxies=proxies, headers=header,
                                                    timeout=5)
            if region_er_house_info_response.status_code != 200:
                print('页面状态码错误，位置在get_house_url_list,URL:%s' % region_name_url)
                return False
            region_er_house_info_soup = BeautifulSoup(region_er_house_info_response.text, 'lxml')
        except:
            print('\r获取页面源码错误，url：%s' % region_name_url)
            return False
        try:
            total_page = region_er_house_info_soup.find_all(class_='page-box')[0]
            total_page_re = r'"totalPage":(.*),"curPage"'
            total_num = re.search(total_page_re, str(total_page)).group(1)
            page_num = int(total_num)
            print(page_num)
        except:
            print('\r获取页面总页码错误，错误在：%s' % region_name_url)
            return False

        # 以下代码为获取每一个区域页面的url,并返回url lsit
        if page_num <= 0:
            print('获取页面总数是小于0！')
            return False
        sell_list = []
        for i in range(page_num + 1):
            if i == 0:
                continue
            url = region_url + 'pg' + str(i) + '/'
            # print('\r' + url,end='')
            url_list = self.get_sell_url_list(url)
            if url_list:
                sell_list += [region_name + '#' + i for i in url_list]
                print('*', end='')
                if i % 20 == 0:
                    print('*')
            else:
                print('获取页面list失败')
            time.sleep(1.5)
        print(region_name)
        return sell_list

    def get_house_info(self, url):
        """
        获取某一正在出售房屋的详细信息
        url：具体值某一正在出售房屋的详细地址
        :return: house_info_dic  ,以字典方式返回房屋的详细的出售信息
        """
        house_info_dic = {
            '省市': '',
            'title': '',
            '小区': '',
            '区域': '',
            '贝壳编号': '',
            '总价': '',
            '单价': '',
            '房屋户型': '',
            '建筑面积': '',
            '建筑类型': '',
            '建筑结构': '',
            '梯户比例': '',
            '配备电梯': '',
            '所在楼层': '',
            '户型结构': '',
            '房屋朝向': '',
            '装修情况': '',
            '供暖方式': '',
            '产权年限': '',
            '挂牌时间': '',
            '上次交易': '',
            '房屋年限': '',
            '抵押信息': '',
            '交易权属': '',
            '房屋用途': '',
            '产权所属': '',
            '房本备件': '',
            'houseurl': ''
        }

        proxies = self.random_ip_proxies()
        if proxies == False:
            return False
        print(proxies)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
                                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', }

        try:
            house_info_response = req.get(url.split('#')[1].strip(), proxies=proxies, headers=header,
                                          timeout=5)
            # print(house_info_response.text)
        except Exception as e:
            print(e)
            print('出现错误,获取房屋页面出错，位置在:house_info_response，url地址%s' % url)
            return False

        house_info_html = etree.HTML(house_info_response.text)
        house_info_dic['houseurl'] = url.split('#')[1]
        house_info_dic['省市'] = url.split('#')[0]
        try:
            house_info_dic['title'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[2]/div[2]/div/div/div[1]/h1/text()')[0].strip()
        except:
            house_info_dic['title'] = ''
        try:
            house_info_dic['小区'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[4]/div/div[2]/div[3]/div[1]/a[1]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['区域'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[4]/div/div[2]/div[3]/div[2]/span[2]/a[1]/text()')[
                    0].strip()
        except:
            pass
        try:
            house_info_dic['贝壳编号'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[4]/div/div[2]/div[3]/div[4]/span[2]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['总价'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[4]/div/div[2]/div[1]/span[1]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['单价'] = \
                house_info_html.xpath('//*[@id="beike"]/div/div[4]/div/div[2]/div[1]/div[1]/div[1]/span/text()')[
                    0].strip()
        except:
            pass
        try:
            house_info_dic['房屋户型'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['建筑面积'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['建筑类型'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['建筑结构'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[7]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['梯户比例'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['配备电梯'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['所在楼层'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['户型结构'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[4]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['房屋朝向'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[6]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['供暖方式'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[10]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['产权年限'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[12]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['挂牌时间'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['上次交易'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['房屋年限'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['抵押信息'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()')[
                    0].strip()
        except:
            pass
        try:
            house_info_dic['交易权属'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['房屋用途'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['产权所属'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[6]/text()')[0].strip()
        except:
            pass
        try:
            house_info_dic['房本备件'] = \
                house_info_html.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[8]/text()')[0].strip()
        except:
            pass
        print('\r', house_info_dic)
        return house_info_dic

    def get_sell_url_list_from_file(self, city_name):
        """
        传入城市名称，获取某一个城市的房价详细信息
        """
        url_list = []
        if city_name == '':
            print('请输入城市名称：')
            return False
        sellURLList = main_path + 'houseData/sellUrlList.txt'
        with open(sellURLList)  as f:
            for i in f.readlines():
                if i.find(city_name) != -1:
                    url_list.append(i)
                    print(i)
        return url_list

    def get_all_house_info(self,house_info_url_list):
        """
        传入房屋信息url地址，返回房屋信息list

        """
        if len(house_info_url_list) <= 0:
            print('房屋url信息错误')
            return False
        info_list = []
        for url in house_info_url_list:
            info = self.get_house_info(url)
            if info:
                info_list.append(info)
            else:
                continue
            time.sleep(1)
        return info_list



class dataDeal():
    '''
    集成各类型的文件处理函数

    '''

    def __init__(self, dirPath):
        self.dirPath = dirPath

    def list_write_to_txt(self, List, dir_fileName):
        '''
        传进 一个列表，然后以追加的方式将列表中中的信息写入TXT文件
        '''
        if dir_fileName.find('.txt'):
            dir_fileName = dir_fileName + '.txt'
        if not os.path.exists(dir_fileName):
            f = open(dir_fileName, 'w')
            f.close()
        with open(dir_fileName, 'a') as f:
            for i in List:
                print('*', end='')
                f.write(str(i) + '\n')

    def write_df_to_DBase(self, path, filename, info_list):
        """
        :param path: 文件保存路径
        :param filename: 文件名称，名称后面会自动加上当前日期
        :param info_list: 要保存的list，list元素最好为字典类型
        :return:
        """
        DB_name = path + '\\' + filename + '-' + time.strftime('%Y%m%d %H%M%S ') + '.csv'
        if not os.path.exists(DB_name):
            f = open(DB_name, 'w')
            f.close()
            print('数据文件建立成功！')
        else:
            print('数据文件已经存在！')
        all_Price = pd.DataFrame(info_list)
        all_Price.to_csv(DB_name, encoding='utf-8-sig')
        print('数据写入成功')
        pass


def main():
    path = main_path +'/houseData'
    ip_tool = getIPTool()
    beike = getBeikeData(ip_tool.IPPool)
    data_deal = dataDeal(path)
    city_names = ['深圳', '武汉', '郑州', '广州']
    for city_name in city_names:
        sell_url_list = beike.get_sell_url_list_from_file(city_name=city_name)
        info_list = beike.get_all_house_info(sell_url_list)
        if len(info_list) <= 0:
            print('获取失败')
            continue
        try:
            data_deal.write_df_to_DBase(path=path, filename=city_name, info_list=info_list)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    today = time.time()
    main()
