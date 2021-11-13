from pico2d import *
import time

background_Width, background_Height = 1200, 800

PIXEL_PER_METER = (10.0 / 0.01)   # 10 pixel 20cm   속도조절 중
RUN_SPEED_KMPH = 20.0       # km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Stage1_Left_Background:
    def __init__(self):
        self.image = load_image("World_Left.png")

    def draw(self):
        self.image.draw(3000 - mario.x, background_Height - 400)

class Stage1_Right_Background:
    def __init__(self):
        self.image = load_image("World_Right.png")

    def draw(self):
        self.image.draw(8628 - mario.x, background_Height -400)

class Block:
    def __init__(self):
        self.image = load_image("block.png")

    def draw(self):
        self.image.draw(500, 500)

class Mario:
    def __init__(self):
        self.image = load_image("mario_sheet2.png")
        self.x, self.y = 300, 160
        self.cx = self.x        #미정
        self.cy = self.y
        self.dir = 0            # 방향값 ,  속도 = 방향 * 20
        self.turn = 0           # 얼굴돌리는 방향값
        self.accl = 0           # 가속도
        self.Max_accl = 1       # 최대 가속도
        self.frame = 0.0          # 프레임
        self.jump = False       # 점프키 눌렸는지
        self.jump_y = 0         # 점프량 값
        self.gravity = 0        # 중력값
        self.ground_y = 160       # 현재 서있는 땅의 y값


    def update(self):
        self.cx = self.x
        self.cy = self.y
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
            self.x += self.dir * RUN_SPEED_PPS * frame_time * self.accl
        elif self.dir == -1:                                # 왼쪽으로 가고있을때 가속 붙여서 x좌표 왼쪽으로
            self.x += self.dir * RUN_SPEED_PPS * frame_time * (-self.accl)
        elif self.dir == 0 and self.turn == 1:              # 오른쪽으로 가다 멈출때
            self.x += RUN_SPEED_PPS * frame_time * self.accl
        elif self.dir == 0 and self.turn == -1:             # 왼쪽으로 가다 멈출때
            self.x += RUN_SPEED_PPS * frame_time * self.accl

        if self.jump == True:
            self.jump_y = 45
            self.gravity += 3

        self.y += self.jump_y - self.gravity
        if self.y < self.ground_y:
            self.y = self.ground_y
            self.jump = False
            self.gravity = 0
            self.jump_y = 0

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time) % 3
        #self.frame = (self.frame + 1) % 3
        self.x = clamp(-290, self.x, 10800)

    def draw(self):
        if self.x > self.cx and self.jump == False:
            self.image.clip_draw(920 + int(self.frame) * 120, 910, 120, 90, 500, 145)
            self.turn = 1
        elif self.x < self.cx and self.jump == False:
            self.image.clip_draw(560 - int(self.frame) * 120, 910, 120, 90, 500, 145)
            self.turn = -1
        elif self.turn == 1 and self.jump == False:
            self.image.clip_draw(800, 910, 120, 90, 500, 145)
        elif self.turn == -1 and self.jump == False:
            self.image.clip_draw(680, 910, 120, 90, 500, 145)
        elif self.x > self.cx and self.jump == True:
            self.image.clip_draw(1400, 910, 120, 90, 500, self.y)
            self.turn = 1
        elif self.x < self.cx and self.jump == True:
            self.image.clip_draw(80, 910, 120, 90, 500, self.y)
            self.turn = -1
        elif self.dir == 0 and self.jump == True and self.turn == 1:
            self.image.clip_draw(1400, 910, 120, 90, 500, self.y)
        elif self.dir == 0 and self.jump == True and self.turn == -1:
            self.image.clip_draw(80, 910, 120, 90, 500, self.y)
        elif self.jump == True and self.turn == -1:
            self.image.clip_draw(1400, 910, 120, 90, 500, self.y)
        else:
            self.image.clip_draw(800, 910, 120, 90, 500, self.y)


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
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1

        if event.type == SDL_KEYDOWN and event.key == SDLK_x and mario.jump == False:
            mario.jump = True


open_canvas(background_Width, background_Height)
St1_L_background = Stage1_Left_Background()
St1_R_background = Stage1_Right_Background()
block = Block()
mario = Mario()

frame_time = 0.0
current_time = time.time()
running = True

while running:
    clear_canvas()

    St1_L_background.draw()
    St1_R_background.draw()
    block.draw()
    mario.draw()
    mario.update()

    update_canvas()
    handle_events()

    frame_time = time.time() - current_time
    frame_rate = 1.0 / frame_time
    current_time += frame_time

    #delay(0.02)


