import os
import random
import sys
import time


class QuitException(Exception):
    pass


class Category:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class SubjectIsComplementCategory(Category):
    def __init__(self):
        super().__init__("SUBJECT is COMPLEMENT")
        self.subject = "unset"
        self.complement = "unset"

    def populate(self, subject, complement):
        self.subject = subject
        self.complement = complement

    def e(self):
        return f"{self.subject.english} is {self.complement.english}"

    def j(self):
        return f"{self.subject.japanese} is {self.complement.japanese}"


class SubjectVerbAdverbCategory(Category):
    def __init__(self):
        super().__init__("SUBJECT VERB ADVERB")
        self.subject = "unset"
        self.verb = "unset"
        self.adverb = "unset"

    def populate(self, subject, complement):
        self.subject = subject
        self.complement = complement

    def e(self):
        return f"{self.subject.english} is {self.complement.english}"

    def j(self):
        return f"{self.noun.japanese} is {self.complement.japanese}"


class Adjective():
    def __init__(self, japanese, english):
        self.japanese = japanese
        self.english = english


class Noun():
    def __init__(self, japanese, english):
        self.japanese = japanese
        self.english = english


categories = [
    SubjectIsComplementCategory(),
    SubjectVerbAdverbCategory(),
]


nouns = [
    Noun("りんご", "apple"),
]


adjectives = [
    Adjective("あか", "red"),
]


def continue_or_quit(prompt=""):
    choice = input(prompt)
    if choice == "q":
        raise QuitException("quitting")


def print_japanese_english(verb, where=None, when=None):
    os.system("clear")
    print(f"{verb[1]} {where[1] if where else ''} {when.english if when else ''}")
    continue_or_quit()
    print(f"{verb[0]} {where[0] if where else ''} {when.japanese if when else ''}")
    continue_or_quit()


def main(argv):
    global categories

    if len(argv) > 1 and argv[1] != "all":
        names = argv[1].split(",")
        categories = list(filter(lambda c: c.name in names, categories))
        assert categories
    else:
        category = input(f"Category {categories}: ")
        if category != "":
            names = category.split(",")
            categories = list(filter(lambda c: c.name in names, categories))
        assert categories

    while True:
        category = categories[random.randint(0, len(categories) - 1)]
        if isinstance(category, SubjectIsComplementCategory):
            print(category)
            category.populate(
                nouns[random.randint(0, len(nouns) - 1)],
                adjectives[random.randint(0, len(adjectives) - 1)],
            )
            print(category.e())
            continue_or_quit()
            print(category.j())
            continue_or_quit()
        elif isinstance(category, SubjectVerbAdverbCategory):
            print(category)
        else:
            print("unknown category")

        continue_or_quit()


if __name__ == '__main__':
    try:
        main(sys.argv)
    except QuitException:
        pass
