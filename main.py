import requests
import uvicorn
from fastapi import FastAPI, Response
from lxml import etree

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
