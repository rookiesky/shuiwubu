from Https import Https
import json
import math
from bs4 import BeautifulSoup
import time

request = Https(is_porxy=False)
list_url = []
post_api = 'https://www.swubu.com/wordpress_post_api.php?action=save'
error = 0
is_city_new = False
post_cate = ''


def bodyFormat(soup,url):
    title = soup.find('meta',attrs={'name':'ArticleTitle'}).get('content')
    if is_city_new == False:
        keyword = soup.find('meta',attrs={'name':'ColumnName'}).get('content')
    else:
        if '：' in title:
            keyword = title[0:title.find('：')]
        elif '市' in title:
            keyword = title[0:title.find('市') + 1]
        elif '省' in title:
            keyword = title[0:title.find('省') + 1]
        else:
            keyword = ''

    create_date = soup.find('meta',attrs={'name':'PubDate'}).get('content')
    content = soup.find(id='fontzoom')
    try:
        content.find(id='tk-container-2020').extract()
    except:
        pass
    try:
        content.find('div',attrs={'class','jiuc'}).extract()
    except:
        pass
    try:
        content.find('script').extract()
    except:
        pass
    try:
        content.find('style').extract()
    except:
        pass
    try:
        for item in content.find_all('a'):
            item.attrs['href'] = url.replace('content.html',item.get('href'))
    except:
        pass
    try:
        for item in content.find_all('img'):
            item.attrs['src'] = url.replace('content.html',item.get('src'))
    except:
        pass
    
    return {'post_title':title,'tag':keyword,'post_date':create_date,'post_content':str(content)}

def body():
    global list_url
    for url in list_url:
        response = request.get(url)
        if response == False:
            continue

        soup = BeautifulSoup(response,'html.parser')
        try:
            data = bodyFormat(soup,url)
            data['post_category'] = post_cate
            request.post(url=post_api,data=data)
            request.logger.info('Success,title:{}'.format(data['post_title']))
        except Exception as e:
            request.logger.error('body formay error,msg:{}'.format(e))
        soup = ''
        response = ''
        time.sleep(1)
    list_url = []

def getListLink(url,page):
    global page_total_number, list_url, error
    headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Cookie": "_Jo0OQK=3B42EE9F2EFD498DDE7E5B8634810542CE338D6790E6341D22F46FB9B97F3477CD0D9303E585EA92085BB616961315CF167C7E9FEA577C612EB683018C078B9517E01C83797AB67C7627EF4EAE0C6A2C5647EF4EAE0C6A2C56491A0E8A83004FA3FGJ1Z1ag==; CPS_SESSION=97702068E9758A2956FA1292C56AEF64",
                }
    data = {
        'timeOption' : 0,
        'page' : page,
        'pageSize' : 10,
        'keyPlace' : 1,
        'sort' : 'dateDesc',
        'qt': '*'
    }
    response = request.post(url,data=data,header=headers)
    if response == False:
        return False
    try:
        result = json.loads(response)
        if len(result['resultList']) <= 0:
            request.logger.info('resultList is empty')
            return False
        list_url = {item['url'] for item in result['resultList']}
    except Exception as e:
        request.logger.error('json loads error msg:{}'.format(e))
        if error > 3:
            return False
        error = error + 1
        time.sleep(5)
        return getListLink(url,page)

def zhengce():
    global page_temp_number,error,is_city_new,post_cate
    is_city_new = False
    post_cate = '税收政策库'
    url = 'http://www.chinatax.gov.cn/api/query?siteCode=bm29000fgk&tab=all&key=9A9C42392D397C5CA6C1BF07E2E0AA6F'

    error = 0
    result = getListLink(url,page = 1)
    if result == False:
        return False
    if len(list_url) <= 0:
        request.logger.error('list url empty')
        return False
    body()
    request.logger.info('success cate:{}'.format(post_cate))


def getNew(url):
    global list_url
    response = request.get(url)
    if response == False:
        exit()
    soup = BeautifulSoup(response,'html.parser')
    ul = soup.find('ul',attrs={'class','list'})
    list_url = [item.get('href') for item in ul.find_all('a')]

def newNews():
    global is_city_new,post_cate
    is_city_new = True
    urls = {
        '全国税务动态':'http://www.chinatax.gov.cn/chinatax/manuscriptList/n810739?_isAgg=0&_pageSize=20&_template=index&_channelName=%E5%90%84%E5%9C%B0%E5%8A%A8%E6%80%81&_keyWH=wenhao&page=1',
        '税务新闻':'http://www.chinatax.gov.cn/chinatax/manuscriptList/n810780?_isAgg=0&_pageSize=20&_template=index&_channelName=%E5%AA%92%E4%BD%93%E8%A7%86%E7%82%B9&_keyWH=wenhao&page=1'
    }
    for key,url in urls.items():
        post_cate = key
        getNew(url)
        if len(list_url) <= 0 :
            request.logger.info('list url empty')
            continue
        body()
        request.logger.info('success cate:{}'.format(post_cate))

def news():
    global is_city_new,post_cate
    is_city_new = True
    for i in range(50,202):
        # url = 'http://www.chinatax.gov.cn/chinatax/manuscriptList/n810739?_isAgg=0&_pageSize=20&_template=index&_channelName=%E5%90%84%E5%9C%B0%E5%8A%A8%E6%80%81&_keyWH=wenhao&page={}'.format(i)
        url = 'http://www.chinatax.gov.cn/chinatax/manuscriptList/n810780?_isAgg=0&_pageSize=20&_template=index&_channelName=%E5%AA%92%E4%BD%93%E8%A7%86%E7%82%B9&_keyWH=wenhao&page={}'.format(i)
        getNew(url)
        if len(list_url) <= 0 :
            request.logger.info('list url empty')
            continue
        body()
        request.logger.info('success page:{}'.format(i))

def main():
    try:
        zhengce()
    except:
        pass
    try:
       newNews()
    except:
        pass 

main()