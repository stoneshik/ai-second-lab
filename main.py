from pyswip import Prolog

import re

class PrologWrapper:
    def __init__(self, prolog: Prolog):
        self.__russifier: dict = {
            "медная руда": "copper_ore",
            "железная руда": "iron_ore",
            "дерево": "wood",
            "камень": "stone",
            "уголь": "coal",
            "медная плита": "copper_plate",
            "железная плита": "iron_plate",
            "кирпич": "stone_brick",
            "медный провод": "copper_cable",
            "деревянный ящик": "wooden_chest",
            "железный ящик": "iron_chest",
            "шестерня": "iron_gear_wheel",
            "каменная печь": "stone_furnace",
            "конвеер": "transport_belt",
            "печатная плата": "electronic_circuit",
            "стена": "wall",
            "туррель": "gun_turret",
            "научный пакет автоматизации": "automation_science_pack",
            "технология стен": "wall_technology",
            "технология туррелей": "turrets_technology",
        }
        self.__russifier_inverse: dict = {value: key for key, value in
                                          zip(self.__russifier.keys(), self.__russifier.values())}
        self.__prolog = prolog
        self.__raw_ingredients: tuple = tuple([self.__russifier_inverse[key] for key in
                                               [x['X'] for x in self.make_query('raw_ingredient(X).')]])
        self.__fuels: tuple = tuple([self.__russifier_inverse[key] for key in
                                     [x['X'] for x in self.make_query('fuel(X).')]])
        self.__items: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                     [x['X'] for x in self.make_query('item(X).')]])
        self.__technologies: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                            [x['X'] for x in self.make_query('technology(X).')]])
        self.__info_string: str = self.__compile_info_string()

    @property
    def prolog(self) -> Prolog:
        return self.__prolog

    @property
    def info_string(self) -> str:
        return self.__info_string

    def __compile_info_string(self) -> str:
        return "Начальные ресурсы:\n" + ", ".join(self.__raw_ingredients) + "\n" + \
            "Предметы, которые можно использовать как топливо:\n" + ", ".join(self.__fuels) + "\n" + \
            "Предметы, которые можно скрафтить:\n" + ", ".join(self.__items) + "\n" + \
            "Технологии:\n" + ", ".join(self.__technologies)

    def make_query(self, query_string: str) -> [list, None]:
        return self.__prolog.query(query_string)


class Console:
    def __init__(self, prolog_wrapper: PrologWrapper):
        self.__prolog_wrapper: PrologWrapper = prolog_wrapper

    def io(self):
        """
        Шаблоны запросов
        У меня есть: ... топливо + сырой материал -> жарка
        ингредиенты -> вещь которая получается, то что получается из всех вещей которые можно скрафтить
        Используя ... ты получишь ...
        Скрафтив ... <и используя> ты получишь ...
        Изучив технологию, ты сможешь скрафтить ...
        Я хочу что-то сделать из: ...; У меня изучены технологии ...
        """
        print(self.__prolog_wrapper.info_string)
        print("Формат запроса:\nУ меня есть: первый предмет, второй предмет; Изучены технологии: технология")
        items_regexp = re.compile(r"У меня есть: (?:[ ]*([а-яА-Я ]+),[ ]*)*(?:[ ]*([а-яА-Я ]+)[ ]*)+")
        technologies_regexp = re.compile(r"Изучены технологии: (?:[ ]*([а-яА-Я ]+),[ ]*)*(?:[ ]*([а-яА-Я ]+)[ ]*)+")
        while True:
            raw_string: str = input("Введите запрос (чтобы завершить работу введите exit)...\n").strip()
            if raw_string == "exit":
                return
            strings: list = raw_string.split(';')
            if len(strings) > 2:
                print("Формат ввода неправильный, повторите ввод...")
                continue
            string_items: str = strings[0].strip()
            items: list = re.findall(items_regexp, string_items)
            string_technologies: str = strings[1].strip()
            technologies: list = re.findall(technologies_regexp, string_technologies)
            answer = self.__prolog_wrapper.make_query(raw_string)
            print(list(answer))


def main():
    prolog: Prolog = Prolog()
    prolog.consult('first.pl')
    prolog_wrapper: PrologWrapper = PrologWrapper(prolog)
    console: Console = Console(prolog_wrapper)
    console.io()


if __name__ == '__main__':
    main()
