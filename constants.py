ATTRIBUTES = [
    'strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma'
]

SIMPLE_BLASTERS = [
    'Blaster Carbine',
    'Bowcaster',
    'Ion Carbine',
    'Light Pistol',
    'Light Repeater',
    'Light Slugpistol',
    'Hold-out',
    'Needler',
    'Scattergun',
    'Shotgun',
    'Slugpistol',
    'Tranquilizer Rifle',
    'Wristblaster',
    'Wrist Launcher'
]

MARTIAL_BLASTERS = [
    'Assault Cannon',
    'Blaster Cannon',
    'Blaster Pistol',
    'Blaster Rifle',
    'Carbine Rifle',
    'Chaingun',
    'Cycler Rifle',
    'Heavy Bowcaster',
    'Heavy Pistol',
    'Heavy Shotgun',
    'Heavy Slugpistol',
    'Hunting Rifle',
    'Ion Pistol',
    'Ion Rifle',
    'Repeating Blaster',
    'Revolver',
    'Slugthrower',
    'Sniper Rifle',
    'Subrepeater'
]

SIMPLE_VIBROWEAPONS = [
    'Techaxe',
    'Vibrodagger',
    'Vibrodart',
    'Vibroknuckler',
    'Vibromace',
    'Vibrostaff',
    'Vibrospear'
]

MARTIAL_VIBROWEAPONS = [
    'Chakram',
    'Doubleblade',
    'Doublesword',
    'Hidden Blade',
    'Net',
    'Techblade',
    'Techstaff',
    'Vibroaxe',
    'Vibrobaton',
    'Vibroblade',
    'Vibrolance',
    'Vibropike',
    'Vibrorapier',
    'Vibrosword',
    'Vibrowhip'
]

SIMPLE_LIGHTWEAPONS = ['Lightclub', 'Lightdagger', 'Lightsaber', 'Shotosaber']
MARTIAL_LIGHTWEAPONS = ['Doublesaber', 'Doubleshoto', 'Greatsaber', 'Lightfoil',
                        'Light Ring', 'Lightsaber Pike', 'Martial Lightsaber', 'Saberspear', 'Saberwhip']

WEAPON_TYPES = {
    'Simple Blasters': SIMPLE_BLASTERS,
    'Martial Blasters': MARTIAL_BLASTERS,
    'All Blasters': SIMPLE_BLASTERS + MARTIAL_BLASTERS,
    'Simple Vibroweapons': SIMPLE_VIBROWEAPONS,
    'Martial Vibroweapons': MARTIAL_VIBROWEAPONS,
    'All Vibroweapons': SIMPLE_VIBROWEAPONS + MARTIAL_VIBROWEAPONS,
    'Simple Lightweapons': SIMPLE_LIGHTWEAPONS,
    'Martial Lightweapons': MARTIAL_LIGHTWEAPONS,
    'All Lightweapons': SIMPLE_LIGHTWEAPONS + MARTIAL_LIGHTWEAPONS,
    'All Weapons': SIMPLE_BLASTERS + MARTIAL_BLASTERS + SIMPLE_VIBROWEAPONS + MARTIAL_VIBROWEAPONS + SIMPLE_LIGHTWEAPONS + MARTIAL_LIGHTWEAPONS
}

SKILLS_TO_ABILITIES = {
    'athletics': 'str',
    'acrobatics': 'dex', 'sleight_of_hand': 'dex', 'stealth': 'dex',
    'investigation': 'int', 'lore': 'int', 'nature': 'int', 'piloting': 'int', 'technology': 'int',
    'animal_handling': 'wis', 'insight': 'wis', 'medicine': 'wis', 'perception': 'wis', 'survival': 'wis',
    'deception': 'cha', 'intimidation': 'cha', 'performance': 'cha', 'persuasion': 'cha'
}

CR_TO_PB = {
    "0": 2,
    '1/8': 2,
    '1/4': 2,
    '1/2': 2,
    '1': 2,
    '2': 2,
    '3': 2,
    '4': 2,
    '5': 3,
    '6': 3,
    '7': 3,
    '8': 3,
    '9': 4,
    '10': 4,
    '11': 4,
    '12': 4,
    '13': 5,
    '14': 5,
    '15': 5,
    '16': 5,
    '17': 6,
    '18': 6,
    '19': 6,
    '20': 6,
    '21': 7,
    '22': 7,
    '23': 7,
    '24': 7,
    '25': 8,
    '26': 8,
    '27': 8,
    '28': 8,
    '29': 9,
    '30': 9}
