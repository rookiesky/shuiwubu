from HttpPorxy import HttpPorxy
from bs4 import BeautifulSoup
import time
import re

http = HttpPorxy()
list_link = []
post_api = 'https://www.swubu.com/wordpress_post_api.php?action=save'


def getListLink(url):
    global list_link
    response = http.get(url=url)
    if response == False:
        return False

    soup = BeautifulSoup(response,'html.parser')
    urls = soup.find_all('p',attrs={'class','title'})
    list_link = [item.next.get('href') for item in urls]

def bodyFormat(soup,response):
    title = soup.find('h1').text
    create_time = soup.find('span',attrs={'class','publish-time'}).text
    create_rp = time.strptime(create_time,'%Y年%M月%d日')
    create_time = time.strftime('%Y-%M-%d %H:%m',create_rp)

    body = soup.find('div',attrs={'class','article-main'})
    try:
        body.find('div',attrs={'class','atta'}).extract()
    except:
        pass
    try:
        body.find('div',attrs={'class','article-share'}).extract()
    except:
        pass
    try:
        body.find('div',attrs={'style':'position:relative'}).extract()
    except:
        pass
    try:
        body.find(id='logindiv').extract()
    except:
        pass
    try:
        body.find(id='sudokuUpload').extract()
    except:
        pass
    try:
        body.find(id='discuss').extract()
    except:
        pass

    pattern = re.compile(r'<!--enpproperty(.*?)/enpproperty-->')
    body = re.sub(pattern,'',str(body))

    tags = ''
    try:
        tags = re.findall('<keyword>(.*?)</keyword>',response,re.S)[0]
    except:
        pass
    return {'post_title':title,'tag':tags,'post_date':create_time,'post_content':str(body)}


def body():
    global list_link
    for url in list_link:
        response = http.get(url=url)
        if response == False:
            continue

        soup = BeautifulSoup(response,'html.parser')
        try:
            data = bodyFormat(soup=soup,response=response)
            data['post_category'] = '法规解读'
            response = http.post(url=post_api,data=data)
            http.logger.info('success title:{},response:{}'.format(data['post_title'],response.strip()))
            data = None
        except Exception as e:
            http.logger.error('body format error,msg:{}'.format(e))
        soup = None
        time.sleep(1)
    list_link = []

def main():
    url = 'http://www.ctaxnews.com.cn/node_27.html'
    getListLink(url=url)
    if len(list_link) <= 0:
        http.logger.error('list link is empty')
        return False
    body()
    time.sleep(2)

main()