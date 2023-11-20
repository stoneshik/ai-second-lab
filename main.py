import pytholog as pl


def initial_knowledge_base() -> pl.KnowledgeBase:
    kbase = pl.KnowledgeBase('factorio')
    kbase([
        "raw_ingredient(copper_ore).",
        "raw_ingredient(iron_ore).",
        "raw_ingredient(wood).",
        "raw_ingredient(stone).",

        "fuel(wood).",
        "fuel(coal).",
        "fuel(X) :- ingredient(wood, X).",

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

        "technology(wall_technology).",
        "technology(turrets_technology).",
        "technology_relation(wall, wall_technology).",
        "technology_relation(gun_turret, turrets_technology).",

        "starting_craft_item(X) :- item(X),  \\+ technology_relation(X, _).",
        "studied_craft_item(X) :- technology_relation(X, Y), studied(Y).",
        "craftable_item(X) :- starting_craft_item(X); studied_craft_item(X).",
        "unstadied_craft_item(X) :- technology_relation(X, Y),  \\+ studied(Y)."
    ])
    return kbase


class KBaseWrapper:
    def __init__(self, kbase: pl.KnowledgeBase):
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
        self.__russifier_inverse: dict = {value: key for key, value in zip(self.__russifier.keys(), self.__russifier.values())}
        self.__kbase = kbase
        self.__raw_ingredients: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                               [x['X.'] for x in self.make_query('raw_ingredient(X).')]])
        self.__fuels: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                            [x['X.'] for x in self.make_query('fuel(X).')]])
        self.__items: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                               [x['X.'] for x in self.make_query('item(X).')]])
        self.__technologies: tuple = tuple([self.__russifier_inverse[key.strip('.')] for key in
                                               [x['X.'] for x in self.make_query('technology(X).')]])
        self.__info_string: str = self.__compile_info_string()

    @property
    def kbase(self) -> pl.KnowledgeBase:
        return self.__kbase

    @property
    def info_string(self) -> str:
        return self.__info_string

    def __compile_info_string(self) -> str:
        return "Начальные ресурсы:\n" + ", ".join(self.__raw_ingredients) + "\n" + \
            "Предметы которые можно скрафтить:\n" + ", ".join(self.__items) + "\n" + \
            "Технологии:\n" + ", ".join(self.__technologies)

    def make_query(self, query_string: str) -> [list, None]:
        return self.__kbase.query(pl.Expr(query_string))


class Console:
    def __init__(self, kbase_wrapper: KBaseWrapper):
        self.__kbase_wrapper: KBaseWrapper = kbase_wrapper

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
            answer = self.__kbase_wrapper.make_query(string)
            print(answer)
            string: str = input("Введите запрос...\n")


def main():
    kbase: pl.KnowledgeBase = initial_knowledge_base()
    kbase_wrapper: KBaseWrapper = KBaseWrapper(kbase)
    console: Console = Console(kbase_wrapper)
    console.io()
    l = kbase_wrapper.kbase.query(pl.Expr("ingredient(iron_gear_wheel, X)."))
    e = 1


if __name__ == '__main__':
    main()
