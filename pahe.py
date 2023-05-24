import telebot
import base64
import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

bot = telebot.TeleBot('YOUR_BOT_TOKEN')
def extract_arg(arg):
    return arg.split()[1:]

def driversetup():    
    options = webdriver.ChromeOptions()
    #run Selenium in headless mode
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    #overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    #open Browser in maximized mode
    options.add_argument("start-maximized")
    #disable infobars
    options.add_argument("disable-infobars")
    #disable extension
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)
    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver

reallink = []
@bot.message_handler(commands=['sp'])
def gdtotme(message):
    link = extract_arg(message.text)
    message_ids= bot.reply_to(message,text=f"𝗕𝘆𝗽𝗮𝘀𝘀𝗶𝗻𝗴 𝗟𝗶𝗻𝗸 🔄",parse_mode='markdown',disable_web_page_preview=True).message_id
    url = link[0]
    total = []
    text1 = f"<b>Org Link : </b>{url}\n\n"
    driver = driversetup()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    for i in soup.find_all('a',{'class':'purple'},rel="nofollow noreferrer noopener"):
        print(i['href'])
        text1+=f"Link : {i['href']}\n\n"
    bot.edit_message_text(text=f"{text1}",
      chat_id=message.chat.id,
      message_id=message_ids,
      parse_mode="html",disable_web_page_preview=True)
    driver.quit()
    
@bot.message_handler(commands=['bp'])
def gdtotme(message):
    link = extract_arg(message.text)
    message_ids= bot.reply_to(message,text=f"𝗕𝘆𝗽𝗮𝘀𝘀𝗶𝗻𝗴 𝗟𝗶𝗻𝗸 🔄",parse_mode='markdown',disable_web_page_preview=True).message_id
    url = link[0]
    driver = driversetup()
    driver.get(url)
    time.sleep(8)
    driver.find_element("id", "soralink-human-verif-main").click()
    time.sleep(5)
    driver.find_element(By.ID, "generater").click()
    time.sleep(6)
    driver.find_element(By.CLASS_NAME,"spoint").click()
    driver.switch_to.window(driver.window_handles[1])
    html = driver.page_source
    text1=f"Org Link : {url}\n\nLink : {driver.current_url}\n\n"
    bot.edit_message_text(text=f"{text1}",
      chat_id=message.chat.id,
      message_id=message_ids,
      parse_mode="html",disable_web_page_preview=True)
    soup = BeautifulSoup(html,'lxml')
    text = soup.find_all('script')
    #                     match = re.search(r"[a-zA-Z1-90]+?=?='",str(text))
    #                     if match == None:
    match= re.search(r"atob\('[a-zA-Z1-90]+'",str(text))
    if match == None:
        match = re.search(r"[a-zA-Z1-90]+?=?='",str(text))
        reallink = base64.b64decode(match.group()).decode("utf-8")
        print(f"{reallink}")
        bot.edit_message_text(text=f"{text1}Bypassed Link : {reallink}",
              chat_id=message.chat.id,
              message_id=message_ids,
              parse_mode="html",disable_web_page_preview=True)
    driver.quit()
        
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
