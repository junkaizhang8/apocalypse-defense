# Jun Kai Zhang
# April 7, 2021
# ICS3U0 - C
# This program creates a game in Pygame called Apocalypse Defense. The goal
# of this game is to try and survive 10 waves of zombies without letting the
# base shield run out of energy. The character defending the base shoots out
# bullets to deal damage to the zombies. The user can control their character
# by pressing W or S keys.

import pygame
import sys
import random

class Image(pygame.sprite.Sprite):
    def __init__(self, image, x_value, y_value, x_change):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.x_value = x_value
        self.y_value = y_value
        self.x_change = x_change
        self.rect = self.image.get_rect()
        self.rect.center = [x_value, y_value]

class Zombie(Image):
    def __init__(self,image, x_value, y_value, x_change, health_points,\
                 current_health,coin_drop):
        super().__init__(image, x_value, y_value, x_change)
        self.health_points = health_points
        self.current_health = current_health
        self.coin_drop = coin_drop
        self.sprite_image = image
        
    def update(self):
        global total_coins, zombies_alive, current_shield_energy
        if self.sprite_image == "abnormal zombie.png":
            self.x_change -= 0.01
        elif self.sprite_image == "healing zombie.png":
            if self.current_health < self.health_points:
                self.current_health += 0.25
        elif self.sprite_image == "demon zombie.png":
            if self.current_health <= (self.health_points * 0.75):
                self.x_change = -5
                self.image = pygame.image.load("enraged demon zombie.png")             
        else:
            pass
        self.x_value = self.x_value + self.x_change
        self.rect.center = (self.x_value, self.y_value)
        if self.x_value <= 200 or self.current_health <= 0:
            if self.current_health <= 0:
                total_coins += self.coin_drop
            else:
                current_shield_energy -= self.current_health
            zombies_alive -= 1
            self.kill()
            
    def resetZombie(self):
        self.kill()
        
class Bullet(Image):
    def __init__(self,image, x_value, y_value, x_change, damage):
        super().__init__(image, x_value, y_value, x_change)
        self.damage = damage
        
    def update(self):
        self.x_value = self.x_value + self.x_change
        self.rect.center = (self.x_value, self.y_value)
        if self.x_value > 1000:
            self.kill()
    def resetBullet(self):
        self.kill()

class Button(pygame.sprite.Sprite):
    def __init__(self, image, x_value, y_value, width, height, button_colour,\
                 press_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.x_value = x_value
        self.y_value = y_value
        self.width = width
        self.height = height
        self.button_colour = button_colour
        self.press_colour = press_colour
        
    def display_button(self, button_type):
        global button_pressed
        draw_button = True
        mouse_position = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x_value, self.y_value, self.width,\
                                  self.height)
        if button_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.draw.rect(screen, self.press_colour, button_rect)
                button_pressed = True
            else:
                if button_pressed:
                    image = buttonConditionCheck(button_type)
                    if image != None:
                        self.image = pygame.image.load(image)
                        self.image_width = self.image.get_width()
                        self.image_height = self.image.get_height()
                    else:
                        draw_button = False
                    button_pressed = False
                if draw_button != False:
                    pygame.draw.rect(screen, self.button_colour, button_rect)
                else:
                    if button_type == "return":
                        return True
        else:       
            pygame.draw.rect(screen, self.button_colour, button_rect)
        if draw_button != False:
            screen.blit(self.image, (((self.x_value + self.width / 2)\
                                     - (self.image_width / 2)),\
                                    ((self.y_value + self.height / 2)\
                                     - (self.image_height / 2))))
        if button_type == "return":
            return False
        
            
def startup(background):
    clock.tick(60)
    screen.fill(background)
    # This is part of the graphical user interface where the program fills the
    # Pygame window with a colour given by the parameter background.

def spriteLocation(sprite_image, x_value, y_value):
    screen.blit(sprite_image, (x_value, y_value))

def returnToMenu(x_value, y_value, width, height):
    button_colour = (150, 75, 0)
    button_press_colour = (200, 100, 0)    
    return_button = Button("return to menu.png", x_value, y_value, width,\
                           height, button_colour, button_press_colour)
    return_to_menu = return_button.display_button("return")
    return return_to_menu
    
