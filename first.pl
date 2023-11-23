/*
База знаний по компьютерной игре Factorio
с описанием крафтов
*/
% все крафты вещей сводятся к начальным сырым ресурсам, которые были преобразованы
raw_ingredient(copper_ore). % медная руда
raw_ingredient(iron_ore). % железная руда
raw_ingredient(wood). % дерево
raw_ingredient(stone). % измельчённый камень

% для заправки печей импользуется топливо
fuel(wood). % дерево
fuel(coal). % уголь
fuel(X) :- ingredient(wood, X). % предметы которые сделаны из дерева можно использовать как топливо

% перечисление всех предметов которые могут быть получены
item(wood).
item(copper_plate).
item(iron_plate).
item(stone_brick).
item(copper_cable).
item(wooden_chest).
item(iron_chest).
item(iron_gear_wheel).
item(stone_furnace).
item(transport_belt).
item(electronic_circuit).
item(wall).
item(gun_turret).
item(automation_science_pack).

% в печах можно расплавить сырые материалы и получить новые
smelting(copper_ore, copper_plate). % получение медной плиты
smelting(iron_ore, iron_plate). % получение железной плиты
smelting(stone, stone_brick). % получение кирпича
% перечисление крафтов
% первый аргумент предиката - ингредиент для крафта, второй аргумент - получаемый предмет
ingredient(copper_plate, copper_cable). % крафт медной плиты
ingredient(wood, wooden_chest). % крафт деревянного ящика
ingredient(iron_plate, iron_chest). % крафт железного ящика
ingredient(iron_plate, iron_gear_wheel). % крафт железной шестерни
ingredient(stone, stone_furnace). % крафт каменной печи
% крафт конвеера
ingredient(iron_plate, transport_belt).
ingredient(iron_gear_wheel, transport_belt).
% крафт печатной платы
ingredient(copper_cable, electronic_circuit).
ingredient(iron_plate, electronic_circuit).
% крафт научного пака атоматизации (красной колбы)
ingredient(iron_gear_wheel, automation_science_pack).
ingredient(copper_plate, automation_science_pack).
% крафты для которых требуется изучение технологий
ingredient(stone_brick, wall). % крафт стены
ingredient(iron_plate, gun_turret). % крафт турели

% технологии
technology(wall_technology).
technology(turrets_technology).
technology_relation(wall, wall_technology). % технология которая нужна для крафта стены
technology_relation(gun_turret, turrets_technology). % технология которая нужна для крафта турели

% правила
starting_craft_item(X) :- item(X), \+ technology_relation(X, _). % рецепты которые доступны сразу без изучения технологий
studied_craft_item(X) :- technology_relation(X, Y), studied(Y). % рецепты которые стали доступны после изучения технологий
craftable_item(X) :- starting_craft_item(X) ; studied_craft_item(X). % все доступные для крафта рецепты
unstadied_craft_item(X) :- technology_relation(X, Y), \+ studied(Y). % рецепты технологии которых ещё не изучены

/* запросы к базе знаний
% предметы для крафта которых используется шестерня
ingredient(iron_gear_wheel, X).
% предметы которые нужны для крафта печатной платы
ingredient(X, electronic_circuit).
% просмотр правил
starting_craft_item(X).
studied_craft_item(X).
craftable_item(X).
unstadied_craft_item(X).
% предметы ингредиенты которых крафтятся из железной плиты
ingredient(iron_plate, X), ingredient(X, Y).
% предметы крафт которых доступен со старта и которые можно использовать как топливо
starting_craft_item(X), fuel(X).
% предметы которые были открыты после изучения технологии в чьём крафте используется железная плита
studied_craft_item(X), ingredient(iron_plate, X).
% доступные для крафта предметы, которые крафтятся из сырых ресурсов, либо переплавленных сырых ресурсов
craftable_item(Y), (ingredient(raw_material(X), Y); smelting(X, Z), ingredient(Z, Y)).
*/
