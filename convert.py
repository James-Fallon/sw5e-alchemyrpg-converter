import json
from constants import ATTRIBUTES, WEAPON_TYPES, SKILLS_TO_ABILITIES

def convert_classes(full_dict: dict) -> list:
    output_classes = [{
            "class": full_dict["class"],
            "level": full_dict["level"]
    }]
    return output_classes

def convert_ability_scores(full_dict: dict) -> list:
    results = []
    for x in ATTRIBUTES:
        results.append({
            'name': x.lower()[:3],
            'value': full_dict[x]
        })
    return results

def convert_skills(attribs):
    result = []
    for skill in SKILLS_TO_ABILITIES.keys():

        prof_level = attribs[f'{skill}_type']

        result.append({
            "abilityName": SKILLS_TO_ABILITIES[skill],
            "doubleProficiency": prof_level == 2,
            "name": skill.replace('_', ' ').title(),
            "proficient": prof_level == 1
        })

    return result

def get_tool_profs(attribs):

    tool_ids = []
    for x in attribs.keys():
        if x.startswith('repeating_tool'):
            id = x.split('_')[2]
            if id not in tool_ids:
                tool_ids.append(id)

    tool_profs = []
    for tool_id in tool_ids:
        tool_profs.append({
            "name": attribs[f"repeating_tool_{tool_id}_toolname"],
            "type": "tool"
        })
    
    return tool_profs

def get_save_profs(attribs):
    save_profs = []
    for x in ATTRIBUTES:
        if attribs[f"{x}_save_prof"] != 0:
            save_profs.append({
                "name": x.capitalize(),
                "type": 'save'
            })
    
    return save_profs

def convert_profs(attribs):
    all_profs = get_save_profs(attribs)
    all_profs.extend(get_tool_profs(attribs))
    all_profs.extend(get_weapon_and_armor_profs(attribs))
    return all_profs

def add_weapon_group(weapon_type):
    result = []
    
    for x in WEAPON_TYPES[weapon_type]:
        result.append({
            "name": x,
            "type": 'weapon'
        })
    return result

def get_weapon_and_armor_profs(attribs):
    prof_ids = []
    for x in attribs.keys():
        if x.startswith('repeating_proficiencies'):
            id = x.split('_')[2]
            if id not in prof_ids:
                prof_ids.append(id)

    profs = []
    for prof_id in prof_ids:
        name  = attribs[f"repeating_proficiencies_{prof_id}_name"].title()
        type_key = f"repeating_proficiencies_{prof_id}_prof_type"

        if name in WEAPON_TYPES.keys():
            profs.extend(add_weapon_group(name))
            continue

        if type_key not in attribs.keys():
            type = 'language'
        else:
            type = attribs[f"repeating_proficiencies_{prof_id}_prof_type"].lower()
        profs.append({
            "name": name,
            "type": type
        })
    
    return profs

def _parse_repeating_fields(attribs, type):
    ids = []
    for x in attribs.keys():
        if x.startswith(f'repeating_{type}'):
            id = x.split('_')[2]
            if id not in ids:
                ids.append(id)
    
    items = []
    for id in ids:
        starter_str = f'repeating_{type}_{id}'
        keys = [x.split(starter_str)[1] for x in attribs.keys() if x.startswith(starter_str)]
        keys = [x[1:] for x in keys]
        item = {}
        for x in keys:
            item[x] = attribs[f'{starter_str}_{x}']
        items.append(item)
    return items

def get_inventory(attribs):
    return(_parse_repeating_fields(attribs, 'inventory'))

def get_traits(attribs):
    return(_parse_repeating_fields(attribs, 'traits'))

def get_attacks(attribs):
    return(_parse_repeating_fields(attribs, 'attack'))

def convert_text_blocks(attribs):
    traits = get_traits(attribs)
    text_blocks = convert_traits_to_text_blocks(traits)

    add_defaults_to_text_blocks(text_blocks)

    return text_blocks

