# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import json
import pymongo

class BookSpiderPipeline(object):

    def __init__(self):
        host = '127.0.0.1'
        port = 27017
        dbname = 'Book'

        # 创建数据库
        client = pymongo.MongoClient(host,port)

        # 指定数据库
        self.mydb = client[dbname]


    def process_item(self, item, spider):
        
        if item['spider_type'] == 'book_desc':
            # 书的简介信息
            book_item = item
            # 章节的简介信息
            book_page = item['book_page']
            # 把章节信息置为空
            book_item['book_page'] = ''

            # 书的简介内容
            book_desc_json_data = {
            'id':str(book_item['book_id']),'book_title':book_item['book_title'],'book_author':book_item['book_author'],
                    'book_type':book_item['book_type'],'total_count':book_item['book_total_count'],
                    'desc':book_item['book_desc'],'new_page_tilte':book_item['book_new_page_title'],
                    'new_page_id':book_item['book_new_page_id'],'book_cover':book_item['book_cover_image']

            }
            # 存放数据的表
            book_desc_mysheet = self.mydb['Book_Desc']
            # 插入到数据库
            book_desc_mysheet.insert(book_desc_json_data)



            # 章节信息
            book_page_desc_json_data = {'id':str(book_page['book_id']),'book_pages':book_page['book_pages']}
            # 存放数据的表
            book_page_desc_mysheet = self.mydb['Book_Page_Desc']
            # 插入到数据库
            book_page_desc_mysheet.insert(book_page_desc_json_data)




            # content = json.dumps(dict(book_item), ensure_ascii=False) + "\n"
            # filename = codecs.open('book_desc.json', 'a+', encoding='utf-8')
            # filename.write(content)

            # content = json.dumps(dict(book_page), ensure_ascii=False) + "\n"
            # filename = codecs.open('page_desc.json', 'a+', encoding='utf-8')
            # filename.write(content)
        else:

            # 书的简介内容
            book_content_desc_json_data = {'id':str(item['book_page_id']),'book_id':item['book_id'],'content':item['book_pages_content']}
            # 存放数据的表
            book_content_desc_mysheet = self.mydb['Book_Content_Desc']
            # 插入到数据库
            book_content_desc_mysheet.insert(book_content_desc_json_data)

            # content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # filename = codecs.open('content_desc.json', 'a+', encoding='utf-8')
            # filename.write(content)
        
        return item     
