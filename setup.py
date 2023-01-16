from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication, QFileDialog)
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtCore import QCoreApplication, Qt

import subprocess
import re


Form, _ = uic.loadUiType("untitled.ui") 

class Ui(QtWidgets.QMainWindow,Form):
      def __init__(self):
         super(Ui,self).__init__()
         self.setupUi(self)
         
         self.pushButton.clicked.connect(self.compile)
         self.pushButton_2.clicked.connect(self.shild)
         self.pushButton_3.clicked.connect(self.browse)
         self.pushButton_4.clicked.connect(self.browse2)
         self.pushButton_5.clicked.connect(self.browse3)
         self.pushButton_6.clicked.connect(self.all)
         self.label_6.setAlignment(Qt.AlignCenter)
         self.label_7.setAlignment(Qt.AlignCenter)
         self.label_8.setAlignment(Qt.AlignCenter)

         self.pushButton_3.setToolTip('Выбрать файл с расширением "hex"')
         self.pushButton_4.setToolTip('Выбрать файл с расширением "C"')
         self.pushButton_5.setToolTip('Выбрать файл с расширением "C"')

         lists = 'attiny10,attiny11,attiny12,attiny13,attiny15,attiny1634,attiny20,attiny2313,attiny24,attiny25,attiny26,attiny261,attiny4,attiny40,attiny4313,attiny43u,attiny44,attiny45,attiny461,attiny5,attiny84,attiny85,attiny861,attiny88,attiny9,atmega103,atmega128,atmega1280,atmega1281,atmega1284P,atmega1284RFR2,atmega128RFA1,atmega128RFR2,atmega16,atmega161,atmega162,atmega163,atmega164P,atmega168,atmega168P,atmega169,atmega16U2,atmega2560,atmega2561,atmega2564RFR2,atmega256RFR2,atmega32,atmega324P,atmega324PA,atmega325,atmega3250,atmega328,atmega328P,atmega329,atmega3290,atmega3290P,atmega329P,atmega32U2,atmega32U4,atmega406,atmega48,atmega48P,atmega64,atmega640,atmega644,atmega644P,atmega644rfr2,atmega645,atmega6450,atmega649,atmega6490,atmega64rfr2,atmega8,atmega8515,atmega8535,atmega88,atmega88p,atmega8u2'
         lists = lists.split(',')
         for line in lists:
             self.comboBox_2.addItem(line.strip()) 
             self.comboBox_3.addItem(line.strip()) 
             self.comboBox_5.addItem(line.strip()) 

         lists2 ='usbasp,usbtiny,xil,arduino,abcmini,alf,atisp,avr109,avr910,avr911,avrftdi,avrisp,avrisp2,avrispmkII, avrispv2,bascom,blaster,bsd,butterfly,c2n232i,dapa,dasa,dasa3,dragon_dw,dragon_hvsp,dragon_isp,dragon_jtag,dragon_pp,dt006 ere-isp-avr,frank-stk200,futurlec,jtag1,jtag1slow,jtag2slow,jtag2,jtag2fast,jtag2isp,jtag2dw,jtagmkI,jtagmkII,mib510,pavr, picoweb,pony-stk200,ponyser,siprog,sp12,stk200,stk500,stk500hvsp,stk500pp,stk500v1,stk500v2,stk600,stk600hvsp,stk600pp'
         lists2 = lists2.split(',')
         for line in lists2:
             self.comboBox.addItem(line.strip())
             self.comboBox_4.addItem(line.strip()) 


      #ФУНКЦИЯ ДЛЯ ОПОВЕЩЕНИЯ ОБ ОШИБКЕ
      def error(self,cod_error):
          if cod_error==300: message = 'Прошивание прервано из-за ошибки'
          if cod_error==250: message = 'Компиляция прервана из-за ошибки'
          if cod_error==150: message = 'Файл не выбран'
          #Диалоговое окно
          msg = QMessageBox()
          msg.setWindowTitle("ОШИБКА!")     #Заголовок
          msg.setText(message)              #Текст
          msg.setIcon(QMessageBox.Critical) #Иконка
          msg.exec_()

       
      #ФУНКЦИЯ ДЛЯ ОПОВЕЩЕНИЯ
      def dialog(self,cod_dialog):
          if cod_dialog == 120: message = 'Компиляция прошла успешно!'
          if cod_dialog == 500: message = 'Прошивка успешно завершена!'
          #Диалоговое окно
          msg = QMessageBox()
          msg.setWindowTitle("СООБЩЕНИЕ")     #Заголовок
          msg.setText(message)                #Текст
          msg.setIcon(QMessageBox.Information)#Иконка
          msg.exec_()


      #ФУНКЦИЯ КОМПИЛЯЦИИ
      def compile(self):
          name_file  = self.lineEdit.text() 
          if len(name_file)==0:
             self.error(150)
             return         
          controller = self.comboBox_2.currentText()
          name_file2 = re.sub(r'c', 'o', name_file) 
          cmd = "avr-gcc -mmcu="+controller+" -I. -gdwarf-2 -Os -o "+name_file2+" "+name_file 
          out = subprocess.getstatusoutput('cd && '+cmd)

          if len(out[1]) == 0: result = 'Completes...'
          else: result = str(out[1])

          self.textBrowser_2.clear() 
          self.textBrowser_2.append(result)

          if len(out[1]) == 0: self.dialog(120)
          else: self.error(250)

          name_file3 = re.sub(r'o', 'hex', name_file2)
          cmd = "avr-objcopy -O ihex "+name_file2+" "+name_file3
          out = subprocess.getstatusoutput('cd && '+cmd)
          self.textBrowser_2.append(str(out[1]))
 
      #ФУНКЦИЯ ДЛЯ ПРОШИВКИ КОНТРОЛЛЕРА 
      def shild(self):
          name_file = self.lineEdit_2.text()
          if len(name_file)==0:
             self.error(150)
             return      
          get_text_0 = self.comboBox.currentText()  
          get_text_1 = self.comboBox_3.currentText() 
          result = re.search(r'ATtiny'.upper(), get_text_1.upper())
          try:
             result.group(0)
             controller = 't'+get_text_1[6:]
          except: 
                controller = 'm'+get_text_1[6:]
          cmd = "avrdude -c "+get_text_0+" -p "+controller+" -P /dev/ttyUSB0 -U flash:w:"+name_file
          out = subprocess.getstatusoutput('cd && '+cmd)
          self.textBrowser.clear() 
          self.textBrowser.append(str(out[1]))
          result  = re.search(r'Fuses OK', str(out[1]))
          if result == None: self.error(300)
          else: self.dialog(500)


      #ФУНКЦИЯ ДЛЯ ВЫБОРА ФАЙЛА С РАСШИРЕНИЕМ "hex"
      def browse(self):
          get_file = QFileDialog.getOpenFileName(self, 'Open file', '/home/user','*.hex')[0]
          get_file = get_file.split('/')      
          if len(get_file)==1: return
          count = 0                           
          for line in get_file:
              count +=1                       
              if count==4: way = line         
              if count> 4: way = way+'/'+line 
          self.lineEdit_2.clear()     
          self.lineEdit_2.setText(way)


      #ФУНКЦИЯ ДЛЯ ВЫБОРА ФАЙЛА С РАСШИРЕНИЕМ "c"
      def browse2(self):
          get_file = QFileDialog.getOpenFileName(self, 'Open file', '/home/user','*.c')[0]
          get_file = get_file.split('/')      
          if len(get_file)==1: return
          count = 0                          
          for line in get_file:
              count +=1                       
              if count==4: way = line        
              if count> 4: way = way+'/'+line 
          self.lineEdit.clear()     
          self.lineEdit.setText(way)


      #ФУНКЦИЯ ДЛЯ ВЫБОРА ФАЙЛА С РАСШИРЕНИЕМ "c"
      def browse3(self):
          get_file = QFileDialog.getOpenFileName(self, 'Open file', '/home/user','*.c')[0]
          get_file = get_file.split('/')      
          if len(get_file)==1: return
          count = 0                           
          for line in get_file:
              count +=1                       
              if count==4: way = line         
              if count> 4: way = way+'/'+line
          self.lineEdit_3.clear()     
          self.lineEdit_3.setText(way)

      #ФУНКЦИЯ ДЛЯ КОМПИЛЯЦИИ И ПРОШИВКИ КОНТРОЛЛЕРА
      def all(self):
          name_file  = self.lineEdit_3.text() 
          if len(name_file)==0:
             self.error(150)
             return         
          controller = self.comboBox_5.currentText()
          name_file2 = re.sub(r'c', 'o', name_file) 
          cmd = "avr-gcc -mmcu="+controller+" -I. -gdwarf-2 -Os -o "+name_file2+" "+name_file 
          out = subprocess.getstatusoutput('cd && '+cmd)

          if len(out[1]) == 0: result = 'Completes...'
          else: result = str(out[1])

          self.textBrowser_3.clear() 
          self.textBrowser_3.append(result)
          if len(out[1]) > 0: 
             self.error(250)
             return

          name_file3 = re.sub(r'o', 'hex', name_file2)
          cmd = "avr-objcopy -O ihex "+name_file2+" "+name_file3
          out = subprocess.getstatusoutput('cd && '+cmd)
          self.textBrowser_3.append(str(out[1]))

          name_file = name_file3
          if len(name_file)==0:
             self.error(150)
             return      
          get_text_0 = self.comboBox_4.currentText()   
          get_text_1 = self.comboBox_5.currentText() 
          result = re.search(r'ATtiny'.upper(), get_text_1.upper())
          try:
             result.group(0)
             controller = 't'+get_text_1[6:]
          except: 
                controller = 'm'+get_text_1[6:]
          cmd = "avrdude -c "+get_text_0+" -p "+controller+" -P /dev/ttyUSB0 -U flash:w:"+name_file
          out = subprocess.getstatusoutput('cd && '+cmd)
          self.textBrowser_3.append(str(out[1]))
          result  = re.search(r'Fuses OK', str(out[1]))
          if result == None: self.error(300)
          else: self.dialog(500)
          



if __name__=="__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())




