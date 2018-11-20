from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
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
import math
import datetime
def get_shop_detail(self,_str):
    p = PyQuery(_str);
    p('.ctd_content_controls').remove();
    return p.text();


fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='dl > dt > a'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='dl > dt > a',attr='href', is_debug=True,is_info=True),
)
page_shop_1 = Page(name='千岛湖游记店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='body > div.content.cf > div.main > div.search-content.cf > div > div.result > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_TAG, css_selector='body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content > div.ctd_content_controls.cf > div', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_DETAIL, css_selector='body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content',attr='innerHTML', filter_func=get_shop_detail, is_info=False)
)
page_shop_2 = Page(name='携程游记详情页面', fieldlist=fl_shop2)



class XieChengYouSpider(TravelDriver):

    def get_shop_info_list(self):


        self.fast_get_page(url='http://you.ctrip.com/')
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="#gsSearch", text=self.data_region)
        time.sleep(5)
        self.fast_click_page_by_css_selector(click_css_selector='#SearchBtn')
        time.sleep(10)
        self.fast_click_page_by_css_selector(click_css_selector='body > div.content.cf > div.main > div.search-content.cf > ul > li.current > a > span')
        # #body > div.content.cf > div.main > div.search - content.cf > div > div.result > div.desNavigation.cf > p > span > a.left_arrow
        # body > div.content.cf > div.main > div.search - content.cf > div > div.result > div.desNavigation.cf > p > span > em.right_arrow
        self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页', is_proxy=False,
                                                                                 main_pagefunc=PageFunc(
                                                                                     self.from_page_get_data_list,
                                                                                     page=page_shop_1)))

    def get_shop_detial(self):
        self.fast_new_page(url="http://www.baidu.com");
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='localhost').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_url'):
                shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))
        for i in range(len(shop_name_url_list)):
            self.fast_new_page(url='http://www.baidu.com');
            self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
            # while (True):
            #     self.is_ready_by_proxy_ip()
            #     self.switch_window_by_index(index=-1)
            #     self.deal_with_failure_page()
            #     self.fast_new_page(url=shop_name_url_list[i][1])
            #     time.sleep(1)
            #     self.switch_window_by_index(index=-1)  # 页面选择
            #     if '请求数据错误' in self.driver.title:
            #         self.info_log(data='关闭验证页面!!!')
            #         self.close_curr_page()
            #     else:
            #         break

            self.fast_new_page(url=shop_name_url_list[i][1])
            self.fast_click_first_item_same_page_by_partial_link_text(link_text='只看文字')
            data = self.from_fieldlist_get_data(page=page_shop_2)
            self.update_data_to_mongodb(shop_collcetion,
                                        self.merge_dict(self.get_data_key(), {FieldName.SHOP_URL: shop_name_url_list[i][1]}), data)
            self.close_curr_page();

    def run_spider(self):

       #self.get_shop_info_list()

       self.get_shop_detial()