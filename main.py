import re
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class King(object):

    def __init__(self, acc, pwd, opt):
        self.acc = acc
        self.pwd = pwd
        self.driver = Chrome(options=opt)  # 创建Chrome无界面对象

    def login(self):
        self.driver.get('http://www.uucps.edu.cn/')
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="loginAbleSky"]/a[1]').click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最新页面
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="pc-form"]/div[1]/div[2]/div[1]/div[1]/input').send_keys(self.acc)
        self.driver.find_element_by_xpath('//*[@id="pc-form"]/div[1]/div[2]/div[1]/div[2]/input').send_keys(self.pwd)
        self.driver.find_element_by_xpath('//*[@id="pc-form"]/div[1]/div[2]/div[1]/div[4]/button').click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最新页面
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="J_userGradeList"]/div/div[3]/p[1]/a/i').click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最新页面
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[2]/a').click()
        time.sleep(1)
        name = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/span/a')
        who = str(name.text)
        time.sleep(1)
        all_work = self.driver.find_element_by_xpath('//*[@id="J_tabsContent"]/div/div[1]/div/p[1]')
        all_time = str(all_work.text)
        no_work = self.driver.find_element_by_xpath('//*[@id="J_tabsContent"]/div/div[1]/div/p[2]')
        no_time = str(no_work.text)
        content = who + "   " + all_time + "   " + no_time
        print(content)
        print("=" * 60)

    def watch(self):
        self.driver.refresh()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="J_tabsContent"]/div/ul/li[2]/span').click()
        time.sleep(3)
        time_all = self.driver.find_element_by_xpath('//*[@id="J_myOptionRecords"]/tbody/tr[2]/td[2]/span')
        time_all = str(time_all.text)
        allin = re.split(r'[:：]', time_all)
        res = [ele.lstrip('0') for ele in allin]
        time_h = res[0]
        time_m = res[1]
        time_s = res[2]
        try:
            time_allin = int(time_h) * 3600 + int(time_m) * 60 + int(time_s)
        except:
            time_allin = int(time_m) * 60 + int(time_s)
        print("总时长:%s秒" % time_allin)
        time_per = self.driver.find_element_by_xpath('//*[@id="J_myOptionRecords"]/tbody/tr[2]/td[5]/div/p')
        time_per = str(time_per.text)
        print("已学习:%s" % time_per)
        try:
            time_need = time_allin * (1 - int(time_per.strip('%')) / 100)
        except:
            time_need = time_allin
        print("还需要学习:%s秒" % time_need)
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="J_myOptionRecords"]/tbody/tr[2]/td[6]/a').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最新页面
        time.sleep(1)
        title = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[1]/span')
        title = str(title.text)
        print("正在学习:%s" % title)
        time.sleep(int(time_need))  # 扫描监控时间
        print("内容学习完成，进入缓冲时间为5分钟，确保内容学习完成")
        time.sleep(300)
        self.driver.close()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换到最新页面

    def main(self):
        self.login()
        for u in range(1, 30):
            try:
                self.watch()
            except Exception as e:
                pass
            print("-" * 40)
        self.driver.quit()


if __name__ == '__main__':
    opt = Options()
    opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    opt.add_argument('window-size=950x955')  # 设置浏览器分辨率（宽，高）
    opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    opt.add_argument('user-agent=%s' % user_agent)
    opt.add_argument("--mute-audio")
    # opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
    opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # 用cmd打开chrome --remote-debugging-port=9222
    king = King("17717691506", "zty03163727", opt)
    king.main()
