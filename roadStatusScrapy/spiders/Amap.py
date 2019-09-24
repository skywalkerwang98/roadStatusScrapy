# -*- coding: utf-8 -*-
import scrapy
import json
from time import time
from roadStatusScrapy.items import RoadstatusscrapyItem

#TODO 后期要写入配置文件
TRAFFIC_STATUS_KEY = "6360bd48f5dde0b59ae19fc88f7ee309"

class AmapSpider(scrapy.Spider):
    name = 'Amap'
    domain = 'https://restapi.amap.com/v3/traffic/status/rectangle?key={key}&level=6&extensions=all&rectangle='.format(key=TRAFFIC_STATUS_KEY)
    time = time()

#TODO　后期要写入配置文件
    class args:
        leftLng = 106.309736
        leftLat = 29.450751
        rightLng = 106.741362
        rightLat = 29.728119
        rows = 6
        cols = 6

    def start_requests(self):
        self.time = time()
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
                urls.append(self.domain+locStr)
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
        