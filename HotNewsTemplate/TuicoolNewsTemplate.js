{
  "START_URL": "https://www.tuicool.com/",
  "SPIDER_NAME": "TuicoolNewsSpider",
  "SITE_NAME": "tuicool",
  "REFERER": "https://www.tuicool.com/",
  "METHOD": "GET",
  "REQUESTS": [
    {
      "request_id": 1,
      "method": "GET",
      "result": "RESULTS.1",
      "next_request": "REQUESTS.2"
    },
    {
      "request_id": 2,
      "start_url": "RESULTS.1.url",
      "referer": "https://www.tuicool.com/a/1?lang=0",
      "extra_headers": {
        "Host": "www.tuicool.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "https://www.tuicool.com/login",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
      },
      "result": "RESULTS.2",
      "return_type": "css",
      "is_duplicate": true,
      "return_item": "items.HotNewsItem"
    }
  ],
  "PROCESSES": [
  ],
  "RESULTS": [
    {
      "result_id": 1,
      "title": "//div[@class='aricle_item_info']/div[@class='title']//a/text()#list",
      "part_url": "//div[@class='aricle_item_info']/div[@class='title']//a/@href#list",
      "url": "$https://www.tuicool.com{part_url}",
      "author": "//div[@class='tip']/span[1]/text()#list",
      "news_time": "",
      "description": "//div[@class='aricle_item_info']/div[@class='title']//a/text()#list"
    },
    {
      "result_id": 2,
      "temp_time": "span.timestamp::text",
      "news_time": "时间\\W(.*)@temp_time#one",
      "content": "div.article_body::text"
    }
  ],
  "RENDER": false,
  "TIMEOUT": 10,
  "USE_PROXY": false,
  "SLEEP_TIME": 10,
  "USE_SESSION": false,
  "MAX_SESSION_TIMES": 10,
  "COOKIES": {
    "__gads": "ID=4a38102b88894e8f-225e771d4cb9009f:T=1617023078:RT=1617023078:S=ALNI_MYPNAZdGZJnXGQWh1BN1DVCxJrD7g",
    "_tuicool_session": "SlJLWEROZHcrMDhoSlF5aFNweUpvQlRLWFk5OHU0cjM2N1kvcGNSd041TTE4M3IrRm9kVmtIcm8wZDdVcTloQktDN0pkdllPMFNiSWFLV3Q0a0hhZnppNFFIaWpZQ09zbG93d2lhVzZOTWZKZjRvSjlCQUtmYkpRUk0wQ011dGs3ZmFQMXJNeUo1VWUvbWswcGVKUHFCOGdiNEZsWHE2UnFzT0hkdzJTS1p6TDVrTGhlU0w0QVR5cTFXcHR5SnZFd2NubllUaEI3VFArY0ZSam93WnYyQ2FkYjZhWGFQbUN1cTl3RkJhUEk0dnd4SHFBODdkS0NwZkJiN0dDVWJsa21iNjE4S1ovamRJUjNreXRRZTVJNnJaT2RydG0zRWphY3AvVjZTSnplZ1YrVWhXS0VUQUFrZ0lWVzRMTit4R3JHRFo1amV3dGdCb2JiY1J1OURZaFpmcnZTZ1IzWVZPYXlaTFgzQTAxTVY3Q0tFTnNObElJTHNyUjdxYURJMWFTV3ltbjdwZWpaQmtERi91NllPTlhIODI4aDA1ZzE0azB6K1VzdGpLaWhEWktweURMbFZiU1BVZ3Z5MVhiR2hIczJGVTRCbkZZRWtjMm1pdnIzcU1HQTNJNnNmeEJVVlpKRUhWbEpSU0FCK2c9LS1xODJtMG8zTlZBbWtIeDFpYXJjSmRBPT0%3D--8daded66dc2b7be5ddb7726aa3daea8390e42a0a"
  },
  "RANGE_TIME": "",
  "RETURN_TYPE": "html",
  "DATA_TABLE": "mongo@technology",
  "PRIORITY": 1
}