def energyInputInterface():
    global current_time, invalid_message_start_time, invalid_message_display,\
           screen_width
    background = (200, 140, 0)
    startup(background)            
    input_box = pygame.Rect(300, 280, 400, 40)
    pygame.draw.rect(screen, (255, 255, 255), input_box)
    request_font = pygame.font.Font("freesansbold.ttf", 20)
    
    input_request = request_font.render("Please enter the amount of energy you \
want for the base shield.", True, (255, 255, 255))
    input_request_width = input_request.get_width()
    screen.blit(input_request,\
                (screen_width / 2 - input_request_width / 2, 100))
    
    range_text = request_font.render("Required input: Any integer from \
1 - 1000.", True, (255, 255, 255))
    range_text_width = range_text.get_width()
    screen.blit(range_text,\
                (screen_width / 2 - range_text_width / 2, 150))
    
    confirm_text = request_font.render("Press ENTER to confirm your input.",\
                                       True, (255, 255, 255))
    confirm_text_width = confirm_text.get_width()
    screen.blit(confirm_text,\
                (screen_width / 2 - confirm_text_width / 2, 350))

    if invalid_message_display == True:
        display_time = current_time - invalid_message_start_time
        if display_time > 2000:
            invalid_message_display = False
        else:
            invalidInput()

def characterInput():
    global shield_energy, character_counter, inputting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                inputting = False
            elif event.key == pygame.K_BACKSPACE:
                if character_counter > 0:
                    character_counter -= 1
                    shield_energy = shield_energy[0: character_counter]
            else:
                if user_text_width <= 350:
                    shield_energy += event.unicode
                    character_counter += 1

def invalidInput():
    # The purpose of this function is to display an invalid message when the
    # user doesn't enter an integer between 1 and 1000 during the shield energy
    # input interface. The function uses the global keyword screen_width. It
    # first renders (or creates a new surface) the string for the invalid
    # message, then enter True for the antialias (meaning smooth edges), then
    # enter the RGB values for the colour of the text, then enter nothing for
    # the background of the surface. The program stores this surface in
    # invalid_text. Then, calculate the width of invalid_text and store it in
    # text_width. Finally, the program displays invalid text on the screen at
    # the location (screen_width / 2 - text_width / 2, 500).
    global screen_width
    invalid_text = font.render("The input value for the shield \
must be an integer between 1 and 1000!", True, (255, 0, 0))
    text_width = invalid_text.get_width()
    screen.blit(invalid_text, (screen_width / 2 - text_width / 2, 500))

def buttonConditionCheck(button_type):
    global shield_input_flag, menu_flag, rules_flag, page_number, gameplay_flag
    if button_type == "bullet upgrade":
        image = bulletUpgrade()
    elif button_type == "unlock ability":
        image = unlockAbility(button_type)
    elif button_type == "unlock heal":
        image = unlockAbility(button_type)
    elif button_type == "play":
        shield_input_flag = True
        menu_flag = False
        return None
    elif button_type == "rules":
        rules_flag = True
        return None
    elif button_type == "exit":
        pygame.quit()
        sys.exit()
    elif button_type == "next page":
        page_number += 1
        if page_number == 6:
            return None
        else:
            image = "next page.png"
    elif button_type == "previous page":
        page_number -= 1
        if page_number == 1:
            return None
        else:
            image = "previous page.png"
    elif button_type == "menu":
        page_number = 1
        rules_flag = False
        return None
    elif button_type == "return":
        gameplay_flag = False
        return None
    
    return image

def buttonColour(cost):
    global total_coins
    if total_coins < cost:
        button_colour = (200, 0, 0)
    else:
        button_colour = (0, 200, 0)
    return button_colour
    
def pressColour(cost):
    # This is a function that determines the upgrade/unlock buttons' colours
    # when pressed.The function has a parameter for cost. The function uses the
    # global keyword total_coins. It checks if total_coins is less than cost.
    # If true, it will assign the RGB value (255, 0, 0) to press_colour, also
    # known as red. If total_coins is not less than cost, it will assign the
    # RGB value (0, 255, 0) to press_colour, also known as green. It will then
    # return the value of press_colour.
    
    global total_coins
    if total_coins < cost:
        press_colour = (255, 0, 0)
    else:
        press_colour = (0, 255, 0)
    return press_colour

