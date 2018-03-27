import jieba as jieba
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import TouchActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import matplotlib.pyplot as plt

global search_name
search_name = input('请输入要查找的好友：')
mobile_emulation = {"deviceName":"Galaxy S5"}#模拟手机
option = webdriver.ChromeOptions()
option.add_experimental_option('mobileEmulation',mobile_emulation)
browser = webdriver.Chrome(chrome_options=option)
wait = WebDriverWait(browser,10)
def log_qkone():
    print('正在登录......')
    browser.get(r'https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&pt_ttype=1&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex')
    account = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#u')))#获取账号输入框
    passwd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#p')))#获取密码输入框
    go = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#go')))#获取登录按钮
    account.send_keys(ACCOUNT)
    passwd.send_keys(PW)
    go.click()
    search_friend()
    get_info()

def search_friend():
    print('正在查找...')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#feed_list_cot_all')))
    browser.get(
        'https://h5.qzone.qq.com/mqzone/jsp?starttime=1522070776838&hostuin=1490860381#1490860381/friend?res_uin=1490860381')


    input_txt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#aria-panel-normal > div > div.type-area > span > input.input-text')))
    input_txt.send_keys(search_name)
    return_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#aria-panel-normal > div > div.frd-list > ul:nth-child(2) > li > div')))
    # print(return_name.text)
    TouchActions(browser).tap(return_name).perform()#模拟手机点击

def get_info():
    print('正在获取信息...')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#feed_list_cot_mine')))
    for i in range(1,30):#这里定义翻页次数
        browser.execute_script("window.scrollBy(0, 10000)")
        time.sleep(2)
        browser.execute_script("window.scrollBy(0, 10000)")
        time.sleep(2)
        browser.execute_script("window.scrollBy(0, 10000)")
        get_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#feeds_more_mine')))
        get_more.click()
        time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dataItem')))
    html=browser.page_source
    soup = BeautifulSoup(html,'lxml')
    items = soup.select('.dataItem')
    name = soup.select_one('.fn').get_text()
    info={'name':name}
    txt =''
    txt_list=[]
    pub_time=[]
    for item in items:
        info={
            'time':pub_time.append(item.select_one('.time').get_text()),
            'txt':txt_list.append(item.select_one('.bd').get_text())

        }
        txt= txt + (item.select_one('.bd').get_text())
    # print(txt)


    seg_list = jieba.lcut(txt)  # 默认是精确模式
    seg_dic={}

    # print(seg_list)
    i = 0
    for item in seg_list:

        if len(item)>1:

            if item in seg_dic:

                seg_dic[item]+=1

            else:
                seg_dic[item]=1
    result = sorted(seg_dic.items(),key=lambda e:e[1],reverse=True)[:15]#降序排列
    results = sorted(seg_dic.items(), key=lambda e: e[1], reverse=True)
    # print(results)
    word = []
    data = []
    for item in result:
        word.append(item[0])
        data.append(item[1])

    sum = str(len(txt_list))
    with open(r'F:\QQzone_spider\\' +r'\\'+name+'.txt', 'w',encoding='UTF-8') as f:#文件保存路径
        i=0

        f.write('>>>>>>共爬取\t'+name+'\t'+str(len(txt_list))+'条空间动态<<<<<<\n')

        for line in results:
            i=i+1
            f.write(str(line))
            if i % 5 == 0:
                f.write('\n')
    print('写入文本成功')
    plot_bar(data,word,name,sum)


def plot_bar(data,word,name,sum):
    yy = data
    labels = word
    xx = range(len(data))

    plt.bar(range(len(data)), data, tick_label=labels)
    for x, y in zip(xx, yy):
        plt.text(x, y + 0.05, '%d' % y, ha='center',
                 va='bottom')  # a, b+0.05表示在每一柱子对应x值、y值上方0.05处标注文字说明， '%.0f' % b,代表标注的文字，即每个柱子对应的y值， ha='center', va= 'bottom'代表horizontalalignment（水平对齐）、verticalalignment（垂直对齐）的方式
    plt.title('共爬取...'+name+'...'+sum+'条空间动态',color='blue')
    plt.xlabel('词语',color='blue')
    plt.ylabel('出现次数',color='blue')
    plt.savefig(r'F:\QQzone_spider\\' +r'\\'+name+ ".png")#图片保存路径
    print('图片保存成功')
    plt.show()


def main():
    log_qkone()
if __name__ == '__main__':
    main()