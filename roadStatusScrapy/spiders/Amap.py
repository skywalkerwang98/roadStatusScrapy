# -*- coding: utf-8 -*-
import scrapy
import json
from time import time
from roadStatusScrapy.items import RoadstatusscrapyItem

#TODO 后期要写入配置文件
TRAFFIC_STATUS_KEY_LIST = ["a1159650f573893560c1a783f41ed595","c8ab5db12998d42492c7d484abe61a4d","3e891357cb7611d22185afe02d98d57f"]

class keyGenerate(object):
    def __init__(self, keyList, start=0, end=-1):
        self.keyList = keyList
        self.start = start
        self.end = end if end != -1 else len(keyList)
        self.cur = start
        self.length = self.end - self.start
    
    def getKey(self):
        key = self.keyList[self.cur]
        self.cur = (self.cur + 1)%self.length
        return key


class AmapSpider(scrapy.Spider):
    name = 'Amap'
    domain = 'https://restapi.amap.com/v3/traffic/status/rectangle?key={key}&level=6&extensions=all&rectangle='
    time = time()

#TODO　后期要写入配置文件
    class args:
        ##左下和右上的坐标
        leftLng = 103.710900
        leftLat = 30.471200
        rightLng = 104.445600
        rightLat = 30.843900
        rows = 11
        cols = 11

    def start_requests(self):
        self.time = time()
        keys = keyGenerate(TRAFFIC_STATUS_KEY_LIST)
        leftLng, leftLat, rightLng, rightLat, rows, cols = self.args.leftLng, self.args.leftLat, self.args.rightLng, self.args.rightLat, self.args.rows, self.args.cols
        widthlng = round(abs(leftLng - rightLng)/rows, 2)
        widthlat = round(abs(leftLat - rightLat)/cols, 2)
        urls = []
        for row in range(0, rows):
            startLat = round(leftLat+row*widthlat, 6)
            endLat = round(startLat+widthlat, 6)
            for col in range(cols):
                startLng = round(leftLng+col*widthlng, 6)
                endLng = round(startLng+widthlng, 6)
                locStr = str(startLng)+","+str(startLat) + \
                    ";"+str(endLng)+","+str(endLat)
                urls.append(self.domain.format(key=keys.getKey())+locStr)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body, encoding='utf-8')
        # self.logger.info([item for item in data['trafficinfo']['roads']])
        item = RoadstatusscrapyItem()
        for record in data['trafficinfo']['roads']:
            item['timeStamp'] = int(self.time*1000)
            item['name'] = record.get('name')
            item['status'] = record.get('status')
            item['direction'] = record.get('direction')
            item['angle'] = record.get('angle')
            item['speed'] = record.get('speed')
            item['lcodes'] = record.get('lcodes')
            item['polyline'] = record.get('polyline')
            yield item

# if __name__ == '__main__':
#     keys = keyGenerate(['1','2'])
#     keys.getKey()
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     print(keys.getKey())
#     keys.getKey()
#     keys.getKey()