# -*- coding: utf-8 -*-
import scrapy
from book_spider.items import BookSpiderItem,BookPageItem,BookContentItem


class XiaoshuoSpider(scrapy.Spider):
    name = "xiaoshuo"
    allowed_domains = ["biqukan.cc"]
    # 保存书的内容
    book_content = ''

    offset = 1
    url = 'http://www.biqukan.cc/fenlei1/'
    start_urls = (
        url + str(offset) + '.html',
    )

    def parse(self, response):
        
        # 推荐书的url
    	book_urls = response.xpath("//div[contains(@class,'list-group list-top')]/li/a/@href").extract()
    	# 最新书的url
    	book_urls += response.xpath("//div[contains(@class,'col-md-8')]//td/a/@href").extract()

    	for book_url in book_urls:

            if not book_url.endswith('.html'):
                # print book_url
            	# 发送请求
            	yield scrapy.Request(book_url,callback=self.parse_book_desc)

        if self.offset < 30:
            self.offset += 1
            url_str = self.url + str(self.offset) + '.html'
            print url_str   
            yield scrapy.Request(url_str,callback=self.parse)



    def parse_book_desc(self,response):
    	'''书的信息及章节'''
    	book_item = BookSpiderItem()

    	book_item['book_id'] = response.url.split('/')[-2]
    	book_item['book_title'] = response.xpath("//h1[contains(@class,'bookTitle')]/text()").extract()[0]
    	book_item['book_author'] = response.xpath("//p[contains(@class,'booktag')]/a[1]/text()").extract()[0]
    	book_item['book_type'] = response.xpath("//p[contains(@class,'booktag')]/a[2]/text()").extract()[0]
    	book_item['book_total_count'] = response.xpath("//p[contains(@class,'booktag')]/span[1]/text()").extract()[0]
    	descs = response.xpath('//p[contains(@class,"text-muted")]/text()').extract()
        descs = ''.join(descs)
        book_item['book_desc'] = descs.strip().replace(' ','').replace('\n','') #response.xpath("//div[contains(@class,'row')]//p[contains(@class,'text-muted')]/text()").extract()[0].strip()
        book_item['spider_type'] = 'book_desc'
        book_item['book_new_page_title'] = response.xpath("//div[contains(@class,'row')]//p[2]/a/@title").extract()[0]
        page_new_id = response.xpath("//div[contains(@class,'row')]//p[2]/a/@href").extract()[0]
        book_item['book_new_page_id'] = page_new_id.split('.')[0]
        book_item['book_cover_image'] = response.xpath("//div[contains(@class,'row')]/div[1]/img/@src").extract()[0]

        # 章节信息
        page_item = BookPageItem()
        page_item['book_id'] = response.url.split('/')[-2]
        book_page_titles = response.xpath("//div[contains(@id,'list-chapterAll')]/dl//a/@title").extract()
        page_urls = response.xpath("//div[contains(@id,'list-chapterAll')]/dl//a/@href").extract()
        page_info_arr = []
        index = 0
        for page_url in page_urls:
            page_id = page_url.split('.')[0]
            page_info_arr.append({'book_page_id':page_id,'book_page_title':book_page_titles[index],'number':str(index)})
            index += 1
            yield scrapy.Request(response.url + page_url, meta={'book_page_id': page_id,'book_id':page_item['book_id']},
                                 callback=self.parse_content_desc)

        page_item['book_pages'] = page_info_arr
        # 把page_item赋值给book_item
        book_item['book_page'] = page_item
        yield book_item


    def  parse_content_desc(self,response):
    	'''内容'''
    	content_item = BookContentItem()

    	content_item['book_page_id'] = response.meta['book_page_id']
        contents = response.xpath('//div[@class="panel-body"]/text()').extract()
        content_list = []
        str_content = ''
        for c in contents:
            str_content += c
        
        book_content_page = str_content.strip().replace('\r\n','').replace(' ','').replace('一秒记住【笔趣阁www.biqukan.cc】，更新快，无弹窗，免费读！    ','').replace('&nbsp-->>','').replace('&-->>','').replace('&nb-->>','').replace('-->>','').strip()

        next_url = response.xpath('//a[@id="linkNext"]/@href').extract()[0]
        next_title = response.xpath('//a[@id="linkNext"]/text()').extract()[0]
        content_item['book_pages_content'] = book_content_page
        content_item['spider_type'] = 'content_desc'
        content_item['book_id'] = response.meta['book_id']

        if next_url.startswith('www'):
            yield scrapy.Request(next_url,callback=self.parse_content_desc)

        yield content_item

        
