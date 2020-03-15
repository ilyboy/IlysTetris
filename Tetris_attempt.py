import pygame as pg
from dataclasses import dataclass
import random as rnd
import time
reihenlöschung = 0
breite, spalten, zeilen = 400, 10, 43
mino = breite // spalten
höhe = mino * zeilen
grid = [0] * spalten * zeilen
fallrate = 48
score, level, lines = 0, 0, 0
levelspeed = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
currentbags = []
nextqueue = []
nextpiececount = 3 #Beim Anpassen Anzahl unten ändern!!!
CurrentTetrimino = 7
GlobalSaveTet = []
HoldPiece = 7
Gehalten = False
HoldLetter = ' '
Combo = -1
festgesetzt = False
stop = False
LastactionSpin = False
TSpin = False
B2B = False
RotationStatus = 0
Tspinresult = 0
RenderedTspinOrPC = ' '
RenderedLineCount = ' '
RenderedB2B = ' '
RenderedCombo = ' '
PC = False
LockTimer = 0
RotateStallCount = 0
MoveStallCount = 0
Rotated = False
Moved = False
MoveRightTimer = 0
MoveRightDAS = False
MoveLeftTimer = 0
MoveLeftDAS = False
RotatedRight = False
RotatedLeft = False
Harddropped = False
Softdropped = True
Autodroptimer = 8
LastKick = False





blockColors = {
'I' : (19,232,232), #CYAN
'O' : (236,236,14), #YELLOW
'T' : (126,5,126), #PURPLE
'S' : (0,128,0), #GREEN
'Z' : (236,14,14), #RED
'J' : (30,30,201), #BLUE
'L' : (240,110,2) }
#for n in range(8):
#    bilder.append(pg.transform.scale(pg.image.load(f'tt3_{n}.gif')(mino, mino))

pg.init()
screen = pg.display.set_mode([breite, 810])

