
import pygame

from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (64, 64, 64)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('font/Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('font/Roboto-Bold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]  # each beat disabled for each instrument
active_list = [1 for _ in range(instruments)]  # each instrument is initially enabled
bpm = 250
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
# initialize saved_beats from file
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)

beat_name = ''
typing = False

# load in sounds
hi_hat = mixer.Sound('sounds/hi_hat.wav')
snare = mixer.Sound('sounds/snare.wav')
kick = mixer.Sound('sounds/kick.wav')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')
tom = mixer.Sound('sounds/tom.wav')

pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat, actives):
    # instrument controls
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    # player controls
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    # hi-hat
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    # snare
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    # kick
    kick_text = label_font.render('Kick', True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))
    # crash
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    # clap
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    # floor tom
    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_tom_text, (30, 530))

    for i in range(instruments):
        pygame.draw.line(
            screen,
            gray,
            (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue,
                                  [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats),
                                   instruments * 100], 5, 3)
    return boxes


def draw_save_menu(beat_name, typing):
    # background
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    # menu text
    menu_text = label_font.render('save menu: enter a new for current beat', True, white)
    screen.blit(menu_text, (400, 40))
    # do save
    do_save_button = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    do_save_text = label_font.render('save beat', True, white)
    screen.blit(do_save_text, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    # close button
    save_exit_button = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    save_exit_text = label_font.render('close', True, white)
    screen.blit(save_exit_text, (WIDTH - 190, HEIGHT - 70))
    # entry rect border
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    # entry rect
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))

    return save_exit_button, do_save_button, entry_rect


def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    load_exit_button = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    load_exit_text = label_font.render('close', True, white)
    screen.blit(load_exit_text, (WIDTH - 190, HEIGHT - 70))

    return load_exit_button


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons (play/pause)
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('play/pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))
    # bpm
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    bpm_add_text = medium_font.render('+5', True, white)
    bpm_sub_text = medium_font.render('-5', True, white)
    screen.blit(bpm_add_text, (520, HEIGHT - 140))
    screen.blit(bpm_sub_text, (520, HEIGHT - 90))
    # beats
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (618, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    beats_add_text = medium_font.render('+1', True, white)
    beats_sub_text = medium_font.render('-1', True, white)
    screen.blit(beats_add_text, (820, HEIGHT - 140))
    screen.blit(beats_sub_text, (820, HEIGHT - 90))
    # instrument rects
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    # save and load
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render('save', True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render('load', True, white)
    screen.blit(load_text, (920, HEIGHT - 90))
    # clear board 
    clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('clear', True, white)
    screen.blit(clear_text, (1160, HEIGHT - 120))
    # menus
    if save_menu:
        exit_button, do_save_button, entry_rect = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:  # save/load menu are blocking
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        elif event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:  # save/load menu are blocking
            # play/pause
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            # bpm add
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            # bpm sub
            elif bpm_sub_rect.collidepoint(event.pos):
                if bpm > 5:
                    bpm -= 5
            # add beat
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            # remove beat
            elif beats_sub_rect.collidepoint(event.pos):
                if beats > 1:
                    beats -= 1
                    for i in range(len(clicked)):
                        clicked[i].pop(-1)
            # clear all
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]  # re-init clicked
            # save beat
            elif save_button.collidepoint(event.pos):
                save_menu = True
            # load beat
            elif load_button.collidepoint(event.pos):
                load_menu = True
            # beat/instrument (active list) selected
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            elif entry_rect.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            elif do_save_button.collidepoint(event.pos):
                file = open('saved_beats.txt', 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
        if event.type == pygame.TEXTINPUT:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]  # remove the last char

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
