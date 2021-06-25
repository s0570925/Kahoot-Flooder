import os
import random
import logging
import requests
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format=f"\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class Kahoot:

    def __init__(self, code: str, name: str, amount: int):
        self.code = code
        self.name = name
        self.amount = amount
        self.game_info = None
        self.threads = []
        self.headers = {"Content-Type": "application/json"}

    def _check(self):
        try:
            r = requests.get("https://kahoot.it/rest/challenges/pin/%s" % (self.code), headers=self.headers)
            if "error" in r.text:
                logging.info("Invalid pin has been passed")
                os.system("pause >NUL")
                os._exit(0)
            else:
                self.game_info = r.json()
                logging.info("Loaded %s hosted by %s" % (self.game_info["challenge"]["title"], self.game_info["challenge"]["quizMaster"]["username"]))
        except Exception:
            logging.info("Failed to check game pin")
            os.system("pause >NUL")
            os._exit(0)

    def _uuid(self):
        return "abf4a130-%s-498b-80dd-12bd4b8fdd59" % (random.randint(1000, 9999))

    def _join(self):
        generated_uuid = self._uuid()
        r = requests.post("https://kahoot.it/rest/challenges/%s/join/?nickname=%s" % (self.game_info["challenge"]["challengeId"], self.name), cookies={"generated_uuid": generated_uuid}, headers=self.headers)
        if "MAX_PLAYERS_REACHED" in r.text:
            logging.info("Max players reached on this game")
            os.system("pause >NUL")
            os._exit(0)
        else:
            logging.info("New client connected, %s" % (self.name))

    def start(self):
        self._check()
        for x in range(self.amount):
            try:
                t = Thread(target=self._join).start()
                self.threads.append(t)
            except Exception:
                pass

        for x in self.threads:
            try:
                x.join()
            except Exception:
                pass

        logging.info("Finished kahoot flooder.")
        os.system("pause >NUL")
        os._exit(0)

if __name__ == "__main__":
    os.system("cls && title [Kahoot flooder]")

    code = input("\x1b[38;5;197mCode \x1b[0>\x1b[38;5;197m ")
    name = input("\x1b[38;5;197mName \x1b[0m>\x1b[38;5;197m ")
    amount = input("\x1b[38;5;197mAmount \x1b[0m>\x1b[38;5;197m ")

    kahoot = Kahoot(
        code=code,
        name=name,
        amount=int(amount)
    )

    kahoot.start()