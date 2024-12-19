import pygame

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1066
SCREEN_HEIGHT = 600

bg = pygame.image.load("images/bgtown.jpg")

walk = [
    pygame.image.load("images/run1.png"),
    pygame.image.load("images/run2.png"),
    pygame.image.load("images/run3.png"),
    pygame.image.load("images/run4.png"),
    pygame.image.load("images/run5.png"),
    pygame.image.load("images/run6.png"),
    pygame.image.load("images/run7.png"),
    pygame.image.load("images/run8.png"),
]

playerStand = pygame.image.load("images/idle.png")


# ------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    right = False
    left = False
    animCount = 0

    # ------------------------------------------------------------------------------
    # Методы
    def __init__(self):
        super().__init__()

        self.image = playerStand

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

    # ------------------------------------------------------------------------------
    def update(self):
        self.calc_grav()
        if self.animCount + 1 >= 30:
            self.animCount = 0
        if self.right:
            self.image = walk[self.animCount // 5]
            self.animCount += 1
        elif self.left:
            self.image = pygame.transform.flip(walk[self.animCount // 5], True, False)
            self.animCount += 1
        else:
            self.stop()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    # ------------------------------------------------------------------------------
    def calc_grav(self):

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.95

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    # ------------------------------------------------------------------------------
    def jump(self):

        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -16

    # ------------------------------------------------------------------------------
    def go_left(self):

        self.change_x = -9
        if not self.left:
            self.flip()
            self.right = False
            self.left = True

    # ------------------------------------------------------------------------------
    def go_right(self):

        self.change_x = 9
        if not self.right:
            self.flip()
            self.right = True
            self.left = False

    # ------------------------------------------------------------------------------
    def stop(self):
        if self.left:
            self.flip()
        elif self.right:
            self.image = playerStand
        self.change_x = 0
        self.right = False
        self.left = False
        self.animCount = 0

    # ------------------------------------------------------------------------------
    def flip(self):

        self.image = pygame.transform.flip(playerStand, True, False)


# ------------------------------------------------------------------------------
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("images/platform2.png")

        self.rect = self.image.get_rect()


# ------------------------------------------------------------------------------
class Level(object):
    def __init__(self, player):

        self.platform_list = pygame.sprite.Group()

        self.player = player

    # ------------------------------------------------------------------------------
    def update(self):
        self.platform_list.update()

    # ------------------------------------------------------------------------------
    def draw(self, screen):

        screen.blit(bg, (0, 0))

        self.platform_list.draw(screen)


# ------------------------------------------------------------------------------
class Level_01(Level):
    def __init__(self, player):

        Level.__init__(self, player)

        level = [
            [210, 32, 500, 500],
            [210, 32, 200, 400],
            [210, 32, 600, 300],
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# ------------------------------------------------------------------------------
def main():

    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Платформер")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(30)

        pygame.display.flip()

    pygame.quit()


main()
