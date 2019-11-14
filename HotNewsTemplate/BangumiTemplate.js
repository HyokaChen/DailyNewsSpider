{
  "START_URL": "http://bgm.tv/anime/browser/tv",
  "SPIDER_NAME": "Bangumi",
  "SITE_NAME": "bangumi",
  "METHOD": "GET",
  "REFERER": "http://bgm.tv/",
  "REQUESTS": [
    {
      "request_id": 1,
      "extra_headers": {
        "Host": "bgm.tv",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.34 Safari/537.36 Edg/78.0.276.11"
      },
      "return_type": "html",
      "timeout": "20000",
      "process": "PROCESSES.1",
      "result": "RESULTS.1",
      "next_request": "REQUESTS.2"
    },
    {
      "request_id": 2,
      "start_url": "http://bgm.tv/anime/browser/tv?page={_page}",
      "parameters": "RESULTS.1._page",
      "extra_headers": {
        "Host": "bgm.tv",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.34 Safari/537.36 Edg/78.0.276.11"
      },
      "process": "PROCESSES.2",
      "timeout": "20000",
      "return_type": "html",
      "result": "RESULTS.2",
      "next_request": "REQUESTS.3"
    },
    {
      "request_id": 3,
      "start_url": "RESULTS.2.url",
      "extra_headers": {
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1"
      },
      "result": "RESULTS.3",
      "return_type": "css",
      "timeout": "20000",
      "is_duplicate": true,
      "return_item": "items.PaperItem"
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
      "_page": "random.randint(1, 234)"
    },
    {
      "result_id": 2,
      "part_url": "//ul[@id='browserItemList']/li/a/@href#list",
      "url": "$http://bgm.tv/{part_url}"
    },
    {
      "result_id": 3,
      "title": "#infobox > li:nth-child(1)::text",
      "director": "div.authors > p > span::text",
      "description": "div.paper-abstract > div > div > p::text",
      "tags": "div.paper-tasks > div > div > ul.list-unstyled > li > a > span::text",
      "episodes": "",
      "show_time": "div#id_paper_implementations_collapsed > div > div > div.paper-impl-cell > a::href"
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
  "DATA_TABLE": "mongo@paper",
  "PRIORITY": 1
}

