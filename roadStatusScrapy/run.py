#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# @File    : run_spider.py
# @Date    : 2018-08-06
# @Author  : Peng Shiyu

from multiprocessing import Process
from scrapy import cmdline
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('roadStatusCallLog.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')

# 配置参数即可, 爬虫名称，运行频率
confs = {"spider_name": "Amap",
         "frequency": 2 * 60}


def start_spider(spider_name):
    args = ["scrapy", "crawl", spider_name]
    # while True:
    start = time.time()
    p = Process(target=cmdline.execute, args=(args,))
    p.start()
    p.join()
    logger.info("### use time: %s" % (time.time() - start))
    # time.sleep(frequency)


if __name__ == '__main__':
    while True:
        process = Process(target=start_spider, args=(confs["spider_name"], ))
        process.start()
        time.sleep(confs["frequency"])
