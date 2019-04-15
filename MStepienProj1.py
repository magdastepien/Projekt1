# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 00:16:00 2019

@author: Magda
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class AppWindow(QWidget):
    #Wyznaczenie podstawowych parametrów aplikacji
    def __init__(self):
        super().__init__()
        self.title='Wyznaczenie punktu przecięcia dwóch odcinków'
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,400,300)
        self.show()
    #Zdefiniowanie widgetów aplikacji    
    def initWidgets(self):
        btn=QPushButton("Rysuj",self)
        btnColor=QPushButton("Zmien kolor",self)
        btnClear=QPushButton("Wyczysć",self)
        xaLabel=QLabel("Xa",self)
        yaLabel=QLabel("Ya",self)
        xbLabel=QLabel("Xb",self)
        ybLabel=QLabel("Yb",self)
        xcLabel=QLabel("Xc",self)
        ycLabel=QLabel("Yc",self)
        xdLabel=QLabel("Xd",self)
        ydLabel=QLabel("Yd",self)
        Xp1Label=QLabel("Xp",self)
        Yp1Label=QLabel("Yp",self)
        
        self.xaEdit=QLineEdit()
        self.yaEdit=QLineEdit()
        self.xbEdit=QLineEdit()
        self.ybEdit=QLineEdit()
        self.xcEdit=QLineEdit()
        self.ycEdit=QLineEdit()
        self.xdEdit=QLineEdit()
        self.ydEdit=QLineEdit()
        self.Xp1Edit=QLineEdit()
        self.Yp1Edit=QLineEdit()
        
        
        self.resultLabel=QLabel(" ",self)
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
    
        
        grid=QGridLayout()
        grid.addWidget(xaLabel, 1, 0)
        grid.addWidget(self.xaEdit ,1,1)
        grid.addWidget(yaLabel,1,2)
        grid.addWidget(self.yaEdit,1,3)
        
        grid.addWidget(xbLabel, 2, 0)
        grid.addWidget(self.xbEdit ,2,1)
        grid.addWidget(ybLabel,2,2)
        grid.addWidget(self.ybEdit,2,3)
        
        grid.addWidget(xcLabel, 3, 0)
        grid.addWidget(self.xcEdit ,3,1)
        grid.addWidget(ycLabel,3,2)
        grid.addWidget(self.ycEdit,3,3)
        
        grid.addWidget(xdLabel, 4,0)
        grid.addWidget(self.xdEdit ,4,1)
        grid.addWidget(ydLabel,4,2)
        grid.addWidget(self.ydEdit,4,3)
        
        grid.addWidget(btn,26,0,1,2)
        grid.addWidget(btnColor,26,3,1,2)
        grid.addWidget(self.resultLabel,27,0,1,2)
        grid.addWidget(self.canvas,5,0,20,10)
    
        grid.addWidget(Xp1Label, 28, 0)
        grid.addWidget(self.Xp1Edit, 28, 1)
        grid.addWidget(Yp1Label, 28, 2)
        grid.addWidget(self.Yp1Edit, 28, 3)
        
        grid.addWidget(btnClear,29,0,1,2)
        
        self.setLayout(grid)
        
        btn.clicked.connect(self.oblicz)
        btnColor.clicked.connect(self.zmienKolor)
        btnClear.clicked.connect(self.czysc)
        
    #Zdefiniowanie funkcji czyszczącej pola    
    def czysc(self):
        self.xaEdit.clear()
        self.yaEdit.clear()
        self.xbEdit.clear()
        self.ybEdit.clear()
        self.xcEdit.clear()
        self.ycEdit.clear()
        self.xdEdit.clear()
        self.ydEdit.clear()
        self.Xp1Edit.clear()
        self.Yp1Edit.clear()
        self.resultLabel.clear()
    
    #Definiowanie koloru wykresów
    def zmienKolor(self):
        color=QColorDialog.getColor()
        if color.isValid():                    #sprawdza czy kolor jest własciwy
            self.rysuj(col=color.name())
        
    def oblicz(self):
        self.rysuj()
    
    #Rysuje wykres
    def rysuj(self, col='r'):
        #sprawdzenie, czy wartosci są liczbami
        xa=self.sprawdzWartosc(self.xaEdit)
        ya=self.sprawdzWartosc(self.yaEdit)
        xb=self.sprawdzWartosc(self.xbEdit)
        yb=self.sprawdzWartosc(self.ybEdit)
        xc=self.sprawdzWartosc(self.xcEdit)
        yc=self.sprawdzWartosc(self.ycEdit)
        xd=self.sprawdzWartosc(self.xdEdit)
        yd=self.sprawdzWartosc(self.ydEdit)
        #dla liczb obliczenie przyrostów
        if (xa is not None) and (ya is not None) and  (xb is not None) and (yb is not None) and  (xc is not None) and (yc is not None) and  (xb is not None) and (yb is not None):      #można sprawdzać od razu cała liste if None not in [x,y]
            self.figure.clear()
            ax=self.figure.add_subplot(111)
            ax.plot(xa,ya,xb,yb,xc,yc,xd,yd, color=col,marker='o')
            self.canvas.draw()    #odswiezenie wykresu
            
            deltaXac = xc - xa
            deltaYcd = yd - yc
            deltaYac = yc - ya
            deltaXcd = xd - xc
            deltaXab = xb - xa
            deltaYab = yb - ya
            
            #warunek dla prostych, które są równoległe
            if ((deltaXab*deltaYcd-deltaYab*deltaXcd))==0:
                self.resultLabel.setText("Proste są równoległe")
                
                X =[xa, xb, xc, xd]
                Y=[ya, yb, yc, yd]
                
                ax = self.figure.add_subplot(111)
                ax.scatter(X,Y)
                ax.plot([xa,xb],[ya,yb], color=col)
                ax.plot([xc,xd],[yc,yd], color=col)
                self.canvas.draw()
            #obliczenie współrzędnych przecięcia prostych w przypadku, gdy nie są one równoległe    
            else:
                t1 = (deltaXac * deltaYcd - deltaYac * deltaXcd)/(deltaXab * deltaYcd - deltaYab * deltaXcd)
                t2 = (deltaXac * deltaYab - deltaYac * deltaXab)/(deltaXab * deltaYcd - deltaYab * deltaXcd)
                Xp1 = xa + t1 * deltaXab
                Yp1 = ya + t1 * deltaYab
                
                print(round(Xp1,3),round(Yp1,3))
                self.Xp1Edit.setText(str(Xp1))
                self.Yp1Edit.setText(str(Yp1))
                
                ax = self.figure.add_subplot(111)
                ax.plot([xa,xb],[ya,yb], color = col)
                ax.plot([xc,xd],[yc,yd], color = col)
                
                ax.plot(Xp1,Yp1, color = col, marker = 'o')
                self.canvas.draw()
                #sprawdzenie sposobu przecinania się linii
                if (0<=t1<=1) and (0<=t2<=1):
                            self.resultLabel.setText("Odcinki się przecinają")
                elif (0<=t1<=1) and ((0>t2) or (t2>1)):
                            self.resultLabel.setText("Proste się przecinają na przedłużeniu jednego odcinka")
                            ax = self.figure.add_subplot(111)
                            ax.plot([xa, Xp1],[ya, Yp1], color = col, linestyle = '--')
                            ax.plot([xc,Xp1],[yc,Yp1], color = col, linestyle = '--')
                            self.canvas.draw()
                else:
                            self.resultLabel.setText("Proste się przecinają na przedłużeniu obu odcinków")
                            ax = self.figure.add_subplot(111)
                            ax.plot([xa, Xp1],[ya, Yp1], color = col, linestyle = '--')
                            ax.plot([xc,Xp1],[yc,Yp1], color = col, linestyle = '--')
                            self.canvas.draw()
                #eksport wyniku do pliku tekstowego
                with open ('wynik.txt') as wynik:
                            wynik.write(28*'-')
                            wynik.write('\n|{:^8}|{:^8}|{:^8}|\n'.format('Punkt', 'X', 'Y'))        
                            wynik.write(28*'-')
                            wynik.write('\n|{:^8}|{:^8}|{:^8}|\n'.format('P', Xp1,Yp1))

    #funkcja sprawdzająca poprawnosc współrzędnych         
    def sprawdzWartosc(self, element):
        if element.text().lstrip('-').replace('.','',1). isdigit():
            return float(element.text())
        else:
            element.setFocus() #element staje się widoczny
            return None #nic nie zwraca 
        
    
    
def main():
    app=QApplication(sys.argv)
    window=AppWindow()
    app.exec_()
    
if __name__=='__main__':
    main()