def bulletUpgrade():
    global total_coins, upgrade_cost, bullet_tier, bullet_sprite, damage,\
           upgrade_button_image, message_display
    if total_coins >= upgrade_cost:
        total_coins -= upgrade_cost
        bullet_tier += 1
        bullet_sprite = bullet_types[bullet_tier][0]
        damage = bullet_types[bullet_tier][1]
        if bullet_tier == 4:
            upgrade_cost = ""
            upgrade_button_image = ""
            return None
        else:
            upgrade_cost = bullet_types[bullet_tier][2]
            upgrade_button_image = bullet_types[bullet_tier + 1][0]
    else:
        message_display = True
    return upgrade_button_image

def unlockAbility(button_type):
    global total_coins, ability_unlock_cost, ability_unlocked, ability_image,\
           heal_unlock_cost, heal_unlocked, heal_image, message_display
    if button_type == "unlock ability":
        if total_coins >= ability_unlock_cost:
            total_coins -= ability_unlock_cost
            ability_unlocked = True
            return None
        else:
            message_display = True
            return ability_image
    else:
        if total_coins >= heal_unlock_cost:
            total_coins -= heal_unlock_cost
            heal_unlocked = True
            return None
        else:
            message_display = True
            return heal_image

def insufficientCoinMessage(message_start_time, screen_width):
    global current_time, message_display, message_cooldown_flag
    time_since_message = current_time - message_start_time
    if time_since_message > 2000:
        message_display = False
        message_cooldown_flag = True
    else:
        insufficient_coins = font.render("You do not have enough coins!",\
                                         True, (255, 0, 0))
        width = insufficient_coins.get_width()
        screen.blit(insufficient_coins, (screen_width / 2 - width / 2, 450))

def buttonCostDisplay(cost, x_value, y_value):
    cost_text = font.render(cost, True, (0, 0, 0))
    text_width = cost_text.get_width()
    screen.blit(cost_text, (x_value - text_width / 2, y_value))

def bulletReadyCheck(bullet_sprite):
    global bullet_start_time, ability_set_time, current_time, ability_unlocked,\
           damage, ability_ready
    time_since_last_bullet = current_time - bullet_start_time
            
    if time_since_last_bullet > 300:
        shootBullet()
        bullet_start_time = current_time

def specialAbility():
    global current_time, ability_ready, time_now, ability_time,\
           ability_happening, ability_cooldown_flag
    ability_happening = True
    time_since_activation = current_time - ability_time
    time_since_last_bullet = current_time - time_now
    if time_since_activation < 1500:
        if time_since_last_bullet > 30:
            shootBullet()
            time_now = current_time
    else:
        time_now = current_time
        ability_activation_set_time = time_now
        ability_ready = False
        ability_happening = False
        ability_cooldown_flag = True

def healShield():
    global shield_energy, current_shield_energy, heal_cooldown_flag,\
           heal_ready, heal_happening
    heal_amount = shield_energy * 0.3
    current_shield_energy += heal_amount
    round(current_shield_energy, 2)
    if current_shield_energy >= shield_energy:
        current_shield_energy = shield_energy
    activation_time = pygame.time.get_ticks()
    heal_cooldown_flag = True
    heal_ready = False
    heal_happening = True
    return activation_time

def shootBullet():
    global bullet_sprite, character_x_coordinate, character_y_coordinate, damage
    bullet_x_coordinate = character_x_coordinate + 85
    bullet_y_coordinate = character_y_coordinate + 38
    bullet_speed = 12
    spawned_bullet = Bullet(bullet_sprite, bullet_x_coordinate,\
                            bullet_y_coordinate, bullet_speed, damage)
    bullet_group.add(spawned_bullet)    

def drawAbilityIcon(x_value, y_value, unlocked, image, recharge, cooldown,\
                    colour, key):
    if unlocked:
        side_length = 50
        # Here we assign the integer 50 into the variable side_length. This
        # value will be the side length of the square that will be displayed
        # along with the ability icon.
        image = pygame.image.load(image)
        image_width = image.get_width()
        image_height = image.get_height()
        countdown = round((cooldown - recharge) / 1000)
        if countdown <= 0:
            countdown = 0
            countdown_text = "Ready!"
        else:
            countdown_text = "Countdown: " + str(countdown)
            # This is an assignment and string casting example. We cast
            # countdown, which is an integer, into a string. Then, we add the
            # string "Countdown: " by countdown and assign it to the variable
            # countdown_text.
        
        icon = pygame.Rect(x_value, y_value, side_length, side_length)
        pygame.draw.rect(screen, colour, icon)
        screen.blit(image, (((x_value + side_length / 2)\
                                    - (image_width / 2)),\
                                   ((y_value + side_length / 2)\
                                    - (image_height / 2))))
        
        output_text = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(output_text, (x_value + side_length + 5,\
                                  y_value +\
                                  (image_height / 2)))
        hotkey = font.render(key, True, (0, 0, 0))
        screen.blit(hotkey, (x_value + side_length + 5,\
                             y_value +\
                             (image_height / 2) - 25))
    else:
        pass
    
