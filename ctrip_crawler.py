import time
import json
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from airport_codes import get_city_name
import re

class CtripCrawler:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # 新版Chrome的无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
        
        # Mac系统特定的设置
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        try:
            service = Service('/opt/homebrew/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome驱动设置成功")
        except Exception as e:
            print(f"设置Chrome驱动时出错: {str(e)}")
            print("请确保已安装Chrome浏览器，并且版本与ChromeDriver兼容")
            raise
        
    def get_flight_prices(self):
        """获取航班价格信息"""
        url = CTRIP_URL_TEMPLATE.format(
            departure=DEPARTURE_CODE,
            destination=DESTINATION_CODE,
            date=DEPARTURE_DATE
        )
        
        try:
            print(f"正在访问URL: {url}")
            print(f"出发地: {DEPARTURE_CITY}({DEPARTURE_CODE})")
            print(f"目的地: {DESTINATION_CITY}({DESTINATION_CODE})")
            print(f"出发日期: {DEPARTURE_DATE}")
            print(f"目标航班: {', '.join(TARGET_FLIGHTS)}")
            
            self.driver.get(url)
            
            # 等待页面加载
            print("等待页面加载...")
            time.sleep(5)  # 初始等待

            # 自动下拉页面，加载更多航班
            max_retries = 15  # 增加最大重试次数
            no_update_count = 0  # 连续无更新的次数
            last_flight_count = 0  # 上一次的航班数量
            
            for i in range(max_retries):
                # 获取当前航班数量
                current_flights = self.driver.find_elements(By.CSS_SELECTOR, ".flight-list .flight-item")
                current_count = len(current_flights)
                
                print(f"当前航班数量: {current_count}")
                
                # 如果航班数量没有增加，增加无更新计数
                if current_count == last_flight_count:
                    no_update_count += 1
                    print(f"航班数量未增加，连续 {no_update_count} 次无更新")
                    if no_update_count >= 3:  # 如果连续3次无更新，尝试点击"加载更多"按钮
                        try:
                            load_more = self.driver.find_element(By.CSS_SELECTOR, ".load-more")
                            if load_more.is_displayed():
                                load_more.click()
                                print("点击了加载更多按钮")
                                time.sleep(3)
                                no_update_count = 0
                                continue
                        except:
                            pass
                    if no_update_count >= 5:  # 如果连续5次无更新，认为已加载完所有航班
                        print("连续多次无更新，停止加载")
                        break
                else:
                    no_update_count = 0  # 重置无更新计数
                    print(f"发现新航班，数量从 {last_flight_count} 增加到 {current_count}")
                
                # 使用更精确的滚动方式
                try:
                    # 尝试滚动到最后一个航班元素
                    if current_flights:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", current_flights[-1])
                    else:
                        # 如果没有找到航班元素，则滚动到页面底部
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except:
                    # 如果滚动失败，使用普通的页面滚动
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                print(f"已下拉 {i+1} 次，等待新内容加载...")
                time.sleep(3)  # 等待新内容加载
                
                last_flight_count = current_count

            # 保存页面源码
            page_source = self.driver.page_source
            with open('page_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print("页面源码已保存到 page_source.html")
            
            # 获取航班信息
            print("开始获取航班信息...")
            
            selectors = [
                ".flight-list .flight-item",
                ".flight-list-item",
                ".flight-item",
                "[class*='flight']",
                "[class*='Flight']"
            ]
            
            flights = []
            for selector in selectors:
                try:
                    flights = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if flights:
                        print(f"使用选择器 '{selector}' 找到 {len(flights)} 个航班")
                        break
                except Exception as e:
                    print(f"选择器 '{selector}' 未找到元素")
                    continue
            
            if not flights:
                print("未找到任何航班信息，请检查页面源码")
                return []
            
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            print(f"数据获取时间: {current_time}")
            
            flight_data = []
            for flight in flights:
                try:
                    print("\n航班元素HTML:")
                    print(flight.get_attribute('outerHTML'))

                    airline_names = flight.find_elements(By.CSS_SELECTOR, ".airline-name")
                    
                    # 获取航空公司名称
                    airline = ""
                    if len(airline_names) > 1:
                        airline = "+".join([a.text.strip() for a in airline_names if a.text.strip()])
                    elif airline_names:
                        airline = airline_names[0].text.strip()

                    # 获取航班号
                    flight_no = ""
                    
                    # 首先尝试从plane-No类获取航班号
                    plane_nos = flight.find_elements(By.CSS_SELECTOR, ".plane-No")
                    if plane_nos:
                        for plane_no in plane_nos:
                            if plane_no.text.strip():
                                flight_text = plane_no.text.strip()
                                flight_match = re.search(r'([A-Z0-9]+)', flight_text)
                                if flight_match:
                                    flight_no = flight_match.group(1)
                                    break
                    
                    # 如果没有找到航班号，尝试从id属性中提取
                    if not flight_no:
                        try:
                            plane_div = flight.find_element(By.CSS_SELECTOR, ".plane")
                            plane_id = plane_div.get_attribute('id')
                            if plane_id:
                                flight_match = re.search(r'([A-Z0-9]+)_', plane_id)
                                if flight_match:
                                    flight_no = flight_match.group(1)
                        except:
                            pass

                    # 如果还是没有找到航班号，尝试从航空公司名称中提取
                    if not flight_no and airline:
                        flight_match = re.search(r'([A-Z0-9]+)$', airline)
                        if flight_match:
                            flight_no = flight_match.group(1)

                    # 打印调试信息
                    print(f"航空公司: {airline}")
                    print(f"航班号: {flight_no}")

                    # 只处理目标航班
                    if flight_no in TARGET_FLIGHTS:
                        departure_time = flight.find_element(By.CSS_SELECTOR, ".depart-box .time").text
                        arrival_time = flight.find_element(By.CSS_SELECTOR, ".arrive-box .time").text
                        price = flight.find_element(By.CSS_SELECTOR, ".price").text.replace('¥', '')

                        flight_data.append({
                            "数据获取时间": current_time,
                            "航空公司": airline,
                            "航班号": flight_no,
                            "出发时间": departure_time,
                            "到达时间": arrival_time,
                            "价格": price
                        })
                        print(f"已获取目标航班信息: {airline} {flight_no}")
                except Exception as e:
                    print(f"解析航班信息时出错: {str(e)}")
                    continue
            
            return flight_data
        except Exception as e:
            print(f"获取航班信息时出错: {str(e)}")
            return []
        finally:
            self.driver.quit()

    def save_to_excel(self, flight_data):
        """将航班数据保存到Excel文件"""
        if not flight_data:
            print("没有找到航班数据")
            return
            
        filename = f"flights_{DEPARTURE_CITY}_{DESTINATION_CITY}_{DEPARTURE_DATE}.xlsx"
        
        try:
            # 尝试读取现有文件
            existing_df = pd.read_excel(filename)
            # 将新数据添加到现有数据中
            new_df = pd.DataFrame(flight_data)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            # 保存合并后的数据
            combined_df.to_excel(filename, index=False)
            print(f"数据已追加到 {filename}")
        except FileNotFoundError:
            # 如果文件不存在，创建新文件
            df = pd.DataFrame(flight_data)
            df.to_excel(filename, index=False)
            print(f"数据已保存到新文件 {filename}")

def main():
    crawler = CtripCrawler()
    flight_data = crawler.get_flight_prices()
    crawler.save_to_excel(flight_data)

if __name__ == "__main__":
    main() 