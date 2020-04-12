from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import smtplib
import config
from time import sleep


class Bot_ikariam:

    attack_el = '//*[@id="js_MilitaryMovementsFleetMovementsTable"]/table/tbody/tr[contains(@class, "hostile")]'

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()
        self.name = ''
        self.attackers = []
        self.attackers2 = []

    def get_browser(self):
        self.driver.get('https://lobby.ikariam.gameforge.com/en_US/hub')

    def login_tab(self):
        login_tab_btn = self.driver.find_element_by_xpath(
            "//*[@id='loginRegisterTabs']/ul/li/span")
        login_tab_btn.click()

    def email(self):
        email_address = config.GAME_LOGIN
        email_input = self.driver.find_element_by_css_selector(
            "input[type='email']")
        email_input.send_keys(email_address)

    def password(self):
        password_login = config.GAME_PASSWORD
        password_input = self.driver.find_element_by_css_selector(
            "input[type='password']")
        password_input.send_keys(password_login)

    def login(self):
        login_btn = self.driver.find_element_by_xpath(
            "//form[@id='loginForm']/p/button[@type='submit']")
        self.driver.implicitly_wait(100)
        login_btn.click()

    def join(self):
        join_game_btn = self.driver.find_element_by_css_selector(
            "#joinGame > button")
        join_game_btn.click()

    def switch_tab(self):
        self.driver.switch_to_window(self.driver.window_handles[1])

    def military_tab(self):
        btn = self.driver.find_element_by_xpath(
            '//*[@id="js_GlobalMenu_military"]')
        btn.click()

    def check_attack(self):
        try:
            attacks = self.driver.find_elements_by_xpath(self.attack_el)
            for num in range(0, len(attacks)):
                name = self.check_name(num)
                city = self.check_city(num)
                if {"player": name, "city": city} not in self.attackers:
                    self.attackers.append({"player": name, "city": city})

            if str(self.attackers) != str(self.attackers2):
                self.attackers2 = self.attackers
                self.send_email()

            print('Attack')
            self.check_again()
        except:
            print('No Attack')
            self.check_again()

    def check_name(self, num):
        name_el = self.driver.find_element_by_xpath(
            f'{self.attack_el}[{num+1}]/td[@class="source"]/a')
        name = name_el.text
        return name

    def check_city(self, num):
        city_el = self.driver.find_element_by_xpath(
            f'{self.attack_el}[{num+1}]/td[@class="source"]/span')
        city = city_el.text
        return city

    def send_email(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.PASSWORD)
            message = ''
            for asd in self.attackers:
                message = message + \
                    f'\n {asd["city"]} is attacking me from {asd["player"]}'
            print(message)
            server.sendmail(config.EMAIL_ADDRESS,
                            config.EMAIL_ADDRESS, message)
            server.quit()
            print('Email Success')
        except:
            print('Email Failed')

    def run_bot(self):
        self.get_browser()
        self.login_tab()
        self.email()
        self.password()
        self.login()
        self.join()
        self.switch_tab()
        self.military_tab()
        self.check_attack()

    def check_again(self):
        # print('again')
        sleep(15)
        self.military_tab()
        self.check_attack()


game = Bot_ikariam()
game.run_bot()


# //*[@id = "js_MilitaryMovementsFleetMovementsTable"]/table/tbody/tr[2]/td[6]
