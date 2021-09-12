class OracleCogg:
    from queue import Queue
    import random

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

    def check(self, author, content, chat_queue: Queue, logger):
        if content.startswith("8ball"):
            chat_queue.put(self.random.choice(self.eightballanswers))
            return True

module_coggs = [OracleCogg]