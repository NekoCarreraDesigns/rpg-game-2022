# screen settings for rpg game
tile_size = 64
fps = 60
screen_width = 1200
screen_height = 720

# ui
bar_height = 20
health_bar_width = 200
energy_bar_width = 140
item_box_size = 80
ui_font = './level graphics/graphics/font/joystix.ttf'
ui_font_size = 18

# ui colors
health_color = 'red'
energy_color = 'blue'
ui_border_color_active = 'gold'

# general colors
water_color = '#71ddee'
ui_bg_color = '#222222'
ui_border_color = '#111111'
text_color = '#EEEEEE'

# upgrade menu
text_bar_color = '#111111'
bar_color = '#EEEEEE'
bar_color_selected = '#111111'
upgrade_bg_color_selected = '#EEEEEE'

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': './level graphics/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': './level graphics/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': './level graphics/graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': './level graphics/graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': './level graphics/graphics/weapons/sai/full.png'}}

# magic spells
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': './level graphics/graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': './level graphics/graphics/particles/heal/heal.png'}}

# monster dictionary
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound': '../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',  'attack_sound': '../audio/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 110, 'damage': 8, 'attack_type': 'thunder', 'attack_sound': '../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack', 'attack_sound': '../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
