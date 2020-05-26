# -*- coding: utf-8 -*-
import scrapy
import logging

class BookscrapeSpider(scrapy.Spider):
    name = 'BookScrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        #pageTitle = response.xpath("//h1/text()").get()
        currentPageBooks = response.xpath("//div/ol[@class='row']/li")
        for book in currentPageBooks:
            # bookURL = response.urljoin(book.xpath(".//article/h3/a/@href").get())
            bookURL = book.xpath(".//article/h3/a/@href").get()
            bookName = book.xpath(".//article/h3/a/text()").get()
            bookPrice = book.xpath(".//article/div[@class='product_price']/p[@class='price_color']/text()").get()

            yield response.follow(url=bookURL, callback = self.parseBookDetails , meta={'book_name': bookName})
            # yield{
            # 'productURL': bookURL,
            # 'bookName':bookName,
            # 'bookPrice':bookPrice
            # }

        isNextPageExist = response.urljoin(response.xpath("//div/ul[@class='pager']/li[@class='next']/a/@href").get())
        logging.info(isNextPageExist)
        if(isNextPageExist):
            yield scrapy.Request(url=isNextPageExist, callback= self.parse)
        
    def parseBookDetails(self,response):
        bookName = response.request.meta['book_name']
        rows = response.xpath("//article[@class='product_page']")
        fullBookName = rows.xpath(".//div[@class='row']/div[@class='col-sm-6 product_main']/h1/text()").get()
        productDesc = rows.xpath(".//div[@id='product_description']/following::p/text()").get()
        yield{
                'fullBookName':fullBookName,
                'productDescription':productDesc
            }