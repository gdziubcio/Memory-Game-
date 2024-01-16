import pygame 
import random
from icecream import ic
import pygame_gui
import pandas as pd 
import os 
import json
import time 

# Pygame initialization
pygame.init()

# Setting up the display size and window title
SIZE = WIDTH, HEIGHT = (800,400)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Words Matrix') 
clock = pygame.time.Clock()
font = pygame.font.Font(None, size=40)
running = True 

class Player:
    def __init__(self, name):
        self.name = name
        self.file_name = f'player_data_{self.name}.json'
        self.data = {
            'name': self.name,
            'difficulty': {},
            # Add more player-specific attributes if needed
        }
        self.load_data()

    def update_attempt(self, difficulty, sentence, success, failed_word, attempt_duration):

        self.load_data()

        if difficulty not in self.data['difficulty']:
            self.data['difficulty'][difficulty] = {}

        if sentence not in self.data['difficulty'][difficulty]:
            self.data['difficulty'][difficulty][sentence] = {
                'attempts': [],
            }

        attempt = {
            'success': success,
            'failed_word': failed_word,
            'duration': attempt_duration,
            'timestamp': time.time()
        }
        self.data['difficulty'][difficulty][sentence]['attempts'].append(attempt)
        self.save_data()

    def save_data(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.data = json.load(file)
        else:
            self.save_data() 

class Menu(): 
    def __init__(self) -> None:
        self.manager = pygame_gui.UIManager(SIZE, 'assets/themes/quick_theme.json')
        self.active = True 
        self.start_button = self.get_start_button()
        self.drop_down = self.get_drop_down()
        self.get_entry_text = self.get_entry_text()

    def get_start_button(self): 
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 185, 100,30)), 
                                                    text = 'Start',
                                                    manager=self.manager)
    def get_drop_down(self): 
        return pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(300, 240, 200, 30),
                                                    manager=self.manager, 
                                                    options_list=['Easy', 'Medium', 'Hard'],
                                                    starting_option='Easy')
    def get_entry_text(self): 
        return pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(300, 40, 200, 30), 
                                                    manager=self.manager, 
                                                    placeholder_text='Login')
    def process(self, event, time_delta): 
        self.manager.process_events(event)
        self.manager.update(time_delta)

    def draw(self, window): 
        window.fill('#424443')
        self.manager.draw_ui(window)

    def is_active(self):
        return self.active
    
    def on(self): 
        self.active = True

    def off(self): 
        self.active = False 

class GameState():
    def __init__(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def get_state(self): 
        current_time = (pygame.time.get_ticks() - self.start_time) /1000 # miliseconds to seconds
        return 'Read' if (current_time < 4) else 'Show' if (current_time < 10) else 'Play'
    
    def reset_state(self): 
        self.start_time = pygame.time.get_ticks()
    
class Square(pygame.sprite.Sprite): 
    def __init__(self, position, word) -> None:
        super().__init__()
        self.image = pygame.image.load('assets/images/button.jpg').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(100,100))
        self.rect = self.image.get_rect(center = position)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.font_surf = self.font.render(word, True, 'black')
        self.font_rect = self.font_surf.get_rect(center = self.rect.center)
        self.word = word 
        self.clicked = False
    
    def draw_text(self, game_state): 
        if self.clicked or game_state == 'Show':
            screen.blit(self.font_surf, self.font_rect)

    def click(self, event):
        if (self.clicked == False) and (self.rect.collidepoint(event.pos)): 
            self.clicked = True 
            return True 
        else: 
            return False 

