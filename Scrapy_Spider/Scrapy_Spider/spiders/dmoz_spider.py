#coding:utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from Scrapy_Spider.items import *

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = ['http://movie.douban.com/top250']
    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        print response
        item = ScrapySpiderItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            # 把两个名称合起来
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle.encode('utf-8')
            str = ''
            for mov in movieInfo:
                str += mov.strip().encode('utf-8')
                str += ';'
            item['movieInfo'] = str
            # item['movieInfo'] = ';'.join(movieInfo).encode('utf-8')
            item['star'] = star.encode('utf-8')
            item['quote'] = quote.encode('utf-8')
            item['url'] = response._get_url()
            print response._get_url()
            yield item
            nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
            # 第10页是最后一页，没有下一页的链接
            if nextLink:
                nextLink = nextLink[0]
                # print nextLink
                yield Request(self.url + nextLink, callback=self.parse)