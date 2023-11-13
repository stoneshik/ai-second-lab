import pytholog as pl


def main():
    kbase = pl.KnowledgeBase('factorio')
    kbase([
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


if __name__ == '__main__':
    main()
