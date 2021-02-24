import requests
import logging
import json
import random
from datetime import datetime, timedelta

class Https():
    porxy_ips = []
    is_porxy = False
    get_porxy_date = None
    porxy_ips_total = 0
    porxy_now_ip_number = 0

    def __init__(self,is_porxy = False):
        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)
        self.logger = logging
        self.is_porxy = is_porxy
        if self.is_porxy == True:
            self.get_porxy_date = datetime.now()
            self.getPorxy()

    def userAgent(self):
        ua = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/87.0.4280.88 Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
            'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
            'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62'
        ]
        return random.choice(ua)
    
    def nowPorxyIp(self):
        porxy = {}
        if self.is_porxy == False:
            return porxy
        if self.porxy_now_ip_number >= (self.porxy_ips_total - 1):
            self.porxy_now_ip_number = 0
            now_date = datetime.now()
            is_exp = now_date - slef.get_porxy_date > timedelta(minutes=15)
            if is_exp:
                self.getPorxy()
        porxy = self.porxy_ips[self.porxy_now_ip_number]
        self.porxy_now_ip_number = self.porxy_now_ip_number + 1
        return porxy


    def httpHeader(self,header):
        head = {'user-agent': self.userAgent()}
        header = {**head,**header}
        return {'porxies':self.nowPorxyIp(),'header':header}
        

    def get(self,url,header={}):
        '''http get请求
        Parameters
        -------------------
        url : string 请求链接
        header : dict 请求header

        Returns
        -------------------
        string
        '''
        header = self.httpHeader(header=header)
        try:
            response = requests.get(url=url, headers = header['header'], proxies = header['porxies'], timeout = 120)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            self.logger.error('http get error,msg:{}'.format(e))
        finally:
            try:
                response.close()
            except:
                pass

    def post(self,url,data,header = {}):
        '''http post请求
        Parameters
        ----------------
        url : string 请求接口
        data : dict  请求数据
        header : http header

        RETURNS
        ---------------
        string response
        '''
        header = self.httpHeader(header=header)
        try:
            response = requests.post(url=url,data=data, headers = header['header'], proxies = header['porxies'], timeout = 120)
            return response.text
        except Exception as e:
            self.logger.error('http post error,msg:{}'.format(e))
        finally:
            try:
                response.close()
            except:
                pass

    def postJson(self,url,json,header = {}):
        '''http post json请求
        Parameters
        ----------------
        url : string 请求接口
        json : dict  请求数据

        RETURNS
        ---------------
        string response
        '''
        header = self.httpHeader(header=header)
        try:
            response = requests.post(url=url,json=json,headers = header['header'], proxies = header['porxies'], timeout = 120)
            return response.text
        except Exception as e:
            self.logger.error('post json error,msg:{}'.format(e))
        finally:
            try:
                response.close()
            except:
                pass  

    def getPorxyApi(self):
        '''请求代理ip接口或者代理ip
        RETURN:
            data = []
        '''
        try:
            response = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
            return response.text.split("\n")
        except Exception as e:
            self.logger.error('get porxy api error,msg:{}'.format(e))
            return False
    
    def checkPorxyIp(self,ip):
        '''检测代理ip是否可用
        RETURN:
            True 可用
            Flase 不可用
        '''
        try:
            response = requests.get('https://www.baidu.com', proxies=ip, timeout=5)
            if response.status_code > 302:
                return False
            return True
        except:
            return False
        finally:
            try:
                response.close()
            except:
                pass


    def getPorxy(self):
        '''获取代理ip
        '''
        ips = self.getPorxyApi()
        if ips == False:
            exit()
        
        for ip in ips:
            if ip == '':
                continue
            ip = json.loads(ip)
            porxy_host = {ip['type']:ip['type'] + '://' + ip['host'] + ':' + str(ip['port'])}
            check = self.checkPorxyIp(porxy_host)
            if check == False:
                continue
            self.porxy_ips.append(porxy_host)
            print(len(self.porxy_ips))
        
        if len(self.porxy_ips) <= 0:
            self.logger.error('get ips list empty')
            exit()
        
        self.porxy_ips_total = len(self.porxy_ips)

