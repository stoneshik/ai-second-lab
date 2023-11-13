import pytholog as pl


def initial_knowledge_base() -> pl.KnowledgeBase:
    kbase = pl.KnowledgeBase('factorio')
    return kbase([
        "raw_ingredient(copper_ore).",
        "raw_ingredient(iron_ore).",
        "raw_ingredient(wood).",
        "raw_ingredient(stone).",

        "fuel(wood).",
        "fuel(coal).",
        "fuel(X): - ingredient(wood, X).",

        "item(copper_plate).",
        "item(iron_plate).",
        "item(stone_brick).",
        "item(copper_cable).",
        "item(wooden_chest).",
        "item(iron_chest).",
        "item(iron_gear_wheel).",
        "item(stone_furnace).",
        "item(transport_belt).",
        "item(electronic_circuit).",
        "item(wall).",
        "item(gun_turret).",
        "item(automation_science_pack).",

        "smelting(copper_ore, copper_plate).",
        "smelting(iron_ore, iron_plate).",
        "smelting(stone, stone_brick).",
        "ingredient(copper_plate, copper_cable).",
        "ingredient(wood, wooden_chest).",
        "ingredient(iron_plate, iron_chest).",
        "ingredient(iron_plate, iron_gear_wheel).",
        "ingredient(stone, stone_furnace).",
        "ingredient(iron_plate, transport_belt).",
        "ingredient(iron_gear_wheel, transport_belt).",
        "ingredient(copper_cable, electronic_circuit).",
        "ingredient(iron_plate, electronic_circuit).",
        "ingredient(iron_gear_wheel, automation_science_pack).",
        "ingredient(copper_plate, automation_science_pack).",
        "ingredient(stone_brick, wall).",
        "ingredient(iron_plate, gun_turret).",

        "technology(wall, wall_technology).",
        "technology(gun_turret, turrets_technology).",

        "starting_craft_item(X): - item(X),  \\+ technology(X, _).",
        "studied_craft_item(X): - technology(X, Y), studied(Y).",
        "craftable_item(X): - starting_craft_item(X); studied_craft_item(X).",
        "unstadied_craft_item(X): - technology(X, Y),  \\+ studied(Y)."
    ])


class Console:
    def __init__(self, kbase: pl.KnowledgeBase):
        self.__russifier: dict = {
            "медная руда": "raw_ingredient(copper_ore).",
            "железная руда": "raw_ingredient(iron_ore).",
            "дерево": "raw_ingredient(wood).",
            "камень": "raw_ingredient(stone).",
            "медная плита": "item(copper_plate).",
            "железная плита": "item(iron_plate).",
            "кирпич": "item(stone_brick).",
            "медный провод": "item(copper_cable).",
            "деревянный ящик": "item(wooden_chest).",
            "железный ящик": "item(iron_chest).",
            "шестерня": "item(iron_gear_wheel).",
            "каменная печь": "item(stone_furnace).",
            "конвеер": "item(transport_belt).",
            "печатная плата": "item(electronic_circuit).",
            "стена": "item(wall).",
            "туррель": "item(gun_turret).",
            "научный пакет автоматизации": "item(automation_science_pack).",
            "технология стен": "technology(wall, wall_technology).",
            "технология туррелей": "technology(gun_turret, turrets_technology).",
        }
        raw_ingredients: tuple = (
            "медная руда",
            "железная руда",
            "дерево",
            "камень",
        )
        items: tuple = (
            ""
        )
        technologies: tuple = (
            ""
        )
        self.__kbase = kbase
        self.__info_string: str = self.__compile_info_string()

    def __compile_info_string(self) -> str:
        pass

    def io(self):
        string: str = input("Введите запрос...\n")
        """
        Шаблоны запросов
        Я хочу что-то сделать из: ... топливо + сырой материал -> жарка
        ингредиенты -> вещь которая получается, то что получается из всех вещей которые можно скрафтить
        Используя ... ты получишь ...
        Скрафтив ... <и используя> ты получишь ...
        Изучив технологию, ты сможешь скрафтить ...
        Я хочу что-то сделать из: ...; У меня изучены технологии ...
        """
        while string != "exit":
            print(f"Введено {string}")
            string: str = input("Введите запрос...\n")


def main():
    initial_knowledge_base()
    io()


if __name__ == '__main__':
    main()