class Sentence(): 
    def __init__(self, difficulty='Medium') -> None:
        # sentence attributes for logic 
        self.sentence = self.get_sentence()
        self.sentence_list = self.sentence.split(' ')
        self.nr_of_words = len(self.sentence_list)
        self.difficulty = difficulty
        self.shuffled_list = None 
        self.current_word_index = 0 
        # sentence attributes for drawing
        self.font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.font_surf = self.font.render(self.sentence, True, '#c99869')
        self.font_rect = self.font_surf.get_rect(midtop=(400,20))

    def get_sentence(self): 
        path_to_file = 'data/sentences.parquet'
        return pd.read_parquet(path_to_file)['Sentence'].sample().iloc[0]

    def get_current_word(self): 
        return self.sentence_list[self.current_word_index]
    
    def update_current_word(self): 
        self.current_word_index += 1

    def reset_current_word(self): 
        self.current_word_index = 0 
    
    def get_shuffled_sentence(self): 
        copied_list = self.sentence_list.copy()
        nr_of_squares = 9 
        if self.difficulty == 'Easy': 
            word_to_append = ''
        elif self.difficulty == 'Medium': 
            word_to_append = 'Empty'

        elif self.difficulty == 'Hard': 
            word_to_append = self.get_shuffled_word(copied_list)
        
        for i in range(nr_of_squares - self.nr_of_words): 
            copied_list.append(word_to_append)
            random.shuffle(copied_list)
        
        self.shuffled_list = copied_list

        return copied_list

    def get_shuffled_word(self, words):
        shuffled_word = ""
        attempts = 0
        max_attempts = len(words) * 2  # To avoid infinite loops

        while not shuffled_word or shuffled_word in words:
            if attempts > max_attempts:
                return 'empty'
            word = random.choice(words)
            word_list = list(word)
            random.shuffle(word_list)
            shuffled_word = ''.join(word_list)
            attempts += 1

        return shuffled_word
    
    def draw(self): 
        screen.blit(self.font_surf, self.font_rect)

def generate_squares(words): 

    squares_positions = [(300,100), (400,100), (500,100), 
                        (300,200), (400,200), (500,200), 
                        (300,300), (400,300), (500,300) ]
    
    all_squares = pygame.sprite.Group()

    for position, word in zip(squares_positions,words): 
        all_squares.add(Square(position, word))
    
    return all_squares

state_controler = GameState()
menu = Menu()



while running: 
    time_delta = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events: # loop for collecting and interpreting all activiy
        if event.type == pygame.QUIT: 
            player.save_data()
            running = False # breaks to close the game window

        if menu.is_active(): 
            menu.process(event, time_delta)

            if event.type == pygame_gui.UI_BUTTON_PRESSED: 
                if event.ui_element == menu.start_button: 
                    player_name = menu.get_entry_text.get_text()
                    difficulty = menu.drop_down.selected_option
                    player = Player(player_name)
                    menu.off()
                    sentence = Sentence(difficulty)
                    squares = generate_squares(sentence.get_shuffled_sentence())
                    sentence_to_guess = sentence.sentence_list
                    state_controler.reset_state()
                    


        else: # menu off
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if state_controler.get_state() == 'Play':
                    for square in squares: 
                        if square.click(event): 
                            if square.word == sentence.get_current_word(): 
                                sentence.update_current_word()
                                
                            else: 
                                attempt_duration = (pygame.time.get_ticks() - state_controler.start_time) / 1000
                                player.update_attempt(difficulty, sentence.sentence, False, square.word, attempt_duration)
                                pygame.time.delay(2000)
                                state_controler.reset_state()
                                sentence.reset_current_word()
                                squares = generate_squares(sentence.get_shuffled_sentence())
         
    
    if menu.is_active(): 
        menu.draw(screen)

    else: 

        for event in events: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    player.save_data()
                    menu.on()

        screen.fill('#424443')
        sentence.draw()
        squares.draw(screen)

        for square in squares: 
            square.draw_text(state_controler.get_state())
        
        if sentence.current_word_index == sentence.nr_of_words:
            attempt_duration = (pygame.time.get_ticks() - state_controler.start_time) / 1000 
            player.update_attempt(difficulty, sentence.sentence, True, '', attempt_duration)
            pygame.time.delay(2000)
            state_controler.reset_state()
            sentence = Sentence(difficulty)
            squares = generate_squares(sentence.get_shuffled_sentence())

    pygame.display.update()


pygame.quit()