def zombieSpawnCheck():
    global zombie_start_time, current_time, number_of_zombies, zombie_count
    delta_time = current_time - zombie_start_time
    if delta_time > 800 and zombie_count < number_of_zombies:
        zombie_count += 1
        zombie_list = list(zombie_types_in_wave.items())
        random_zombie = random.choice(zombie_list)
        zombie_x_coordinate = 1010
        zombie_y_coordinate = random.randrange(155, 436, 70)
        # The module function random.randrange is used here to generate a
        # random y-value for a zombie that is spawning. The starting number in
        # the range is 155 and the ending number is 436, though the range
        # excludes the number itself. Starting at 155, each number can only be
        # in steps of 70 from the original number. This means it only has 5
        # possible y-values to generate from: 155, 225, 295, 365, 435, with each
        # value determining which lane the zombie will spawn at.
        
        health_points = random_zombie[1][1]
        current_health = random_zombie[1][1]
        horizontal_change = random_zombie[1][2]
        coin_drop = random_zombie[1][3]
        spawned_zombie = Zombie(random_zombie[1][0], zombie_x_coordinate,\
                                zombie_y_coordinate, horizontal_change,\
                                health_points, current_health, coin_drop)
        zombie_group.add(spawned_zombie)
        zombie_start_time = current_time

def energyBar(shield_energy, current_shield_energy, energy_colour):
    black = (0, 0, 0) # This is a tuple for the RGB values for black.
    red = (255, 0, 0) # This is a tuple for the RGB values for red.
    base_energy_text = font.render("Shield Energy", True, black)
    text_height = base_energy_text.get_height()
    pygame.draw.rect(screen, black, [296, 46, 408, 38])
    pygame.draw.rect(screen, red, [300, 50, 400, 30])
    pygame.draw.rect(screen, energy_colour, [300, 50, current_shield_energy * \
                                     (400 / shield_energy), 30])
    screen.blit(base_energy_text, (150, 50 + 30 / 2 - text_height / 2))
    current_to_total_energy_ratio = font.render(f"{current_shield_energy} /\
{shield_energy}", True, black)
    screen.blit(current_to_total_energy_ratio, (304, 50 + 30 / 2 -\
                                                text_height / 2))
    
def healthBar(x_value, y_value, full_health, current_health):
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    pygame.draw.rect(screen, black, [x_value - 37, y_value - 52, 52, 7])
    pygame.draw.rect(screen, red, [x_value - 35, y_value - 50, 50, 5])
    pygame.draw.rect(screen, green, [x_value - 35, y_value - 50, current_health\
                                   * (50 / full_health), 5])

def coinDisplay(total_coins):
    coins = font.render(str(total_coins), True, (0, 0, 0))
    screen.blit(coins, (70,40))
    
def nextWave(wave):
    global new_wave_flag, zombie_count, gameplay_flag
    if zombies_alive == 0:
        zombie_types_in_wave.clear()
        wave += 1
        zombie_count = 0
        new_wave_flag = True
    else:
        pass
    if wave <= 10:
        wave_text = font.render("Wave " + str(wave), True, (0, 0, 0))
        width = wave_text.get_width()
        screen.blit(wave_text, (screen_width / 2 - width / 2, 20))
    return wave

def winScreen():
    global screen_width, gameplay_flag
    background = (0, 128, 0)
    startup(background)
    win_message = pygame.image.load("win.png")
    win_message_width = win_message.get_width()
    spriteLocation(win_message, screen_width / 2 -\
                   win_message_width /2, 200)
    return_to_menu = returnToMenu(425, 450, 150, 50)
    if return_to_menu == True:
        # For loops are used here to delete every bullet and zombie object.
        
        # For every zombie object in zombie_group, call resetZombie() method
        # in their class called Zombie. This method will delete the object.
        for zombie in zombie_group:
            zombie.resetZombie()
        # For every bullet sprite in bullet_group, call resetBullet() method
        # in their class called Bullet. This method will delete the object.
        for bullet in bullet_group:
            bullet.resetBullet()
        gameplay_flag = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
