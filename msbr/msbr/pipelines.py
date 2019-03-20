# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from contextlib import closing
import scrapy
import json

class MsbrPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')


    def close_spider(self, spider):
        self.file.close()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('demo2.db'))


    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)


    def process_item(self, item, spider):
        print('product process item')
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS data2 (
                        product_name str NOT NULL,
                        product_price str NOT NULL,
                        product_link str DEFAULT 0,
                        image str
                        ) ;
                
                INSERT OR IGNORE
                INTO data2 (product_name, product_price, product_link, image)
                VALUES ( ?, ?, ?, ? );
                ''',
                (item['product_name'], item['product_price'], item['product_link'],
                 item['image'], )
            )
            return item
            
