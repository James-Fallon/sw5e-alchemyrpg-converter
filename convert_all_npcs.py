import json
from constants import ATTRIBUTES, SKILLS_TO_ABILITIES, CR_TO_PB


default_text_blocks = [{"title": "Class Features"}, {"title": "Racial Traits"}, {"title": "Feats"}, {"textBlocks": [{}, {}], "title": "Background"}, {"textBlocks": [{"title": "Personality Traits"}, {"title": "Ideals"}, {"title": "Bonds"}, {
    "title": "Flaws"}], "title": "Characteristics"}, {"textBlocks": [{}], "title": "Appearance"}, {"title": "Organizations"}, {"title": "Allies"}, {"title": "Enemies"}, {"textBlocks": [{}], "title": "Backstory"}, {"textBlocks": [{}], "title": "Other"}]


def convert_ability_scores(full_dict: dict) -> list:
    results = []
    for x in ATTRIBUTES:
        results.append({
            'name': x.lower()[:3],
            'value': full_dict[x]
        })
    return results


def find_mod(monster, skill):
    abi = SKILLS_TO_ABILITIES[skill]

    for attr in ATTRIBUTES:
        if attr.startswith(abi):
            return monster[f'{attr}Modifier']


def convert_skills(monster, prof_bonus):
    result = []
    for skill in SKILLS_TO_ABILITIES.keys():

        if f'npc_{skill}' not in monster.keys():
            result.append({
                "abilityName": SKILLS_TO_ABILITIES[skill],
                "name": skill.replace('_', ' ').title(),
                "proficient": False
            })
        else:
            mod = find_mod(monster, skill)
            bonus = int(monster[f'npc_{skill}'])
            if bonus == mod + (prof_bonus*2):
                result.append({
                    "abilityName": SKILLS_TO_ABILITIES[skill],
                    "name": skill.replace('_', ' ').title(),
                    "proficient": False,
                    "doubleProficiency": True
                })
            else:
                result.append({
                    "abilityName": SKILLS_TO_ABILITIES[skill],
                    "name": skill.replace('_', ' ').title(),
                    "proficient": True,
                    "doubleProficiency": False
                })

    return result


def convert_movement_modes(speeds_string):
    movement_modes = []

    split = speeds_string.split(',')

    if split[0].split(' ')[0] != 'fly':
        walking_distance = int(split[0].split(' ')[0])
        movement_modes.append({
            "mode": 'Walking',
            "distance": walking_distance
        })
        the_rest = split[1:]
    else:
        the_rest = split

    for s in the_rest:
        if s == '':
            continue
        deets = s.strip().split(' ')
        mode = deets[0].title()
        if '(hover)' in deets:
            mode = mode + ' (Hover)'

        distance = int(deets[1])

        movement_modes.append({
            "mode": mode,
            "distance": distance
        })
    return movement_modes


def convert_profs(languages, saves):
    langs = convert_languages_to_profs(languages)
    saves = convert_save_profs(saves)
    return langs + saves


def convert_languages_to_profs(languages):
    profs = []
    for l in languages:
        if l.strip() == '' or len(l) < 3:
            continue

        profs.append({
            'name': l.strip().title(),
            'type': 'language'
        })
    return profs


def convert_senses(senses_list):

    if senses_list is None:
        return []

    senses = []
    for s in senses_list:
        if 'passive' in s.lower() or len(s) < 3:
            continue

        deets = s.strip().split(' ')
        distance = deets[1]
        sense_name = deets[0].capitalize()
        senses.append({
            "distance": int(distance),
            "name": sense_name
        })
    return senses


def convert_legendary_actions(monster_name, behaviours):

    body = f"The {monster_name} can take 3 legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. The {monster_name} regains spent legendary actions at the start of its turn."

    for b in behaviours:
        name = b['name']
        desc = b['description'].strip()
        restrictions = b['restrictions']

        action_title = f"{name} ({restrictions})" if restrictions else name
        body = body + f"\n\n{action_title}. {desc}"

    return {
        "body": body,
        "title": "Legendary Actions"
    }


def convert_reactions(behaviours):
    reactions = []

    for b in behaviours:
        name = b['name']
        desc = b['description'].strip()
        restrictions = b['restrictions']

        reaction_title = f"{name} ({restrictions})" if restrictions else name
        reactions.append(f"{reaction_title}. {desc}")

    return {
        "body": '\n\n'.join(reactions),
        "title": "Reactions"
    }


def convert_traits(behaviours):
    blocks = []
    for b in behaviours:
        name = b['name']
        desc = b['description'].strip()
        restrictions = b['restrictions']

        trait_title = f"{name} ({restrictions})" if restrictions else name

        blocks.append({
            "body": desc,
            "title": trait_title
        })

    return blocks


