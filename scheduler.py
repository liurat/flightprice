import time
import schedule
import logging
from datetime import datetime
from ctrip_crawler import CtripCrawler
from scheduler_config import *

# 配置日志
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=LOG_FORMAT
)

def run_crawler():
    """执行爬虫任务"""
    try:
        logging.info("开始执行爬虫任务")
        crawler = CtripCrawler()
        flight_data = crawler.get_flight_prices()
        crawler.save_to_excel(flight_data)
        logging.info(f"爬虫任务执行完成，获取到 {len(flight_data)} 条数据")
    except Exception as e:
        logging.error(f"爬虫任务执行出错: {str(e)}")

def main():
    """主函数"""
    logging.info("定时任务启动")
    
    # 设置定时任务
    schedule.every(SCHEDULER_INTERVAL).hours.do(run_crawler)
    
    # 如果配置了立即执行，则先执行一次
    if RUN_IMMEDIATELY:
        logging.info("立即执行一次爬虫任务")
        run_crawler()
    
    # 持续运行定时任务
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次是否有待执行的任务
        except KeyboardInterrupt:
            logging.info("定时任务被手动终止")
            break
        except Exception as e:
            logging.error(f"定时任务执行出错: {str(e)}")
            time.sleep(60)  # 发生错误时等待一分钟后继续

if __name__ == "__main__":
    main() 