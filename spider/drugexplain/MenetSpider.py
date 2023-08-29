import time
import random
import json
from selenium import webdriver
from spider.spider.drugexplain.config import spider_config

# webdriver setup
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
# 隐藏"Chrome正在受到自动软件的控制"
options.add_argument('disable-infobars')
# 使用headless无界面浏览器模式
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')


class MenetSpider():
    def __init__(self):
        self.CHROMEDRIVER_PATH = spider_config.CHROMEDRIVER_PATH
        self.INIT_URL = spider_config.LOGIN_URL
        self.account = spider_config.ACCOUNT
        self.retry_times = spider_config.RETRY_TIMES

    def _login(self):
        # create webdriver and search linkedin login page
        driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)
        self.driver = driver

        # 进入初始化界面
        self.driver.get(self.INIT_URL)

        # 输入账号密码登录
        time.sleep(random.randint(50, 80) / 10)
        self.driver.find_element(by='xpath', value='*//input[@placeholder="请输入用户名"]').send_keys(self.account['account'])
        self.driver.find_element(by='xpath', value='*//input[@placeholder="请输入密码"]').send_keys(self.account['password'])
        self.driver.find_element(by='xpath', value='*//button[@class="el-button el-button--success el-button--large"]').click()

        time.sleep(random.randint(50, 80) / 10)

        # 存储 cookie and driver
        cookie_list = driver.get_cookies()
        self.cookie = cookie_list

    def _save_cookie(self, file_path):
        with open(file_path, 'w+') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.cookie))

    def _load_cookie(self, file_path):
        # create webdriver and search linkedin login page
        driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)

        # 进入初始化界面
        driver.get(self.INIT_URL)

        # 首先清除由于浏览器打开已有的cookies
        self.driver.delete_all_cookies()

        with open(file_path, 'r') as cookief:
            cookieslist = json.load(cookief)
            for cookie in cookieslist:
                self.driver.add_cookie(cookie)

        self.driver.refresh()
        # 存储 cookie and driver
        cookie_list = driver.get_cookies()
        self.cookie = cookie_list
        self.driver = driver

    def medicine_descripe(self, start_page, end_page, data_path):

        def get_current_page_num():
            cnt = 0
            while cnt < self.retry_times:
                try:
                    return eval(self.driver.find_element(by='xpath', value='*//ul[@class="el-pager"]/li[@class="number active"]').text)
                except:
                    print(f"Function Retry: get_current_page_num, {cnt+1} / {self.retry_times}")
                    time.sleep(0.5)
                    cnt += 1

        def click_next_page():
            cnt = 0
            while cnt < self.retry_times:
                try:
                    self.driver.find_element(by='xpath', value='*//button[@class="btn-next"]').click()
                    return None
                except:
                    print(f"Function Retry: get_current_page_num, {cnt + 1} / {self.retry_times}")
                    time.sleep(0.5)
                    cnt += 1

        def click_target_page(page_num):
            cnt = 0
            while cnt < self.retry_times:
                try:
                    element = self.driver.find_element(by='xpath', value='*//ul[@class="el-pager"]/li[@class="number active"]')
                    self.driver.execute_script(f"arguments[0].innerHTML = '{page_num}';", element)
                    self.driver.find_element(by='xpath', value='*//ul[@class="el-pager"]/li[@class="number active"]').click()
                    return None
                except:
                    print(f"Function Retry: get_current_page_num, {cnt + 1} / {self.retry_times}")
                    time.sleep(0.5)
                    cnt += 1

        # 进入 DRUG_EXPLAIN 页面
        self.driver.get(spider_config.DRUG_EXPLAIN)
        time.sleep(random.randint(100, 150) / 10)

        # 获取当前页面
        current_page = get_current_page_num()
        if current_page != start_page:
            click_target_page(str(start_page))

        current_page = get_current_page_num()
        while current_page < end_page:
            current_page = get_current_page_num()
            page_source = self.driver.page_source

            file_path = data_path + f'{str(start_page)}-{str(end_page)}drug_explain_{str(current_page)}.txt'

            with open(file_path, 'w') as f:
                f.write(page_source)

            click_next_page()


if __name__ == '__main__':
    menet = MenetSpider()
    menet._login()

    start_page = 8001
    end_page = 9000
    data_path = spider_config.DATA_SAVE_PATH + '/' + f'{str(start_page)}-{str(end_page)}' + '/'
    menet.medicine_descripe(start_page, end_page, data_path)

