from SocialGraph import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from random import randint
import math

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.lst = [] #lista que salva a localização dos circulos na tela
        '''Define os 3 frames contidos no frame principal'''
        self.leftframe = Frame(master)
        self.leftframe.grid(row=0,column=0,stick=NS+E)
        self.centerframe = Frame(master)
        self.centerframe.grid(row=0,column=1,stick=NS)
        self.rightframe = Frame(master)
        self.rightframe.grid(row=0,column=50,stick=NS+W)

        '''Nomeando os 3 frames contidos no frame principal'''
        self.container1 = LabelFrame(self.centerframe, text="Escolha o arquivo", padx=5, pady=5)
        self.container2 = LabelFrame(self.centerframe, text="Entrada de dados", padx=5, pady=5)
        self.container3 = LabelFrame(self.centerframe, text="Escolha aleatória", padx=5, pady=5)

        '''Montando o frame da esquerda'''
        lblframe = LabelFrame(self.leftframe, text="Selecione entrada", padx=5, pady=5)
        lblframe.grid(row=0,column=0)
        button1 = Button(lblframe, text="Arquivo", width=20,command= lambda: self.botaoSelecionaEntrada(1))
        button1.grid(row=0,column=0)
        button2 = Button(lblframe, text="Manual",  width=20,command= lambda: self.botaoSelecionaEntrada(2))
        button2.grid(row=1,column=0)

        '''define a forma de entrada por arquivo'''
        self.container1.grid(row=0, column=0)
        buttonFile = Button(self.container1, text = 'Ler arquivo', command=self.askopenfilename)
        buttonFile.grid(row=0,column=0,sticky='N')
        self.displayManual()
    
    def botaoSelecionaEntrada(self, value):
        """
           @param[in] integer
           @example self.botaoSelecionaEntrada(1)
        """              
        self.buttonClick = value
        print ("Called"+str(value))
        self.container1.isgridded = False
        self.container1.grid_forget()
        self.container2.isgridded = False
        self.container2.grid_forget()
        self.container3.isgridded = False
        self.container3.grid_forget()
        if self.buttonClick == 1:
            self.container1.isgridded=True
            self.container1.grid(row=0,column=0)
        if self.buttonClick == 2:
            self.container2.isgridded = True
            self.container2.grid(row=0, column = 0)

    def askopenfilename(self):
        """@note Open ranking file
           @example self.askopenfilename()
        """   
        filepath = askopenfilename()
        Graph = SocialGraph(filepath)
        Graph.create()
        self.desenhaGrafo(Graph.dg)
    
    
    def desenhaGrafo(self, dg = DiGraph.DiGraph()):
        '''desenha o Grafo conforme entrada manual.'''

        '''bloco para gerar as posições de um circle e verificar se é válida, ou seja,
        se vai sobrepor algum outro circle'''
        class Circle():
            def __init__(self):
                self.x = randint(80, 420)
                self.y = randint(80,420)
                self.raio = 30
            def getX(self):
                return self.x
            def getY(self):
                return self.y
            def getRaio(self):
                return self.raio
            def dist(self, x, y):
                dist = ((self.x - x)**2 + (self.y - y)**2)**0.5
                return dist
            def __repr__(self):
                return "x= "+str(self.getX())+", y= "+str(self.getY())
        while (len(self.lst) < dg.numVertices()+1):
            circle = Circle()
            overlapping = False
            for i in  range(len(self.lst)):
                d = circle.dist(self.lst[i].getX(), self.lst[i].getY())
                if d < circle.getRaio() + self.lst[i].getRaio()+60:
                    overlapping = True
                    break
            if not overlapping:
                self.lst.append(circle)
        
        '''bloco para inserir o circle nas posições válidas'''        
        i = 0
        '''ordena a lista de posições para colocar os circulos que tem vertices
        perto do outro'''
        self.lst.sort(key=lambda Circle: (Circle.getX(), Circle.getY()))
        while i < len(dg.vertices()):  
            for value in dg.vertices():
                if value not in self.allTags():
                    self.canvas1.create_oval(self.lst[i].getX()+self.lst[i].getRaio(), 
                    self.lst[i].getY()-self.lst[i].getRaio(), 
                    self.lst[i].getX()-self.lst[i].getRaio(), 
                    self.lst[i].getY()+self.lst[i].getRaio(),
                                fill="#FFD2A5", tag = value)
                    self.canvas1.create_text(self.lst[i].getX(), self.lst[i].getY(), text = value)
                    i +=1
                    for v in dg.adjacentTo(value):
                        if v.getVertex() not in self.allTags():
                            self.canvas1.create_oval(self.lst[i].getX()+self.lst[i].getRaio(), 
                            self.lst[i].getY()-self.lst[i].getRaio(), 
                            self.lst[i].getX()-self.lst[i].getRaio(), 
                            self.lst[i].getY()+self.lst[i].getRaio(),
                                        fill="#FFD2A5", tag = v.getVertex())
                            self.canvas1.create_text(self.lst[i].getX(), self.lst[i].getY(), text = v.getVertex())
                            i +=1
                    #self.canvas1.itemconfigure('Liam', fill="white")
            
        '''bloco para inserir as arestas''' 
        for value in dg.vertices():
            for edge in dg.adjacentTo(value):
                coord1 = self.canvas1.coords(value)
                coord2 =  self.canvas1.coords(edge.getVertex())
                x, y = ((coord1[0]+coord1[2])/2), ((coord1[1]+coord1[3])/2)
                a, b = ((coord2[0]+coord2[2])/2),  ((coord2[1]+coord2[3])/2)
                
                intC1L = self.calculaInterseccao(x, y, a, b)
                intC2L = self.calculaInterseccao(a, b, x, y)
                x1, y1 = intC1L[2], intC1L[3]
                x2, y2 = intC2L[2], intC2L[3]
                valueTag =  edge.getVertex()+str(edge.getCost())
                self.canvas1.create_line(x2,y2,x1, y1, tag=valueTag, arrow=FIRST) 
                self.verifyOverlapping(intC1L, intC2L, x2, y2, valueTag)
                self.inserePeso(valueTag, str(edge.getCost()))
                #self.verifyOverlappingCircle(valueTag, value, edge.getVertex())
                self.verifyEgde(valueTag, x1,y1, x2, y2)

    def verifyOverlappingCircle(self, edge, origem, destino):
        coord = self.canvas1.coords(edge)
        for v in  self.canvas1.find_overlapping(coord[0], coord[1], coord[2], coord[3]):
            if self.canvas1.type(v) == "oval" and origem not in self.canvas1.gettags(v) and destino not in self.canvas1.gettags(v):
                ''''valor = 0
                while v in self.canvas1.find_overlapping(coord[0], coord[1], coord[2], coord[3]):
                    valor +=10'''
                coord2 = self.canvas1.coords(v)
                self.canvas1.coords(edge, 
                    coord[0], coord[1], 
                    coord2[0]-5, coord2[1], 
                    coord2[0]-5, coord2[1]+80, 
                    #coord2[2], coord2[3],
                    coord[2], coord[3])
                self.canvas1.itemconfig(edge, joinstyle=ROUND)
                '''valor = 30
                a = self.canvas1.coords(edge)
                if v in self.canvas1.find_overlapping(a[0], a[1], a[4], a[5]):
                    a = self.canvas1.coords(edge)
                    print('a', a, 'self.canvas1.find_overlapping(a[0], a[1], a[4], a[5])',
                    self.canvas1.find_overlapping(a[0], a[1], a[4], a[5]), v)
                    self.canvas1.coords(edge, 
                    coord[0], coord[1], 
                    coord2[0]+valor, coord2[1]+valor, 
                    #coord2[2], coord2[3],
                    coord[2], coord[3])
                    valor +=10'''
                
    def inserePeso(self, edge, cost, deslocamento=10):
        coord = self.canvas1.coords(edge)
        x = ((coord[0]+coord[2]) / 2)+deslocamento
        y = (coord[1]+coord[3]) / 2
        self.canvas1.create_text(x, y, text = cost)
        

    def allTags(self):
        tags = []
        for value in self.canvas1.find_withtag(ALL):
            for v in self.canvas1.gettags(value):
                tags.append(v)
        return tags


                
        
    def verifyEgde(self, tag, x1,y1, x2, y2):
        '''verifica se já tem uma aresta, para não sobrepor'''
        qtdOverlapping = 0
        deslocamento = 0
        coord = self.canvas1.coords(tag)
        coordInver = [coord[2], coord[3], coord[0], coord[1]]
        for v in self.canvas1.find_withtag(ALL):
            coordV = self.canvas1.coords(v)
            for value in (self.canvas1.gettags(v)):
                valueTag = value
            if coordInver == coordV:
                qtdOverlapping += 1
            if qtdOverlapping != 0:
                deslocamento = 15/qtdOverlapping #divide a quantidade de arestas que sobrepoem,
            #pelo raio da circunferência, para calcular o deslocamento 
            for i in range(qtdOverlapping):
                intV = self.calculaInterseccao(x1,y1, x2, y2, True, deslocamento)
                intV2 = self.calculaInterseccao(x2, y2,x1,y1, True, deslocamento)
                intN = self.calculaInterseccao(x1,y1, x2, y2, True, -deslocamento)
                intN2 = self.calculaInterseccao(x2, y2,x1,y1, True, -deslocamento)
                self.canvas1.delete(v)
                self.canvas1.delete(tag)
                self.canvas1.create_line(intV[0], intV[1], intV2[0], intV2[1],
                arrow = FIRST)
                #self.verifyOverlapping(intV, intV2, x2, y2, valueTag)
                self.canvas1.create_line(intN[0], intN[1], intN2[0],intN2[1],
                arrow = FIRST)
  
    def verifyOverlapping(self, inte, inte2, x, y, edge, deslocamento =1):
        '''verifica se a linha está por cima do círculo
        do centro do círculo até o final do círculo'''
        overlapping = False
        for v in  self.canvas1.find_overlapping(inte[0]+1, inte[1]+1, inte[2]+1, inte[3]+1):
            if edge in self.canvas1.gettags(v):
                self.canvas1.delete(edge)
                for v2 in self.canvas1.find_overlapping(inte2[0]+1, inte2[1]+1, inte2[2]+1, inte2[3]+1):
                    if edge in self.canvas1.gettags(v):
                        self.canvas1.create_line(inte[0],inte[1], inte2[0], inte2[1], tag=edge, arrow=FIRST, 
                        capstyle=BUTT, joinstyle=ROUND) 
                        overlapping = True
                        break
                self.canvas1.create_line(x, y,  inte[0], inte[1], tag=edge, arrow=FIRST,
                capstyle=BUTT, joinstyle=ROUND)
        if not overlapping:
             for v2 in self.canvas1.find_overlapping(inte2[0]+1, inte2[1]+1, inte2[2]+1, inte2[3]+1):
                 if edge in self.canvas1.gettags(v2):
                        self.canvas1.delete(edge)
                        self.canvas1.create_line(inte2[0],inte2[1], inte[2], inte[3], tag=edge, arrow=FIRST,
                        capstyle=BUTT, joinstyle=ROUND)
                        break  
    
    def calculaInterseccao(self, x, y, x1, y1, paralelo=False, deslocamento=0):
        '''método para calcular os pontos de interseção entre os circles
        @param x: ponto x inicial da reta (centro da circuferência a ser verificada)
        @param y: ponto y inicial da reta (centro da circuferência a ser verificada)
        @param x1: ponto x1 final da reta
        @param y1: ponto y1 final da reta'''
        m = (y - y1)/(x - x1) #coefiencente angular da reta
        l = y - (m*x) #coeficiente angular da reta
        if paralelo:
            l = deslocamento + l
        a = (1 + m**2) 
        b = (-2*x + 2*m*l - 2*y*m)
        c = x**2 + l**2 - 2*y*l + y**2 - 30**2
        delt = b**2 - (4*a*c)
        #print(a, b, c, delt)
        if delt>0:
            xa1 = ((-b) + (math.sqrt(delt)))/(2*a)
            xa2 = ((-b) - (math.sqrt(delt)))/(2*a)
        ya1 = ((m*xa1) + l)
        ya2 = ((m*xa2) + l)
        return xa1, ya1, xa2, ya2
        


    def displayManual(self):
        '''show the graph on screen'''
        self.container1B = LabelFrame(self.container1, text="Visualiza Grafo", padx=10, pady=5)
        self.container1B.grid(row=0, column=1)
        self.canvas1 = Canvas(self.container1B, bg="#FEFFC2", width=600,
        height = 600)
        self.canvas1.configure(scrollregion = self.canvas1.bbox("all"))
        self.canvas1.grid(row=0, column = 2)
            

        


if __name__ == '__main__':
    app = Application()
    app.master.title("SocialGraph")
    mainloop()



