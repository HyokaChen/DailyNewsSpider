{
  "START_URL": "https://www.producthunt.com/",
  "SPIDER_NAME": "ProductHuntSpider",
  "SITE_NAME": "producthunt",
  "REFERER": "https://www.producthunt.com/",
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
      "referer": "https://www.tuicool.com/a/1?lang=0",
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
      "title": "//div[@class='item-content']//a/text()#list",
      "url": "//div[@class='item-content']//a/@href#list",
      "author": "//div[@class='tip meta-tip']/span[1]/text()#list",
      "description": "",
      "global_parameter": "page"
    },
    {
      "result_id": 2,
      "temp_time": "span.timestamp::text",
      "news_time": "时间\\W(.*)@temp_time#one",
      "content": "div.article_body::text"
    }
  ],
  "RENDER": false,
  "TIMEOUT": 20000,
  "USE_PROXY": false,
  "SLEEP_TIME": 10,
  "SESSION": true,
  "MAX_SESSION_TIMES": 10,
  "COOKIES": "",
  "RANGE_TIME": "",
  "RETURN_TYPE": "html",
  "DATA_TABLE": "mongo@animation",
  "PRIORITY": 1
}

