from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import getpass
from datetime import datetime
import os
import pandas as pd 
class FacebookGroupScraper:
    def __init__(self):
        print('\n===FACEBOOK GROUP MEMBER SCRAPER===')
        self.get_config()
        self.setup_driver()
    def get_config(self):
        try:
            print('Nhap thong tin dang nhap:')
            self.email = input('Email/Username: ').strip()
            self.password = getpass.getpass('Password: ')

            # ID group
            print('\n Nhap ID group facebook:')
            self.group_id = input('Group ID: ').strip()

            # So lan scroll
            print('\n So lan scroll de Load ')
            self.scroll_count = int(input('So lan scroll (mac dinh 5)') or "5")
        except Exception as e:
            print(f"Loi cau hinh:{e}")
            pass

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            print(f"Loi khoi tao trinh duyet:{e}")
    
    def login(self):
        try:
            self.driver.get('https://www.facebook.com')
            
            email_input = self.driver.find_element(By.ID,'email')
            email_input.send_keys(self.email)

            pass_input = self.driver.find_element(By.ID,'pass')
            pass_input.send_keys(self.password)

            login_button = self.driver.find_element(By.NAME, 'login')
            login_button.click()

            time.sleep(10)
            print("Dang nhap thanh cong")
            return True
        except Exception as e:
            print(f'Loi dang nhap: {e}')
            return False
def get_group_member(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(10)

            members = set()  # Sử dụng set để tránh trùng lặp
            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll lần {i+1}/{self.scroll_count}")
                
                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                for user in user_elements:
                    try:
                        href = user.get_attribute('href')
                        name = user.text.strip()
                        if '/user/' in href and name:
                            members.add((href, name))
                            print(href, "-", name)
                    except Exception as e:
                        print(f"Lỗi xử lý phần tử: {e}")
                        continue

            # Chuyển đổi dữ liệu sang DataFrame
            member_list = list(members)
            df = pd.DataFrame(member_list, columns=['Profile Link', 'Name'])

            # Lưu vào file Excel
            output_file = f"facebook_group_{self.group_id}_members.xlsx"
            df.to_excel(output_file, index=False)
            print(f"Danh sách thành viên đã được lưu vào file: {output_file}")

            return member_list

        except Exception as e:
            print(f"Lỗi thu thập thành viên: {e}")
            return None

def main():
    scraper = None
    try:
        scraper = FacebookGroupScraper()
        if scraper.login():
            scraper.get_group_member()
            time.sleep(10)
        time.sleep(10)
    except Exception:
        pass          
if __name__ == '__main__' :
    main()