#!/usr/bin/python3
# -*- coding: utf-8 -*-

# pyuic5 desG.ui -o desG.py
# pyuic5 res/desG.ui -o res/desG.py
#pip install mypackage
#.*;.*;.*;.*;.*\n - поиск ошибки в строках файла
#"C:\Users\Home\Dropbox\reanth\p[ter"

import sys
import os
import os.path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QIcon, QDrag, QFont, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QFileDialog, QInputDialog, QMessageBox, QDesktopWidget, QLineEdit, QDialog, QShortcut
from PyQt5.QtCore import QDate, Qt, QMimeData
from functools import partial
import random
import subprocess
import gc #ручное освобождение памяти
import re

import res.desG as desG
import res.MessageOk as MessageOk
import res.MessageNo as MessageNo

import datetime
import time

class MyInfinity(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.runningI  = False     # Флаг выполнения
        self.timeI      = 1
    def run(self):
        self.runningI = True
        self.countI =0
        while self.runningI:        # Проверяем значение флага
            self.countI += 1
            self.sleep(int(self.timeI))
            if self.countI==1000:
                self.runningI = False
            self.mysignal.emit(str(self.countI))
class MyTimer(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running    = False# Флаг выполнения
    def run(self):
        self.running = True
        self.count =1
        while self.running:    # Проверяем значение флага
            self.count += -1
            self.sleep(1)
            if self.count==0:
                self.count = self.running = False
            self.mysignal.emit(str(self.count))
class messageOk(QtWidgets.QDialog, MessageOk.Ui_MessageOk):
    def __init__(self):     #конструктор
        super().__init__()
        self.setupUi(self)
        self.labOk.setText('')
class messageNo(QtWidgets.QDialog, MessageNo.Ui_MessageNo):
    def __init__(self):     #конструктор
        super().__init__()
        self.setupUi(self)
        self.labNo.setText('')

datanowtime = datetime.datetime.today().strftime("%Y%m%d-%H:%M")
dataNow     = datetime.datetime.today().strftime("%Y-%m-%d")

class ReanApp(QtWidgets.QMainWindow, desG.Ui_MainWindow): 
    def __init__(self):     #конструктор
        super().__init__()
        self.setupUi(self)
 # аргументы   
        self.path=os.getcwd()
        self.user=self.path.split('/')[2]
        self.pathFile=''
        self.chl.setChecked(True)
        self.chw.setChecked(True)
        self.btnExit.clicked.connect    (self.ExitPr)
        self.btnReStart.clicked.connect    (self.Restart)
        self.btnStart.clicked.connect   (partial(self.Infinity, 'hand'))
        self.btnReWrite.clicked.connect (self.btnreWrite)
        self.btnNewStr.clicked.connect  (self.btnnewStr)
        self.btnScalePic.clicked.connect (self.ScalePic)
        self.btnVTh.clicked.connect     (partial(self.Vois, 'VoisTh'))
        self.btnVIs.clicked.connect     (partial(self.Vois, 'VoisIs'))
        self.btnZ.clicked.connect       (partial(self.reWriteDif, 'Z'))
        self.btng.clicked.connect       (partial(self.reWriteDif, 'G'))
        self.btnG.clicked.connect       (partial(self.reWriteDif, 'e'))
        self.btnY.clicked.connect       (partial(self.reWriteDif, 'm'))
        self.btnR.clicked.connect       (partial(self.reWriteDif, 'd'))
        self.btnS.clicked.connect       (partial(self.reWriteDif, 'l'))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.mytimer = MyTimer()     # Создаем экземпляр класса
        self.mytimer.started.connect    (self.TimerStarted)
        self.mytimer.finished.connect   (self.TimerFinished)
        self.mytimer.mysignal.connect (self.OfTimer, QtCore.Qt.QueuedConnection)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.myI = MyInfinity()     # Создаем экземпляр класса
        self.myI.started.connect        (self.TimerIStarted)
        self.myI.finished.connect       (self.TimerIFinished)
        self.myI.mysignal.connect      (self.OfITimer, QtCore.Qt.QueuedConnection)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.messageOk = messageOk()
        self.messageNo = messageNo()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.rdMix.clicked.connect      (self.readSet)
        self.rdOrder.clicked.connect    (self.readSet)
        self.chVNo.clicked.connect     (self.backFocusWrite)
        self.chVYes.clicked.connect    (self.backFocusWrite)
        self.che.clicked.connect        (self.readSet)
        self.chm.clicked.connect        (self.readSet)
        self.chd.clicked.connect        (self.readSet)
        self.chl.clicked.connect        (self.readSet)
        self.chi.clicked.connect        (self.readSet)
        self.chp.clicked.connect        (self.readSet)
        self.chw.clicked.connect        (self.readSet)
        self.chNLetter.clicked.connect (self.readSet) 
        self.chTimer.clicked.connect    (partial(self.Infinity, 'auto'))
        self.nFile      =0  # если больше 1, то перезапись файла при выходе
        self.curSp     =[] # список выбранных записей
        #self.curPhrase=[] # список фраз 
        self.curStr     =[] # выбранная запись
        self.nStr       =0  # номер выбранной строки в списке выбранных записей
        self.nn         =1  # номер нажатия кнопки старт (чет-нечет)
        self.spCurStr =[] # список всех записей
        self.spPhrase=[]    # список фраз (выбранного файла)
        self.arrPicthis=[]
        self.arrPicAWP=[]
        self.arrPicNumer=[]
        self.curFile    ='' # имя файла, который выбрали
        self.spPayan=[] # список слогов
        self.frame.show()
        self.frame_2.hide()
        if self.user=='chin':
            self.pathFile=self.path+'/'+self.user
        elif self.user=='User':
            self.pathFile=r"C:\Users\Home\Dropbox\reanth\piter"
        self.spTexts=os.listdir(path=self.pathFile+"/texts")# список файлов
        self.spTexts.append('payan.txt')
        self.tabTexts.cellClicked.connect           (self.ofTabText)
        self.labPic.show() # начальная картинка и текст
        self.pixmap = QPixmap(self.path+'/res/mainpic.png')
        self.labPic.setPixmap(self.pixmap.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
        self.edSel.setText('เลือกไฟล์เพื่อศึกษา')
        self.mode='' 
        self.dVois={'W': 'res/tr_stop.wav', 'E': 'res/n_event.wav', 'VoisTh': 'res/VoisTh/', 'VoisIs':'res/VoisIs/'}
        self.fsud=['ห', 'ไ', 'ใ', 'โ', 'เ', 'แ', 'ะ', 'อ', 'ำ', 'ั', '้', '่', '๊', '๋', '์', 'ิ', 'ี', 'ื', 'ึ', 'ั', 'ุ', 'ู']
        self.forv=['ไ', 'ใ', 'โ', 'เ', 'แ']
        self.sek=['ะ', 'อ', 'ำ', 'ั', '้', '่', '๊', '๋', '์', 'ิ', 'ี', 'ื', 'ึ', 'ั', 'ุ', 'ู']
        #self.upp=['ั', '้', '่', '๊', '๋', '์', 'ิ', 'ี', 'ื', 'ึ', 'ั']
        #self.dov=['ุ', 'ู']
        self.ledTh.returnPressed.connect(self.batStart)
        self.leNLetter.editingFinished.connect (self.readSet)
        self.ledTh.textChanged.connect  (self.EnterText)
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.Shou)
        self.quitSc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quitSc.activated.connect(self.Shou)
        self.quitSc = QShortcut(QKeySequence('Ctrl+T'), self)
        self.quitSc.activated.connect(partial(self.Vois, 'VoisTh'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+I'), self) 
        self.quitSc.activated.connect(partial(self.Vois, 'VoisIs'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+E'), self)
        self.quitSc.activated.connect(partial(self.reWriteDif, 'e'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+M'), self)
        self.quitSc.activated.connect(partial(self.reWriteDif, 'm'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+D'), self)
        self.quitSc.activated.connect(partial(self.reWriteDif, 'd'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+L'), self)
        self.quitSc.activated.connect(partial(self.reWriteDif, 'l'))
        self.quitSc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.quitSc.activated.connect(self.btnreWrite)
        self.quitSc = QShortcut(QKeySequence('Ctrl+N'), self)
        self.quitSc.activated.connect(self.btnnewStr)
        self.quitSc = QShortcut(QKeySequence('Ctrl+R'), self)
        self.quitSc.activated.connect(self.Restart)
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(self.ExitPr)
        
        self.tabTexts.cellActivated.connect (self.KeyBoard) 
        self.tabTexts.setFocus()
        self.TabFile()     
    def KeyBoard(self, row, column): 
        curFile=str(self.tabTexts.currentItem().text())
        self.ofTabText(row, column)
        self.Infinity('hand')
    def Restart(self): 
        if self.nFile > 0:              # перезапись файла при выходе
            try:
                old_file = os.path.join(self.pathFile+'/texts/', self.curFile)
                new_file = os.path.join(self.pathFile+'/old/', \
                    self.curFile.split('.')[0]+'_'+str(datanowtime)+'.txt')
                os.rename(old_file, new_file)
            except:
                print('no copy file')
            try:
                file = open(self.pathFile+'/texts/'+self.curFile, 'w')
                for i in self.spCurStr:
                    file.write(str(i)+'\n')
                file.close()
            except:
                print('no save file')
            self.message_Ok('rewrite file')
            time.sleep(1)
        os.execl(sys.executable, 'python3', self.path+'/AppRean.py')#, *sys.argv[1:])
    def Shou(self):                         # подсказка
        strS=str(self.curSp[self.nStr]).split(';')[0].split(' ')[0]
        self.tabMain.item(0, 0).setText(strS)
    def EnterText(self, text):              # ввод текста
        if self.nn % 2 == 0:
            curWord=str(self.curSp[self.nStr]).split(';')[0].split(' ')[0]
            kolSymv=len(text)
            spS=list(curWord)
            self.ledTh.setFont(QFont('Loma', 50))
            if text==curWord[:kolSymv]:
                self.ledTh.setText(text)
                self.ledTh.setStyleSheet("QLineEdit { color:NAWI; background-color:white}")
                self.tabMain.item(0, 0).setText('')
                #self.lablePic('yes') #############################################################
            else:
                self.ledTh.setText(text[:-1])
                self.ledTh.setStyleSheet("QLineEdit { color:black; background-color:yellow}")
                d={str('ิ'):str('   -ิ'), str('ี'):str('   -ี'), str('ื'):str('   -ื'), str('ึ'):str('   -ึ'), str('ั'):str('   -ั'), str('็'):str('   -็'), str('์'):str('   -์'), str('่'):str('   -่'), str('้'):str('   -้'), str('๊'):str('   -๊'), str('๋'):str('   -๋'), str('ุ'):str('   -ุ'), str('ู'):str('   -ู')}
                if str(spS[int(kolSymv)-1]) in d:
                    self.tabMain.item(0, 0).setText(str(d[spS[int(kolSymv)-1]]))
                else:
                    self.tabMain.item(0, 0).setText(str(spS[int(kolSymv)-1]))
                if self.chVNo.isChecked():
                    self.Vois('E')#############################################################
                #self.lablePic('no') #############################################################
        print('ช '+str(text)+' '+str(curWord))
        if text==curWord:# and self.nn % 2 == 0: # нажатие кнопки старт(2 уровень)
            self.batStart()
            self.ledTh.setText('')
                #self.lablePic('ok') ############################################## 
            if self.chVYes.isChecked():
                self.Vois('W')
    def Infinity(self, v):
        if not self.chTimer.isChecked() and v=='hand':
            self.batStart()
        if v=='auto':
            self.btnStart.setStyleSheet("QPushButton { color:black; background-color:yellow}")
            if self.curFile=='':
                self.message_No('no have file')
                self.mytimer.start()
                self.chTimer.setChecked(False)
            else:
                kolSek=5 if self.spbTimer.value()==0 else int(self.spbTimer.value()) 
                if self.chTimer.isChecked():
                    self.myI.timeI=kolSek
                    self.myI.start()
                if not self.chTimer.isChecked():
                    self.myI.runningI = False
    def message_Ok(self, txt):
        self.messageOk.labOk.setText(txt)
        self.messageOk.show()
    def message_No(self, txt):
        self.messageNo.labNo.setText(txt)
        self.messageNo.show()
    def TimerStarted(self): 
        print('start') 
    def TimerFinished(self):
        self.messageOk.hide()
        self.messageNo.hide()
    def OfTimer(self, count):
        print(count)
    def TimerIStarted(self):
        self.mode='auto'
    def TimerIFinished(self):
        self.btnStart.setStyleSheet("QPushButton { color:white; background-color:green}")
        self.mode='hand'
    def OfITimer(self, count):
        self.myI.timeI=self.spbTimer.value()
        self.batStart()
    def backFocusWrite(self): # возвратить фокус на ввод текста
        self.ledTh.setFocus()
    def btnnewStr(self):                # новая запись 
        self.tabMain.setCurrentCell(3, 0)
        if self.curFile=='':
            self.message_No('no have file')
            self.mytimer.start()
        else:
            strNewTh=self.tabMain.item(0, 0).text()
            strNewIs=self.tabMain.item(2, 0).text()
            strNewRu=self.tabMain.item(1, 0).text()
            strNewEx=str(self.edSel.toPlainText()).replace('\n', 'ZZZ')
            strNew=str(strNewTh)+';'+str(strNewIs)+';'+str(strNewRu)+';'+str(strNewEx)+';lw'
            self.curSp.append(strNew)
            self.spCurStr.append(strNew)
            self.nFile +=1                  # перезапись файла при выходе
            self.tabMain.clearSelection()
            self.btnStart.setFocus()
            self.message_Ok('new note add in arrey')
            self.mytimer.start()
            self.readSet()
    def reWriteDif(self, v):            # перезапись сложности
        self.nFile += 1             # перезапись файла при выходе
        curDif=self.curStr.split(';')[-1]
        strSet=curDif.replace('e', '').replace('m', '').replace('d', '').replace('l', '')
        newStr=self.curStr.replace(curDif, '')+v+strSet
        nCur=-1
        for i in self.spCurStr:
            nCur += 1
            if str(i) == self.curStr:
                self.spCurStr[nCur]=newStr
                break
        nn=-1
        for i in self.curSp:
            nn += 1
            if str(i) == self.curStr:
                self.curSp.pop(nn)
                break
        self.edDif.setText(v+strSet)
        self.nn = 0 if self.nn==0 else 1
        self.message_Ok('rewrite rating')
        self.mytimer.start()
        self.edKolSel.setText(str(len(self.curSp)))
    def btnreWrite(self):               # перезапись записи
        self.tabMain.setCurrentCell(3, 0)
        if self.curStr != []:
            nCur=-1 # номер выбранной строки в общем списке
            for i in self.spCurStr:
                nCur += 1
                if str(i) == self.curStr:
                    break
            # строка замены записи  strNew
            strNewTh=self.tabMain.item(0, 0).text()
            strNewIs=self.tabMain.item(2, 0).text()
            strNewRu=self.tabMain.item(1, 0).text()
            strNewEx=str(self.edSel.toPlainText()).replace('\n', 'ZZZ')
            strNew=str(strNewTh)+';'+str(strNewIs)+';'+str(strNewRu)+';'+str(strNewEx)+';lw'
            self.curSp[self.nStr-1]=strNew  # замена записи в self.curSp
            self.spCurStr[nCur]=strNew        # замена записи в self.spCurStr
            self.nFile +=1                  # перезапись файла при выходе
            self.tabMain.clearSelection()
            self.message_Ok('rewrite note')
            self.mytimer.start()
            self.btnStart.setFocus()
            #self.batStart()
    def Vois(self, v):                  # звук
        strV=''
        #print(' '+str(v)+' '+str())
        try:
            if v=='W' or v=='E':
                strV=str(self.dVois[v])
            elif v=='VoisTh':
                bb=str(self.curStr.split(';')[0].split(' ')[0]+'.mp3').replace('\x0c', '')
                strV=str(self.dVois[v])+str(bb)
                #strV=str(self.dVois[v])+str(self.curStr.split(';')[0].split(' ')[0])+'.mp3'
            elif v=='VoisIs':
                strV=str(self.dVois[v])+str(self.curStr.split(';')[2].split(' ')[0])+'.mp3'
            if strV != '':
                devnull = open(os.devnull, 'w')
                subprocess.call(["mplayer",str(strV)],stdout=devnull,stderr=devnull)
                devnull.close()
        except:
            pass
    def lablePic(self, pic, scale):            # картинка
        self.labPic.show()
        #print(' '+str(pic)+' '+str())
        #if str(pic+'.jpg') in self.arrPicAWP:
            #self.pixmap = QPixmap(self.path+'/res/picAWP/'+pic+'.jpg')
            #self.labPic.setPixmap(self.pixmap.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
        if str(pic+'.png') in self.arrPicthis:
            self.pixmap = QPixmap(self.path+'/res/picthis/'+pic+'.png')
            self.labPic.setPixmap(self.pixmap.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
        elif str(pic+'.jpg') in self.arrPicNumer:
            if scale=='scale':
                picture = QPixmap(self.path+'/res/picNumer/'+pic+'.jpg').copy(60, 860, 600, 500)
                self.labPic.setPixmap(picture.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
            else:
                self.pixmap = QPixmap(self.path+'/res/picNumer/'+pic+'.jpg')
                ##pixmap4 = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
                #self.labPic.setPixmap(self.pixmap.scaled(1000, 1000, QtCore.Qt.KeepAspectRatio))
                self.labPic.setPixmap(self.pixmap.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
    def readSet(self):                  # записи из файла по спискам
        # выбор по числу букв или обычный режим
        if self.chNLetter.isChecked():
            self.curSp      =[]
            self.leNStr.setText('')
            self.edKolSel.setText('')
            nnL=self.leNLetter.text()
            spNoDif=['d', 'z', 'p', 'i']
            for i in self.spCurStr:
                strDif=i.split(';')[-1]
                lenLet=len(str(i).split(';')[0].split(' ')[0])
                if not strDif in spNoDif and int(lenLet) <=  int(nnL) and int(lenLet) != 0:
                    self.curSp.append(i)
            if self.rdMix.isChecked():
                random.shuffle(self.curSp)
            self.leNStr.setText(str(len(self.curSp)))
            self.edKolSel.setText(str(len(self.curSp)))
        else:
            self.modeReadSet()
    def modeReadSet(self):
        self.curSp      =[]
        #self.spPhrase =[]
        strD=''
        strI=''
        strD+='e' if self.che.isChecked()    else ''
        strD+='m' if self.chm.isChecked()    else ''
        strD+='d' if self.chd.isChecked()    else ''
        strD+='l' if self.chl.isChecked()    else ''
        #strI+='w' if self.chw.isChecked()    else ''
        strI+='p' if self.chp.isChecked()    else ''
        strI+='i' if self.chi.isChecked()    else ''
        ne=0 ; nm=0 ; nd=0 ; nl=0; ng=0 ; nz=0; # для количества
        spD =[]
        for i in self.spCurStr:
            strDif=i.split(';')[-1]
            if 'e' in strDif: ne += 1;     # хорошо
            if 'm' in strDif: nm += 1;   # средне
            if 'd' in strDif: nd += 1;     # тяжело
            if 'l' in strDif: nl += 1;       # учить
            if 'g' in strDif: ng += 1;     # идеально, не повторять
            if 'z' in strDif: nz += 1;     # не уверен в правильности
            for j in strDif:
                if not i in self.curSp:
                    if strI=='' and j in strD:
                        self.curSp.append(i)
                    elif j in strD and strI!='':
                        spD.append(i)
            #if 'p' in i:
                #self.spPhrase.append(i)
        # isan phrase
        if spD!=[]:
            for i in spD: 
                strDif=i.split(';')[-1]
                for j in strI:
                    if  not i in self.curSp:
                        if j=='i' and i.split(';')[2]:
                            self.curSp.append(i)
                        if j=='p' and 'p' in strDif:
                            self.curSp.append(i)
                            #else:
                                #not 'p' in strDif and not i in self.curSp:
                                #self.curSp.append(i)
        if self.rdMix.isChecked():
            random.shuffle(self.curSp)
        #######################################
        else:                           #self.rdOrder.isChecked():
            self.curSp.reverse()
        ######################################
        self.edKolSel.setText(str(len(self.curSp)))
        self.edKolG.setText(str(ne))
        self.edKolY.setText(str(nm))
        self.edKolR.setText(str(nd))
        self.edKolS.setText(str(nl))
        self.edKolg.setText(str(ng))
        self.edKolZ.setText(str(nz))
    def ofTabText(self, row, column):   # выбор файла
        self.spCurStr =[]
        self.spPhrase=[]
        self.nStr       =0
        self.tabMain.clear()
        if self.tabTexts.item(row, column):
            self.curFile = self.tabTexts.item(row, column).text()+'.txt'
            print(' '+str(self.curFile)+' '+str())
            for i in open('/home/chin/Dropbox/REAN/reanth/payan.txt').readlines(): # список слогов
                self.spPayan.append(i.strip())
            if self.curFile=='payan.txt':
                for i in open('/home/chin/Dropbox/REAN/reanth/payan.txt').readlines():
                    self.spCurStr.append(i.strip())
            else:
                for i in open(self.pathFile+'/texts/'+self.curFile).readlines():
                    self.spCurStr.append(i.strip())
            if self.curFile != 'payan.txt':
                for i in open(self.pathFile+'/texts/'+self.curFile.replace('W', 'P')).readlines():
                    self.spPhrase.append(i.strip())
        self.edKolA.setText(str(len(self.spCurStr)))
        self.edSel.setText('ไฟล์ที่เลือก - '+self.curFile)
        # обложка файла
        self.labPic.show()
        self.pixmap = QPixmap(self.path+'/res/'+self.curFile.split('.')[0]+'.png')
        self.labPic.setPixmap(self.pixmap.scaled(self.labPic.size(), QtCore.Qt.KeepAspectRatio))
        self.readSet()
    def TabFile(self):                  # таблица выбора файла и перезапись файла
        if self.nFile > 0:              # перезапись файла
            try:
                file = open(self.pathFile+'/texts/'+self.curFile, 'w')
                for i in self.spCurStr:
                    file.write(str(i)+'\n')
                file.close()
            except:
                print('no save file')
            self.message_Ok('rewrite file')
            self.mytimer.start()
            time.sleep(1)
        self.nFile=0
        # таблица файлов
        self.tabTexts.clear()
        self.tabTexts.setColumnCount(1)
        self.tabTexts.setRowCount(6)
        self.tabTexts.horizontalHeader().hide()
        self.tabTexts.verticalHeader().hide()
        self.spTexts.sort()##############################
        for row in range(len(self.spTexts)):
            item = QtWidgets.QTableWidgetItem(self.spTexts[row].replace('.txt', ''))
            self.tabTexts.setItem(row,0,QTableWidgetItem(item))
        self.tabTexts.selectRow(0)
        self.arrVis =os.listdir('res/VoisIs/')
        self.arrVth =os.listdir('/home/chin/Dropbox/REAN/reanth/res/VoisTh')
        self.arrPicthis=[str(i) for i in os.listdir('/home/chin/Dropbox/REAN/reanth/res/picthis') if '.png' in str(i)]
        self.arrPicAWP=[str(i) for i in os.listdir('/home/chin/Dropbox/REAN/reanth/res/picAWP') if '.jpg' in str(i)]
        self.arrPicNumer=[str(i) for i in os.listdir('/home/chin/Dropbox/REAN/reanth/res/picNumer') if '.jpg' in str(i)]
        #self.arrVth =[i.replace(' ', '').replace('.mp3', '') for i in os.listdir('res/VoisTh/')]
        #print(' '+str(self.arrVth)+' '+str())
    def ExitPr(self):                   # перезапись файла и выход
        if self.nFile > 0:              # перезапись файла при выходе
            try:
                old_file = os.path.join(self.pathFile+'/texts/', self.curFile)
                new_file = os.path.join(self.pathFile+'/old/', \
                    self.curFile.split('.')[0]+'_'+str(datanowtime)+'.txt')
                os.rename(old_file, new_file)
            except:
                print('no copy file')
            try:
                file = open(self.pathFile+'/texts/'+self.curFile, 'w')
                for i in self.spCurStr:
                    file.write(str(i)+'\n')
                file.close()
            except:
                print('no save file')
            self.message_Ok('rewrite file')
            time.sleep(1)
        # telegramBot /home/chin/Dropbox/REAN/reanth/chin/teleg.txt
        #file = open(self.pathFile+'/teleg.txt', 'w')
        #for ff in open(self.pathFile+'/texts/gramW.txt').readlines():
            #if 'l' in ff.split(';')[-1]:
                #strF=ff.split(';')[0]+';'+ff.split(';')[1]+'\n'
                #file.write(str(strF))
        #file.close()
        #time.sleep(1)
        sys.exit()
    def batStart(self):                 # кнопка старт 
        self.ledTh.setFocus()
        self.tabMain.clearSelection()
        if self.spCurStr==[]:
            self.message_No('no have file')
            self.mytimer.start()
        elif self.curSp != []:
            self.labPic.hide()
            kolStr=len(self.curSp)
            self.curStr=self.curSp[self.nStr]
            self.edDif.setText(self.curStr.split(';')[-1])
            # vois
            strT0=self.curStr.split(';')[0].split(' ')[0]+'.mp3'
            strT=strT0.replace('\x0c', '')
            strI=self.curStr.split(';')[2].split(' ')[0]+'.mp3'
            if strT in self.arrVth:# если есть тай.звук и проверка автомата звука
                if self.chVAuto.isChecked() and self.nn % 2 != 0:
                    self.Vois('VoisTh')
                self.btnVTh.setStyleSheet("QPushButton { color:white; background-color:NAVY}")
            else:
                self.btnVTh.setStyleSheet("QPushButton { color:default; background-color:default}")
            if strI in self.arrVis:
                self.btnVIs.setStyleSheet("QPushButton { color:white; background-color:NAVY}")
            else:
                self.btnVIs.setStyleSheet("QPushButton { color:default; background-color:default}")
            payan =''
            for i in self.spPayan: # список слогов
                wTh=self.curStr.split(';')[0].split(' ')[0]
                pay=i.split(';')[0]
                if wTh!='' and pay in wTh and pay != wTh:
                    # вывод если до или после нет (сара)self.fsud
                    fw=str(wTh.split(str(pay))[0])[-1] if wTh.split(str(pay))[0] else ''
                    sw=str(wTh.split(str(pay))[1])[0] if wTh.split(str(pay))[1] else ''
                    if fw in self.forv or sw in self.sek:
                        pass
                    else:
                        payan += pay+'-'+i.split(';')[1]+'\n'
                    if pay[-1]=='อ' and sw=='อ':
                        payan += pay+'-'+i.split(';')[1]+'\n'
            phrase=''
            for i in self.spPhrase:
                wTh=self.curStr.split(';')[0].split(' ')[0]
                wIs=self.curStr.split(';')[2].split(' ')[0]
                if wTh!='' and wTh in i and self.curStr.split(';')[0] != i.split(';')[0]:
                    phrase += str(i.split(';')[0])+'-'+str(i.split(';')[1])+'\n'
                if wIs!='' and wIs in i and self.curStr.split(';')[2] != i.split(';')[2]:
                    phrase += str(i.split(';')[2])+'-'+str(i.split(';')[1])+'\n'
            self.tabMain.setColumnCount(1)
            self.tabMain.setRowCount(4)
            self.tabMain.verticalHeader().hide()
            self.tabMain.horizontalHeader().hide()
            if self.nn % 2 != 0:                    # первое нажатие
                self.btnStart.setText('1\nการแปล')
                itemStr=['','',str(self.curStr.split(';')[1]),' ']
                self.btnReWrite.setEnabled(False)
            else:                                   # второе нажатие
                self.btnStart.setText('2\nคำต่อไป')
                #print(' '+str(self.curStr)+' '+str())
                itemStr=[str(self.curStr.split(';')[0]), str(self.curStr.split(';')[2]), str(self.curStr.split(';')[1]), str(payan)+phrase]
                self.ledTh.setText('')
                self.btnReWrite.setEnabled(True)
            for row in range(4):
                self.tabMain.setItem(row-1,1,QTableWidgetItem(itemStr[row]))
            self.tabMain.item(0, 0).setFont(QFont('Loma', 50))
            self.tabMain.item(1, 0).setFont(QFont('Loma', 30))
            self.tabMain.item(2, 0).setFont(QFont('Loma', 40))
            self.tabMain.item(3, 0).setFont(QFont('Loma', 30))
            self.tabMain.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.tabMain.resizeRowsToContents()
            # подсчет строк для зацикливания
            if self.nn % 2 == 0:
                self.nStr+=1 
                #self.edKolSel.setText(str(self.curSp.index(self.curStr))+' / '+str(kolStr))
                if self.nStr == kolStr: # -1
                    self.nStr = 0
                #ручное освобождение памяти
                if self.nStr == 5:
                    gc.collect()
            else:
                self.edKolSel.setText(str(self.curSp.index(self.curStr)+1)+' / '+str(kolStr))
            # вывод в дополнительное поле
            self.edSel.setText(str(self.curStr.split(';')[3]).replace('ZZZ', '\n'))
            self.nn+=1
            # вывод картинки если есть 
            pic=str(self.curStr.split(';')[0]).split(' ')[0].split('_')[0] 
            picNum=str(self.curStr.split(';')[3]).split('.')[0]
            if str(pic+'.png') in self.arrPicthis:
                self.lablePic(str(pic), 'size')
            #elif str(pic+'.jpg') in self.arrPicAWP:
                #self.lablePic(str(pic))
            elif str(picNum+'.jpg') in self.arrPicNumer:
                self.lablePic(str(picNum), 'size')
        else:
            self.message_No('list empty')
            self.mytimer.start()
    def ScalePic(self):
        pic=str(self.curStr.split(';')[0]).split(' ')[0].split('_')[0] 
        picNum=str(self.curStr.split(';')[3]).split('.')[0]
        if str(pic+'.png') in self.arrPicthis:
            self.lablePic(str(pic), 'scale')
        elif str(picNum+'.jpg') in self.arrPicNumer:
            self.lablePic(str(picNum), 'scale')
def main(): 
    app = QtWidgets.QApplication(sys.argv)  #Создаём объект application
    window = ReanApp()
    window.setWindowTitle('เรียน')
    ico=QtGui.QIcon('./res/mainpic.png')
    window.setWindowIcon(ico)
    window.show()
    app.exec_()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
