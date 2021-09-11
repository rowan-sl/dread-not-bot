import logging
import pathlib
import os

cwd_path = pathlib.PurePath(pathlib.Path(__file__))
main_path = str(cwd_path.parents[1])
log_path = str(pathlib.PurePath(main_path, "logs", "latest.log"))
driver_log_path = str(pathlib.PurePath(main_path, "logs", "gekodriver.log"))
#! add projects main dir to PYTHONPATH
sys.path.append(main_path)
from sqlite3.dbapi2 import connect
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
from selenium import webdriver
import selenium
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import FirefoxWebElement
import threading, queue
from slowo import UwU, main
import re
import sys
import json
import random
from lib.evaluate_str import evalueatestr
import sqlite3

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
# unused
# action_key_down_w = ActionChains(driver).key_down("w")
# action_key_up_w = ActionChains(driver).key_up("w")
# action_key_down_a = ActionChains(driver).key_down("a")
# action_key_up_a = ActionChains(driver).key_up("a")
# action_key_down_s = ActionChains(driver).key_down("s")
# action_key_up_s = ActionChains(driver).key_up("s")
# action_key_down_d = ActionChains(driver).key_down("d")
# action_key_up_d = ActionChains(driver).key_up("d")
space_down = ActionChains(driver).key_down(Keys.SPACE)
space_up = ActionChains(driver).key_up(Keys.SPACE)

with pathlib.Path(main_path, "resources", "items.json").open("r") as f:
    ingameitems = json.load(f)

# with open("database/tags.json", "r") as f:
#     tag_storage = json.load(f)

# new tag system, with sqlite3
conn = sqlite3.connect(str(pathlib.PurePath(main_path, "database", "main.sqlite")))
cur = conn.cursor()

eightballanswers = [
    "Prehaps",
    "Good Question",
    "P r e h a p s",
    "It is certain",
    "For shure",
    "420.69%",
    "Without a doubt",
    "You may rely on it",
    "Yes definitely",
    "It is decidedly so",
    "As I see it, yes",
    "Most likely",
    "Yes",
    "Outlook good",
    "Signs point to yes",
    "Reply hazy try again",
    "Better not tell you now",
    "Ask again later",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don’t count on it",
    "Outlook not so good",
    "My sources say no",
    "Very doubtful",
    "My reply is no",
    "Nah",
    "N o p e",
    "The oracle says go away",

]

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
    

chat_queue = queue.Queue()

def chat_sender():
    logger.detail("sender running")
    while True:
        time.sleep(1.1)
        msg = chat_queue.get()
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
        chat_queue.task_done()


