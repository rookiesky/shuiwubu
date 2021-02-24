from HttpPorxy import HttpPorxy
import requests

# url = 'https://forge.speedtest.cn/api/location/info?z=76498694'
# proxies = {'https': 'http://163.172.93.129:3128'}
# response = requests.get(url,proxies=proxies)
# print(response.text)

# http = HttpPorxy(is_porxy=True)

# response = http.get('https://forge.speedtest.cn/api/location/info?z=76498694')
# print(response)

# response = http.get('https://ipv4.appspot.com/')
# print(response)

# response = http.get('http://myip.ipip.net/')
# print(response)

urls = {
        '法规解读':'https://www.shui5.cn/article/FaGuiJieDu/',
        '地方法规':'https://www.shui5.cn/article/DiFangCaiShuiFaGui/',
        '税务问答':'https://www.shui5.cn/article/ShuiWuWenDa/',
        '纳税评估': 'https://www.shui5.cn/article/NaShuiPingGu/'
    }

for key,item in urls.items():
    print(key,item)