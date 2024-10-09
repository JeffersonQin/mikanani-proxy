import requests
import uvicorn
from fastapi import FastAPI, Response
from lxml import etree
from datetime import datetime

run_host = "0.0.0.0"
run_port = 9115
host_name = "http://1.2.3.4:5555"

app = FastAPI()

mikan_base_url = "https://mikanani.me/RSS/MyBangumi?token="
mikan_token = ""
user_token = ""

mikan_url = f"{mikan_base_url}{mikan_token}"


@app.get("/")
def root(token: str):
    if token != user_token:
        return {}
    content = requests.get(mikan_url).content
    doc = etree.fromstring(content)

    links = doc.xpath("//enclosure")
    print(len(links), "links")

    for link in links:
        url = link.get("url")
        url = url.replace(
            "https://mikanani.me",
            f"{host_name}/get?token={user_token}&link=https://mikanani.me",
        )
        link.set("url", url)
    
    # 修改pubdate格式
    namespaces = {'ns': 'https://mikanani.me/0.1/'}
    for item in doc.findall('.//item'):
        # 使用find找到torrent节点，再找到pubDate
        pub_date_element = item.find('.//ns:torrent/ns:pubDate', namespaces)
        if pub_date_element is not None:
            # 原始pubDate字符串
            pub_date_str = pub_date_element.text
            # 去掉微秒部分，转换格式
            if '.' in pub_date_str:
                pub_date_str = pub_date_str.split('.')[0]  # 去掉微秒部分
            # 解析原始日期字符串
            pub_date = datetime.fromisoformat(pub_date_str)
            # 将日期格式化为目标格式
            formatted_pub_date = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0800')
            # 更新pubDate元素的文本
            # pub_date_element.text = formatted_pub_date  # 也没必要

            # 将pubDate元素移动到item下
            # 创建新的pubDate节点
            new_pub_date_element = etree.Element('pubDate')
            new_pub_date_element.text = formatted_pub_date
            # 将新的pubDate添加到item的最后
            item.append(new_pub_date_element)

    content = etree.tostring(doc)
    return Response(content, media_type="application/xml")


@app.get("/get")
def get(token: str, link: str):
    if token != user_token:
        return {}
    response = requests.get(link)
    media_type = response.headers.get("Content-Type")
    return Response(response.content, media_type=media_type)


if __name__ == "__main__":
    uvicorn.run(app, host=run_host, port=run_port)
