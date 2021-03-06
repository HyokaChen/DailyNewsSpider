{
  "START_URL": "https://www.sncrating.com/cn/research",
  "SPIDER_NAME": "SncratingNewsSpider",
  "SITE_NAME": " sncrating",
  "REFERER": "https://www.sncrating.com/cn/",
  "METHOD": "GET",
  "REQUESTS": [
    {
      "request_id": 1,
      "method": "GET",
      "process": "PROCESSES.1",
      "result": "RESULTS.1",
      "next_request": "REQUESTS.2"
    },
    {
      "request_id": 2,
      "start_url": "RESULTS.1.url",
      "extra_headers": {
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0"
      },
      "result": "RESULTS.2",
      "return_type": "css",
      "is_duplicate": true,
      "return_item": "items.HotNewsItem"
    }
  ],
  "PROCESSES": [
    {
      "process_id": 1,
      "process_method": "spiders.new_tencent_spider.first_process"
    },
    {
      "process_id": 2,
      "process_method": "spiders.new_tencent_spider.second_process",
      "parameters": "RESULTS.2.page"
    }
  ],
  "RESULTS": [
    {
      "result_id": 1,
      "page": "{page} + 1",
      "max_page": "1",
      "title": "//div[@class='news-list']/div/div/a[@target='_blank']//h4/text()#list",
      "part_url": "//div[@class='news-list']/div/div/a[@target='_blank']/@href#list",
      "url": "$https://segmentfault.com/{part_url}",
      "author": "//div[@class='news-list']/div//span[contains(@class, 'author')]/a/text()#list",
      "description": ""
    },
    {
      "result_id": 2,
      "temp_time": "div#sf-article_tags > div > time[itemprop='datePublished']::text",
      "news_time": "发布于\\W(.*)@temp_time#one",
      "content": "article.article::text"
    }
  ],
  "RENDER": false,
  "TIMEOUT": 10,
  "USE_PROXY": false,
  "SLEEP_TIME": 10,
  "SESSION": true,
  "MAX_SESSION_TIMES": 10,
  "COOKIES": "",
  "RANGE_TIME": "",
  "RETURN_TYPE": "html",
  "DATA_TABLE": "mongo@technology",
  "PRIORITY": 1
}

