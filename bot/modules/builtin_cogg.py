class BuiltinCogg:
    from config.conf import owner_username, prefix
    def __init__(self) -> None:
        pass
    
    def check(self, author, content, chat_queue, logger):
        if content.startswith("info"):
            logger.detail("info command")
            info_parts = content.split(" ")
            if len(info_parts) == 1:
                chat_queue.put(f"hi, i am {self.owner_username}, who is definitaly human")
                return True
            else:
                if len(info_parts) == 2:
                    if info_parts[1].lower() == "sharpfloof":
                        chat_queue.put("SharpFloof, creator of this bot.")
                        return True
            return False
        if content == "commands":
            chat_queue.put("my commands are info, help, commands, tag, uwu, ping, bruh, pog, thonk, bible/quaran, iteminfo, sussy, 8ball, and prob others i forgot")
            return True
        if content == "help":
            chat_queue.put(f"run {self.prefix}info for info or {self.prefix}commands for commands")
            return True

module_coggs = [BuiltinCogg]