def convert_spells(attribs):
    spell_ids = []
    for x in attribs.keys():
        if x.startswith('repeating_power-'):

            _ = x.split('repeating_power-')[1].split('_')
            id = _[0] + '_' + _[1]
            if id not in spell_ids:
                spell_ids.append(id)

    spells = []
    for spell_id in spell_ids:

        spell_level = spell_id.split('_')[0]
        level = 0 if spell_level == 'cantrip' else int(spell_level)
        base = f"repeating_power-{spell_id}_"

        spell_name = 'SW ' + attribs[f"{base}powername"]

        spells.append({
            "castingTime": attribs[f"{base}powercastingtime"].title(),
            "components": [
                "V",
                "S",
                "M"
            ],
            "description": attribs[f"{base}powerdescription"],
            "duration": attribs[f"{base}powerduration"],
            "level": level,
            "name": spell_name,
            "range": attribs[f"{base}powerrange"],
            "requiresConcentration": attribs[f"{base}powerconcentration"] != "0",
            "savingThrow": {
                # TODO - Can't get this yet - maybe parse description
            },
            "school": attribs[f"{base}powerschool"].title(),
            "tags": [
                attribs["class"]
            ]
        })

    return spells

def parse_spell_slots(attribs):
    # We are crudely doing 
    # force points = level 1 spell slots 
    # tech points = level 2 spell slots
    # TODO - change this once 'Variant: Spell Points' rule is available in Alchemy
    return [
        {
            "max": attribs["force_power_points_total"],
            "remaining": attribs["force_power_points_total"]
        },
        {
            "max": attribs["tech_power_points_total"],
            "remaining": attribs["tech_power_points_total"]
        },

    ]

def add_defaults_to_text_blocks(text_blocks):
    # If we don't have empty dicts for these the character sheet will break when editing
    blocks_we_have = [x["title"] for x in text_blocks]
    
    defaults_required = [
        "Class Features",
        "Racial Traits",
        "Feats",
        "Characteristics",
        "Appearance",
        "Organizations",
        "Allies",
        "Enemies",
        "Backstory",
        "Background",
        "Other"
    ]

    for default in defaults_required:
        if default not in blocks_we_have:
            if default == 'Characteristics':
                text_blocks.append({'title': default,"textBlocks": [
                    {"title": "Personality Traits"},
                    {"title": "Ideals"},
                    {"title": "Bonds"},
                    {"title": "Flaws"}
                ]})
            else:
                text_blocks.append({'title': default,"textBlocks": [{}]})

def convert_traits_to_text_blocks(traits):
    text_block_categories = {}

    for trait in traits:
        category = trait["source"]
        text_block = {
            "body": trait["description"],
            "title": trait["name"]
        }
        if category not in text_block_categories:
            text_block_categories[category] = [text_block]
        else:
            text_block_categories[category].append(text_block)

    result = []
    for cat, tblocks in text_block_categories.items():
        result.append({
            "title": "Class Features" if cat == 'Feat' else cat,
            "textBlocks": tblocks
        })
    
    return result

def pivot_attribs(attribs):
    res = {}
    hp_max = 0
    hd_max = ""
    for x in attribs:
        res[x['name']] = x['current']
        if x['name'] == 'hp':
            hp_max = x["max"]
        if x['name'] == 'hit_dice':
            hd_max = x["max"]

    return res, hp_max, hd_max

def get_attr_from_attack(attack_string):
    for attr in ATTRIBUTES:
        if attr in attack_string:
            return attr[:3]

def parse_ranges(attack_range_string):
    range_deets = attack_range_string.split('(range')[1].strip().split('/')

    short_range = int(range_deets[0])
    long_range = int(range_deets[1])

    return short_range, long_range

