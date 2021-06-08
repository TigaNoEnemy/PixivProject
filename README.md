# PixivProject
结合PyQt5和pixivpy3模块实现通过图形界面访问Pixiv



# 打包

内置了spec打包文件，打包时在终端输入

```shell
pyinstaller Main_Pixiv.spec
```

打包后或许可能也许包会很大，因此在abandon.txt手动列出了一些不需要用到的链接库，这些库是通过查看程序运行时调用了哪些库，再根据这些去掉没有调用的库而生成的，毕竟是手动的，所以也许还有可以缩小包的途径。若是去掉这些库导致无法运行，那就加回去吧。

# 关于账号密码登录不可用

账号密码登陆已经不可行，需要使用refresh_token进行登录，获取refresh_token需要用到科学上网，在get_fresh_token.py文件的 PROXIES 填入你的代理ip：

```Python
PROXIES = {
    'http': '代理IP:端口',
    'https': '代理IP:端口',
}
```

终端输入 python get_fresh_token.py 运行, 该脚本将会控制浏览器访问PIXIV

之后按照 [github.com @ ZipFile](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) 的方式获取 refresh_token。

获取refresh_token之后，在 utils/Process_Token.py 文件中修改 login_info_parser 类的 get_token 函数的最后一行，改为：

```python
token = '你的fresh_token'
auto = True
login_account = ''
return {'token': token, 'auto': auto, 'login_account': login_account}
```

第一次成功登录后，最后将 utils/Process_Token.py 文件还原，因为以后登录不需要再重复上面步骤了，只需执行 python Main_Pixiv.py 即可。