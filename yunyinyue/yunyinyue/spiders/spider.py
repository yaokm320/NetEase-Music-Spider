from scrapy import Spider,Request
from yunyinyue.items import YunyinyueItem
from urllib.parse import quote
from lxml import etree

class YunyinyueSpider(Spider):

    name = 'yunyinyue'

    def start_requests(self):
        singer = '周杰伦'
        raw_url = 'http://www.xiami.com/search/song/page/{}?spm=a1z1s.3521869.0.0.Nv2jr2&key={}&category=-1'

        for i in range(44):
            url = raw_url.format(str(i+1), quote(singer))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = etree.HTML(response.text)
        hrefs = selector.xpath('//td[@class="song_name"]/a[1]/@href')
        titles = selector.xpath('//td[@class="song_name"]/a[1]/@title')
        for href,title in zip(hrefs, titles):
            yield Request(url=href, callback=self.parse_content, meta={'title': title})

    def parse_content(self,response):
        selector = etree.HTML(response.text)

        song_list = selector.xpath('//div[@class="lrc_main"]/text()')
        song = []
        for line in song_list:
            song.append(line.strip())
        result = '，'.join(song)
        item = YunyinyueItem()
        item['title'] = response.meta['title']
        item['song'] = result
        yield item



# 测试之用
# class YunyinyueSpider(Spider):
#
#     name = 'yunyinyue'
#
#     def start_requests(self):
#         singer = '周杰伦'
#         url = 'http://www.xiami.com/search/song/page/15?spm=a1z1s.3521869.0.0.Nv2jr2&key={}&category=-1'.format(quote(singer))
#
#
#         yield Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         selector = etree.HTML(response.text)
#         href = selector.xpath('//td[@class="song_name"]/a[1]/@href')[0]
#         title = selector.xpath('//td[@class="song_name"]/a[1]/@title')[0]
#         # for href,title in zip(hrefs, titles):
#         yield Request(url=href, callback=self.parse_content, meta={'title': title})
#
#     def parse_content(self,resposne):
#         selector = etree.HTML(resposne.text)
#         raw_song = selector.xpath('//div[@class="lrc_main"]/text()')
#         song = []
#         for line in raw_song:
#             song.append(line.strip())
#         result = '，'.join(song)
#         title = resposne.meta['title']
#         print('这是歌词：',result)
#         print('这是歌名：',title)


