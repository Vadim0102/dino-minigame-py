from threading import Thread
from os import system
from time import sleep
from random import randint, choice

# Настройки игры
long_terrain = 30
clear_screen_cmd = "clear"
max_y = 5
god_mode = False
bot_mode = False
hard_mode = False
easy_mode = False
fly_mode = False
dino = ">"
died_dino = "X"
bird = "<"
cactus = "!"
# Поменяйте на знак "=" если выводится "?"
floor = "¯"
decorations_on_field = (".", "_")

chance = 5
chance_birds = 1
chance_decor = 2
speed = 0.1

# Переменные
game_on = True
jumps = 0
score = 0
y = 0
walked = 0
fields = " " * long_terrain
sky = " " * long_terrain
modes = {
  "GOD": god_mode,
  "BOT": bot_mode,
  "HARD": hard_mode,
  "EASY": easy_mode,
  "FLY": fly_mode
}

def output_screen(y, fields, score, jumps, dino, cactus, floor, modes, sky, died_dino=dino):
  output_down = fields
  if y >= 1:
    if died_dino == dino:
      output_up = sky[0] + died_dino + sky[1:]
    else:
      output_up = sky[0] + dino + sky[1:]
  else:
    output_up = sky
    if died_dino == dino:
      output_down = output_down[0] + dino + output_down[1:]
    else:
      output_down = output_down[0] + died_dino + output_down[1:]
  system(clear_screen_cmd)
  modes_spisok = ""
  for i in modes:
    if modes[i]:
      modes_spisok += i + " "
  print(f"""Score {score}  Jumps {jumps}
  
  {output_up}
  {output_down}
  {floor * long_terrain}
  Press Enter to Jump!\n\n""" + modes_spisok)

def trigger_jump():
  global y
  global game_on
  while game_on:
    try:
      input()
      if y == 0:
        jump_execute()
    except KeyboardInterrupt:
      game_on = False
      exit()

def jump_execute():
  global y
  global jumps
  global score
  y = max_y
  jumps += 1
  score += 10

def gen_cactuses(chance):
  global fields
  if randint(0, 99) < chance:
    fields += cactus
  else:
    fields += " "

def gen_decor(chance_decor):
  global fields
  if randint(0, 99) < chance_decor and fields[-1] == " ":
    fields = fields[:-1] + choice(decorations_on_field)

def gen_birds(chance_birds):
  global sky
  if randint(0, 99) < chance_birds and sky[-1] == " ":
    sky = sky[:-1] + bird
  else:
    sky += " "

def bot_jump(y, fields):
  if y == 0 and fields[2] == cactus:
    jump_execute()

def main():
  global y
  global score
  global fields
  global sky
  global jumps
  global chance
  global chance_decor
  global chance_birds
  global walked
  global game_on
  global dino
  global died_dino
  global cactus
  global floor
  global modes
  global speed
  while game_on:
    if fly_mode:
      y = 999
    # Если включено автопрыг
    if bot_mode:
      bot_jump(y, fields)
    # Падение дино
    if y >= 1:
      y -= 1
    # Проверка кактусов
    fields = fields[1:]
    gen_cactuses(chance)
    gen_decor(chance_decor)
    sky = sky[1:]
    gen_birds(chance_birds)
    # Если кактус на месте дино, и дино не в прыжке, и годмод выключен
    if fields[1] == cactus and y == 0 and not god_mode:
      # Проигрыш!
      output_screen(y, fields, score, jumps, dino, cactus, floor, modes, sky, died_dino)
      print("Game Over")
      print(score, jumps)
      exit()
    # Если птица в месте с дино, и дино в прыжке, и годмод выключен
    elif sky[1] == bird and y >= 1 and not god_mode:
      # Проигрыш!
      output_screen(y, fields, score, jumps, dino, cactus, floor, modes, sky, died_dino)
      print("Game Over")
      print(score, jumps)
      exit()
    if hard_mode:
      chance = randint(5, 12)
      speed = randint(1, 10) / 10
    if easy_mode:
      chance = randint(0, 5)
    score += 20
    walked += 1
    output_screen(y, fields, score, jumps, dino, cactus, floor, modes, sky)
    sleep(speed)

th = Thread(target=trigger_jump)
th.start()
main()