def deal_with_message(msg):
    msg = str(msg)
    if msg == "":
        return
    if not "SharpFloof:" in msg:
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
        author = parts[0]
        author_wo_rank: re.Match = re.search(r"(((\[Captain\] )|(\[Crew\] ))?)(\w+)", author)
        if author_wo_rank is not None:
            author_name = author_wo_rank.group(5)
            author = author_name
        else:
            logger.critical("could not match authors name!")
        content = parts[1][1:]
        if content == "good bot":
            chat_queue.put(":)")
        #if not owner_username in author:#make shure i am not giveing commands, also configurable in diff file
        logger.detail("checking for command prefix")
        if content.startswith(str(prefix)):
            logger.detail("command dettected")
            content = content[len(prefix):]
            if content != "":
                if content == "ping":
                    chat_queue.put("pong!")
                    return
                if content.startswith("info"):
                    info_parts = content.split(" ")
                    if len(info_parts) == 1:
                        chat_queue.put(f"hi, i am {owner_username}, who is definitaly human")
                        return
                    else:
                        if len(info_parts) == 2:
                            if info_parts[1].lower() == "sharpfloof":
                                chat_queue.put("SharpFloof, creator of this bot.")
                                return
                    return
                if content.startswith("iteminfo"):
                    item_name = content[9:]
                    if item_name in ["", " "]:
                        chat_queue.put("that item does not exist!")
                        return
                    for item in ingameitems:
                        if type(item) is dict:
                            if item["name"].lower() == item_name.lower():
                                chat_queue.put(item["description"])
                                return
                    possible_meanings = ""
                    poss_meanings = []
                    for item in ingameitems:
                        if type(item) is dict:
                            if item_name.lower() in item["name"].lower():
                                possible_meanings += item["name"] + ", "
                                poss_meanings.append(item)
                    if possible_meanings != "":
                        if len(poss_meanings) < 7:
                            chat_queue.put(f"That's not a item! did you mean one of these? {possible_meanings}")
                            return
                        else:
                            chat_queue.put(f"Please be more spacific - there are {len(poss_meanings)} items that include {item_name}")
                    else:
                        chat_queue.put("that item does not exist!")
                    return
                if content == "commands":
                    chat_queue.put("my commands are info, help, commands, tag, uwu, ping, bruh, pog, thonk, bible/quaran, iteminfo, sussy, 8ball, and prob others i forgot")
                    return
                if content == "help":
                    chat_queue.put(f"run {prefix}info for info or {prefix}commands for commands")
                    return
                if content == "bruh":
                    chat_queue.put(
"""
.
██████╗░██████╗░██╗░░░██╗██╗░░██╗ 
██╔══██╗██╔══██╗██║░░░██║██║░░██║ 
██████╦╝██████╔╝██║░░░██║███████║ 
██╔══██╗██╔══██╗██║░░░██║██╔══██║ 
██████╦╝██║░░██║╚██████╔╝██║░░██║ 
╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝
"""                                )
                    return
                if content == "pog":
                    chat_queue.put("Coggers! ⚙️ ✨ 😀")
                    return
                if content == "thonk":
                    chat_queue.put("🤔")
                    return
                if content in ["bible", "quaran"]:
                    chat_queue.put("No")
                    return
                if content.startswith("8ball"):
                    chat_queue.put(random.choice(eightballanswers))
                    return
                if content.startswith("sussy"):
                    chat_queue.put("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    return
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
                if content.startswith("eval "):
                    result = evalueatestr(content[5:])
                    if result is None:
                        chat_queue.put("An error occured")
                        return
                    else:
                        chat_queue.put(str(result))
                        return
                if content.startswith("tag "):
                    args = content[4:]
                    args = args.split(" ")
                    if args[0] == "help":
                        chat_queue.put("This is the tag command. to make a new tag, run '##tag new <tag name> <tag content>'.")
                        chat_queue.put("To remove a tag, run '##tag remove <tag name>, to get the value or author of a tag, run '##tag value/author <tag name>', and to edit a tag run ##tag edit <tag name> <new content>")
                        return
                    if args[0] == "value":
                        if len(args) > 1:
                            query = cur.execute('SELECT name, value FROM Tags WHERE name = ?', (args[1],)).fetchall()
                            if query == []:
                                chat_queue.put("that tag does not exist")
                                return
                            else:
                                chat_queue.put(f"{query[0][0]} is: {query[0][1]}")
                                return
                        else:
                            chat_queue.put("Missing argument tag name")
                            return
                        
                        # if len(args) > 1:
                        #     value = None
                        #     name = None
                        #     for tag in tag_storage:
                        #         if tag["name"] == args[1]:
                        #             value = tag["value"]
                        #             name = tag["name"]
                        #     if value is not None:
                        #         chat_queue.put(f"{name} is: {value}")
                        #     else:
                        #         chat_queue.put("that tag does not exist")
                        #     return
                        # else:
                        #     chat_queue.put("Missing argument tag name")
                        #     return
                    if args[0] == "new":
                        if len(args) > 2:
                            contains = ""
                            for arg in args[2:]:
                                contains += arg + " "
                            if cur.execute('''SELECT * FROM Tags WHERE name = ?''', (args[1],)).fetchall() != []:
                                chat_queue.put("That tag already exists")
                                return
                            else:
                                cur.execute('INSERT INTO Tags VALUES (?, ?, ?, ?, ?)', (args[1], contains, author, author, 0))
                                conn.commit()
                                chat_queue.put("new tag created")
                                return
                            # for tag in tag_storage:
                            #     if tag["name"] == args[1]:
                            #         chat_queue.put("that tag already exists")
                            #         return
                            # contains = ""
                            # for arg in args[2:]:
                            #     contains += arg + " "
                            # tag_storage.append({"name": args[1], "value": contains, "author": author})
                            # with open("database/tags.json", "w") as f:
                            #     json.dump(tag_storage, f, indent=4)
                            # chat_queue.put("new tag created")
                            # return
                        else:
                            chat_queue.put("missing some arguments")
                            return
                    if args[0] == "author":
                        if len(args) > 1:
                            query = cur.execute('SELECT name, author, owner FROM Tags WHERE name = ?', (args[1],)).fetchall()
                            if query == []:
                                chat_queue.put("that tag does not exist")
                                return
                            else:
                                chat_queue.put(f"{query[0][0]}'s creator is: {query[0][1]} and latest editor is: {query[0][2]}")
                                return
                        else:
                            chat_queue.put("Missing argument tag name")
                            return
                        # author = None
                        # name = None
                        # for tag in tag_storage:
                        #     if tag["name"] == args[1]:
                        #         author = tag["author"]
                        #         name = tag["name"]
                        # if author is not None:
                        #     chat_queue.put(f"{name}'s author is: {author}")
                        # else:
                        #     chat_queue.put("that tag does not exist")
                        # return
                    if args[0] == "remove":
                        if len(args) > 1:
                            query = cur.execute('SELECT locked FROM Tags WHERE name = ?', (args[1],)).fetchall()
                            if (query != []) and (query[0][0] != 1):
                                cur.execute('DELETE FROM Tags WHERE name = ?', (args[1],))
                                conn.commit()
                                chat_queue.put("Tag removed")
                                return
                            # for index, tag in enumerate(tag_storage):
                            #     if tag["name"] == args[1]:
                            #         tag_storage.pop(index)
                            #         with open("database/tags.json", "w") as f:
                            #             json.dump(tag_storage, f, indent=4)
                            #         chat_queue.put(f"Removed tag {tag['name']}")
                            #         return
                            chat_queue.put("Tag does not exist or is locked")
                            return
                        chat_queue.put("Missing argument tag name")
                        return
                    if args[0] == "edit":
                        if len(args) > 2:
                            contains = ""
                            for arg in args[2:]:
                                contains += arg + " "
                            if cur.execute('''SELECT * FROM Tags WHERE name = ?''', (args[1],)).fetchall() == []:
                                chat_queue.put("That tag does not exist")
                                return
                            else:
                                cur.execute('UPDATE Tags SET value = ? , owner = ? WHERE name = ?', (contains, author, args[1]))
                                conn.commit()
                                chat_queue.put("tag updated")
                                return
                        else:
                            chat_queue.put("missing some arguments")
                            return
                    chat_queue.put("must have valid subcommand, run '##tag help' for a list of subcommands")
                    return
                if content == "haters":
                    chat_queue.put("List of ppl who hate the bot :( they mean")
                    chat_queue.put("Amin")
                    return
                chat_queue.put("Unknown command")
            else:
                logger.detail("no command")
                chat_queue.put("please type a command")
    
old_msges = []

sender_thread = threading.Thread(target=chat_sender)
sender_thread.start()
kill = 0
while kill == 0:
    time.sleep(0.5)
    chat = driver.find_element_by_css_selector("#chat-content")
    current_chat = chat.find_elements(By.XPATH, "./*")
    current_chat = current_chat[len(old_msges):]
    old_msges += current_chat
    if len(current_chat) > 0:
        for msg in current_chat:
            logger.detail(f"new msg:{msg.get_property('textContent')}")
            deal_with_message(msg.get_property("textContent"))