def convert_text_blocks(monster_name, behaviours):
    traits = convert_traits(
        [b for b in behaviours if b['monsterBehaviorType'] == 'Trait'])
    legendaries = convert_legendary_actions(
        monster_name, [b for b in behaviours if b['monsterBehaviorType'] == 'Legendary'])
    reactions = convert_reactions(
        [b for b in behaviours if b['monsterBehaviorType'] == 'Reaction'])

    abilities_text_block = {
        "textBlocks": traits + [legendaries] + [reactions],
        "title": "Abilities"
    }

    full_text_blocks = default_text_blocks + [abilities_text_block]

    return full_text_blocks


def parse_ranges(attack_range_string):
    attack_range_string = attack_range_string.lower().replace(
        'range', '').replace('ft', '').replace('.', '')

    range_deets = attack_range_string.split('/')
    short_range = int(range_deets[0])
    long_range = int(range_deets[1])

    return short_range, long_range


def convert_actions(behaviors):
    actions = []

    for i, b in enumerate(behaviors):
        if b['monsterBehaviorType'] != 'Action':
            continue

        ability = 'str' if b['attackType'] == "MeleeWeapon" else 'dex'
        attack_step = {
            "attack": {
                "ability": ability,
                "crit": 20,
                "damageRolls": [
                    {
                        "abilityName": ability,
                        "dice": b["damageRoll"],
                                "type": b["damageType"]
                    }
                ],
                "isProficient": True,
                "name": b['name']
            },
            "type": "custom-attack"
        }

        if b['attackType'] == 'RangedWeapon':
            short, long = parse_ranges(b['range'])
            attack_step["attack"]["isRanged"] = True
            attack_step["attack"]["longRange"] = long
            attack_step["attack"]["range"] = short

        actions.append({
            "description": b['description'],
            "name": b['name'],
            "sortOrder": i,
            "steps": [
                attack_step
            ]
        })

    return actions


def convert_save_profs(saves):
    if saves is None:
        return []
    save_abbrevs = [save.strip().lower()[:3] for save in saves]
    save_profs = []
    for x in ATTRIBUTES:
        for s in save_abbrevs:
            if x.startswith(s):
                save_profs.append({
                    "name": x.capitalize(),
                    "type": 'save'
                })

    return save_profs


def convert_damage_type(damages):
    return [{"damageType": x} for x in damages]


def convert(monster):

    prof_bonus = CR_TO_PB[str(monster["challengeRating"])]

    result = {
        'abilityScores': convert_ability_scores(monster),
        'actions': convert_actions(monster['behaviors']),
        'alignment': monster["alignment"].title(),
        'armorClass': int(monster["armorClass"]),
        'armorType': monster["armorType"].title() if monster["armorType"] else '',
        'challengeRating': monster["challengeRating"],
        'classes': [
            {
                "class": "Monster",
                "level": 1
            }
        ],
        "conditionImmunities": monster['conditionImmunities'],
        "damageImmunities": convert_damage_type(monster['damageImmunities']),
        "damageResistances": convert_damage_type(monster['damageResistances']),
        "damageVulnerabilities": convert_damage_type(monster['damageVulnerabilities']),
        'currentHp': int(monster["hitPoints"]),
        'description': monster["flavorText"] if monster["flavorText"].strip() != "" else monster["sectionText"],
        'exp': int(monster["experiencePoints"]),
        'hitDice': monster["hitPointRoll"].replace(' ', ''),
        # image
        'initiativeBonus': 0,
        'isNPC': True,
        'maxHp': int(monster["hitPoints"]),
        "movementModes": convert_movement_modes(monster['speeds']),
        'name': monster["name"],
        'proficiencies': convert_profs(monster['languages'], monster['savingThrows']),
        'proficiencyBonus': prof_bonus,
        'race': "NPC",
        'senses': convert_senses(monster["senses"]),
        'size': monster['size'].title(),
        'skills': convert_skills(monster, prof_bonus),
        'speed': int(monster["speed"]),
        'systemKey': "5e",
        'textBlocks': convert_text_blocks(monster['name'], monster['behaviors']),
        'type': monster['types'][0].title()
    }

    return result


def main():
    with open('./all_sw5e_monsters_export.json') as f:
        all_monsters = json.load(f)

    parsed_monsters = [convert(m) for m in all_monsters]

    all = {
        'characters': parsed_monsters
    }
    with open('./all_parsed_sw5e_monsters_alchemy.json', 'w', encoding='utf-8') as f:
        json.dump(all, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