def loseScreen():
    global screen_width, gameplay_flag
    background = (128, 0, 0)
    startup(background)
    lose_message = pygame.image.load("lose.png")
    lose_message_width = lose_message.get_width()
    spriteLocation(lose_message, screen_width / 2 -\
                   lose_message_width / 2, 200)
    return_to_menu = returnToMenu(425, 450, 150, 50)
    if return_to_menu == True:
        for zombie in zombie_group:
            zombie.resetZombie()
        for bullet in bullet_group:
            bullet.resetBullet()
        gameplay_flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


pygame.init()

character_image = pygame.image.load("character.png")

shield_image = pygame.image.load("shield.png")

coin_image = pygame.image.load("coin.png")

ability_image = "bullet storm.png"
heal_image = "heal.png"

zombie_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

game_rules = {1: "page 1.png", 2: "page 2.png", 3: "page 3.png",\
              4: "page 4.png", 5: "page 5.png", 6: "page 6.png"}

bullet_types = {1: ["bullet 1.png", 10, 500], 2: ["bullet 2.png", 15, 1100],\
                3: ["bullet 3.png", 30, 2500], 4: ["bullet 4.png", 50, ""]}

zombie_types = {"Basic": ["basic zombie.png", 40, -1, 20],\
                "Hungry": ["hungry zombie.png", 30, -2, 25],\
                "Crawling": ["crawling zombie.png", 80, -0.7, 25],\
                "Abnormal": ["abnormal zombie.png", 90, -0.1, 35],\
                "Lightning": ["lightning zombie.png", 50, -4.5, 45],\
                "Shield": ["shield zombie.png", 210, -0.6, 45],\
                "Healing": ["healing zombie.png", 140, -0.75, 50],\
                "Demon": ["demon zombie.png", 250, -0.55, 65]}
# This dictionary stores the attributes (image, health, x_change, coin_drop) of
# each individual zombie. Inside each key, a list is used to store all the
# attributes of that zombie.

waves_event = {1: ["Basic"] ,\
               2: ["Basic","Hungry"],\
               3: ["Basic", "Hungry","Crawling"],\
               4: ["Basic", "Hungry", "Crawling"],\
               5: ["Hungry", "Crawling", "Abnormal"],\
               6: ["Abnormal", "Lightning", "Shield"],\
               7: ["Abnormal", "Lightning", "Shield"],\
               8: ["Abnormal", "Lightning", "Shield", "Healing"],\
               9: ["Abnormal", "Lightning", "Shield", "Healing", "Demon"],\
               10: ["Demon"]}

zombies_in_wave = {1: 10, 2: 15, 3: 18, 4: 28, 5: 24, 6: 22, 7: 32, 8: 44,\
                   9: 55, 10: 40}
# This is a dictionary for the number of zombies appearing in each wave. The
# key represents the wave number and the value represents the number of zombies.

zombie_types_in_wave = {}

cement_lines = {1: 200, 2: 270, 3: 340, 4: 410}
ability_cooldown = 25000
heal_cooldown = 50000

font = pygame.font.Font("freesansbold.ttf", 20)

clock = pygame.time.Clock()

bullet_start_time = pygame.time.get_ticks()
zombie_start_time = pygame.time.get_ticks()

invalid_message_start_time = 0

main_flag = True

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Apocalypse Defense")

