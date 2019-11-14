{
  "START_URL": "https://www.ctolib.com/",
  "SPIDER_NAME": "CTOLibSpider",
  "SITE_NAME": "ctolib",
  "REFERER": "https://www.ctolib.com/",
  "METHOD": "GET",
  "REQUESTS": [
    {
      "request_id": 1,
      "method": "GET",
      "process": "PROCESSES.1",
      "timeout": "200000",
      "extra_headers": {
        "sec-fetch-mod": "navigate",
        "sec-fetch-site": "cross-site"
      },
      "result": "RESULTS.1",
      "next_request": "REQUESTS.2"
    },
    {
      "request_id": 2,
      "start_url": "RESULTS.1.url",
      "result": "RESULTS.2",
      "is_duplicate": true,
      "timeout": "200000",
      "extra_headers": {
        "sec-fetch-mod": "navigate",
        "sec-fetch-site": "cross-site"
      },
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
      "max_page": "4",
      "title": "//div[@id='newp']//div[contains(@class, 'item-listing-extra')]//a/text()#list",
      "part_url": "//div[@id='newp']//div[contains(@class, 'item-listing-extra')]//a/@href#list",
      "url": "$https://www.ctolib.com{part_url}",
      "author": "//div[@id='newp']//div[@class='pos-rlt']/div/span/a/text()#list",
      "description": "//div[@id='newp']//div[contains(@class, 'item-listing-extra')]//a/text()#list"
    },
    {
      "result_id": 2,
      "temp_time": "//div[contains(@class, 'row')]/table/tbody/tr[2]/td/text()#one",
      "news_time": "收录时间：(.*)@temp_time#one",
      "temp_content": "//a[@id='githome']/@href",
      "content": "$https://www.ctolib.com{temp_content}"
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

