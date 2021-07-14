# 爬取所有250个页面的内容（所有代码综合）
import re, csv, requests
from lxml import etree

# 1.设置浏览器代理，构造字典
headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}

# 2.创建并打开文件夹，写入内容

fp = open("./豆瓣250.csv", 'a')
writer = csv.writer(fp)
writer.writerow(('排名', '名称', '链接', '星级', '评分', '评价人数'))

# 3.循环所有页面
for page in range(0, 226, 25):
    print("正在获取第%s页" % page)
    url = 'https://movie.douban.com/top250?start=%s&filter=' % page

    # 4.请求源代码，向服务器发出请求
    reponse = requests.get(url=url, headers=headers).text

    # 5.看做筛子筛取数据
    html_etree = etree.HTML(reponse)

    # 6.过滤
    li = html_etree.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li')
    for item in li:
        rank = item.xpath('./div/div[1]/em/text()')[0]  # 电影排名

        name = item.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]  # 电影名字

        dy_url = item.xpath('./div/div[2]/div[1]/a/@href')[0]  # 电影链接

        rating = item.xpath('./div/div[2]/div[2]/div/span[1]/@class')[0]  # 电影星级数相关处理（如5星级）
        rating = re.findall('rating(.*?)-t', rating)[0]
        if len(rating) == 2:  # rating为字符串，故直接求长度
            star = int(rating) / 10  # 字符串不可做运算，故int()转化为整数型
        else:
            star = rating

        rating_num = item.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]  # 电影分数（如9.0分）

        content = item.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0]  # 电影评价人数（如1234人评价）
        content = re.sub(r'\D', "", content)  # ""中的替代部分可写可不写

        print(rank,name,dy_url,star,rating_num,content)

        writer.writerow((rank, name, dy_url, star, rating_num, content))  # 写入身体部分内容
fp.close()
