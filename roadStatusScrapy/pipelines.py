# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo


class RoadstatusScrapyJsonPipeline(object):
    # 存储到json文件
    def open_spider(self, spider):
        self.file = open('items.jl', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # print('processing')
        # for item in items:
        #     # print(item)
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        # return items


class RoadstatusScrapyMongoPipeline(object):

    def __init__(self, mongo_host, port, user, password, db, coll):
        self.mongo_host = mongo_host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.coll = coll

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            port=crawler.settings.get('MONGO_PORT'),
            user=crawler.settings.get('MONGO_USER'),
            password=crawler.settings.get('MONGO_PSW'),
            db=crawler.settings.get('MONGO_DB'),
            coll=crawler.settings.get('MONGO_COLL')
        )

    def open_spider(self, spider):
        # 链接数据库
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.port)
        # 数据库登录需要帐号密码的话
        # 这里因为我创建的是对应数据库的账户，所以client后面要索引数据库的名字，然后再获得数据库曲柄，网上的很多教程都是将账户信息存储到admin表，所以所引导client.admin
        self.client[self.db].authenticate(self.user, self.password)
        self.db = self.client[self.db]  # 获得数据库的句柄
        self.coll = self.db[self.coll]  # 获得collection的句柄

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert_one(postItem)  # 向数据库插入一条记录
        # return item  # 会在控制台输出原item数据，可以选择不写
