import time
import random
import json
from selenium import webdriver
from spider.spider.DrugExplainDetail.config import spider_config

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
        driver = webdriver.Chrome(options=options)
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

    def medicine_descripe(self, base_url, start_page, end_page, data_path):

        # 进入 DRUG_EXPLAIN 页面
        for page in range(start_page, end_page + 1):
            page_url = base_url + '/' + str(page)

            self.driver.get(page_url)
            self.driver.refresh()
            time.sleep(random.randint(5, 8) / 10)
            page_source = self.driver.page_source

            file_path = data_path + f'drug_explain_detail_{str(page)}.txt'

            with open(file_path, 'w+') as f:
                f.write(page_source)


if __name__ == '__main__':
    menet = MenetSpider()
    menet._login()

    start_page = 126715
    end_page = 166100
    data_path = spider_config.DATA_SAVE_PATH + '/' + '100001-150000' + '/'

    base_url = spider_config.DRUG_EXPLAIN_DETAIL
    menet.medicine_descripe(base_url, start_page, end_page, data_path)