# This is the main loop. All other while loops for specific tasks such as rules
# or gameplay are all nested inside the main loop. Things such as wave and
# bullet_tier and other important gameplay variables are assigned here and not
# inside the other nested loops so that once the user decides to exit the
# gameplay loop, all the stats during that round will reset.
while main_flag:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    character_x_coordinate = 70
    character_y_coordinate = 255
    
    zombie_count = 0
    zombies_alive = 0
    
    wave = 0
    
    bullet_tier = 1
    bullet_sprite = bullet_types[bullet_tier][0]
    damage = bullet_types[bullet_tier][1]
    upgrade_cost = bullet_types[bullet_tier][2]
    upgrade_button_image = bullet_types[bullet_tier + 1][0]
    
    ability_unlock_cost = 1250
    heal_unlock_cost = 700
    
    total_coins = 0
    message_current_time = 0
    ability_recharge = 0
    heal_recharge = 0
    
    ability_unlocked = False
    heal_unlocked = False
    button_pressed = False
    message_display = False
    ability_ready = False
    heal_ready = False
    ability_happening = False
    heal_happening = False
    ability_cooldown_flag = True
    heal_cooldown_flag = True
    message_cooldown_flag = True
    invalid_message_display = False
    
    menu_flag = True
    rules_flag = False
    shield_input_flag = False
    gameplay_flag = False
    new_wave_flag = True
    
    page_number = 1
    
    while menu_flag:
        background = (200, 140, 0)
        startup(background)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        name = font.render("Jun Kai Zhang", True, (0, 0, 0))
        name_width = name.get_width()
        name_height = name.get_height()
        screen.blit(name, (screen_width - name_width - 5,\
                           screen_height - name_height - 5))
        
        menu_button_colour = (150, 75, 0)
        menu_button_press_colour = (200, 100, 0)
        
        title_image = pygame.image.load("title.png")
        title_width = title_image.get_width()
        spriteLocation(title_image, screen_width / 2 - title_width / 2, 50)
        play_button = Button("play.png", 350, 200, 300, 100,\
                             menu_button_colour, menu_button_press_colour)
        play_button.display_button("play")
        
        rules_button = Button("rules.png", 350, 325, 300, 100,\
                              menu_button_colour, menu_button_press_colour)
        rules_button.display_button("rules")
        
        exit_button = Button("exit.png", 350, 450, 300, 100,\
                             menu_button_colour, menu_button_press_colour)
        exit_button.display_button("exit")
        pygame.display.update()
        
        while rules_flag:
            background = (200, 140, 0)
            startup(background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            current_page = pygame.image.load(game_rules[page_number])
            spriteLocation(current_page, 0, 0)
            # The two lines of code above is used to display a specific rule
            # page depending on page_number. It first loads an image in the
            # dictionary game_rules with the key determined by page_number.
            # It is then stored in current_page. Then,
            # spriteLocation(sprite_image, x_value, y_value) function is called
            # with the parameters being current_page, 0, and 0 in order to
            # display on the screen.
            if page_number < 6:
                next_page_button = Button("next page.png", 730, 520, 240, 60,\
                                          menu_button_colour,\
                                          menu_button_press_colour)
                next_page_button.display_button("next page")
            if page_number > 1:
                previous_page_button = Button("previous page.png", 30, 520,\
                                              240, 60, menu_button_colour,\
                                              menu_button_press_colour)
                previous_page_button.display_button("previous page")
            menu_button = Button("main menu.png", 380, 520, 240, 60,\
                                 menu_button_colour, menu_button_press_colour)
            menu_button.display_button("menu")
            
            pygame.display.update()
            
    while shield_input_flag:
        input_font = pygame.font.Font("freesansbold.ttf", 40)
        shield_energy = ""
        character_counter = 0
        inputting = True
        insertion_point = True
        while inputting:
            current_time = pygame.time.get_ticks()
            if insertion_point == True:
                insertion_point_timer = pygame.time.get_ticks()
                insertion_point = False
            energyInputInterface()
            user_text = input_font.render(shield_energy, True,\
                                          (0, 0, 0))
            screen.blit(user_text, (300, 280))
            user_text_width = user_text.get_width()
            time_since_text_cursor = current_time - insertion_point_timer
            if time_since_text_cursor < 600:
                text_cursor = input_font.render("|", True, (0, 0, 0))
                screen.blit(text_cursor, (300 + user_text_width + 1, 280))
            elif time_since_text_cursor > 1200:
                insertion_point = True
            else:
                pass
            
            return_to_menu = returnToMenu(880, 0, 120, 50)
            pygame.display.update()
            
            if return_to_menu == True:
                inputting = False
                shield_input_flag = False
                break
            else:
                characterInput()
                                               
        if return_to_menu != True:
            try:
                shield_energy = int(shield_energy)
                if shield_energy in range(1, 1001):
                    current_shield_energy = shield_energy
                    gameplay_flag = True
                    shield_input_flag = False
                else:
                    invalid_message_start_time = pygame.time.get_ticks()
                    invalid_message_display = True
                    inputting = True
            except ValueError:
                invalid_message_start_time = pygame.time.get_ticks()
                invalid_message_display = True
                inputting = True
            # This section of code uses exception handling. It first tries to
            # cast shield_energy (whatever the user typed) into an integer.
            # If it can be cast into an integer, check if shield_energy is in
            # range from 1-1000. If true, current_shield_energy is equal to
            # shield energy. Assign True to gameplay_flag and False to
            # shield_input_flag. If shield_energy is not in range from 1-1000,
            # get the current time in milliseconds since the program initiated
            # and assign True to invalid_message_display and inputting. If
            # shield_energy cannot be cast into an integer, get the current
            # time in milliseconds since the program was initiated and assign
            # True to invalid_message_display and inputting.
            pygame.display.update()
    
    # This while loop is used to continuously run the gameplay aspect of the
    # game. If gameplay_flag is false, it means the user is no longer playing
    # the game and is instead on the menu or inputting the shield energy.
    while gameplay_flag:
        current_time = pygame.time.get_ticks()
        
        if current_shield_energy <= 0:
            loseScreen()
        else:         
            background = (135, 206, 235)
            startup(background)
            cement = pygame.Rect(0, 130, 1000, 350)
            pygame.draw.rect(screen, (128, 128, 128), cement)
            
            for line in cement_lines:
                new_line = pygame.Rect(0, cement_lines[line], 1000, 4)
                pygame.draw.rect(screen, (0, 0, 0), new_line)
            
            grass = pygame.Rect(0, 480, 1000, 120)
            pygame.draw.rect(screen, (198, 171, 114), grass)
            
            return_to_menu = returnToMenu(880, 0, 120, 50)
            if return_to_menu == True:
                for zombie in zombie_group:
                    zombie.resetZombie()
                for bullet in bullet_group:
                    bullet.resetBullet()
                gameplay_flag = False
            else:
                energyBar(shield_energy, current_shield_energy,\
                          (0, 75, 255))                
                if ability_cooldown_flag:
                    previous_ability_end_time = pygame.time.get_ticks()
                    ability_cooldown_flag = False
                if heal_cooldown_flag:
                    previous_heal_end_time = pygame.time.get_ticks()
                    heal_cooldown_flag = False
                
                ability_recharge = current_time - previous_ability_end_time
                heal_recharge = current_time - previous_heal_end_time
                
                if ability_recharge > ability_cooldown:
                    ability_ready = True
                if heal_recharge > heal_cooldown:
                    heal_ready = True
                
                wave = nextWave(wave)
                
                if wave > 10:
                    if current_shield_energy <= 0:
                        loseScreen()
                    else:
                        winScreen()
                # This section of code uses conditional statements to check if
                # the user has won or not after when they pass wave 10. It
                # first checks if wave is greater than 10. If true, check if
                # current_shield_energy is less than or equal to 0. If true,
                # call loseScreen() function. If false, call winScreen()
                # function.
                
                else:
                    spriteLocation(shield_image, 150, 130)
                    # This line displays shield_image at the location (150, 130)
                    # on the game screen. This is a visual cue to show the user
                    # where the shield is located and where the zombies are
                    # trying to reach.
                    
                    ability_unlock_button_colour =\
                        buttonColour(ability_unlock_cost)
                    ability_unlock_press_colour =\
                        pressColour(ability_unlock_cost)
                    
                    heal_unlock_button_colour =\
                        buttonColour(heal_unlock_cost)
                    heal_unlock_press_colour =\
                        pressColour(heal_unlock_cost)
                    
                    if bullet_tier != 4:
                        bullet_upgrade_button_colour =\
                            buttonColour(upgrade_cost)
                        bullet_upgrade_press_colour =\
                            pressColour(upgrade_cost)
                        
                        upgrade_button = Button(upgrade_button_image,\
                                                550, 510, 100, 50,\
                                                bullet_upgrade_button_colour,\
                                                bullet_upgrade_press_colour)
                    
                        upgrade_button.display_button("bullet upgrade")
                        if bullet_tier != 4:
                            buttonCostDisplay(str(upgrade_cost), 550 + 100 / 2,\
                                              565)
                    else:
                        pass
                    
                    if ability_unlocked == False:
                        ability_unlock_button =\
                            Button(ability_image, 700, 510, 100, 50,\
                                   ability_unlock_button_colour,\
                                   ability_unlock_press_colour)
                        ability_unlock_button.display_button("unlock ability")
                        
                        buttonCostDisplay(str(ability_unlock_cost),\
                                          700 + 100 / 2, 565)
                        
                    if heal_unlocked == False:
                        heal_unlock_button =\
                            Button(heal_image, 850, 510, 100, 50,\
                                   heal_unlock_button_colour,\
                                   heal_unlock_press_colour)
                        heal_unlock_button.display_button("unlock heal")
                        
                        buttonCostDisplay(str(heal_unlock_cost),\
                                          850 + 100 / 2, 565)
                        
                    if message_display:
                        if message_cooldown_flag:
                            message_start_time = pygame.time.get_ticks()
                            message_cooldown_flag = False
                        insufficientCoinMessage(message_start_time,\
                                                screen_width)
                
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                character_y_coordinate -= 70
                                if character_y_coordinate < 115:
                                    character_y_coordinate = 115
                            elif event.key == pygame.K_s:
                                character_y_coordinate += 70
                                if character_y_coordinate > 395:
                                    character_y_coordinate = 395
                            elif event.key == pygame.K_f:
                                if ability_unlocked and ability_ready:
                                    if ability_happening == False:
                                        time_now = pygame.time.get_ticks()
                                        ability_time = pygame.time.get_ticks()
                                        specialAbility()
                            elif event.key == pygame.K_g:
                                if heal_unlocked and heal_ready:
                                    activation_time = healShield()
                            else:
                                pass
                    # This block of code checks if user has either exited or
                    # pressed any of specific keys mentioned in the code, such
                    # as W, S, F, or G (input). If user presses W or S, it will
                    # increase/decrease the character_y_coordinate (processing).
                    # As a result, the program would be showing the character
                    # sprite moving up or down (output).
                    
                    if ability_happening == False:
                        bulletReadyCheck(bullet_sprite)
                    else:
                        specialAbility()
                    
                    drawAbilityIcon(50, 525, ability_unlocked, ability_image,\
                                    ability_recharge, ability_cooldown,\
                                    (0, 0, 200), "(F)")
                    drawAbilityIcon(300, 525, heal_unlocked, heal_image,\
                                    heal_recharge, heal_cooldown,\
                                    (0, 200, 0), "(G)")
                    
                    if new_wave_flag:
                        number_of_zombies = zombies_in_wave[wave]
                        zombies_alive = number_of_zombies
                        zombies = waves_event[wave]
                        for zombie in zombies:
                            zombie_types_in_wave[zombie] = zombie_types[zombie]
                        new_wave_flag = False
                        
                    zombieSpawnCheck()
                    
                    if bullet_group and zombie_group:
                        for bullet in bullet_group:
                            for zombie in zombie_group:
                                collision =\
                                    pygame.sprite.collide_rect(bullet,zombie)
                                if collision:
                                    zombie.current_health -= damage
                                    bullet.kill()
                    # This block of code uses conditional statements to check
                    # if any bullet object stored in bullet_group have
                    # collided with any zombie object stored in zombie_group.
                    # It first checks if bullet_group and zombie_group have
                    # anything in them. If true, for every zombie in
                    # zombie_group, check for every bullet in bullet_group. The 
                    # program then checks if the rectangles (in this case, the 
                    # dimensions of the png file) around the bullet and zombie 
                    # overlap. If true, subtract the zombie's current health by
                    # damage and kill the bullet object.
                    
                    coinDisplay(total_coins)
                    spriteLocation(coin_image, 20, 15)
                    spriteLocation(character_image, character_x_coordinate,\
                                   character_y_coordinate)
                    
                    zombie_group.draw(screen)
                    zombie_group.update()
                    for zombie in zombie_group:
                        healthBar(zombie.x_value, zombie.y_value,\
                                  zombie.health_points,\
                                  zombie.current_health)    
                    bullet_group.draw(screen)
                    bullet_group.update()
                    
                    if heal_happening:
                        effect_duration = current_time - activation_time
                        if effect_duration < 200:
                            energyBar(shield_energy, current_shield_energy,\
                                      (0, 150, 255))
                        else:
                            heal_happening = False

        pygame.display.update()