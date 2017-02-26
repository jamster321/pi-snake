#!/usr/bin/env python

import time
import scrollphat
import sys
import random
import curses

def main(win):
    direction = "RIGHT"
    snakeX=[2, 1, 0]
    snakeY=[2, 2, 2]
    snakeLength = 3
    score = 0

    gameOver = False
    
    scrollphat.set_brightness(5)
    scrollphat.write_string("      PI SNAKE")
    length = scrollphat.buffer_len()

    for i in range(length):
        scrollphat.scroll()
        time.sleep(0.06)
            
    fruitX = random.randint(0,10)
    fruitY = random.randint(0,4)

    fruitBlink = True

    win.nodelay(True)
    key=""
    while 1:
        if gameOver == False:

            # move snake head forward in the direction its travelling
            if direction == "RIGHT":
                if snakeX[0] < 10:
                    snakeX[0] = snakeX[0] + 1
            if direction == "LEFT":
                if snakeX[0] > 0:
                    snakeX[0] = snakeX[0] - 1
            if direction == "UP":
                if snakeY[0] > 0:
                    snakeY[0] = snakeY[0]- 1
            if direction == "DOWN":
                if snakeY[0] < 4:
                    snakeY[0] = snakeY[0] + 1
                    
            # check if the new head position is illegal
            for i in range(1, snakeLength):
                if snakeX[i] == snakeX[0] and snakeY[i] == snakeY[0]:
                    gameOver = True
                    
            # check if the new head position is at a fruit
            if snakeX[0] == fruitX and snakeY[0] == fruitY:
                snakeLength = snakeLength + 1
                score = score + 1
                snakeX.append(fruitX)
                snakeY.append(fruitY)
                fruitX = random.randint(0,10)
                fruitY = random.randint(0,4)

            time.sleep(0.15)
            scrollphat.clear_buffer()

            # shift all the snake parts forward
            for i in range(1, snakeLength):
                snakeX[snakeLength - i] = snakeX[snakeLength - i - 1]
                snakeY[snakeLength - i] = snakeY[snakeLength - i - 1]

            # draw the snake
            for i in range(0, snakeLength):                                                  
                scrollphat.set_pixel(snakeX[i],snakeY[i],True)

            # blink the fruit
            if fruitBlink:
                scrollphat.set_pixel(fruitX,fruitY,True)
                fruitBlink = False
            else:
                scrollphat.set_pixel(fruitX,fruitY,False)
                fruitBlink = True
                
            scrollphat.update()
        else:
            # game over
            gameOverText = "GAME OVER - SCORE: " + str(score) + " PRESS SPACE TO RESTART"
            time.sleep(0.7)
            scrollphat.clear_buffer()
            scrollphat.write_string(gameOverText,len(gameOverText))
            win.clear()
            win.addstr(gameOverText)
            while True:
                try:
                    scrollphat.scroll()
                    time.sleep(0.07)
                    key = win.getkey()
                    if str(key) == " ":
                        break
                except Exception as e:
                    # No input
                    pass
            direction = "RIGHT"
            snakeX=[2, 1, 0]
            snakeY=[2, 2, 2]
            snakeLength = 3
            score = 0
            gameOver = False

        try:
           key = win.getkey()
           win.clear()
           win.addstr("PI SNAKE - SCORE: ")           
           win.addstr(str(score))
           
           if str(key) == "KEY_RIGHT":
               direction = "RIGHT"
           if str(key) == "KEY_LEFT":
               direction = "LEFT"
           if str(key) == "KEY_UP":
               direction = "UP"
           if str(key) == "KEY_DOWN":
               direction = "DOWN"
               
           if key == os.linesep:
              break
        except Exception as e:
           # No input
           pass

curses.wrapper(main)
