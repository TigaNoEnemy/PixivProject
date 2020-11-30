# PixivProject
结合PyQt5和pixivpy3模块实现通过图形界面访问Pixiv



# 打包

内置了spec打包文件，打包时在终端输入

```shell
pyinstaller Main_Pixiv.spec
```

打包后或许可能也许包会很大，因此在abandon.txt手动列出了一些不需要用到的链接库，这些库是通过查看程序运行时调用了哪些库，再根据这些去掉没有调用的库而生成的，毕竟是手动的，所以也许还有可以缩小包的途径。若是去掉这些库导致无法运行，那就加回去吧。