from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from pyquery import PyQuery as pq
from selenium import webdriver
import re
import time
import json
from pyquery import PyQuery

def get_shop_address(self,_str):
    return ""
def get_shop_grade(self,_str):
    return ""
def get_shop_feature(self,_str):
    return ""
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='a > div.search-scenic-content > h3'),
#\31 302 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
#\32 0808 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='a > div.search-scenic-content > div.search-scenic-wrapper > div.search-scenic-price > span',is_info=True),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='a',attr='href', is_debug=True,is_info=True),
    #img还有些许问题
#\33 6822720 > div:nth-child(1) > div
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > div.img-container.lazy-img-box.fl > img', attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= '',filter_func=get_shop_address, is_info=True),
    #这里应该做一个转换
#\34 187 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='',filter_func=get_shop_grade, is_info=True),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='a > div.search-scenic-content > div.search-scenic-wrapper > div.search-scenic-detail > p',is_info=True),
    #无shop_feature

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='',filter_func=get_shop_feature, is_info=True),

    Field(fieldname=FieldName.SHOP_RATE,css_selector='',filter_func=get_shop_rate, is_info=True)
)
page_shop_1 = Page(name='途牛景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#search-container > section > div > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

def get_comment_grade(self,_str):
    doc = pq(_str)
    if (doc('.star-active').length) == 3:
        return "5"
    elif (doc('.star-active').length) == 2:
        return "2.5"
    else:
        return "0"
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#detail-placeholder > div.main > div.banner > div.footer-info > div.scenic-info > span', is_info=True,is_isolated=True),
#app > div > div.poi-rate-container > div:nth-child(2) > div.rate-content-container > div
#app > div > div.poi-rate-container > div:nth-child(7) > div.rate-content-container > div
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div > div.remark-content > span', is_info=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.user-info.clearfix > div.user-cell > span.user-name', is_info=True),
    #comment_grade有待商榷
    Field(fieldname=FieldName.COMMENT_GRADE, css_selector='div > div.user-info.clearfix > div.attitude', attr='innerHTML',filter_func=get_comment_grade, is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.user-info.clearfix > div.user-cell > span.remark-time', is_info=True),
)
page_comment_1 = Page(name='飞猪景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#detail-placeholder > div.main > div.tabs-box > div.tab-container > div:nth-child(3) > div > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)
class TuniuMobileSpotSpider(TravelDriver):

    def get_shop_info_list(self):
        self.fast_get_page(url='https://m.tuniu.com/m2015/mpChannel/search?searchType=1&catId=0&poiId=0&productType=4&keyword=' + self.data_region)
        shop_data_list = self.from_page_get_data_list(page=page_shop_1)

    def get_comment_info_list(self):
       shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 host='localhost').get_collection()
       shop_name_url_list = list()
       for i in shop_collcetion.find(self.get_data_key()):
           if i.get('shop_url'):
               shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))

       for i in range(len(shop_name_url_list)):
           # 可能会有反爬
           self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
           self.fast_new_page(url=shop_name_url_list[i][1])
           time.sleep(20)
           self.fast_click_page_by_css_selector('#detail-placeholder > div.main > div.tabs-box > div:nth-child(1) > ul > li:nth-child(3)')

           comment_data_list = self.from_page_get_data_list(page=page_comment_1)
           self.close_curr_page()



    def run_spider(self):
       #self.get_shop_info_list()
       #self.get_shop_detail()
       self.get_comment_info_list()