from pico2d import *

background_Width, background_Height = 1200, 800

class Backgraund:
    def __init__(self):
        self.image = load_image("background3.png")

    def draw(self):
        self.image.draw(background_Width / 2, background_Height / 2)

class Mario:
    def __init__(self):
        self.image = load_image("mario_sheet2.png")
        self.x, self.y = 300, 160
        # self.cx = self.x        #미정
        # self.cy = self.y
        self.dir = 0            # 방향값 ,  속도 = 방향 * 20
        self.turn = 0           # 얼굴돌리는 방향값
        self.accl = 0           # 가속도
        self.Max_accl = 1       # 최대 가속도
        self.frame = 0          # 프레임
        self.jump = False       # 점프키 눌렸는지
        self.jump_y = 0         # 점프량 값
        self.gravity = 0        # 중력값
        self.ground_y = 160       # 현재 서있는 땅의 y값


    def update(self):
        # 가속 처리
        if self.dir == 1 and self.accl < self.Max_accl and self.accl >= 0:  # 가만히 있다가 달릴때 서서히 빨라지게
            self.accl += 0.08
        elif self.dir == -1 and self.accl > (-self.Max_accl) and self.accl <= 0:
            self.accl -= 0.08
        elif self.dir == 1 and self.accl < 0:                       # 가속 있는데 갑자기 방향 바꿀때
            self.accl += 0.2
        elif self.dir == -1 and self.accl > 0:
            self.accl -= 0.2
        elif self.dir == 0 and self.accl > 0:                       # 달리는 도중 키를 때면 서서히 멈추게
            self.accl -= 0.15
            if self.accl < 0:
                self.accl = 0
        elif self.dir == 0 and self.accl < 0:
            self.accl += 0.15
            if self.accl > 0:
                self.accl = 0

        # 가속을 더한 이동 표시
        if self.dir == 1:                                   # 오른쪽으로 가고있을때 가속 붙여서 x좌표 오른쪽으로
            self.x += self.dir * 25 * self.accl
        elif self.dir == -1:                                # 왼쪽으로 가고있을때 가속 붙여서 x좌표 왼쪽으로
            self.x += self.dir * 25 * (-self.accl)
        elif self.dir == 0 and self.turn == 1:              # 오른쪽으로 가다 멈출때
            self.x += 10 * self.accl
        elif self.dir == 0 and self.turn == -1:             # 왼쪽으로 가다 멈출때
            self.x += 10 * self.accl

        if self.jump == True:
            self.jump_y = 45
            self.gravity += 3

        self.y += self.jump_y - self.gravity
        if self.y < self.ground_y:
            self.y = self.ground_y
            self.jump = False
            self.gravity = 0
            self.jump_y = 0

        self.frame = (self.frame + 1) % 3

    def draw(self):
        if self.dir == 1 and self.turn == 1 and self.jump == False:
            self.image.clip_draw(920 + self.frame*120, 910, 120, 90, self.x, self.y)
        elif self.dir == -1 and self.turn == -1 and self.jump == False:
            self.image.clip_draw(560 - self.frame*120, 910, 120, 90, self.x, self.y)
        elif self.turn == 1 and self.jump == True:
            self.image.clip_draw(1400, 910, 120, 90, self.x, self.y)
        elif self.turn == -1 and self.jump == True:
            self.image.clip_draw(80, 910, 120, 90, self.x, self.y)
        elif self.turn == 1:
            self.image.clip_draw(800, 910, 120, 90, self.x, self.y)
        elif self.turn == -1:
            self.image.clip_draw(680, 910, 120, 90, self.x, self.y)
        else:
            self.image.clip_draw(800, 910, 120, 90, self.x, self.y)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mario.dir += 1
                mario.turn = 1
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
                mario.turn = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1

        if event.type == SDL_KEYDOWN and event.key == SDLK_x and mario.jump == False:
            mario.jump = True


open_canvas(background_Width, background_Height)
backgraund = Backgraund()
mario = Mario()

running = True

while running:
    clear_canvas()

    backgraund.draw()
    mario.draw()
    mario.update()


    update_canvas()
    handle_events()

    delay(0.03)