tetriminoDown = pg.USEREVENT + 1
speedup = pg.USEREVENT + 2
clearRenderedLineclear = pg.USEREVENT + 3
pg.time.set_timer(tetriminoDown, (1000*levelspeed[level]//60))
#pg.key.set_repeat(1,100)

tetriminos = [[0,2,2,0,0,2,2,0,0,0,0,0,0,0,0,0],#O
              [0,0,0,0,7,7,7,7,0,0,0,0,0,0,0,0],#I
              [6,0,0,0,6,6,6,0,0,0,0,0,0,0,0,0],#J
              [0,0,3,0,3,3,3,0,0,0,0,0,0,0,0,0],#L
              [0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0],#S
              [4,4,0,0,0,4,4,0,0,0,0,0,0,0,0,0],#Z
              [0,8,0,0,5,9,5,0,0,0,0,0,0,0,0,0]]#T


IRotations = [[0,0,0,0,7,7,7,7,0,0,0,0,0,0,0,0],
              [0,0,7,0,0,0,7,0,0,0,7,0,0,0,7,0],
              [0,0,0,0,0,0,0,0,7,7,7,7,0,0,0,0],
              [0,7,0,0,0,7,0,0,0,7,0,0,0,7,0,0]]

WallKicksRight = [[0,0],[-1,0],[-1,-1],[0,2] ,[-1,2], #0>>>1
                  [0,0],[1,0] ,[1,1]  ,[0,-2],[1,-2], #1>>>2
                  [0,0],[1,0] ,[1,-1] ,[0,2] ,[1,2],  #2>>>3
                  [0,0],[-1,0],[-1,1] ,[0,-2],[-1,-2]]#3>>>0

WallKicksLeft =  [[0,0],[1,0] ,[1,-1] ,[0,2] ,[1,2],  #0>>>3
                  [0,0],[-1,0],[1,1]  ,[0,-2],[1,-2], #1>>>0
                  [0,0],[-1,0],[-1,-1],[0,2] ,[-1,2], #2>>>1
                  [0,0],[1,0] ,[-1,1] ,[0,-2],[-1,-2]]#3>>>2

IWallKicksRight = [[0,0],[-2,0],[1,0] ,[-2,1] ,[1,-2], #0>>>1
                   [0,0],[-1,0],[2,0] ,[-1,-2],[2,1],  #1>>>2
                   [0,0],[2,0] ,[-1,0],[2,-1] ,[-1,2], #2>>>3
                   [0,0],[1,0] ,[-2,0],[1,2]  ,[-2,-1]]#3>>>0

IWallKicksLeft =  [[0,0],[-1,0],[2,0] ,[-1,-2],[2,1],  #0>>>3
                   [0,0],[2,0] ,[-1,0],[2,-1] ,[-1,2], #1>>>0
                   [0,0],[1,0] ,[-2,0],[1,2]  ,[-2,-1],#2>>>1
                   [0,0],[-2,0],[1,0] ,[-2,1] ,[1,-2]] #3>>>2



@dataclass
class Tetrimino():
    
    tet : list
    zeile : int = 22
    spalte : int = 3

    def show(self, ghost):
        for n in range(16):
            x = (self.spalte + n % 4) * mino
            y = (self.zeile + n // 4) * mino
            p = self.tet[n]
            if ghost == False:
                if p == 1:
                    pg.draw.rect(screen, (0, 128, 0),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (0, 64, 0),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 2:
                    pg.draw.rect(screen, (236, 236, 14),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (118, 118, 7),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 3:
                    pg.draw.rect(screen, (240,110,2),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (120, 55, 1),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 4:
                    pg.draw.rect(screen, (236,14,14),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (118, 7, 7),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 5:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 6:
                    pg.draw.rect(screen, (30,30,201),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (15, 15, 101),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 7:
                    pg.draw.rect(screen, (19,232,232),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (10, 116, 116),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 8:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
                elif p == 9:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
                    pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
            elif ghost == True:
                if p == 1:
                    pg.draw.rect(screen, (0, 128, 0),[x, y - 910, mino, mino], 2)
                elif p == 2:
                    pg.draw.rect(screen, (236, 236, 14),[x, y-910, mino, mino], 2)
                elif p == 3:
                    pg.draw.rect(screen, (240,110,2),[x, y-910, mino, mino], 2)
                elif p == 4:
                    pg.draw.rect(screen, (236,14,14),[x, y-910, mino, mino], 2)
                elif p == 5:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 2)
                elif p == 6:
                    pg.draw.rect(screen, (30,30,201),[x, y-910, mino, mino], 2)
                elif p == 7:
                    pg.draw.rect(screen, (19,232,232),[x, y-910, mino, mino], 2)
                elif p == 8:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 2)
                elif p == 9:
                    pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 2)
    
    def gültig(self, z, s):
        for n in range(16):
            r = self.tet[n]
            if r > 0:
                z1 = z + n // 4
                s1 = s + n % 4
                if z1 >= zeilen or s1 < 0 or s1 >= spalten or grid[z1 * spalten + s1] > 0:
                    return False
        return True
      
    def update(self, zoff, soff):
        if self.gültig(self.zeile + zoff, self.spalte + soff):
            self.zeile += zoff
            self.spalte += soff
            #LastactionSpin = False
            return True
        return False

    def rotateLeft(self):
        global LastactionSpin
        global LastKick
        NewRotationStatus = RotationStatus
        NewIRotationStatus = NewRotationStatus
        saveTet = self.tet.copy()
        if not CurrentTetrimino == 1:
            for n in range(16):
                z = n // 4
                s = n % 4
                q = saveTet[n]
                self.tet[((2-s)*4+z)] = q
        else:
            NewIRotationStatus = NewIRotationStatus - 1
            if NewIRotationStatus == -1:
                NewIRotationStatus = 3
            self.tet = IRotations[NewIRotationStatus]
        if not self.gültig(self.zeile, self.spalte):
            for i in range(5):
                saveZeile = self.zeile
                saveSpalte = self.spalte
                if not CurrentTetrimino == 1:
                    UpdateList = WallKicksLeft[5*NewRotationStatus + i][:]
                else:
                    UpdateList = IWallKicksLeft[5*NewRotationStatus + i][:]
                ZeilenUpdate = UpdateList[1]
                SpaltenUpdate = UpdateList[0]
                self.update(ZeilenUpdate,SpaltenUpdate)
                if self.gültig(self.zeile, self.spalte):
                    LastKick = True
                    break
                else:
                    self.zeile = saveZeile
                    self.spalte = saveSpalte
                if i == 4:
                    self.tet = saveTet.copy()
                    return NewRotationStatus
            LastactionSpin = True
            NewRotationStatus = NewRotationStatus - 1
            if NewRotationStatus == -1:
                NewRotationStatus = 3
            return NewRotationStatus
        else:
            LastactionSpin = True
            NewRotationStatus = NewRotationStatus - 1
            if NewRotationStatus == -1:
                NewRotationStatus = 3
            return NewRotationStatus

    def hold(self, HoldPiece):
        if HoldPiece == 7:
            HoldPiece = CurrentTetrimino
            return 7 + 10 * HoldPiece
        else:
            TransitionHoldPiece = HoldPiece
            HoldPiece = CurrentTetrimino
            return (TransitionHoldPiece + HoldPiece * 10)
         
    def rotateRight(self):
        global LastactionSpin
        global LastKick
        NewRotationStatus = RotationStatus
        NewIRotationStatus = NewRotationStatus
        saveTet = self.tet.copy()
        saveTet2 = self.tet.copy()
        for j in range(3):
            
            if not CurrentTetrimino == 1:
                for n in range(16):
                    z = n // 4
                    s = n % 4
                    v = saveTet2[n]
                    self.tet[((2-s)*4+z)] = v
                saveTet2 = self.tet.copy()
            if j == 2 and CurrentTetrimino == 1:
                NewIRotationStatus = NewIRotationStatus + 1
                if NewIRotationStatus == 4:
                    NewIRotationStatus = 0
                saveTet = self.tet.copy()
                self.tet = IRotations[NewIRotationStatus]
        if not self.gültig(self.zeile, self.spalte):
            for i in range(5):
                saveZeile = self.zeile
                saveSpalte = self.spalte
                if not CurrentTetrimino == 1:
                    kicklist = WallKicksRight[5*NewRotationStatus + i][:]
                else:
                    kicklist = IWallKicksRight[5*NewRotationStatus + i][:]
                self.update(kicklist[1],kicklist[0])
                Check = self.gültig(self.zeile, self.spalte)
                if Check == True:
                    LastKick = True
                    break
                else:
                    self.zeile = saveZeile
                    self.spalte = saveSpalte
                if i == 4:
                    self.tet = saveTet.copy()
                    return NewRotationStatus



                        
    
        LastactionSpin = True
        if NewRotationStatus == 3:
            NewRotationStatus = 0
        else:
            NewRotationStatus = NewRotationStatus + 1
        return NewRotationStatus
    
    def Tspincheck(self):
        BelegteEcken = 0
        BelegterRand = 0
        if LastKick == True:
            return 2
        for i in range(16):
            w = self.tet[i]
            if w == 9:
                s3 = self.spalte + i % 4 - 1
                z3 = self.zeile + i // 4 - 1
                if z3 >= zeilen or s3 < 0 or s3 >= spalten or grid[z3 * spalten + s3] > 0:
                    BelegteEcken = BelegteEcken + 1
                s3 = self.spalte + i % 4 + 1
                z3 = self.zeile + i // 4 - 1
                if z3 >= zeilen or s3 < 0 or s3 >= spalten or grid[z3 * spalten + s3] > 0:
                    BelegteEcken = BelegteEcken + 1
                s3 = self.spalte + i % 4 - 1
                z3 = self.zeile + i // 4 + 1
                if z3 >= zeilen or s3 < 0 or s3 >= spalten or grid[z3 * spalten + s3] > 0:
                    BelegteEcken = BelegteEcken + 1
                s3 = self.spalte + i % 4 + 1
                z3 = self.zeile + i // 4 + 1
                if z3 >= zeilen or s3 < 0 or s3 >= spalten or grid[z3 * spalten + s3] > 0:
                    BelegteEcken = BelegteEcken + 1
                if BelegteEcken > 2:
                    for j in range(16):
                        c = self.tet[j]
                        if c == 8:
                            #print(RotationStatus)
                            if RotationStatus % 2 == 0:
                                s4 = self.spalte + j % 4 + 1
                                z4 = self.zeile + j // 4
                                if z4 >= zeilen or s4 < 0 or s4 >= spalten or grid[z4 * spalten + s4] > 0:
                                    BelegterRand = BelegterRand + 1
                                s4 = self.spalte + j % 4 - 1
                                z4 = self.zeile + j // 4
                                if z4 >= zeilen or s4 < 0 or s4 >= spalten or grid[z4 * spalten + s4] > 0:
                                    BelegterRand = BelegterRand + 1
                            elif RotationStatus % 2 == 1:
                                s4 = self.spalte + j % 4 
                                z4 = self.zeile + j // 4 + 1
                                if z4 >= zeilen or s4 < 0 or s4 >= spalten or grid[z4 * spalten + s4] > 0:
                                    BelegterRand = BelegterRand + 1
                                s4 = self.spalte + j % 4 
                                z4 = self.zeile + j // 4 - 1
                                if z4 >= zeilen or s4 < 0 or s4 >= spalten or grid[z4 * spalten + s4] > 0:
                                    BelegterRand = BelegterRand + 1
                            if BelegterRand == 2:
                                return 2
                            else: 
                                return 1
                return 0
        

    def festsetzen(self):
        #Mid-Air-
        global CurrentTetrimino
        global score
        global Gehalten
        global RenderedB2B
        global RenderedCombo
        global RenderedLineCount
        global RenderedTspinOrPC
        global Combo
        global B2B
        global currentbags
        global gameLoop
        global level
        global Tspinresult
        global RotateStallCount
        global MoveStallCount
        global LockTimer
        global lines
        RotateStallCount = 0
        MoveStallCount = 0
        LockTimer = 0
        for n in range(16):
            t = self.tet[n]
            if t > 0:
                z = self.zeile + n // 4
                s = self.spalte + n % 4
                grid[z * spalten + s] = t
                global RotationStatus
                RotationStatus = 0
        if LastactionSpin == True and CurrentTetrimino == 6:
            Tspinresult = self.Tspincheck()
        if Tspinresult == 0:
            Tspintype = ' '
        elif Tspinresult == 1:
            Tspintype = 'Mini T-Spin'
            RenderedTspinOrPC = 'Mini T-Spin'
            print(Tspintype)
            score = score + (50 *(level+1))
        elif Tspinresult == 2:
            Tspintype = 'T-Spin'
            RenderedTspinOrPC = 'T-Spin'
            print(Tspintype)
            score = score + (250 *(level+1))
        Gehalten = False
        reihenlöschung = LineClear()
        if reihenlöschung > 0:
            RenderedLineCount = ' '
            RenderedB2B = ' '
            RenderedCombo = ' '
            if not Tspintype == RenderedTspinOrPC:
                RenderedTspinOrPC = ' '
        if reihenlöschung == 1:
            score = score + (40*(level+1))
            print('Single')
            RenderedLineCount = 'Single'
            if Tspinresult == 1:
                score = score + (60*(level+1))
            elif Tspinresult == 2:
                score = score + (710*(level+1))                        
        elif reihenlöschung == 2:
            if Tspinresult == 1:
                score = score + (150*(level+1))
            elif Tspinresult == 2:
                score = score + (1650*(level+1))  
            score = score + (100*(level+1))
            print('Double')
            RenderedLineCount = 'Double'
        elif reihenlöschung == 3:
            if Tspinresult == 2:
                score = score + (4350*(level+1))
            score = score + (400*(level+1))
            print('Triple')
            RenderedLineCount = 'Triple'
        elif reihenlöschung == 4:
            score = score + (1200*(level+1))
            print('Tetris')
            RenderedLineCount = 'Tetris'
        if reihenlöschung > 0 or Tspinresult > 0:
            pg.time.set_timer(clearRenderedLineclear, 1000)
        if reihenlöschung > 0:

            Combo = Combo + 1
            score = score + (40*Combo*(level+1))
            if Combo > 0:
                RenderedCombo = str(Combo) + ' Combo'
            if B2B == False:
                if Tspinresult > 0 or reihenlöschung == 4:
                    B2B = True
            elif Tspinresult > 0 or reihenlöschung == 4:
                score = score + (500*(level+1))
                print('Back-To-Back')
                RenderedB2B = 'Back-To-Back'
            else:
                B2B = False
            PC = True
            for i in range(430):
                if not grid[i] == 0:
                    PC = False
            if PC == True:
                score = score + (10000*(level+1))
                RenderedTspinOrPC = 'Perfect Clear'
            
            GraphicUpdate()
            '''time.sleep(3)'''
        else:
            Combo = -1
            RenderedCombo = ' '
        for i in range(reihenlöschung):
            lines = lines + 1
            if lines % 10 == 0:
                level = level + 1
                
                pg.time.set_timer(tetriminoDown, (1000*levelspeed[level]//60))
        #savetetriminos = tetriminos.copy()
    

    def groundedcheck(self, z, s):
        for n in range(16):
            r = self.tet[n]
            if r > 0:
                z1 = z + n // 4 + 1
                s1 = s + n % 4
                if z1 >= zeilen or s1 < 0 or s1 >= spalten or grid[z1 * spalten + s1] > 0:
                    return False
        return True

    

def LineClear():
    anzahlZeilen = 0
    for zeile in range(zeilen):
        for spalte in range(spalten):
            if grid[zeile*spalten+spalte] == 0:
                break
        else:
            del grid[zeile*spalten:zeile*spalten + spalten]
            grid[0:0] = [0]*spalten
            anzahlZeilen = anzahlZeilen + 1
            #GraphicUpdate()
            #time.sleep(1)
    return anzahlZeilen

def GetBag():
    newBag = [1,2,3,4,5,6,0]
    rnd.shuffle(newBag)
    return newBag

def GetQueue():
    Nextqueued = []
    for i in range(nextpiececount):
        if currentbags[i] == 0:
            Nextqueued.append('O')
        elif currentbags[i] == 1:
            Nextqueued.append('I')    
        elif currentbags[i] == 2: 
            Nextqueued.append('J')
        elif currentbags[i] == 3: 
            Nextqueued.append('L')
        elif currentbags[i] == 4: 
            Nextqueued.append('S')
        elif currentbags[i] == 5: 
            Nextqueued.append('Z')
        elif currentbags[i] == 6:  
            Nextqueued.append('T')
    return Nextqueued

def GetHoldLetter(HoldLetter):
    
    if HoldLetter == 0:
        NewHoldLetter = ('O')
    elif HoldLetter == 1:
        NewHoldLetter = ('I')    
    elif HoldLetter == 2: 
        NewHoldLetter = ('J')
    elif HoldLetter == 3: 
        NewHoldLetter = ('L')
    elif HoldLetter == 4: 
        NewHoldLetter = ('S')
    elif HoldLetter == 5: 
        NewHoldLetter = ('Z')
    elif HoldLetter == 6:  
        NewHoldLetter = ('T')
    return NewHoldLetter

def GraphicUpdate():
    
    textsurface = pg.font.SysFont('comic sans', 20).render('Punkte: ' + str(score), False, (255, 255, 255) )
    screen.blit(textsurface,(230 , 5))
    textsurface = pg.font.SysFont('comic sans', 20).render('Level: ' + str(level), False, (255, 255, 255) )
    screen.blit(textsurface,(165 , 5))
    textsurface = pg.font.SysFont('comic sans', 20).render('Reihen: ' + str(lines), False, (255, 255, 255) )
    screen.blit(textsurface,(90 , 5))
    textsurface = pg.font.SysFont('comic sans', 20).render('Halten:', False, (255, 255, 255) )
    screen.blit(textsurface,(10 , 5))
    textsurface = pg.font.SysFont('comic sans', 60).render(HoldLetter , False, (255, 255, 255) )
    screen.blit(textsurface,(15 , 25))
    nextpiece1 = nextqueue[0]
    nextpiece2 = nextqueue[1]
    nextpiece3 = nextqueue[2]
    textsurface = pg.font.SysFont('comic sans', 20).render(('Nächste: '), False, (255, 255, 255))
    screen.blit(textsurface,(340 , 5))
    textsurface = pg.font.SysFont('comic sans', 66).render((nextpiece1), False, (255, 255, 255))
    screen.blit(textsurface,(350 , 25))
    textsurface = pg.font.SysFont('comic sans', 66).render((nextpiece2), False, (255, 255, 255))
    screen.blit(textsurface,(350 , 65))
    textsurface = pg.font.SysFont('comic sans', 66).render((nextpiece3), False, (255, 255, 255))
    screen.blit(textsurface,(350 , 105))
    textsurface = pg.font.SysFont('comic sans', 30).render((RenderedCombo), False, (255, 255, 255))
    screen.blit(textsurface,(150 , 25))
    textsurface = pg.font.SysFont('comic sans', 30).render((RenderedTspinOrPC), False, (255, 255, 255))
    screen.blit(textsurface,(150 , 50))
    textsurface = pg.font.SysFont('comic sans', 30).render((RenderedLineCount), False, (255, 255, 255))
    screen.blit(textsurface,(150 , 75))
    textsurface = pg.font.SysFont('comic sans', 30).render((RenderedB2B), False, (255, 255, 255))
    screen.blit(textsurface,(150 , 100))
    pg.display.flip()




currentbags = GetBag() + GetBag()
#print(currentbags)



#savetetriminos = tetriminos.copy()
CurrentTetrimino = currentbags[0]
#savetetriminos = tetriminos[CurrentTetrimino]
figur = Tetrimino(tetriminos[currentbags[0]][:])
ghost = Tetrimino(tetriminos[currentbags[0]][:])
del currentbags[0]
currentbags.append(7)
nextqueue = GetQueue()

gameLoop = True
clock = pg.time.Clock()
while gameLoop:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameLoop = False
        if event.type == clearRenderedLineclear:
            RenderedTspinOrPC = ' '
            RenderedLineCount = ' '
            RenderedB2B = ' '
            RenderedCombo = ' '
        if LockTimer > 30 or RotateStallCount > 16 or MoveStallCount > 16:
            if not figur.groundedcheck(figur.zeile, figur.spalte):
                festgesetzt = True
                figur.festsetzen()
                figur = Tetrimino(tetriminos[currentbags[0]][:])
                ghost = Tetrimino(tetriminos[currentbags[0]][:])
                TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
                if TopOutCheck == False:
                    figur.update(-1, 0)
                    TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
                    if TopOutCheck == False:
                        figur.update(-1, 0)
                        TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
                        if TopOutCheck == False:
                            gameLoop = False
                                

                CurrentTetrimino = currentbags[0]
                del currentbags[0]
                nextqueue = GetQueue()
                currentbags.append(7)
                if currentbags[7] == 7:
                    
                    #print(currentbags)
                    del currentbags[7:14]
                    
                    #print(currentbags)
                    currentbags = currentbags + GetBag()
                #print(currentbags)
    keys = pg.key.get_pressed()

        #if event.key == pg.K_LEFT:
    
    if Autodroptimer < 1:
        figur.update(1,0)
        Autodroptimer = levelspeed[level] // 1.4999
    if keys[pg.K_LEFT]:
        if MoveLeftTimer == 0:
            if figur.update(0, -1) == True:
                LockTimer = 0
                if not figur.groundedcheck(figur.zeile, figur.spalte):
                    MoveStallCount = MoveStallCount + 1
                LastactionSpin = False
                if MoveLeftDAS == False:
                    MoveLeftTimer = 5
                    MoveLeftDAS = True
                else:
                    MoveLeftTimer = 2
        else:
            MoveLeftTimer = MoveLeftTimer - 1
    else:
        MoveLeftTimer = 0
        MoveLeftDAS = False

#if event.key == pg.K_RIGHT:
    if keys[pg.K_RIGHT]:
        if MoveRightTimer == 0:
            if figur.update(0, 1) == True:
                LockTimer = 0
                if not figur.groundedcheck(figur.zeile, figur.spalte):
                    MoveStallCount = MoveStallCount + 1
            LastactionSpin = False
            if MoveRightDAS == False:
                MoveRightTimer = 5
                MoveRightDAS = True
            else:
                MoveRightTimer = 2
        else:
            MoveRightTimer = MoveRightTimer - 1
    else:
        MoveRightTimer = 0
        MoveRightDAS = False

    #if event.key == pg.K_DOWN:
    if keys[pg.K_DOWN]:
        if Softdropped:
            if figur.update(1,0) == True:
                LastactionSpin = False
                Softdropped = False
        else:
            Softdropped = True
    else:
        Softdroppde = True
#if event.key == pg.K_a:
    if keys[pg.K_a]:
        if not RotatedLeft:
            RotatedLeft = True
            OldRotationStatus = RotationStatus
            GroundCheck = figur.groundedcheck(figur.zeile, figur.spalte)
            if not CurrentTetrimino == 0 and RotateStallCount < 17:
                RotationStatus = figur.rotateLeft()
            if not GroundCheck == True:
                if not OldRotationStatus == RotationStatus or CurrentTetrimino == 0:
                    RotateStallCount = RotateStallCount + 1
                    LockTimer = 0
    else:
        RotatedLeft = False
#if event.key == pg.K_f:
    if keys[pg.K_f]:
        if not RotatedRight:
            RotatedRight = True
            OldRotationStatus = RotationStatus
            GroundCheck = figur.groundedcheck(figur.zeile, figur.spalte)
            if not CurrentTetrimino == 0:
                RotationStatus = figur.rotateRight()
            if not GroundCheck == True:
                if not OldRotationStatus == RotationStatus or CurrentTetrimino == 0:
                    RotateStallCount = RotateStallCount + 1
                    LockTimer = 0
    else:
        RotatedRight = False
#if event.key == pg.K_s:
    if keys[pg.K_s]:
        if Gehalten == False:
            HoldResult = figur.hold(HoldPiece)
            HoldPiece = HoldResult // 10
            HoldResult = HoldResult % 10
            RotateStallCount = 0
            MoveStallCount = 0
            LockTimer = 0
            if HoldResult == 7:
                figur = Tetrimino(tetriminos[currentbags[0]][:])
                ghost = Tetrimino(tetriminos[currentbags[0]][:])
                CurrentTetrimino = currentbags[0]
                del currentbags[0]
                nextqueue = GetQueue()
                currentbags.append(7)
            else:
                figur = Tetrimino(tetriminos[HoldResult][:])
                CurrentTetrimino = HoldResult
            Gehalten = True
            HoldLetter = GetHoldLetter(HoldPiece)
#if event.key == pg.K_d:
    if keys[pg.K_d]:
        if not Harddropped:
            Harddropped = True
            while True:
                if not figur.update(1, 0):
                    break
                else:
                    LastactionSpin = False
                
            
            festgesetzt = True
            figur.festsetzen()
            figur = Tetrimino(tetriminos[currentbags[0]][:])
            ghost = Tetrimino(tetriminos[currentbags[0]][:])
            TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
            if TopOutCheck == False:
                figur.update(-1, 0)
                TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
                if TopOutCheck == False:
                    figur.update(-1, 0)
                    TopOutCheck = figur.gültig(figur.zeile, figur.spalte)
                    if TopOutCheck == False:
                        gameLoop = False
                        

            CurrentTetrimino = currentbags[0]
            del currentbags[0]
            nextqueue = GetQueue()
            currentbags.append(7)
            if currentbags[7] == 7:
                
                #print(currentbags)
                del currentbags[7:14]
                
                #print(currentbags)
                currentbags = currentbags + GetBag()
    else:
        Harddropped = False
    if not figur.groundedcheck(figur.zeile, figur.spalte):
        LockTimer = LockTimer + 1
    else:
        LockTimer = 0
    ghost.spalte = figur.spalte
    ghost.zeile = figur.zeile
    ghost.tet = figur.tet[:]
    while True:
        if not ghost.update(1, 0):
            break
    screen.fill((5,5,5))
    for i in range(9):
        pg.draw.rect(screen, (30, 30, 30), [mino*i + mino, 0, 0, 810], 1)
    for i in range(20):
        pg.draw.rect(screen, (30, 30, 30), [0, mino*i + 10, 400, 0], 1)
    ghost.show(True)
    figur.show(False)
    #pg.draw.rect(screen, (19,232,232),[0, 0, 40, 40], 0)
    for n in range(spalten * zeilen):
        x = n % spalten * mino
        y = n // spalten * mino
        o = grid[n]
        if o == 1:
            pg.draw.rect(screen, (0, 115, 0),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (0, 64, 0),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 2:
            pg.draw.rect(screen, (213, 213, 13),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (118, 118, 7),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 3:
            pg.draw.rect(screen, (216,99,2),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (120, 55, 1),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 4:
            pg.draw.rect(screen, (213,13,13),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (118, 7, 7),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 5:
            pg.draw.rect(screen, (113,5,113),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 6:
            pg.draw.rect(screen, (27,27,181),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (15, 15, 101),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 7:
            pg.draw.rect(screen, (17,209,209),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (10, 116, 116),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 8:
            pg.draw.rect(screen, (113,5,113),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
        elif o == 9:
            pg.draw.rect(screen, (113,5,113),[x, y-910, mino, mino], 0)
            pg.draw.rect(screen, (63, 3, 63),[x + 1, y-909, mino - 2, mino - 2], 4)
    
    for n in range(spalten * zeilen):
        x = n % spalten * mino
        y = n // spalten * mino
        
        pg.draw.rect(screen, (30, 30, 30),[x- 2, y + 48, 4, 4,], 0)
        
        #print(n)
    #for n, farbe in enumerate(grid):
     #   if farbe > 0:
           # x = n % spalten * mino
            #y = n // spalten * mino
         #   screen.blit(bilder[farbe],(x,y))
    GraphicUpdate()
    Tspinresult = 0
    Autodroptimer = Autodroptimer - 1
    LastKick = False
    
clock.tick(1)
'''while True:
    screen.fill((0,0,0))
    rowdelete = 42

    for n in range(spalten * zeilen):
        x = n % spalten * mino
        y = n // spalten * mino
        o = grid[n]
        if o == 1:
            pg.draw.rect(screen, (0, 128, 0),[x, y-910, mino, mino], 0)
        elif o == 2:
            pg.draw.rect(screen, (236, 236, 14),[x, y-910, mino, mino], 0)
        elif o == 3:
            pg.draw.rect(screen, (240,110,2),[x, y-910, mino, mino], 0)
        elif o == 4:
            pg.draw.rect(screen, (236,14,14),[x, y-910, mino, mino], 0)
        elif o == 5:
            pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
        elif o == 6:
            pg.draw.rect(screen, (30,30,201),[x, y-910, mino, mino], 0)
        elif o == 7:
            pg.draw.rect(screen, (19,232,232),[x, y-910, mino, mino], 0)
        elif o == 8:
            pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
        elif o == 9:
            pg.draw.rect(screen, (126,5,126),[x, y-910, mino, mino], 0)
        
        for i in range(10):
            del grid[10 * rowdelete]
            grid.append(0)
        rowdelete = rowdelete - 1

        if rowdelete < 0:
            break'''





print(score)
pg.quit()


