# 蜜柑计划 RSS 代理服务器

悲报！被墙了！所以这里是解决方案。【轻量到我甚至不想写配置文件】

## 使用方法

1. 编辑 `main.py`
   - `host_name`: 对外暴露的域名或者 IP，以协议 `http://` 活 `https://` 开头，没有结尾的 `/`。
   - `mikan_token`: 蜜柑计划的 RSS Token，看一眼你的 RSS URL 就知道了。
   - `user_token`: 设一个你自己的 Token，用于验证身份。
   - `run_host`: Host IP（不知道这个是什么意思的就别动）。
   - `run_port`: 端口
2. 运行
   ```bash
   python main.py
   ```
3. torrent 下载器的 RSS 如下配置：
   ```
   http(s)://<服务器的暴露 IP/域名>/?token=<user_token>
   ```
