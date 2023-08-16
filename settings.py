# Scrapy settings for twitter_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "twitter_scraper"

SPIDER_MODULES = ["twitter_scraper.spiders"]
NEWSPIDER_MODULE = "twitter_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "twitter_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# config this
DEFAULT_REQUEST_HEADERS = {
   """:authority: services.bovada.lv
        :method: POST
        :path: /services/login-service/v1/login
        :scheme: https
        accept: application/json, text/plain, */*
        accept-encoding: gzip, deflate, br
        accept-language: en-US,en;q=0.9,th;q=0.8
        content-length: 82
        content-type: application/json
        cookie: VISITED=true; Device-Type=Desktop|false; _hjSessionUser_510373=eyJpZCI6IjdiNzMzNWVhLWMwYjQtNWE2NS1hMWVjLWVmNTFiMzk0MTk0ZSIsImNyZWF0ZWQiOjE2NjgxNDk1MTg0MTgsImV4aXN0aW5nIjp0cnVlfQ==; LANG=en; ln_grp=2; odds_format=AMERICAN; JOINED=true; url-prefix=/; _hjAbsoluteSessionInProgress=0; JSESSIONID=BD32B572B54747813B2D0F00E35D480D; variant=v:1|lgn:0|dt:d|os:mac|cntry:US|cur:USD|jn:1|rt:o|pb:0; wt_rla=205099820688534%2C26%2C1678342617442
        origin: https://services.bovada.lv
        referer: https://services.bovada.lv/
        sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "macOS"
        sec-fetch-dest: empty
        sec-fetch-mode: same-origin
        sec-fetch-site: same-origin
        traceid: dcf363f5-a18c-4e6b-8fd0-f6db158ff2fb
        user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
        x-captcha-token: 03AFY_a8XDReEm5c4OVbojOZsv1NYy5SggX22_f3qFI0u08UkUxKLXSgo02KbrU_eyC-YsMm-bOM8pgngaoZTF_6cH1NuFltUIYSIWeol2XH4Th1EMW22enW0hzQxLiO91uttasz5kAM_vsVmukAbwfQh-EfURwCX3LjbgOtSkYr3nVKqiGRgxErF3llzYPepV3bxbZd6yPFdMhm2UPKjrsHMDesv_qyUgR7RA9DBOr7KgYbHqMA5wSlbYbkqjMpXfMmt1L4RB3uYsVUXASXLsbxmKKhx2k1ENVGMk3x5w_GIzcfpCY71EXGNfKgc4LfemnV-oZDhyG8Mf-swm1MHnV_09r2z7BU5VVKQVzOgW8xbnqmPY4NU7fEbFWISZVAe136a4kX5DaG0S_qC5lJl_FMQi0I3WJxHmTzXinBjBZ-j61CEQCgp8AD5fA66UJel91psy4imM9Lyc-khfMFhrZ2XTgoldKMTXa1OwkR_QKHzQDzIQu4uG953xpLVL1pnuC_lgkE9rVjfqVTQ6__G-U42ogNUxCER1NZxMS6dvXOD4D4zrWATceb8WnLoXVINhVNr9aqEN_AR6
        x-channel: desktop
        """
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "twitter_scraper.middlewares.TwitterScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "twitter_scraper.middlewares.TwitterScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "twitter_scraper.pipelines.TwitterScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
