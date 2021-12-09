class ProgramControl:

    # ************ Program control ************
    windowSize = (1400, 750)
    windowPos = (80, 50)  # initial position of the game window on the computer screen
    frequency = 60
    levelUp = 200  # time gap of increment of difficulty
    slowLevelUp = 660  # after some time, the increment of difficulty slows down
    bigImageSize = {"./image/player/PlayerShipDisplayA.png": (240, 150),
                    "./image/player/PlayerShipDisplayB.png": (240, 155),
                    "./image/player/PlayerShipDisplayC.png": (268, 137),
                    "./image/player/PlayerShipDisplayD.png": (228, 167)}
    gameEndWaitTime = 120

    backgroundColor = (0, 0, 0)
    scoreColor = (100, 100, 100)
    shipSelectionColor = (135, 206, 250)   # the rectangle that choose the ship
    shipConfirmColor = (160, 32, 240)   # when the ship is clicked
    chooseCharacterTextColor = (255, 255, 255)  # to display "hp", "speed", "damage"...
    chooseCharacterInfoBarBackgroundColor = (190, 190, 190)
    chooseCharacterInfoBarColor = (238, 173, 14)
    skillInfoColor = (255, 255, 200)
    skillRectColor = (255, 255, 200)
    skillTitleColor = (255, 255, 200)

    # *********** intro window *****************
    introBackgroundColor = (0, 0, 0)

    # ***************** stats ********************
    statsWindowFontColor = (255, 255, 255)   # statistics (score, time...)
    statsWindowFontColor2 = (100, 100, 100)  # (Press Enter to continue)
    statsWindowFontSize = 30                 # (Press Enter to continue)
