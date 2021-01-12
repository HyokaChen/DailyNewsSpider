![DailyNewsSpider](./DailyNewsSpider.png)


[每日随机资讯](https://blog.emptychan.xyz)的新闻资讯来源

#### 目前采集进程如下：

- [x] [Acg 门户](https://www.acgmh.com/category/news)
- [x] [Bing 壁纸](https://cn.bing.com/)
- [x] [CTOLIB](https://www.ctolib.com/)
- [x] [动漫之家](https://www.dmzj.com/)
- [x] [IT之家](https://www.ithome.com/list/)
- [x] [Papers With Code](https://paperswithcode.com/latest)
- [x] [起点中文网](https://www.qidian.com/)
- [x] [纵横中文网](http://www.zongheng.com/)
- [x] [新浪娱乐新闻](http://ent.sina.com.cn/rollnews.shtml)
- [x] [新浪财经资讯](http://finance.sina.com.cn/china/)
- [x] [腾讯动漫资讯](https://new.qq.com/ch/comic/)
- [x] [腾讯娱乐新闻](http://ent.qq.com/articleList/rolls/)
- [x] [推酷](https://www.tuicool.com/)
- [x] [3DMGame](https://www.3dmgame.com/)
- [x] [游民星空动漫资讯](https://acg.gamersky.com/news/)
- [ ] [Bangumi 动漫](http://bgm.tv/anime/browser/tv)
- [x] [集智斑图](https://pattern.swarma.org/?type=newpaper)
- [x] [SegmentFault](https://segmentfault.com/)
- [x] [虎嗅](https://www.huxiu.com/)
- [x] [HackerNews](https://hackernews.io/)

#### 安装步骤

1. 安装 redis, MacOS 底下可以采用 Homebrew 安装 redis，命令```brew install redis```
1. 安装 [mongodb](https://docs.mongodb.com/manual/installation/)
2. 安装 [python 3.7.4](https://www.python.org/downloads/)以上，并安装[poetry](https://python-poetry.org/)
3. 在代码的当前目录执行```poetry install```来安装环境依赖

#### 执行程序

```bash
python insert_new_item_template.py  # 具体的 item定义查看这个 python 文件
python main.py -m True
python main.py
```

