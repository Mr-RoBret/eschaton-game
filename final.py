'''
    "Eschaton Mini"

    Written by Bret Farley, Nov 19, 2018

    This program will present the user with a field or two, and use those input values to simulate a
    bomber-type game. The user will input the trajectory and speed at which to lob the bomb,
    heretofore known as the 'tennis-ball' toward the target.

    If the ball misses, the user gets up to two more tries.
    If the tennis ball hits the target, the user wins the game, and can play again with a different target
    (randomly placed).

    This code is largely based on Zelle's Animated Cannonball simulation code.
'''


import math
from graphics import *
from random import *
from button import Button

class InputDialog:
    '''
        Class and function structure From Zelle, pg 350
    '''
    def __init__(self, angle, velocity, height):
        self.window = window = GraphWin("Initial Values", 200, 300)
        window.setCoords(0, 4.5, 4, .5)

        Text(Point(1, 1), "Angle").draw(window)
        self.angle = Entry(Point(3, 1), 5).draw(window)
        self.angle.setText(str(angle))

        Text(Point(1, 2), "Velocity").draw(window)
        self.velocity = Entry(Point(3, 2), 5).draw(window)
        self.velocity.setText(str(velocity))

        Text(Point(1, 3), "Height").draw(window)
        self.height = Entry(Point(3, 3), 5).draw(window)
        self.height.setText(str(height))

        self.lob = Button(window, Point(1,4), 1.25, .5, "Lob")
        self.lob.activate()

        self.quit = Button(window, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.window.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.lob.clicked(pt):
                return "Lob!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.velocity.getText())
        h = float(self.height.getText())
        return a, v, h

    def close(self):
        self.window.close()

class Projectile:
    '''
        Class and function structure From Zelle, pg 326
    '''
    def __init__(self, angle, velocity, x_pos, height):
        self.x_position = x_pos
        self.y_position = height
        self.theta = math.radians(angle)
        self.x_velocity = velocity * math.cos(self.theta)
        self.y_velocity = velocity * math.sin(self.theta)

    def update(self, time):
        self.x_position = self.x_position + (time * 6) * self.x_velocity
        self.y_velocity1 = self.y_velocity - 9.8 * (time * 6)
        self.y_position = self.y_position + (time * 6) * (self.y_velocity + self.y_velocity1) / 2.0
        self.y_velocity = self.y_velocity1

    def getY(self):
        return self.y_position

    def getX(self):
        return self.x_position

class ShotTracker:
    '''
        Class and function structure From Zelle, pg 348
    '''
    def __init__(self, window, angle, velocity, x_pos, height):
        self.projectile = Projectile(angle, velocity, x_pos, height)
        self.ball = Circle(Point(x_pos, height), 20)
        self.graphic = Image(Point(self.ball.getP1().getX(), self.ball.getP1().getY()), "tennis_ball.gif")
        self.graphic.draw(window)

    def update(self, frame_rate):
        '''
        Move the shot frame-rate-amount farther along on trajectory.
        '''
        self.projectile.update(frame_rate)
        center = self.graphic.getAnchor()
        dx = self.projectile.getX() - center.getX()
        dy = self.projectile.getY() - center.getY()
        self.graphic.move(dx, dy)

    def getX(self):
        return self.projectile.getX()

    def getY(self):
        return self.projectile.getY()

    def undraw(self):
        self.ball.undraw()

class Target:
    '''
        Create target at random placement, within given parameters. Use invisible 'bounding box' for collision,
        and insert towel graphic as visible target.
    '''
    def __init__(self, window):
        self.minX = randint(700, 1000)
        self.maxX = self.minX+130
        self.minY = randint(100, 200)
        self.maxY = self.minY+124

        self.anchor_point_X = self.minX + (self.maxX - self.minX)//2
        self.anchor_point_y = self.minY + (self.maxY - self.minY)//2
        self.towel = Rectangle(Point(self.minX, self.maxY), Point(self.maxX, self.minY)) #get towel shape
        self.graphic = Image(Point(self.anchor_point_X, self.anchor_point_y), "towel.gif")

    def getX_left(self):
        return self.towel.getP1().getX()

    def getX_right(self):
        return self.towel.getP2().getX()

    def getY_top(self):
        return self.towel.getP1().getY()

    def getY_bottom(self):
        return self.towel.getP2().getY()

    def draw(self, window):
        self.draw(window)

class CourtFloor:
    '''
        Using target's randomized height, create tennis court behind target's graphic.
    '''
    def __init__(self, window, window_width, target):
        self.top_left_X = -10
        self.top_left_Y = target.getY_top() - 30
        self.bottom_right_X = window_width + 10
        self.bottom_right_Y = -10
        self.ground = Rectangle(Point(self.top_left_X, self.top_left_Y), Point(self.bottom_right_X, self.bottom_right_Y))
        self.ground.setFill(color_rgb(148, 202, 144))
        self.ground.setOutline('black')
        self.ground.draw(window)

    def draw(self, window):
        self.draw(window)

class Announce:
    '''
        Class announce will be used for both initial Welcome announcement and other text announcing 'hit', 'miss',
        or 'loss.' But in Wallacian terminology.
    '''
    def __init__(self, window, window_width, window_height, message):
        self.window = window
        self.x = (window_width // 2)
        self.y = (window_height - window_height // 3)
        self.message = Text(Point(self.x - 100, self.y), message)
        self.message.setTextColor(color_rgb(28, 136, 6))
        self.message.setSize(36)
        self.message.setFace('helvetica')
        self.message.setStyle('italic')

    def new_message(self, message):
        self.message = Text(Point(self.x, self.y), message)
        self.message.setTextColor(color_rgb(184, 60, 43))
        self.message.setSize(36)
        self.message.setFace('helvetica')

    def draw(self, window):
        self.message.draw(window)

    def undraw(self):
        self.message.undraw()

def main():
    '''
        First creates window of specified width/height, then sets coords to make physics simulation more
        logical way and imports graphic for background.
        Announces beginning of game, creates target, tennis court. Sets counter to 3 (for number of turns) and
        increments down with each turn taken, until win or loss occurs.
        Each turn is a loop, during which user can enter custom values for angle, velocity, and height
        of ball, then choose 'Lob,' unless they would rather 'Quit.'
        For each lob, new values are used to simulate, via time loop which updates position of ball,
        overall animated arc, until ball either strikes target or outer edge of window.
    '''

    window_width = 1280
    window_height = 720
    game_window = GraphWin("Welcome to Eschaton. Mini.", window_width, window_height, autoflush=False)
    game_window.setCoords(-10, -10, 1280, 720)
    game_window.setBackground(color_rgb(138, 190, 189))
    bg_graphic = Image(Point(window_width//2, window_height//2), "clouds.gif")
    bg_graphic.draw(game_window)
    announcement = Announce(game_window, window_width, window_height, "Welcome to Eschaton.\n "
                                                                      "Click 'Lob' to begin... the Entertainment.")
    announcement.draw(game_window)

    initial_angle = 45
    initial_velocity = 100
    initial_height = 250
    x_pos = 100
    counter = 3

    target = Target(game_window)
    tennis_court = CourtFloor(game_window, window_width, target)
    target.graphic.draw(game_window)

    while True:
        input_window = InputDialog(initial_angle, initial_velocity, initial_height)
        choice = input_window.interact()
        input_window.close()
        strike = False

        if choice == 'Quit':
            break
        if choice == 'Lob!':
            announcement.undraw()
            angle, velocity, height = input_window.getValues()
            shot = ShotTracker(game_window, angle, velocity, x_pos, height)
            while 0 <= shot.getY() <= (window_height -100) and shot.getX() <= (window_width + 20):
                if target.getX_left() <= shot.getX() <= target.getX_right() and\
                        target.getY_bottom() <= shot.getY() <= target.getY_top():
                    strike = True
                    announcement.new_message('KERTWANG! You win.')
                    announcement.draw(game_window)
                    break
                else:
                    shot.update(1 / 24)
                    update(24)
            counter -= 1

            if strike == False and counter < 1:
                announcement.new_message('UTTER GLOBAL CRISIS! You Lost!'.format(counter))
                announcement.draw(game_window)
            elif strike == False and counter >= 1:
                announcement.new_message('DAMN\n {0} ball(s) left.'.format(counter))
                announcement.draw(game_window)

    game_window.close()

main()