def convert_items_with_actions(attribs):
    items_with_actions = []

    items = get_inventory(attribs)
    attacks = get_attacks(attribs)

    # TODO - what about armor?

    for i in items:
        is_weapon = i["itemname"].title() in WEAPON_TYPES['All Weapons']
        item = {
            "cost": "UNKNOWN",
            "name": i["itemname"].title(),
            "properties": [],
            "quantity": int(i["itemcount"]),
            "type": "Weapon" if is_weapon else "Adventuring gear",
            "weaponType": i["itemname"].title(),
            "weight": float(i["itemweight"])
        }

        weapon_attacks = [a for a in attacks if a["atkname"] == i["itemname"]]
        
        if not is_weapon or len(weapon_attacks) == 0:
            items_with_actions.append({
                "item": item
            })
            continue

        actions = []
        for count, attack in enumerate(weapon_attacks):
            attack_attr = get_attr_from_attack(attack["atkattr_base"])
            damage_attr = get_attr_from_attack(attack["dmgattr"])

            attack_step = {
                "ability": attack_attr,
                "crit": 20,
                "damageRolls": [
                    {
                    "abilityName": damage_attr,
                    "dice": attack["dmgbase"],
                    "type": attack["dmgtype"]
                    }
                ],
                "isProficient": True, # Just say yes for now
                "name": f"{i['itemname'].title()} Attack",
                "rollsAttack": True,
                "savingThrow": {
                } # TODO
            }
            
            is_ranged = attack["atkrange"].strip() != ""
            if is_ranged:
                attack_step["isRanged"] = True
                short_range, long_range = parse_ranges(attack["atkrange"])
                attack_step["range"] = short_range
                attack_step["longRange"] = long_range
            else:
                attack_step["isRanged"] = False

            actions.append({
                "name": f"{i['itemname'].title()} Attack",
                "sortOrder": count+1,
                "steps": [
                    {
                        "attack": attack_step,
                        "type": "custom-attack"
                    }
                ]
            })

        items_with_actions.append({
            "actions": actions,
            "item": item
        })

    return items_with_actions

def convert(input_dict):
    
    attribs, hp_max, hd_max = pivot_attribs(input_dict["attribs"])

    result = {
        'name': input_dict["name"],
        'maxHp': int(hp_max),
        'hitDice': hd_max,
        'abilityScores': convert_ability_scores(attribs),
        'alignment': attribs["alignment"],
        'armorClass': int(attribs["ac"]),
        'classes': convert_classes(attribs),
        'currentHp': int(attribs["hp"]),
        'exp': int(attribs["experience"]),
        'eyes': attribs["eyes"],
        'gold': attribs["cr"], # todo - can we just change this to credits in Alchemy?
        'hair': attribs["hair"],
        'height': attribs["height"],
        'initiativeBonus': int(attribs["initiative_bonus"]),
        'isNPC': False,
        'isSpellcaster': True, # TODO - Not sure how to get this
        'itemsWithActions': convert_items_with_actions(attribs), 
        'movementModes': [], # Is this needed?
        'proficiencies': convert_profs(attribs),
        'proficiencyBonus': int(attribs["pb"]),
        'race': attribs["race"],
        'size': 'Medium', # TODO - not available i dont think
        'skills': convert_skills(attribs),
        'skin': attribs["skin"],
        'speed': int(attribs["speed"].split(' ')[0]),
        'spellFilters': ["Known"], # Not sure on this 
        'spellSlots': parse_spell_slots(attribs), 
        'spellcastingAbility': "wis", # TODO - not sure how to get this
        'spells': convert_spells(attribs),
        'systemKey': "5e",
        'textBlocks': convert_text_blocks(attribs),
        'trackers': [] # TODO - this will be hard to implement
    }
    
    return result

def main():
    with open('./sampleSW5e_roll20Export.json') as f:
        sw5e_json = json.load(f)

    alchemyjson = convert(sw5e_json)

    with open('./alchemy-character.json', 'w', encoding='utf-8') as f:
        json.dump(alchemyjson, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
