import os
import random
import re
import sys
import time


def clean(str):
    return re.sub(' +', ' ', str)


class QuitException(Exception):
    pass


class Category:
    def __init__(self, name):
        self.name = name
        self.english = "english"
        self.japanese = "japanese"

    def __repr__(self):
        return self.name


class Word:
    def __init__(self, english, japanese):
        self.english = english
        self.japanese = japanese


# Examples:
# [this] apple is red [right?]
# is the apple red?
#
class SubjectIsAdjectiveCategory(Category):
    def __init__(self):
        super().__init__("SUBJECT is ADJECTIVE")
        self.subject = "unset"
        self.adjective = "unset"

        self.format = Word(
            "%s %s %s %s",
            "%s %s %s %s %s"
        )

    def populate(self, subject, adjective):
        self.subject = subject
        self.adjective = adjective

        is_or_isnot = [
            Word("IS", "です"),
            Word("IS NOT", "じゃないです"),
        ]
        prefix = [
            Word("THE", ""),
            Word("THIS (NEAR ME)", "この"),
            Word("THAT (NEAR YOU)", "その"),
            Word("THAT (NOT NEAR)", "あの"),
        ]

        v = is_or_isnot[random.randint(0, len(is_or_isnot) - 1)]
        p = prefix[random.randint(0, len(prefix) - 1)]

        self.japanese = clean(self.format.japanese % (
            p.japanese,
            self.subject.japanese,
            "は",
            self.adjective.japanese,
            v.japanese,
        ))
        self.english = clean(self.format.english % (
            p.english,
            self.subject.english,
            v.english,
            self.adjective.english,
        ))


class SubjectVerbAdverbCategory(Category):
    def __init__(self):
        super().__init__("SUBJECT VERB ADVERB")
        self.subject = "unset"
        self.verb = "unset"
        self.adverb = "unset"

    def populate(self, subject, adjective):
        self.subject = subject
        self.adjective = adjective

        self.japanese = f"TODO"
        self.english = f"TODO"


class Adjective():
    def __init__(self, english, japanese):
        self.japanese = japanese
        self.english = english


class Noun():
    def __init__(self, english, japanese):
        self.japanese = japanese
        self.english = english


categories = [
    SubjectIsAdjectiveCategory(),
    #SubjectVerbAdverbCategory(),
]


nouns = [
    Noun("APPLE", "りんご"),
]


adjectives = [
    Adjective("RED", "あかい"),
]


def continue_or_quit(prompt=""):
    choice = input(prompt)
    if choice == "q":
        raise QuitException("quitting")


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
        if isinstance(category, SubjectIsAdjectiveCategory):
            print(category)
            category.populate(
                nouns[random.randint(0, len(nouns) - 1)],
                adjectives[random.randint(0, len(adjectives) - 1)],
            )
            print(category.english)
            continue_or_quit()
            print(category.japanese)
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
