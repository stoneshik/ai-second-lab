# -*- coding: utf-8 -*-
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

    def get_value_from_russifier(self, russifier_key: str) -> str:
        return self.__russifier[russifier_key]

    def get_value_from_russifier_inverse(self, russifier_key: str) -> str:
        return self.__russifier_inverse[russifier_key]

    def make_query(self, query_string: str) -> [list, None]:
        return self.__prolog.query(query_string)

    def is_key_string_in_russifier(self, key_string) -> bool:
        return key_string in self.__russifier.keys()

    def is_it_raw_ingredients(self, value: str) -> bool:
        return value in self.__raw_ingredients

    def is_it_fuel(self, value: str) -> bool:
        return value in self.__fuels

    def is_it_item(self, value: str) -> bool:
        return value in self.__items

    def is_it_technology(self, value: str) -> bool:
        return value in self.__technologies


class ConsoleHandler:
    def __init__(self, prolog_wrapper: PrologWrapper):
        self.__prolog_wrapper: PrologWrapper = prolog_wrapper

    @staticmethod
    def __show_error_message(message: str) -> None:
        print(message)
        print("Формат ввода неправильный, повторите ввод...")

    def __parsing_items(self, string_items: str) -> [list, None]:
        items_regexp = re.compile(r"У меня есть: (?:[а-яА-Я ]+(?:[ ]*,[ ]*)?)+")
        if re.match(items_regexp, string_items) is None:
            return None
        items: list = [string.strip() for string in string_items.split(':')[1].strip().split(',')]
        return items

    def __parsing_technologies(self, string_technologies: str) -> [list, None]:
        technologies_regexp = re.compile(r"Изучены технологии: (?:[а-яА-Я ]+(?:[ ]*,[ ]*)?)+")
        if re.match(technologies_regexp, string_technologies) is None:
            return None
        technologies: list = [string.strip() for string in string_technologies.split(':')[1].strip().split(',')]
        return technologies

    def __finding_wrong_item_names(self, items: list) -> list:
        return [item for item in items if not self.__prolog_wrapper.is_key_string_in_russifier(item)]

    def __finding_wrong_technology_names(self, technologies: list) -> list:
        return [technology for technology in technologies
                if not self.__prolog_wrapper.is_key_string_in_russifier(technology)]

    def __input_handling(self, items: list, technologies: list) -> None:
        raw_ingredients_in_russian: list = [item for item in items if self.__prolog_wrapper.is_it_raw_ingredients(item)]
        fuels_in_russian: list = [item for item in items if self.__prolog_wrapper.is_it_fuel(item)]
        if len(raw_ingredients_in_russian) > 0 and len(fuels_in_russian) > 0:
            smelting: list = [
                list(self.__prolog_wrapper.make_query(
                    f"smelting({self.__prolog_wrapper.get_value_from_russifier(raw_ingredient)}, X)."
                ))[0]['X']
                for raw_ingredient in raw_ingredients_in_russian
            ]
            smelting_in_russian: list = [
                self.__prolog_wrapper.get_value_from_russifier_inverse(item) for item in smelting
            ]
            result_string: str = ', '.join(
                [f"{raw_ingredient} -> {smelting_result}\n" for raw_ingredient, smelting_result in
                 zip(raw_ingredients_in_russian, smelting_in_russian)]
            )
            print(f"Можно получить при помощи плавки:\n{result_string}")
        else:
            smelting: list = []
        r = list(self.__prolog_wrapper.make_query(
            f"ingredient({smelting[0]}, X)."
        ))
        l = 0


    def input(self):
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
        while True:
            raw_string: str = input("Введите запрос (чтобы завершить работу введите exit)...\n").strip()
            if raw_string == "exit":
                return
            strings: list = raw_string.split(';')
            if len(strings) > 2:
                self.__show_error_message('Использовано несколько точек с запятой')
                continue
            items: list = self.__parsing_items(strings[0].strip())
            if items is None:
                self.__show_error_message('Ошибка в первой части строки')
                continue

            if len(strings) == 2:
                technologies: list = self.__parsing_technologies(strings[1].strip())
                if technologies is None:
                    self.__show_error_message('Ошибка во второй части строки')
                    continue
            else:
                technologies: list = []
            wrong_items: list = self.__finding_wrong_item_names(items)
            wrong_technologies: list = self.__finding_wrong_technology_names(technologies)
            if len(wrong_items) > 0 or len(wrong_technologies) > 0:
                if len(wrong_items) > 0 and len(wrong_technologies) > 0:
                    self.__show_error_message(
                        f"Ошибка в следующих названиях: {', '.join(wrong_items)}, {', '.join(wrong_technologies)}"
                    )
                else:
                    self.__show_error_message(
                        f"Ошибка в следующих названиях: {', '.join(wrong_items)}{', '.join(wrong_technologies)}"
                    )
            self.__input_handling(items, technologies)


def main():
    prolog: Prolog = Prolog()
    prolog.consult('first.pl')
    prolog_wrapper: PrologWrapper = PrologWrapper(prolog)
    console: ConsoleHandler = ConsoleHandler(prolog_wrapper)
    console.input()


if __name__ == '__main__':
    main()

# if item not in self.__prolog_wrapper.is_key_string_in_russifier(item)
