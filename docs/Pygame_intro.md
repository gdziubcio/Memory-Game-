# Pygame tutorial 

### Why use pygame? 

1. **Learning to code**



### How games work 

1. Checking the player input - **event loop** 
2. Use information to influence elements on the screen 
   1. Create **image**
      1. Go to the beginning ⤴️  - 30-60 times per seconds 



### Most important pygame utility 

1. Drawing images 
2. Check for player input *without stopping the game*
3. Simple gamedev tools



### Frames 

We need **constant frame rate** - to keep elements behavior constant across different devices 

- 60 fps ceiling - *easy* - pause if needed 
- 60 fps floor  - *hard* - but probably not concern with pygame





### Displaying images 

#### Surface 

- **Display surface** - game window 
- **Regular surface** 
  - image (rendered, imported, text, color)
  - must be displayed on *display surface*



### Creating text 

1. create **font** - *size* and *style* 
2. write text on the surface 
3. blit the text surface 



### Rectangles 

- precise position of surfaces 

![image-20240105191208472](/assets/images/rects.png)

- basic collisions 
  - `rect1.collidirect(rect2)`
  - `rect1.collidepoint((x,y))` - **for mouse clicking**
- drawing 
  - `pygame.draw.rect(surface, color, rectangle)`

 

### Mouse position 

1. `pygame.mouse` 

```python
    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos): 
        print(pygame.mouse.get_pressed())
```

2. event loop

   ```pyt
   for event in pygame.event.ger()
   	if event.type == pygame.MOUSEMOTION: #or 
   #	if event.type == pygame.MOUSEBUTTONDOWN: #or
   #	if event.type == pygame.MOUSEBUTTONDOWN:				
   ```



### Keyboard input 

1. `pygame.key`

```python
keys = pygame.key.get_pressed()
	if keys[pygame.K_SPACE]: 
		print('jump')
```



1. event loop 

 ```python
if event.type == pygame.KEYDOWN: 
	if event.key == pygame.K_SPACE:
		print('jump')
 ```





### Pygame. vs event loop 

- `pygame.something` - better for controls inside classes
- event loops - more general stuff like closing the game 



### Gravity 

**accurate physics < fun and ease of programming**

  

### Timers 

1. create a custom user event 
2. trigger this event in certain time intervals with pygame 
3. add code in the event loop 



### Obstacle enemies 

1. list of obstacles rectangles 
2. each time the timer triggers append new rectangle
3.  move each rectangle in the list to the left on every frame  
4. delete rectangles too far left 



### Animation 

1. **Player**  - create *own* timer that updates surface every few milliseconds 
2. **Obstacle** - *inbuilt* timers updating all obstacle surfaces  



### Sprite class 

```python
import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))  # Create a blank surface for 													the player's image
        self.image.fill((255, 0, 0))  # Fill it with a red color
        self.rect = self.image.get_rect()  # Get the rectangle that encloses 															the image
```



### Groups 



1. **Group**
   - for multiple sprites that share functionality (snails, flies)
2. **GroupSingle** 
   - for a single sprite like a player 

Obstacles and player must be in different groups to check for collisions between them

Sprite groups have two main functions:

1. **draw**

`player.draw(screen)` 

1. **update**

```python
def update(self): 
    self.player_input()
    self.apply_gravity()
    
```

