# -*- coding: utf-8 -*-
from pyswip import Prolog

import re


class PrologWrapper:
    def __init__(self, prolog: Prolog):
        self.__entities_in_russian: dict = {
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
        self.__entities_in_english: dict = {value: key for key, value in
                                            zip(self.__entities_in_russian.keys(), self.__entities_in_russian.values())}
        self.__prolog = prolog
        self.__raw_ingredients_in_russian: tuple = tuple([self.__entities_in_english[key] for key in
                                                          [x['X'] for x in self.make_query('raw_ingredient(X).')]])
        self.__fuels_in_russian: tuple = tuple([self.__entities_in_english[key] for key in
                                                [x['X'] for x in self.make_query('fuel(X).')]])
        self.__items_in_russian: tuple = tuple([self.__entities_in_english[key.strip('.')] for key in
                                                [x['X'] for x in self.make_query('item(X).')]])
        self.__technologies_in_russian: tuple = tuple([self.__entities_in_english[key.strip('.')] for key in
                                                       [x['X'] for x in self.make_query('technology(X).')]])
        self.__info_string_in_russian: str = self.__compile_info_string()

    @property
    def prolog(self) -> Prolog:
        return self.__prolog

    @property
    def info_string(self) -> str:
        return self.__info_string_in_russian

    def __compile_info_string(self) -> str:
        return "Начальные ресурсы:\n" + ", ".join(self.__raw_ingredients_in_russian) + "\n" + \
            "Предметы, которые можно использовать как топливо:\n" + ", ".join(self.__fuels_in_russian) + "\n" + \
            "Предметы, которые можно скрафтить:\n" + ", ".join(self.__items_in_russian) + "\n" + \
            "Технологии:\n" + ", ".join(self.__technologies_in_russian)

    def get_entity_by_key_in_russian(self, key_in_russian: str) -> str:
        return self.__entities_in_russian[key_in_russian]

    def get_entity_by_key_in_english(self, key_in_english: str) -> str:
        return self.__entities_in_english[key_in_english]

    def make_query(self, query_string: str) -> [list, None]:
        return self.__prolog.query(query_string)

    def is_key_string_in_russian_entity(self, key_string_in_russian) -> bool:
        return key_string_in_russian in self.__entities_in_russian.keys()

    def is_it_raw_ingredient_in_russian(self, value_in_russian: str) -> bool:
        return value_in_russian in self.__raw_ingredients_in_russian

    def is_it_fuel_in_russian(self, value_in_russian: str) -> bool:
        return value_in_russian in self.__fuels_in_russian

    def is_it_item_in_russian(self, value_in_russian: str) -> bool:
        return value_in_russian in self.__items_in_russian

    def is_it_technology_in_russian(self, value_in_russian: str) -> bool:
        return value_in_russian in self.__technologies_in_russian


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

    def __finding_wrong_entites_names(self, entities_in_russian: list) -> list:
        return [entity for entity in entities_in_russian
                if not self.__prolog_wrapper.is_key_string_in_russian_entity(entity) or
                self.__prolog_wrapper.is_it_technology_in_russian(entity)]

    def __finding_wrong_technology_names(self, technologies: list) -> list:
        return [technology for technology in technologies
                if not self.__prolog_wrapper.is_it_technology_in_russian(technology)]

    def __input_handling(self, entities_in_russian: list, technologies_in_russian: list) -> None:
        raw_ingredients_in_russian: list = [item for item in entities_in_russian
                                            if self.__prolog_wrapper.is_it_raw_ingredient_in_russian(item)]
        fuels_in_russian: list = [item for item in entities_in_russian
                                  if self.__prolog_wrapper.is_it_fuel_in_russian(item)]
        if len(raw_ingredients_in_russian) > 0 and len(fuels_in_russian) > 0:
            smelting_results: list = [
                list(self.__prolog_wrapper.make_query(
                    f"smelting({self.__prolog_wrapper.get_entity_by_key_in_russian(raw_ingredient)}, X)."
                ))[0]['X']
                for raw_ingredient in raw_ingredients_in_russian
            ]
            smelting_results_in_russian: list = [
                self.__prolog_wrapper.get_entity_by_key_in_english(item) for item in smelting_results
            ]
            result_string: str = ', '.join(
                [f"{raw_ingredient} -> {smelting_result}\n" for raw_ingredient, smelting_result in
                 zip(raw_ingredients_in_russian, smelting_results_in_russian)]
            )
            print(f"Можно получить при помощи плавки:\n{result_string}")
        else:
            smelting_results: list = []
        items: list = [self.__prolog_wrapper.get_entity_by_key_in_russian(item) for item in entities_in_russian]
        r = {item: list(self.__prolog_wrapper.make_query(f"ingredient({item}, X).")) for item in items}
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
            raw_string: str = input("Введите запрос (чтобы завершить работу введите выход)...\n").strip()
            if raw_string == "выход":
                return
            strings: list = raw_string.split(';')
            if len(strings) > 2:
                self.__show_error_message('Использовано несколько точек с запятой')
                continue
            entities_in_russian: list = self.__parsing_items(strings[0].strip())
            if entities_in_russian is None:
                self.__show_error_message('Ошибка в первой части строки')
                continue

            if len(strings) == 2:
                technologies_in_russian: list = self.__parsing_technologies(strings[1].strip())
                if technologies_in_russian is None:
                    self.__show_error_message('Ошибка во второй части строки')
                    continue
            else:
                technologies_in_russian: list = []
            wrong_entities: list = self.__finding_wrong_entites_names(entities_in_russian)
            wrong_technologies: list = self.__finding_wrong_technology_names(technologies_in_russian)
            if len(wrong_entities) > 0 or len(wrong_technologies) > 0:
                if len(wrong_entities) > 0 and len(wrong_technologies) > 0:
                    self.__show_error_message(
                        f"Ошибка в следующих названиях: {', '.join(wrong_entities)}, {', '.join(wrong_technologies)}"
                    )
                else:
                    self.__show_error_message(
                        f"Ошибка в следующих названиях: {', '.join(wrong_entities)}{', '.join(wrong_technologies)}"
                    )
                continue
            self.__input_handling(entities_in_russian, technologies_in_russian)


def main():
    prolog: Prolog = Prolog()
    prolog.consult('first.pl')
    prolog_wrapper: PrologWrapper = PrologWrapper(prolog)
    console: ConsoleHandler = ConsoleHandler(prolog_wrapper)
    console.input()


if __name__ == '__main__':
    main()

# if item not in self.__prolog_wrapper.is_key_string_in_russifier(item)
