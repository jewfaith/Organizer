import xml.etree.ElementTree as ET
import os
import sys
from colorama import Fore, init
import textwrap

init(autoreset=True)


class XmlLoader:
    @staticmethod
    def load(file):
        xml = {}
        try:
            tree = ET.parse(file)
            root = tree.getroot()
        except ET.ParseError:
            print(Fore.RED + "Error: File is malformed")
            sys.exit(1)
        except FileNotFoundError:
            print(Fore.RED + "Error: File not found")
            sys.exit(1)

        for theme in root:
            theme_name = theme.tag
            if theme_name:
                xml[theme_name] = XmlLoader.get_books(theme)
            else:
                print(Fore.RED + "Error: Ignoring unnamed theme")

        return xml

    @staticmethod
    def get_books(theme):
        books = {}
        for book in theme:
            tag_name = book.tag
            verses = [
                "\n".join(textwrap.wrap(value.text, 32))
                for value in book.findall("value")
                if value.text
            ]
            books[tag_name] = verses if verses else ["Error: No verses found"]
        return books


class Display:
    @staticmethod
    def cls():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_menu(bible):
        Display.cls()
        print(Fore.YELLOW + "\nOrganizer - XMLManager 2024")
        print(Fore.CYAN + "https://github.com/jewfaith\n")
        print("=" * 32)

        for i, theme in enumerate(bible.keys(), start=1):
            theme_wrapped = f"{i}. {theme.capitalize()}"
            print(f"{theme_wrapped:<25}")

        print("=" * 32)

    @staticmethod
    def display_verses(xml, theme):
        Display.cls()

        if theme in xml:
            print(Fore.YELLOW + f"\n{theme.capitalize()}")
            print("=" * 32)
            for book, verses in xml[theme].items():
                print(Fore.CYAN + f"\n{book.capitalize()}")
                print("-" * 32)
                for i, verse in enumerate(verses, start=1):
                    verse_wrapped = "\n".join(textwrap.wrap(f"{i}. {verse}", 32))
                    print(verse_wrapped)
                print("-" * 32)
            print("=" * 32)
        else:
            print(Fore.RED + "Error: Theme not found")

        input("\nPress any key to continue ")


class XmlApp:
    def __init__(self, file):
        self.xml = XmlLoader.load(file)

    def run(self):
        while True:
            Display.display_menu(self.xml)
            option = self.get_user_option()
            if option is None:
                print(Fore.RED + "Error: Exiting the program")
                break

            if option < 0 or option >= len(self.xml):
                continue

            theme = list(self.xml.keys())[option]
            Display.display_verses(self.xml, theme)

    def get_user_option(self):
        while True:
            Display.display_menu(self.xml)
            try:
                option = int(input("\nChoose an element: "))
                if 1 <= option <= len(self.xml):
                    return option - 1
            except Exception:
                continue


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python main.py script.xml")
        sys.exit(1)
    app = XmlApp(sys.argv[1])
    app.run()
