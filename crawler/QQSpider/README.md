##  这是一只爬取特定号码的qq空间图片的爬虫
用法:在根目录下面添加一个QQ_for_crawl.txt的文件，写上你想要爬的账号，然后在项目的根目录下面 输入命令行 scrapy crawl qq

注意事项:1.能爬到的图片，是你登录的账号有权限看到所爬账号的图片，有点绕。意思是，你用来登录的账号，在朋友的qq空间能看到那些图片，你才能爬，没权限看，就不能爬
2.更改setting.py里面的IMAGES_STORE 值，
安装phantomjs ，并且在get_cookie里面更改phantomjs的安装路径