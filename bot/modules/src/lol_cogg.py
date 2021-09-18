class LolCogg:
    from queue import Queue
    from slowo import UwU

    def check(self, author, content, chat_queue: Queue, logger):
        if content.startswith("uwu "):
            text_to_uwu = content[4:]
            if text_to_uwu != "":
                chat_queue.put(self.UwU.ify(text_to_uwu)+" UwU ❤️️")
            else:
                chat_queue.put("please enter text to uwu")
            return True
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
            return True
        if content == "pog":
            chat_queue.put("Coggers! ⚙️ ✨ 😀")
            return True
        if content == "thonk":
            chat_queue.put("🤔")
            return True
        if content in ["bible", "quaran"]:
            chat_queue.put("No")
            return True
        if content.startswith("sussy"):
            chat_queue.put("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            return True
        if content == "haters":
            chat_queue.put("List of ppl who hate the bot :( they mean")
            chat_queue.put("Amin")
            return True

module_coggs = [LolCogg]