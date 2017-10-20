from scrapy import cmdline
cmdline.execute("scrapy crawl dmoz -o items.csv -t csv".split())