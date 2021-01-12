{
  "START_URL": "https://www.jinse.com/",
  "SPIDER_NAME": "SinaFinanceSpider",
  "SITE_NAME": "sina",
  "REFERER": "http://finance.sina.com.cn/",
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
      "start_url": "http://feed.mix.sina.com.cn/api/roll/get?pageid={pageid}&lid={lid}&k=&num=10&page={page}&_={_random}",
      "parameters": "RESULTS.1 & RESULTS.2.page",
      "process": "PROCESSES.2",
      "return_type": "json",
      "result": "RESULTS.2",
      "next_request": "REQUESTS.3",
      "is_multiple": true,
      "stopped": "max_page"
    },
    {
      "request_id": 3,
      "start_url": "RESULTS.2.url",
      "category": "news",
      "result": "RESULTS.3",
      "is_duplicate": true,
      "return_item": "items.FinanceItem"
    }
  ],
  "PROCESSES": [
    {
      "process_id": 1,
      "process_method": "spiders.new_sina_spider.first_process"
    },
    {
      "process_id": 2,
      "process_method": "spiders.new_sina_spider.second_process",
      "parameters": "RESULTS.2.page"
    }
  ],
  "RESULTS": [
    {
      "result_id": 1,
      "page": 1,
      "pageid": "155",
      "lid": "1686",
      "_random": "int(time.time())",
      "global_parameter": "page"
    },
    {
      "result_id": 2,
      "page": "{page} + 1",
      "title": "result>data>title",
      "url": "result>data>url",
      "description": "result>data>intro",
      "news_time": "result>data>ctime",
      "max_page": "2",
      "global_parameter": "page"
    },
    {
      "result_id": 3,
      "content": "//div[@id='artibody']/p/text()#text"
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
  "DATA_TABLE": "mongo@finance",
  "PRIORITY": 1
}

