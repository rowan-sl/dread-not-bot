class TagCogg:
    from queue import Queue
    import sqlite3
    import pathlib

    def __init__(self) -> None:
        cwd_path = self.pathlib.PurePath(self.pathlib.Path(__file__))
        self.main_path = str(cwd_path.parents[2])

        self.conn = self.sqlite3.connect(str(self.pathlib.PurePath(self.main_path, "database", "main.sqlite")))
        self.cur = self.conn.cursor()

    def check(self, author, content, chat_queue: Queue, logger):
        if content.startswith("tag "):
            args = content[4:]
            args = args.split(" ")
            if args[0] == "help":
                chat_queue.put("This is the tag command. to make a new tag, run '##tag new <tag name> <tag content>'.")
                chat_queue.put("To remove a tag, run '##tag remove <tag name>, to get the value or author of a tag, run '##tag value/author <tag name>', and to edit a tag run ##tag edit <tag name> <new content>")
                return True
            if args[0] == "value":
                if len(args) > 1:
                    query = self.cur.execute('SELECT name, value FROM Tags WHERE name = ?', (args[1],)).fetchall()
                    if query == []:
                        chat_queue.put("that tag does not exist")
                        return True
                    else:
                        chat_queue.put(f"{query[0][0]} is: {query[0][1]}")
                        return True
                else:
                    chat_queue.put("Missing argument tag name")
                    return True

            if args[0] == "new":
                if len(args) > 2:
                    contains = ""
                    for arg in args[2:]:
                        contains += arg + " "
                    if self.cur.execute('''SELECT * FROM Tags WHERE name = ?''', (args[1],)).fetchall() != []:
                        chat_queue.put("That tag already exists")
                        return True
                    else:
                        self.cur.execute('INSERT INTO Tags VALUES (?, ?, ?, ?, ?)', (args[1], contains, author, author, 0))
                        self.conn.commit()
                        chat_queue.put("new tag created")
                        return True

                else:
                    chat_queue.put("missing some arguments")
                    return True
            if args[0] == "author":
                if len(args) > 1:
                    query = self.cur.execute('SELECT name, author, owner FROM Tags WHERE name = ?', (args[1],)).fetchall()
                    if query == []:
                        chat_queue.put("that tag does not exist")
                        return True
                    else:
                        chat_queue.put(f"{query[0][0]}'s creator is: {query[0][1]} and latest editor is: {query[0][2]}")
                        return True
                else:
                    chat_queue.put("Missing argument tag name")
                    return True
            if args[0] == "remove":
                if len(args) > 1:
                    query = self.cur.execute('SELECT locked FROM Tags WHERE name = ?', (args[1],)).fetchall()
                    if (query != []) and (query[0][0] != 1):
                        self.cur.execute('DELETE FROM Tags WHERE name = ?', (args[1],))
                        self.conn.commit()
                        chat_queue.put("Tag removed")
                        return True
                    chat_queue.put("Tag does not exist or is locked")
                    return True
                chat_queue.put("Missing argument tag name")
                return True
            if args[0] == "edit":
                if len(args) > 2:
                    contains = ""
                    for arg in args[2:]:
                        contains += arg + " "
                    if self.cur.execute('''SELECT * FROM Tags WHERE name = ?''', (args[1],)).fetchall() == []:
                        chat_queue.put("That tag does not exist")
                        return True
                    else:
                        self.cur.execute('UPDATE Tags SET value = ? , owner = ? WHERE name = ?', (contains, author, args[1]))
                        self.conn.commit()
                        chat_queue.put("tag updated")
                        return True
                else:
                    chat_queue.put("missing some arguments")
                    return True
            chat_queue.put("must have valid subcommand, run '##tag help' for a list of subcommands")
            return True

module_coggs = [TagCogg]