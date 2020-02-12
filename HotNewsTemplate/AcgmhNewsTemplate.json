{
  "START_URL": "https://www.acgmh.com/category/news",
  "SPIDER_NAME": "AcgmhNewsSpider",
  "SITE_NAME": "acgmh",
  "METHOD": "GET",
  "REQUESTS": [
    {
      "request_id": 1,
      "extra_headers": {
        "Origin": "https://www.acgmh.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0",
        "sec-fetch-mode": "navigate"
      },
      "return_type": "html",
      "timeout": "200000",
      "process": "PROCESSES.1",
      "result": "RESULTS.1",
      "next_request": "REQUESTS.2"
    },
    {
      "request_id": 2,
      "start_url": "https://www.acgmh.com/wp-admin/admin-ajax.php?action=zrz_load_more_posts",
      "method": "POST",
      "post_data": {
        "type": "catL3",
        "paged": "RESULTS.2.page"
      },
      "extra_headers": {
        "origin": "https://www.acgmh.com",
        "sec-fetch-mod": "cors",
        "sec-fetch-site": "same-origin",
        "content-type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3858.0 Safari/537.36 Edg/77.0.229.0"
      },
      "process": "PROCESSES.2",
      "timeout": "200000",
      "return_type": "json",
      "result": "RESULTS.2",
      "next_request": "REQUESTS.3",
      "is_multiple": true,
      "stopped": "max_page"
    },
    {
      "request_id": 3,
      "start_url": "RESULTS.2.url",
      "extra_headers": {
        "origin": "https://www.acgmh.com",
        "cookies": "RESULTS.2.cookies"
      },
      "result": "RESULTS.3",
      "timeout": "200000",
      "referer": "https://www.acgmh.com/category/news",
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
      "page": 1,
      "global_parameter": "page"
    },
    {
      "result_id": 2,
      "page": "{page} + 1",
      "max_page": "1",
      "data": "msg>#one",
      "url": "https:\\/\\/www.acgmh.com\\/\\d+.html@data#list",
      "global_parameter": "page"
    },
    {
      "result_id": 3,
      "title": "h1.entry-title::text",
      "author": "span.author-name::text",
      "description": "",
      "news_time": "time[datetime]::text",
      "content": "div#content-innerText::text"
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

