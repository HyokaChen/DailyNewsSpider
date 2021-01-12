{
  "START_URL": "https://www.jiqizhixin.com/",
  "SPIDER_NAME": "TuicoolNewsSpider",
  "SITE_NAME": "tuicool",
  "REFERER": "https://www.tuicool.com/",
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
      "start_url": "https://www.tuicool.com/a/1/0?lang=0",
      "parameters": "RESULTS.1",
      "process": "PROCESSES.2",
      "extra_headers": {
        "Host": "www.tuicool.com",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0"
      },
      "return_type": "html",
      "result": "RESULTS.2",
      "parallel_request": "REQUESTS.3",
      "next_request": "REQUESTS.4",
      "stopped": "max_page"
    },
    {
      "request_id": 3,
      "start_url": "https://www.tuicool.com/a/1/{page}?lang=0",
      "parameters": "RESULTS.2.page",
      "process": "PROCESSES.2",
      "extra_headers": {
        "Host": "www.tuicool.com",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0"
      },
      "return_type": "html",
      "result": "RESULTS.2",
      "next_request": "REQUESTS.4",
      "is_multiple": true,
      "stopped": "max_page"
    },
    {
      "request_id": 4,
      "start_url": "RESULTS.2.url",
      "referer": "https://www.tuicool.com/a/1?lang=0",
      "extra_headers": {
        "Host": "www.tuicool.com",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0"
      },
      "result": "RESULTS.3",
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
      "page": 0,
      "global_parameter": "page"
    },
    {
      "result_id": 2,
      "page": "{page} + 1",
      "max_page": "1",
      "title": "//div[@class='article_title abs-title']/a/text()#list",
      "part_url": "//div[@class='article_title abs-title']/a/@href#list",
      "url": "$https://www.tuicool.com{part_url}",
      "author": "//div[@class='tip meta-tip']/span[1]/text()#list",
      "description": "",
      "global_parameter": "page"
    },
    {
      "result_id": 3,
      "temp_time": "span.timestamp::text",
      "news_time": "时间\\W(.*)@temp_time#one",
      "content": "div.article_body::text"
    }
  ],
  "RENDER": false,
  "TIMEOUT": 10,
  "USE_PROXY": false,
  "SLEEP_TIME": 10,
  "SESSION": true,
  "MAX_SESSION_TIMES": 10,
  "COOKIES": {"_tuicool_session": "BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWVjY2VkYzBjZDU5MDBmZDJhMTZlOTg0NmFkZjFkZjEyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVM3dEZsdnpScTUvWFRiblJmY1JLVVFyZU9COHpNcXBkSVpyVE5aQ0VtZEU9BjsARkkiDHVzZXJfaWQGOwBGaQNVLAFJIg5yZXR1cm5fdG8GOwBGSSItaHR0cHM6Ly93d3cudHVpY29vbC5jb20vYXJ0aWNsZXMveVVycWVpdQY7AFQ%3D--9b40aa260dda322d6c1b613cad5c9788bed22bf4"},
  "RANGE_TIME": "",
  "RETURN_TYPE": "html",
  "DATA_TABLE": "mongo@technology",
  "PRIORITY": 1
}

