from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_x_speed,player_y_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
      ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
      # сначала движение по горизонтали
      if pacman.rect.x <= win_width-80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
        self.rect.x += self.x_speed
      # если зашли за стенку, то встанем вплотную к стене
      platforms_touched = sprite.spritecollide(self, barriers, False)
      if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
          for p in platforms_touched:
              self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
      elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
          for p in platforms_touched:
              self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
      if pacman.rect.y <= win_height-80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed < 0:
        self.rect.y += self.y_speed
      # если зашли за стенку, то встанем вплотную к стене
      platforms_touched = sprite.spritecollide(self, barriers, False)
      if self.y_speed > 0: # идем вниз
          for p in platforms_touched:
              self.y_speed = 0
              # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
              if p.rect.top < self.rect.bottom:
                  self.rect.bottom = p.rect.top
      elif self.y_speed < 0: # идем вверх
          for p in platforms_touched:
              self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
              self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
    def fire(self):
        bullet = Bullet('weapon.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_spead):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.spead = player_spead
    def update(self):
        self.rect.x += self.spead
        if self.rect.x > win_width+10:
            self.kill()



win_height = 500
win_width = 700
window = display.set_mode((700,500))
pic = transform.scale(image.load('galaxy_1.jpg'), (700,500))
pacman = Player('packman.png', 300, 300, 50, 50, 0, 0)
back = (225,200,225)
window.fill(back)
display.set_caption('Лабиринт')
wall = GameSprite('wall.jpg', 370, 100, 50, 400)
wall1 = GameSprite('wall1.jpg', 120, 100, 400, 50)
monster1 = GameSprite('pacman.jpg', 550, 300, 75, 75)
monster2 = GameSprite('monster_3.png', 300, 0, 75, 75)
prize = GameSprite('prize.png', 600, 400, 100, 100)
finish = False
run = True

barriers = sprite.Group()
barriers.add(wall)
barriers.add(wall1)
bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)




while run:
    time.delay(60)
    for e in event.get():
        if e.type == QUIT:
            run = False
    if e.type == KEYDOWN:
        if e.key == K_RIGHT:
            pacman.x_speed = 5
        if e.key == K_LEFT:
            pacman.x_speed = -5
        if e.key == K_UP:
            pacman.y_speed = -5
        if e.key == K_DOWN:
            pacman.y_speed = 5
        if e.key == K_SPACE:
            pacman.fire()
    elif e.type == KEYUP:
        if e.key == K_RIGHT:
            pacman.x_speed = 0
        if e.key == K_LEFT:
            pacman.x_speed = 0
        if e.key == K_UP:
            pacman.y_speed = 0
        if e.key == K_DOWN:
            pacman.y_speed = 0

    if not finish:        
        window.blit(pic,(0,0))
        wall.reset()
        wall1.reset()
        pacman.reset()
        prize.reset()
        pacman.update()
        barriers.draw(window)
        bullets.update()  
        bullets.draw(window)
        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)
        monsters.update()
        monsters.draw(window)


        if sprite.spritecollide(pacman, monsters, False):
            finish = True
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90,0))
        
        if sprite.collide_rect(pacman, prize):
            finish = True
            img = image.load('pobeda.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height, win_height)), (0,0))    

    display.update()


