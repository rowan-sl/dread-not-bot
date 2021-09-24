import logging
import pathlib
import os, sys

cwd_path = pathlib.PurePath(pathlib.Path(__file__))
main_path = str(cwd_path.parents[1])
log_path = str(pathlib.PurePath(main_path, "logs", "latest.log"))
driver_log_path = str(pathlib.PurePath(main_path, "logs", "gekodriver.log"))
#! add projects main dir to PYTHONPATH
sys.path.append(main_path)
if os.path.exists(log_path):
    os.remove(log_path)
from lib.customlog import CustomLoggerLevels
logging.setLoggerClass(CustomLoggerLevels)
logging.basicConfig(
    filename=log_path,
    level=15,#detail level
    format="[%(asctime)s] %(name)s/%(module)s/%(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("MAIN")
logger.info("Program Startup")
def log_detail(message):
    logger.log(15, message)
#? logger.detail is a custom logging level used instead of DEBUG (for most things that are not spammers), so that it hides other things DEBUG messages in the logs
logger.detail = log_detail
# selenium
import selenium
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import FirefoxWebElement
#builtin things
import re
import sys
import time
import threading, queue
import json
#installed modules

#other files
from lib.evaluate_str import evalueatestr

#import from file of config stuff
from config.conf import firefox_profile, owner_username, prefix
if firefox_profile is not None:
    profile = webdriver.FirefoxProfile(firefox_profile)# in seperate file bc the path has my name in it
    driver = webdriver.Firefox(profile, service_log_path=driver_log_path)
else:
    driver = webdriver.Firefox(service_log_path=driver_log_path)
driver.get("https://test.drednot.io")
time.sleep(1)
input("press enter once you have selected a ship")

chat_queue = queue.Queue()

banned_path = pathlib.Path(main_path, "database", "banned.json")
flag_path = pathlib.Path(main_path, "database", "flags.json")

with banned_path.open("r") as f:
    banned = json.load(f)

with flag_path.open("r") as f:
    flags = json.load(f)

# setup module thingy
from module_interface import ModuleController
mc = ModuleController(logger, chat_queue)

# unused
action_key_down_w = ActionChains(driver).key_down("w")
action_key_up_w = ActionChains(driver).key_up("w")
action_key_down_a = ActionChains(driver).key_down("a")
action_key_up_a = ActionChains(driver).key_up("a")
action_key_down_s = ActionChains(driver).key_down("s")
action_key_up_s = ActionChains(driver).key_up("s")
action_key_down_d = ActionChains(driver).key_down("d")
action_key_up_d = ActionChains(driver).key_up("d")
space_down = ActionChains(driver).key_down(Keys.SPACE)
space_up = ActionChains(driver).key_up(Keys.SPACE)

def sendchat(msg):
    logger.detail("sending chat")
    logger.detail(msg)
    if len(msg) < 300:
        driver.execute_script(
    f"""
    document.querySelector("#chat-send").click()
    document.querySelector("#chat-input").value = String(arguments[0])
    document.querySelector("#chat-input").value = String(arguments[0])
    document.querySelector("#chat-send").click()
    """, str(msg))
    else:
        print("message to long!")
        logger.warning("message to long to send")

def chat_sender():
    logger.detail("sender running")
    while True:
        time.sleep(1.1)
        msg = chat_queue.get()
        if type(msg) is str:
            if msg is None:
                logger.detail("recieved kill msg")
                while True:
                    try:
                        chat_queue.task_done()
                    except ValueError:
                        break
                logger.detail("exiting loop")
                break
            logger.detail("got new message to say")
            if len(msg) < 300:
                sendchat(msg)
            else:
                n = 299
                chunks = [msg[i:i+n] for i in range(0, len(msg), n)]
                for chunk in chunks:
                    time.sleep(1.1)
                    sendchat(chunk)
        elif type(msg) is dict:
            if "move" in msg.keys():
                movements = msg["move"]
                for action in movements:
                    direction = action[0]
                    duration = action[1]
                    if direction == "w": action_key_down_w.perform()
                    elif direction == "a": action_key_down_a.perform()
                    elif direction == "s": action_key_down_s.perform()
                    elif direction == "d": action_key_down_d.perform()
                    elif direction == "sp": space_down.perform()
                    time.sleep(duration)
                    if direction == "w": action_key_up_w.perform()
                    elif direction == "a": action_key_up_a.perform()
                    elif direction == "s": action_key_up_s.perform()
                    elif direction == "d": action_key_up_d.perform()
                    elif direction == "sp": space_up.perform()
        chat_queue.task_done()


def deal_with_message(msg):
    global flags, banned
    msg = str(msg)
    if msg == "":
        return
    if not "SharpFloof:" in msg:
        if flags["do_join_msg"]:
            # check for join/leave
            welcome_check:re.Match = re.search(r"^(.*) joined the ship.$", msg)
            if welcome_check:
                chat_queue.put(f"Welcome, {welcome_check.group(0)[:-17]}")
                return
            goodbye_check:re.Match = re.search(r"^(.*) left the ship.$", msg)
            if goodbye_check:
                chat_queue.put(f"Goodbye, {goodbye_check.group(0)[:-15]}")
                return
    parts = msg.split(":", 1)
    if len(parts) > 1:
        logger.detail("dealing with chat")
        author: re.Match = re.search(r"(((\[Captain\] )|(\[Crew\] ))?)(#?\w+)", parts[0])
        if author is not None:
            author = author.group(5)
        else:
            logger.critical("could not match authors name!")
        if author in banned:
            return
        content = parts[1][1:]
        if content == "good bot":
            chat_queue.put(":)")
        #if not owner_username in author:#make shure i am not giveing commands, also configurable in diff file
        logger.detail("checking for command prefix")
        if content.startswith(str(prefix)):
            logger.detail("command dettected")
            content = content[len(prefix):]
            if content != "":
                if content.startswith("shutdown"):
                    if "SharpFloof" in author:
                        chat_queue.put("Goodbye")
                        logger.info("Shutting down")
                        print("shutting down")
                        chat_queue.put(None)
                        logger.detail("joining queue")
                        chat_queue.join()
                        logger.detail("Joining thread")
                        sender_thread.join()
                        logger.detail("exiting main loop")
                        global kill
                        kill = 1
                        logger.detail("closing driver")
                        driver.close()
                        logger.info("exiting")
                        sys.exit(10)
                if content == "reload data":
                    if "SharpFloof" in author:
                        with banned_path.open("r") as f:
                            banned = json.load(f)

                        with flag_path.open("r") as f:
                            flags = json.load(f)
                        chat_queue.put("reloaded data")
                        return
                if content.startswith("ban"):
                    if "SharpFloof" in author:
                        args = content.split(" ")
                        if len(args) == 2:
                            with banned_path.open("r") as f:
                                banned = json.load(f)
                            banned.append(args[1])
                            with banned_path.open("w") as f:
                                json.dump(banned, f, indent=2)
                            chat_queue.put(f"{args[1]} was banned!")
                        else:
                            chat_queue.put('must include person to ban!')
                        return
                    else:
                        chat_queue.put("you cannot ban people!")
                        return
                if content.startswith("unban"):
                    if "SharpFloof" in author:
                        args = content.split(" ")
                        if len(args) == 2:
                            with banned_path.open("r") as f:
                                banned = json.load(f)
                            try:
                                banned.remove(args[1])
                            except ValueError:
                                chat_queue.put(f"{args[1]} is not banned!")
                            with banned_path.open("w") as f:
                                json.dump(banned, f, indent=2)
                            chat_queue.put(f"{args[1]} was banned!")
                        else:
                            chat_queue.put('must include person to ban!')
                        return
                    else:
                        chat_queue.put("you cannot ban people!")
                        return
                logger.debug("running interpret")
                sucsess = mc.interpet(author, content)
                if not sucsess:
                    chat_queue.put("Unknown command")
                    return
            else:
                logger.detail("no command")
                chat_queue.put("please type a command")
    
msges_len = 0

sender_thread = threading.Thread(target=chat_sender)
sender_thread.start()

kill = 0
while kill == 0:
    time.sleep(0.5)
    chat = driver.find_element_by_css_selector("#chat-content")
    current_chat = chat.find_elements(By.XPATH, "./*")
    current_chat = current_chat[msges_len:]
    msges_len += len(current_chat)
    print()
    if len(current_chat) > 0:
        for msg in current_chat:
            logger.detail(f"new msg:{msg.get_property('textContent')}")
            deal_with_message(msg.get_property("textContent"))

