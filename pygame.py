import pygame
import sys
import random
import time
import math
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
FPS = 60

font_small = pygame.font.SysFont(None, 24)
font_medium = pygame.font.SysFont(None, 36)
font_large = pygame.font.SysFont(None, 48)

class GameData:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.reset()
        return cls._instance
    
    @classmethod
    def reset(cls):
        cls.player_name = ""
        cls.defeated_opponents = {}
        cls.player_level = 1
        cls.player_xp = 0
        cls.player_max_hp = 120
        cls.player_damage = 25
        cls.player_sp_charge_rate = 10
        cls.player_sp_usage = 0
        cls.player_crit_chance = 5
        cls.player_abilities = []
        cls.current_upgrades = []
    
    def add_win(self, opponent_name):
        if opponent_name in self.defeated_opponents:
            self.defeated_opponents[opponent_name] += 1
        else:
            self.defeated_opponents[opponent_name] = 1

class GameState:
    def __init__(self, game):
        self.game = game
    
    def handle_events(self, events):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass

class LoadingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = time.time()
        self.duration = 3
        self.progress = 0
        self.tips = [
            "Совет: Противники имеют разные предпочтения в выборе",
            "Совет: Используйте специальные атаки когда шкала SP заполнена",
            "Совет: После победы выбирайте улучшения, которые дополняют ваш стиль игры",
            "Совет: Критические удары наносят в 1.5 раза больше урона",
            "Совет: Уровень повышается после победы над несколькими противниками"
        ]
        self.current_tip = random.choice(self.tips)
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(2, 5),
                'speed': random.uniform(0.5, 2),
                'color': (random.randint(50, 200), random.randint(50, 200), random.randint(200, 255))
            })
    
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    def update(self):
        elapsed = time.time() - self.start_time
        self.progress = min(elapsed / self.duration, 1.0)
        
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > SCREEN_HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, SCREEN_WIDTH)
        
        if elapsed > self.duration:
            self.game.change_state(ChooseOpponentState(self.game))
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        for p in self.particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
        
        text = font_large.render("ЗАГРУЗКА БОЕВОГО МОДУЛЯ", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(text, text_rect)

        bar_width = SCREEN_WIDTH * 0.7
        bar_height = 30
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT // 2
        
        pygame.draw.rect(screen, WHITE, (bar_x-2, bar_y-2, bar_width+4, bar_height+4), 2)

        progress_width = int(bar_width * self.progress)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, bar_height))
        
        percent = int(self.progress * 100)
        percent_text = font_medium.render(f"{percent}%", True, WHITE)
        screen.blit(percent_text, (bar_x + bar_width + 20, bar_y))
        
        tip_text = font_small.render(self.current_tip, True, ORANGE)
        screen.blit(tip_text, (SCREEN_WIDTH//2 - tip_text.get_width()//2, bar_y + 100))
        

        for i in range(8):
            angle = time.time() * 5 + i * math.pi/4
            radius = 10 + math.sin(time.time() * 3 + i) * 5
            x = SCREEN_WIDTH//2 + math.cos(angle) * 100
            y = SCREEN_HEIGHT//2 + 200 + math.sin(angle) * 30
            pygame.draw.circle(screen, BLUE, (int(x), int(y)), int(radius))

class ChooseOpponentState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.player_name = GameData().player_name
        self.opponents = self.generate_opponents()
        self.selected_index = 0
        self.input_active = not bool(self.player_name)
        self.rotation_angle = 0
        self.animation_time = 0
    
    def generate_opponents(self):
        level = GameData().player_level
        base_hp = 100 + (level - 1) * 20
        base_damage = 20 + (level - 1) * 5
        
        return [
            {
                "name": "Бульдог",
                "hp": int(base_hp * 0.9),
                "max_hp": int(base_hp * 0.9),
                "damage": base_damage,
                "prefs": {"rock": 0.7, "scissors": 0.2, "paper": 0.1},
                "color": (139, 69, 19),
                "sp_rate": 8,
                "sp_chance": 30,
                "crit_chance": 10,
                "image": "bulldog",
                "quotes": {
                    "win": ["Ты слаб!", "Еще один легкий бой!", "Ха-ха, проиграл!"],
                    "lose": ["Невозможно...", "Ты сильнее, чем кажешься!", "Я недооценил тебя..."],
                    "draw": ["Ничья? Скучно!", "Давай решительнее!", "Снова одинаково?"]
                }
            },
            {
                "name": "Лис",
                "hp": base_hp,
                "max_hp": base_hp,
                "damage": int(base_damage * 1.1),
                "prefs": {"rock": 0.1, "scissors": 0.7, "paper": 0.2},
                "color": (255, 140, 0),
                "sp_rate": 12,
                "sp_chance": 50,
                "crit_chance": 15,
                "image": "fox",
                "quotes": {
                    "win": ["Было слишком легко!", "Ты предсказуем!", "Победа за мной!"],
                    "lose": ["Умно сыграно...", "Ты перехитрил меня!", "Неожиданный ход..."],
                    "draw": ["Интересно...", "Равные силы?", "У нас похожая тактика"]
                }
            },
            {
                "name": "Феникс",
                "hp": int(base_hp * 1.3),
                "max_hp": int(base_hp * 1.3),
                "damage": int(base_damage * 0.8),
                "prefs": {"rock": 0.2, "scissors": 0.2, "paper": 0.6},
                "color": (255, 69, 0),
                "sp_rate": 15,
                "sp_chance": 40,
                "crit_chance": 5,
                "image": "phoenix",
                "quotes": {
                    "win": ["Пламя победы!", "Ты сгорел!", "Моя стихия сильнее!"],
                    "lose": ["Ты погасил мое пламя...", "Поражение? Невероятно!", "Сильнее, чем я ожидал..."],
                    "draw": ["Равная мощь!", "Огонь встретил огонь?", "Ничья в поединке стихий"]
                }
            }
        ]
    
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if self.input_active:
                    if event.key == K_RETURN and self.player_name.strip():
                        self.input_active = False
                        GameData().player_name = self.player_name
                    elif event.key == K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.unicode.isprintable():
                        self.player_name += event.unicode
                else:
                    if event.key == K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.opponents)
                    elif event.key == K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.opponents)
                    elif event.key == K_RETURN:
                        self.game.start_battle(self.opponents[self.selected_index])
                    elif event.key == K_s:
                        self.game.change_state(StatsState(self.game))
    
    def draw(self, screen):
        screen.fill((30, 30, 50))
        
        title = font_large.render("ВЫБОР ПРОТИВНИКА", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Информация об игроке
        player_info = font_medium.render(
            f"{GameData().player_name} | Уровень: {GameData().player_level} | XP: {GameData().player_xp}/100", 
            True, GREEN
        )
        screen.blit(player_info, (SCREEN_WIDTH//2 - player_info.get_width()//2, 80))
        
        if self.input_active:
            input_text = font_medium.render(f"Ваш ник: {self.player_name}", True, WHITE)
            screen.blit(input_text, (SCREEN_WIDTH//2 - 150, 140))
            hint = font_small.render("Введите ник и нажмите Enter", True, WHITE)
            screen.blit(hint, (SCREEN_WIDTH//2 - 120, 180))
        else:
            hint = font_small.render("Нажмите S для просмотра статистики", True, WHITE)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 140))
        
        self.rotation_angle += 0.5
        self.animation_time += 0.05
        for i, opponent in enumerate(self.opponents):
            is_selected = i == self.selected_index
            x = SCREEN_WIDTH // 2 + (i - 1) * 250
            y = SCREEN_HEIGHT // 2 - 50
            
            # Выделение выбранного противника
            if is_selected:
                radius = 100
                pygame.draw.circle(screen, (100, 100, 150, 100), (x, y), radius + 10, 3)
                
                pygame.draw.rect(screen, (50, 50, 70), (x - 120, y + 90, 240, 180))
                pygame.draw.rect(screen, WHITE, (x - 120, y + 90, 240, 180), 2)
                
                name_text = font_medium.render(opponent["name"], True, WHITE)
                screen.blit(name_text, (x - name_text.get_width()//2, y + 110))
                
                hp_text = font_small.render(f"HP: {opponent['hp']}", True, WHITE)
                screen.blit(hp_text, (x - 100, y + 150))
                
                dmg_text = font_small.render(f"Урон: {opponent['damage']}", True, WHITE)
                screen.blit(dmg_text, (x - 100, y + 180))
                
                crit_text = font_small.render(f"Крит: {opponent['crit_chance']}%", True, WHITE)
                screen.blit(crit_text, (x - 100, y + 210))
                
                sp_text = font_small.render(f"SP: {opponent['sp_rate']}/ход", True, WHITE)
                screen.blit(sp_text, (x + 10, y + 150))
                
                spc_text = font_small.render(f"Шанс SP: {opponent['sp_chance']}%", True, WHITE)
                screen.blit(spc_text, (x + 10, y + 180))
                
                pref_text = font_small.render(f"Предпочтение: {max(opponent['prefs'], key=opponent['prefs'].get)}", True, WHITE)
                screen.blit(pref_text, (x - pref_text.get_width()//2, y + 240))
            
            # Аватар противника
            angle = self.rotation_angle if is_selected else 0
            self.draw_opponent_avatar(screen, x, y, 80, opponent["color"], angle, opponent["name"], self.animation_time)
        
        # Подсказки
        if not self.input_active:
            hint = font_small.render("← → для выбора, Enter - начать бой", True, WHITE)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))
    
    def draw_opponent_avatar(self, screen, x, y, radius, color, angle, name, animation_time):
        # Анимация выбранного противника
        pulse = math.sin(animation_time * 5) * 5 if name == self.opponents[self.selected_index]["name"] else 0
        r = radius + int(pulse)
        
        # Рисуем разных противников
        if name == "Бульдог":
            # Тело
            pygame.draw.circle(screen, color, (x, y), r)
            # Уши
            pygame.draw.circle(screen, color, (x - r//2, y - r//2), r//3)
            pygame.draw.circle(screen, color, (x + r//2, y - r//2), r//3)
            # Морда
            pygame.draw.circle(screen, (200, 150, 150), (x, y + r//4), r//2)
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - r//4, y), r//6)
            pygame.draw.circle(screen, WHITE, (x + r//4, y), r//6)
            pygame.draw.circle(screen, BLACK, (x - r//4, y), r//12)
            pygame.draw.circle(screen, BLACK, (x + r//4, y), r//12)
            # Нос
            pygame.draw.circle(screen, BLACK, (x, y + r//4), r//8)
            
        elif name == "Лис":
            # Тело
            pygame.draw.ellipse(screen, color, (x - r, y - r//2, r*2, r))
            # Голова
            pygame.draw.circle(screen, color, (x, y - r//2), r//1.5)
            # Уши
            pygame.draw.polygon(screen, color, [
                (x - r//2, y - r), 
                (x - r//3, y - r*1.5), 
                (x, y - r)
            ])
            pygame.draw.polygon(screen, color, [
                (x + r//2, y - r), 
                (x + r//3, y - r*1.5), 
                (x, y - r)
            ])
            # Хвост
            pygame.draw.ellipse(screen, color, (x + r//2, y, r, r//2))
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - r//4, y - r//2), r//6)
            pygame.draw.circle(screen, WHITE, (x + r//4, y - r//2), r//6)
            pygame.draw.circle(screen, BLACK, (x - r//4, y - r//2), r//12)
            pygame.draw.circle(screen, BLACK, (x + r//4, y - r//2), r//12)
            # Нос
            pygame.draw.circle(screen, BLACK, (x, y - r//4), r//10)
            
        elif name == "Феникс":
            # Тело
            pygame.draw.circle(screen, color, (x, y), r)
            # Крылья
            for i in range(3):
                wing_color = (color[0], max(0, color[1] - 50*i), max(0, color[2] - 20*i))
                wing_x = x + math.cos(animation_time + i*2) * r
                wing_y = y + math.sin(animation_time + i*2) * r
                pygame.draw.circle(screen, wing_color, (int(wing_x), int(wing_y)), r//2)
            # Голова
            pygame.draw.circle(screen, (255, 200, 0), (x, y - r), r//2)
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - r//6, y - r), r//8)
            pygame.draw.circle(screen, WHITE, (x + r//6, y - r), r//8)
            pygame.draw.circle(screen, BLACK, (x - r//6, y - r), r//16)
            pygame.draw.circle(screen, BLACK, (x + r//6, y - r), r//16)
            # Клюв
            pygame.draw.polygon(screen, (255, 200, 0), [
                (x - r//8, y - r*0.9), 
                (x + r//8, y - r*0.9), 
                (x, y - r*0.7)
            ])

class BattleState(GameState):
    def __init__(self, game, opponent):
        super().__init__(game)
        self.opponent = opponent
        self.player_hp = GameData().player_max_hp
        self.opponent_hp = opponent["hp"]
        self.player_choice = None
        self.opponent_choice = None
        self.result = None
        self.message = ""
        self.dialog_timer = 0
        self.dialog_duration = 2.5
        self.game_over = False
        self.winner = None
        self.player_sp = 0
        self.opponent_sp = 0
        self.player_sp_charge = GameData().player_sp_charge_rate
        self.critical_hit = False
        self.player_used_sp = False
        self.opponent_used_sp = False
        self.ability_used = None
        self.ability_cooldown = 0
        self.round_count = 0
        self.animation_time = 0
        self.damage_popups = []
    
    def handle_events(self, events):
        if self.game_over:
            for event in events:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    if self.winner == "player":
                        self.game.change_state(UpgradeState(self.game))
                    else:
                        self.game.change_state(ChooseOpponentState(self.game))
            return
        
        if self.ability_cooldown > 0:
            return
        
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                # Камень
                if 100 <= x <= 200 and 550 <= y <= 650:
                    self.make_choice("rock")
                # Ножницы
                elif 400 <= x <= 500 and 550 <= y <= 650:
                    self.make_choice("scissors")
                # Бумага
                elif 700 <= x <= 800 and 550 <= y <= 650:
                    self.make_choice("paper")
                # Специальная атака
                elif 900 <= x <= 950 and 50 <= y <= 150 and self.player_sp >= 100:
                    self.use_special_attack()
                # Способности
                elif 50 <= x <= 90 and y >= 600 and len(GameData().player_abilities) > 0:
                    ability_index = (y - 600) // 40
                    if ability_index < len(GameData().player_abilities):
                        self.use_ability(GameData().player_abilities[ability_index])
    
    def use_ability(self, ability):
        if ability == "Лечение" and self.player_hp < GameData().player_max_hp:
            heal_amount = min(30, GameData().player_max_hp - self.player_hp)
            self.player_hp += heal_amount
            self.message = f"Вы восстановили {heal_amount} HP!"
            self.ability_used = ability
            self.ability_cooldown = 3
            self.damage_popups.append({
                'x': 100, 'y': 200, 
                'text': f"+{heal_amount} HP", 
                'color': GREEN,
                'timer': 60
            })
        elif ability == "Усиление" and self.player_sp < 100:
            self.player_sp = min(100, self.player_sp + 50)
            self.message = "Ваша SP увеличена на 50!"
            self.ability_used = ability
            self.ability_cooldown = 3
            self.damage_popups.append({
                'x': 100, 'y': 200, 
                'text': "+50 SP", 
                'color': PURPLE,
                'timer': 60
            })
        elif ability == "Ослабление":
            sp_loss = min(30, self.opponent_sp)
            self.opponent_sp = max(0, self.opponent_sp - 30)
            self.message = f"{self.opponent['name']} потерял {sp_loss} SP!"
            self.ability_used = ability
            self.ability_cooldown = 4
            self.damage_popups.append({
                'x': 800, 'y': 200, 
                'text': f"-{sp_loss} SP", 
                'color': RED,
                'timer': 60
            })
        elif ability == "Критический удар":
            self.critical_hit = True
            self.message = "Следующий удар будет критическим!"
            self.ability_used = ability
            self.ability_cooldown = 5
    
    def use_special_attack(self):
        self.player_used_sp = True
        self.player_sp = 0
        self.player_choice = None
        self.opponent_choice = None
        self.determine_outcome()
    
    def make_choice(self, player_choice):
        self.player_choice = player_choice
        
        if self.opponent_sp >= 100 and random.randint(1, 100) <= self.opponent["sp_chance"]:
            self.opponent_used_sp = True
            self.opponent_sp = 0
        else:
            self.opponent_used_sp = False
            choices = list(self.opponent["prefs"].keys())
            weights = list(self.opponent["prefs"].values())
            self.opponent_choice = random.choices(choices, weights=weights)[0]
        
        self.determine_outcome()
    
    def determine_outcome(self):
        if self.player_used_sp and self.opponent_used_sp:
            self.result = "sp_vs_sp"
            damage = self.calculate_damage(GameData().player_damage * 1.5, True)
            self.opponent_hp -= damage
            opp_damage = self.calculate_damage(self.opponent["damage"] * 1.5, False)
            self.player_hp -= opp_damage
            self.message = (f"Столкновение спец.атак! Вы нанесли {damage} урона, "
                           f"получили {opp_damage} урона!")
            self.damage_popups.append({
                'x': 800, 'y': 200, 
                'text': f"-{damage}", 
                'color': RED,
                'timer': 60
            })
            self.damage_popups.append({
                'x': 200, 'y': 200, 
                'text': f"-{opp_damage}", 
                'color': RED,
                'timer': 60
            })
        elif self.player_used_sp:
            self.result = "win"
            damage = self.calculate_damage(GameData().player_damage * 1.5, True)
            self.opponent_hp -= damage
            self.message = f"Спец.атака! Нанесено {damage} урона! {random.choice(self.opponent['quotes']['lose'])}"
            self.damage_popups.append({
                'x': 800, 'y': 200, 
                'text': f"-{damage}", 
                'color': RED,
                'timer': 60
            })
        elif self.opponent_used_sp:
            self.result = "lose"
            damage = self.calculate_damage(self.opponent["damage"] * 1.5, False)
            self.player_hp -= damage
            self.message = f"Спец.атака противника! Получено {damage} урона! {random.choice(self.opponent['quotes']['win'])}"
            self.damage_popups.append({
                'x': 200, 'y': 200, 
                'text': f"-{damage}", 
                'color': RED,
                'timer': 60
            })
        elif self.player_choice == self.opponent_choice:
            self.result = "draw"
            self.message = f"Ничья! Оба выбрали {self.translate_choice(self.player_choice)}. {random.choice(self.opponent['quotes']['draw'])}"
        elif ((self.player_choice == "rock" and self.opponent_choice == "scissors") or
              (self.player_choice == "scissors" and self.opponent_choice == "paper") or
              (self.player_choice == "paper" and self.opponent_choice == "rock")):
            self.result = "win"
            damage = self.calculate_damage(GameData().player_damage, True)
            self.opponent_hp -= damage
            self.message = (f"{self.translate_choice(self.player_choice)}! Нанесено {damage} урона! "
                          f"{random.choice(self.opponent['quotes']['lose'])}")
            self.damage_popups.append({
                'x': 800, 'y': 200, 
                'text': f"-{damage}", 
                'color': RED,
                'timer': 60
            })
        else:
            self.result = "lose"
            damage = self.calculate_damage(self.opponent["damage"], False)
            self.player_hp -= damage
            self.message = (f"{self.translate_choice(self.opponent_choice)}! Получено {damage} урона! "
                          f"{random.choice(self.opponent['quotes']['win'])}")
            self.damage_popups.append({
                'x': 200, 'y': 200, 
                'text': f"-{damage}", 
                'color': RED,
                'timer': 60
            })
        
        if self.result == "win":
            self.player_sp = min(100, self.player_sp + self.player_sp_charge + 20)
        elif self.result == "draw":
            self.player_sp = min(100, self.player_sp + self.player_sp_charge + 10)
        else:
            self.player_sp = min(100, self.player_sp + self.player_sp_charge + 5)
        
        self.opponent_sp = min(100, self.opponent_sp + self.opponent["sp_rate"])
        

        if self.critical_hit and self.result in ["win", "sp_vs_sp"]:
            self.critical_hit = False
        
        if self.player_hp <= 0:
            self.player_hp = 0
            self.game_over = True
            self.winner = "opponent"
            self.message = f"{self.opponent['name']} ПОБЕДИЛ! {GameData().player_name} повержен!"
        elif self.opponent_hp <= 0:
            self.opponent_hp = 0
            self.game_over = True
            self.winner = "player"
            self.message = f"{GameData().player_name} ПОБЕДИЛ! {self.opponent['name']} повержен!"
            GameData().add_win(self.opponent["name"])
            GameData().player_xp += 30
            if GameData().player_xp >= 100:
                GameData().player_level += 1
                GameData().player_xp = 0
        
        self.dialog_timer = time.time()
        self.round_count += 1
    
    def calculate_damage(self, base_damage, is_player):
        crit_chance = GameData().player_crit_chance if is_player else self.opponent["crit_chance"]
        crit_multiplier = 1.5
        
        if self.critical_hit and is_player:
            return int(base_damage * crit_multiplier)
        
        if random.randint(1, 100) <= crit_chance:
            return int(base_damage * crit_multiplier)
        return base_damage
    
    def translate_choice(self, choice):
        translations = {"rock": "Камень", "scissors": "Ножницы", "paper": "Бумага"}
        return translations.get(choice, choice)
    
    def update(self):
        if not self.game_over and self.dialog_timer > 0 and time.time() - self.dialog_timer > self.dialog_duration:
            self.player_choice = None
            self.opponent_choice = None
            self.player_used_sp = False
            self.opponent_used_sp = False
            self.message = ""
            self.dialog_timer = 0
        
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1
            if self.ability_cooldown == 0:
                self.ability_used = None
        
        self.animation_time += 0.05
        
        for popup in self.damage_popups[:]:
            popup['timer'] -= 1
            popup['y'] -= 1
            if popup['timer'] <= 0:
                self.damage_popups.remove(popup)
    
    def draw(self, screen):
        screen.fill((20, 20, 40))
        
        pygame.draw.rect(screen, RED, (50, 20, 
                                      self.player_hp * 300 // GameData().player_max_hp, 30))
        pygame.draw.rect(screen, BLACK, (50, 20, 300, 30), 2)
        player_hp_text = font_small.render(
            f"{GameData().player_name}: {self.player_hp}/{GameData().player_max_hp}", True, WHITE)
        screen.blit(player_hp_text, (50, 55))
        
        pygame.draw.rect(screen, RED, (650, 20, 
                                      self.opponent_hp * 300 // self.opponent["max_hp"], 30))
        pygame.draw.rect(screen, BLACK, (650, 20, 300, 30), 2)
        opponent_hp_text = font_small.render(
            f"{self.opponent['name']}: {self.opponent_hp}/{self.opponent['max_hp']}", True, WHITE)
        screen.blit(opponent_hp_text, (650, 55))
        
        pygame.draw.rect(screen, BLUE, (50, 60, 
                                       self.player_sp * 3, 15))
        pygame.draw.rect(screen, BLACK, (50, 60, 300, 15), 1)
        
        pygame.draw.rect(screen, BLUE, (650, 60, 
                                       self.opponent_sp * 3, 15))
        pygame.draw.rect(screen, BLACK, (650, 60, 300, 15), 1)
        
        self.draw_opponent(screen, SCREEN_WIDTH//2, 200, self.opponent, self.animation_time)
        
        pygame.draw.rect(screen, (40, 40, 60), (50, 300, 900, 120))
        pygame.draw.rect(screen, YELLOW, (50, 300, 900, 120), 2)
        
        if self.message:
            dialog_lines = self.split_text(self.message, 90)
            for i, line in enumerate(dialog_lines):
                dialog_text = font_small.render(line, True, WHITE)
                screen.blit(dialog_text, (70, 320 + i * 25))
        
        if not self.game_over:
            # Камень
            pygame.draw.rect(screen, (100, 100, 100), 
                            (100, 550, 100, 100))
            pygame.draw.circle(screen, (70, 70, 70), 
                             (150, 600), 30)
            rock_text = font_small.render("Камень", True, WHITE)
            screen.blit(rock_text, (115, 530))
            
            # Ножницы
            pygame.draw.rect(screen, (100, 100, 100), 
                            (400, 550, 100, 100))
            pygame.draw.line(screen, WHITE, (400, 580), 
                            (500, 580), 4)
            pygame.draw.line(screen, WHITE, (450, 550), 
                            (450, 650), 4)
            scissors_text = font_small.render("Ножницы", True, WHITE)
            screen.blit(scissors_text, (415, 530))
            
            # Бумага
            pygame.draw.rect(screen, (100, 100, 100), 
                            (700, 550, 100, 100))
            pygame.draw.rect(screen, WHITE, (720, 570, 60, 60))
            paper_text = font_small.render("Бумага", True, WHITE)
            screen.blit(paper_text, (720, 530))
            
            # Специальная атака
            sp_color = PURPLE if self.player_sp >= 100 else (80, 80, 80)
            pygame.draw.rect(screen, sp_color, 
                            (900, 50, 50, 100))
            pygame.draw.rect(screen, WHITE, 
                            (900, 50, 50, 100), 2)
            sp_text = font_small.render("SP", True, WHITE)
            screen.blit(sp_text, (910, 65))
            
            for i, ability in enumerate(GameData().player_abilities):
                color = GREEN if self.ability_cooldown == 0 and ability != self.ability_used else RED
                pygame.draw.rect(screen, color, 
                                (50, 600 + i * 40, 40, 30))
                abbr = ''.join([word[0] for word in ability.split()])
                abbr_text = font_small.render(abbr, True, BLACK)
                screen.blit(abbr_text, (60, 605 + i * 40))
                
                if self.ability_cooldown > 0 and ability == self.ability_used:
                    cd_text = font_small.render(str(self.ability_cooldown), True, WHITE)
                    screen.blit(cd_text, (55, 605 + i * 40))
        
        if self.player_choice:
            choice_text = font_medium.render(f"Ваш выбор: {self.translate_choice(self.player_choice)}", True, GREEN)
            screen.blit(choice_text, (50, 500))
        
        if self.opponent_choice and not self.opponent_used_sp:
            choice_text = font_medium.render(
                f"Выбор противника: {self.translate_choice(self.opponent_choice)}", 
                True, RED
            )
            screen.blit(choice_text, (650, 500))
        elif self.opponent_used_sp:
            choice_text = font_medium.render("Противник использует спец.атаку!", True, RED)
            screen.blit(choice_text, (650, 500))
        
        if self.player_used_sp:
            choice_text = font_medium.render("Вы используете спец.атаку!", True, GREEN)
            screen.blit(choice_text, (50, 500))
        
        if self.critical_hit:
            crit_text = font_medium.render("Следующий удар будет КРИТИЧЕСКИМ!", True, ORANGE)
            screen.blit(crit_text, (SCREEN_WIDTH//2 - crit_text.get_width()//2, 450))
        
        for popup in self.damage_popups:
            alpha = min(255, popup['timer'] * 4)
            text_surface = font_medium.render(popup['text'], True, popup['color'])
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, (popup['x'], popup['y']))
        
        if self.game_over:
            result_color = GREEN if self.winner == "player" else RED
            result_text = font_large.render(
                "ПОБЕДА!" if self.winner == "player" else "ПОРАЖЕНИЕ!", 
                True, result_color
            )
            screen.blit(result_text, (SCREEN_WIDTH//2 - result_text.get_width()//2, 450))
            hint = font_medium.render("Нажмите Enter для продолжения", True, WHITE)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 550))
    
    def draw_opponent(self, screen, x, y, opponent, animation_time):
        # Рисуем разных противников
        if opponent["name"] == "Бульдог":
            # Тело
            pygame.draw.circle(screen, opponent["color"], (x, y), 80)
            # Уши
            pygame.draw.circle(screen, opponent["color"], (x - 40, y - 40), 25)
            pygame.draw.circle(screen, opponent["color"], (x + 40, y - 40), 25)
            # Морда
            pygame.draw.circle(screen, (200, 150, 150), (x, y + 20), 40)
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - 20, y - 10), 10)
            pygame.draw.circle(screen, WHITE, (x + 20, y - 10), 10)
            pygame.draw.circle(screen, BLACK, (x - 20, y - 10), 5)
            pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 5)
            # Нос
            pygame.draw.circle(screen, BLACK, (x, y + 20), 10)
            # Рот
            pygame.draw.arc(screen, BLACK, (x - 20, y + 10, 40, 30), 0, math.pi, 2)
            
        elif opponent["name"] == "Лис":
            # Тело
            pygame.draw.ellipse(screen, opponent["color"], (x - 80, y - 40, 160, 80))
            # Голова
            pygame.draw.circle(screen, opponent["color"], (x, y - 40), 50)
            # Уши
            pygame.draw.polygon(screen, opponent["color"], [
                (x - 30, y - 80), 
                (x - 20, y - 120), 
                (x, y - 80)
            ])
            pygame.draw.polygon(screen, opponent["color"], [
                (x + 30, y - 80), 
                (x + 20, y - 120), 
                (x, y - 80)
            ])
            # Хвост
            tail_wiggle = math.sin(animation_time * 3) * 10
            pygame.draw.ellipse(screen, opponent["color"], (x + 40, y, 80 + tail_wiggle, 40))
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - 15, y - 50), 8)
            pygame.draw.circle(screen, WHITE, (x + 15, y - 50), 8)
            pygame.draw.circle(screen, BLACK, (x - 15, y - 50), 4)
            pygame.draw.circle(screen, BLACK, (x + 15, y - 50), 4)
            # Нос
            pygame.draw.circle(screen, BLACK, (x, y - 30), 6)
            
        elif opponent["name"] == "Феникс":
            # Тело
            pygame.draw.circle(screen, opponent["color"], (x, y), 80)
            # Крылья
            for i in range(5):
                wing_color = (opponent["color"][0], max(0, opponent["color"][1] - 30*i), max(0, opponent["color"][2] - 10*i))
                wing_x = x + math.cos(animation_time + i*1.2) * 70
                wing_y = y + math.sin(animation_time + i*1.2) * 70
                pygame.draw.circle(screen, wing_color, (int(wing_x), int(wing_y)), 40)
            # Голова
            pygame.draw.circle(screen, (255, 200, 0), (x, y - 80), 40)
            # Глаза
            pygame.draw.circle(screen, WHITE, (x - 15, y - 85), 6)
            pygame.draw.circle(screen, WHITE, (x + 15, y - 85), 6)
            pygame.draw.circle(screen, BLACK, (x - 15, y - 85), 3)
            pygame.draw.circle(screen, BLACK, (x + 15, y - 85), 3)
            # Клюв
            pygame.draw.polygon(screen, (255, 200, 0), [
                (x - 10, y - 70), 
                (x + 10, y - 70), 
                (x, y - 50)
            ])
    
    def split_text(self, text, max_len):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_len:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

class UpgradeState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.upgrades = self.generate_upgrades()
        self.selected_index = 0
        self.confirm_timer = 0
        self.confirmed = False
        self.pulse = 0
    
    def generate_upgrades(self):
        upgrades = []
        options = [
            ("Увеличение HP", "Максимальное здоровье +20"),
            ("Усиление атаки", "Базовый урон +5"),
            ("Быстрая зарядка", "SP заряжается на 25% быстрее"),
            ("Критические удары", "Шанс крита +5%"),
            ("Способность: Лечение", "Восстанавливает 30 HP (3 раунда перезарядки)"),
            ("Способность: Усиление", "+50 SP (3 раунда перезарядки)"),
            ("Способность: Ослабление", "-30 SP у противника (4 раунда перезарядки)"),
            ("Способность: Критический удар", "Гарантированный критический удар (5 раундов перезарядки)")
        ]
        

        selected = set()
        while len(selected) < 3:
            idx = random.randint(0, len(options)-1)
            if idx not in selected:
                selected.add(idx)
                name, desc = options[idx]
                upgrades.append({"name": name, "description": desc})
        
        return upgrades
    
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not self.confirmed:
                    if event.key == K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.upgrades)
                    elif event.key == K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.upgrades)
                    elif event.key == K_RETURN:
                        self.confirm_selection()
                elif event.key == K_RETURN and self.confirm_timer == 0:
                    self.apply_upgrade()
                    self.game.change_state(ChooseOpponentState(self.game))
    
    def confirm_selection(self):
        self.confirmed = True
        self.confirm_timer = 30
    
    def apply_upgrade(self):
        upgrade = self.upgrades[self.selected_index]
        name = upgrade["name"]
        
        if name == "Увеличение HP":
            GameData().player_max_hp += 20
        elif name == "Усиление атаки":
            GameData().player_damage += 5
        elif name == "Быстрая зарядка":
            GameData().player_sp_charge_rate = int(GameData().player_sp_charge_rate * 1.25)
        elif name == "Критические удары":
            GameData().player_crit_chance += 5
        elif "Способность" in name:
            ability_name = name.split(": ")[1]
            if ability_name not in GameData().player_abilities:
                GameData().player_abilities.append(ability_name)
    
    def update(self):
        if self.confirmed and self.confirm_timer > 0:
            self.confirm_timer -= 1
        self.pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
    
    def draw(self, screen):
        screen.fill((30, 30, 50))

        title = font_large.render("ВЫБОР УЛУЧШЕНИЯ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        desc = font_medium.render("После победы вы можете выбрать одно улучшение:", True, WHITE)
        screen.blit(desc, (SCREEN_WIDTH//2 - desc.get_width()//2, 120))
        
        # Улучшения
        width = 280
        spacing = 20
        total_width = len(self.upgrades) * width + (len(self.upgrades) - 1) * spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, upgrade in enumerate(self.upgrades):
            x = start_x + i * (width + spacing)
            y = 200
            pulse = self.pulse if i == self.selected_index else 0
            
            color = GREEN if i == self.selected_index and not self.confirmed else BLUE
            pygame.draw.rect(screen, (50, 50, 70), (x, y + pulse, width, 300))
            pygame.draw.rect(screen, color, (x, y + pulse, width, 300), 3)
            
            name_text = font_medium.render(upgrade["name"], True, YELLOW)
            screen.blit(name_text, (x + width//2 - name_text.get_width()//2, y + 20 + pulse))
            
            desc_lines = self.split_text(upgrade["description"], 30)
            for j, line in enumerate(desc_lines):
                desc_text = font_small.render(line, True, WHITE)
                screen.blit(desc_text, (x + 10, y + 70 + j * 30 + pulse))

        if self.confirmed:
            confirm_text = font_medium.render("Улучшение выбрано!", True, GREEN)
            screen.blit(confirm_text, (SCREEN_WIDTH//2 - confirm_text.get_width()//2, 550))
            
            if self.confirm_timer == 0:
                hint = font_medium.render("Нажмите Enter чтобы продолжить", True, WHITE)
                screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 600))
        else:
            hint = font_medium.render("← → для выбора, Enter - подтвердить", True, WHITE)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 550))
    
    def split_text(self, text, max_len):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_len:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

class StatsState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.stats = GameData()
        self.scroll_offset = 0
        self.max_offset = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.game.change_state(ChooseOpponentState(self.game))
                elif event.key == K_UP:
                    self.scroll_offset = max(0, self.scroll_offset - 30)
                elif event.key == K_DOWN:
                    self.scroll_offset = min(self.max_offset, self.scroll_offset + 30)
    
    def draw(self, screen):
        screen.fill((30, 30, 50))
        
        title = font_large.render("СТАТИСТИКА ИГРОКА", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        player_info = font_medium.render(f"Игрок: {self.stats.player_name}", True, GREEN)
        screen.blit(player_info, (SCREEN_WIDTH//2 - player_info.get_width()//2, 120))
        
        level_info = font_medium.render(f"Уровень: {self.stats.player_level} | XP: {self.stats.player_xp}/100", True, GREEN)
        screen.blit(level_info, (SCREEN_WIDTH//2 - level_info.get_width()//2, 160))
        
        pygame.draw.rect(screen, (50, 50, 70), (100, 220, 800, 200))
        pygame.draw.rect(screen, BLUE, (100, 220, 800, 200), 2)
        
        stats_y = 240
        stats = [
            f"Максимальное HP: {self.stats.player_max_hp}",
            f"Базовый урон: {self.stats.player_damage}",
            f"Заряд SP/ход: {self.stats.player_sp_charge_rate}",
            f"Шанс критического удара: {self.stats.player_crit_chance}%",
            f"Способности: {', '.join(self.stats.player_abilities) if self.stats.player_abilities else 'Нет'}"
        ]
        
        for stat in stats:
            stat_text = font_small.render(stat, True, WHITE)
            screen.blit(stat_text, (120, stats_y))
            stats_y += 40
        
        wins_title = font_medium.render("ПОБЕДЫ НАД ПРОТИВНИКАМИ", True, YELLOW)
        screen.blit(wins_title, (SCREEN_WIDTH//2 - wins_title.get_width()//2, 450))
        
        wins_y = 500 - self.scroll_offset
        wins_height = 0
        if self.stats.defeated_opponents:
            for opponent, count in self.stats.defeated_opponents.items():
                win_text = font_small.render(f"- {opponent}: {count} побед", True, WHITE)
                screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, wins_y))
                wins_y += 40
                wins_height += 40
        else:
            no_wins = font_small.render("Пока нет побед", True, WHITE)
            screen.blit(no_wins, (SCREEN_WIDTH//2 - no_wins.get_width()//2, wins_y))
            wins_height = 40
        
        self.max_offset = max(0, wins_height - 200)
        
        if self.max_offset > 0:
            scroll_height = 200
            scroll_pos = (self.scroll_offset / self.max_offset) * (scroll_height - 40)
            pygame.draw.rect(screen, (100, 100, 100), (950, 500, 20, scroll_height))
            pygame.draw.rect(screen, BLUE, (950, 500 + scroll_pos, 20, 40))
        
        hint = font_medium.render("Нажмите Enter для возврата", True, WHITE)
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))

class RockPaperScissorsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Камень-Ножницы-Бумага: ЛЮТАЯ ВЕРСИЯ")
        self.clock = pygame.time.Clock()
        self.state = LoadingState(self)
        GameData.reset()
    
    def change_state(self, new_state):
        self.state = new_state
    
    def start_battle(self, opponent):
        self.state = BattleState(self, opponent)
    
    def run(self):
        while True:
            events = pygame.event.get()
            self.state.handle_events(events)
            self.state.update()
            self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()