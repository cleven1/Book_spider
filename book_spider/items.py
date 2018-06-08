# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    book_id = scrapy.Field()
    # 标题
    book_title = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 书的类型
    book_type = scrapy.Field()
    # 总字数
    book_total_count = scrapy.Field()
    # 描述
    book_desc = scrapy.Field()
    # 最新章节
    book_new_page_title = scrapy.Field()
    # 最新章节id
    book_new_page_id = scrapy.Field()
    # 封面
    book_cover_image = scrapy.Field()

    # pageItem
    book_page = scrapy.Field()
    # contentItem
    book_content = scrapy.Field()

    # 区分item
    spider_type = scrapy.Field()


class BookPageItem(scrapy.Item):
    # 书id
    book_id = scrapy.Field()
    #章节信息
    book_pages = scrapy.Field()
    

class BookContentItem(scrapy.Item):
    # 书的id
    book_id = scrapy.Field()
    # 章节id
    book_page_id = scrapy.Field()
    #章节内容
    book_pages_content = scrapy.Field()

    # 区分item
    spider_type = scrapy.Field()