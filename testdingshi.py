import os
#定时启动
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# os.system("gnome-terminal -e 'pythorun_spider.py 1 携程 千岛湖 景点'");
def start_spider(data_website,data_region,index):
  print(index)
  #os.system("gnome-terminal -e 'bash -c \"python run_spider.py 1 携程 千岛湖 景点; exec bash\"'")
  os.system("gnome-terminal -e 'bash -c \"python run_spider.py "  + str(index) +  " " + data_website
            + " " + data_region + " " + "景点" +
  "; exec bash\"'")
  #os.system("python run_spider.py " + str(index) + " " + data_website + " " + data_region + " " + "景点");
'''

'''
#根据日期奇偶性 判断今日执行什么爬虫
#regions的配置
#在服务器上跑携程和马蜂窝的爬虫
#在Ubuntu上跑驴妈妈和大众点评飞猪的爬虫
#在windows上跑途牛和去哪儿的爬虫
#飞猪晚上走的时候单独开启
server_regions = {
'携程':['千岛湖','西湖','西溪','溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔古镇','神仙居','天台山','根宫佛国文化旅游区','鲁迅','嘉兴南湖','黄山','三清山'],
'马蜂窝':[
'千岛湖','杭州西湖','杭州西溪','宁波溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔','神仙居','台州天台山','根宫佛国文化旅游区','鲁迅','嘉兴南湖','黄山','三清山']
};
ubuntu_regions = {
 '驴妈妈':[
'千岛湖','西湖','西溪','溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔古镇','神仙居','台州天台山','根宫佛国文化旅游区','鲁迅','嘉兴南湖','黄山','三清山'],
'大众点评':[
'千岛湖','西湖','西溪','溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔','神仙居','天台山','根宫佛国文化旅游区','鲁迅','南湖','黄山','三清山']
}
windows_regions = {
'去哪儿':[
'千岛湖','杭州西湖','西溪','溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔','神仙居','台州天台山','根宫佛国文化旅游区','鲁迅','嘉兴南湖','黄山','三清山'],

'途牛':[
'千岛湖','西湖','西溪','溪口','乌镇','西塘','横店','江郎山'
                    '雁荡山','普陀山','南浔','神仙居','天台山','根宫佛国文化旅游区','鲁迅','嘉兴南湖','黄山','三清山'],
};
day = datetime.datetime.now().day
print(day)
sched = BlockingScheduler()
start_hour = 19;
start_minuate = 48;
index = 0;

if(day % 2 == 0):
    website = '携程';
else:
    website = '马蜂窝';

region_search_keys = server_regions[website];



for i,region in enumerate(region_search_keys):
      start_minuate += 5;
      if (start_minuate >= 60):
          start_minuate = 0;
          start_hour += 1;
      if(start_hour >= 24):
        start_hour = 0;
      minuate = start_minuate;
      hour = start_hour;
      print(start_minuate);
      index += 1;
      sched.add_job(start_spider, 'cron', day_of_week='0-6', hour=hour, minute=minuate,args=[website,region,index]);
sched.start();
