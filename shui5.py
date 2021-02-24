from HttpPorxy import HttpPorxy
from bs4 import BeautifulSoup
from w3lib import html
import time

http = HttpPorxy(is_porxy=False)
list_link = []
post_api = 'https://www.swubu.com/wordpress_post_api.php?action=save'
post_cate = ''

def getLinks(url):
    global list_link
    response = http.get(url)

    if response == False:
        return False

    soup = BeautifulSoup(response,'html.parser')
    list_link = [item.next.get('href') for item in soup.find_all('div',attrs={'class','xwt1_a'})]

def bodyFormat(soup):
    post_title = soup.find('h1').text
    create_temp = soup.find('div',attrs={'class','articleResource'}).text
    create_date = create_temp[create_temp.find('时间：') + 3:]
    post_excerpt = soup.find('div',attrs={'class','articleDes'}).text
    body = soup.find('div',attrs={'class','arcContent'})
    try:
        for item in body.find_all('img'):
            if 'https://' not in item.get('src'):
                item.attrs['src'] = 'https://www.shui5.cn' + item.get('src')
    except:
        pass
    post_content = html.remove_tags(str(body),'a')
    return {'post_title':post_title,'post_date':create_date,'post_excerpt':post_excerpt,'post_content':post_content}

def body():
    global list_link, post_cate
    for url in list_link:
        response = http.get(url)
        if response == False:
            continue
        
        soup = BeautifulSoup(response,'html.parser')
        try:
            data = bodyFormat(soup)
            data['post_category'] = post_cate
            # http.is_porxy = False
            response = http.post(url=post_api,data=data)
            # http.is_porxy = True
            http.logger.info('post Success,title:{},response:{}'.format(data['post_title'],response))
        except Exception as e:
            http.logger.error('body format error,msg:{}'.format(e))
        
        soup = ''
        response = ''
        time.sleep(1)
    list_link = []

def boot():
    global post_cate
    urls = {
        '法规解读':'https://www.shui5.cn/article/FaGuiJieDu/',
        '地方法规':'https://www.shui5.cn/article/DiFangCaiShuiFaGui/',
        '税务问答':'https://www.shui5.cn/article/ShuiWuWenDa/',
        '纳税评估': 'https://www.shui5.cn/article/NaShuiPingGu/'
    }
    for key,item in urls.items():
        post_cate = key
        getLinks(item)
        if len(list_link) <= 0:
            continue
        body()
        http.logger.info('success page:{}'.format(i))
        time.sleep(2)

# def main():
#     for i in range(1,128):
#         # url = 'https://www.shui5.cn/article/FaGuiJieDu/12_{}.html'.format(i)
#         # url = 'https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_{}.html'.format(i)
#         # url = 'https://www.shui5.cn/article/ShuiWuWenDa/37_{}.html'.format(i)
#         url = 'https://www.shui5.cn/article/NaShuiPingGu/30_{}.html'.format(i)
#         getLinks(url)
#         if len(list_link) <= 0:
#             continue
#         body()
#         http.logger.info('success page:{}'.format(i))
#         time.sleep(2)

try:
    boot()
except:
    pass