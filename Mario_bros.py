from pico2d import *

background_Width, background_Height = 1200, 800

class Background:
    def __init__(self): #생성자
        self.image = load_image('background3.png')

    def draw(self):
        self.image.draw(600, 400)

class Mario:
    def __init__(self):
        #self.image = load_image('mario_sheet_right.png')
        self.mario_right = load_image('mario_sheet_right.png')
        self.mario_left = load_image('mario_sheet_left.png')
        self.mario_stand_right = load_image('mario_right.png')
        self.mario_stand_left = load_image('mario_left.png')
        self.mario_jump_right = load_image('mario_jump_right.png')
        self.mario_jump_left = load_image('mario_jump_left.png')

        self.mario_status = -1       # 마리오 상태: -1 = 작은마리오, 0 = 일반 마리오, 1 = 플라워마리오
        self.x, self.y = 200, 160
        self.cx, self.cy = self.x, self.y
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 3


    def draw(self):
        self.mario_right.draw(self.x, self.y)
        self.mario_right.clip_draw(self.frame*120, 0, 100, 90, self.x, self.y)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False




open_canvas(background_Width, background_Height)

background = Background() # 백그라운드 객체 생성
mario = Mario()

running = True

while running:

    clear_canvas()   # 캔버스 초기화
    
    handle_events()  # 키 입력을 받아들이는 처리 = 게임 종료 부분

    mario.update()

    background.draw()
    mario.draw()

    update_canvas()

    delay(0.05)

    
