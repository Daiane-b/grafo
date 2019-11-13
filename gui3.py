from SocialGraph import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from random import randint
import math
from operator import itemgetter
from tkinter import messagebox
from tkinter import ttk


class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.lst = [] #lista que salva a localização dos circulos na tela
        '''Define os 3 frames contidos no frame principal'''
        self.leftframe = Frame(master, padx = 5)
        self.leftframe.grid(row=0,column=0,stick=NS+E)
        self.centerframe = Frame(master, padx = 5)
        self.centerframe.grid(row=0,column=1,stick=NS)
        self.rightframe = Frame(master, padx = 5)
        self.rightframe.grid(row=1,column=1)

        self.func = {'Vertice':  self.drawCircle, 'Aresta': self.drawLine, 'Select': None}

        self.selObj = None

        self.selObjText = None

        #for text, func in (('Vertice',),('Aresta', self.drawLine)):
            #self.func[text] = func

        '''botao de fechar'''
        botaFecha = Button(self.rightframe, text="Close",  command=self.quit)
        botaFecha.grid(row=0, column = 1, stick=E)
        botaoLimpar = Button(self.rightframe, text = "Limpar", command = self.Limpar)
        botaoLimpar.grid(row=0, column = 0)
        
        '''container que tem os radio button'''
        self.container3 = LabelFrame(self.leftframe, text = 'Opções', padx=5, pady=5)
        '''Nomeando os 3 frames contidos no frame principal'''
        self.container1 = LabelFrame(self.centerframe, text="Escolha o arquivo", padx=5, pady=5)
        self.container2 = LabelFrame(self.centerframe, text="Construção Manual", padx=5, pady=5)

        '''Montando o frame da esquerda'''
        lblframe = LabelFrame(self.leftframe, text="Selecione entrada", padx=5, pady=5)
        lblframe.grid(row=0,column=0)
        button1 = Button(lblframe, text="Arquivo", width=20,command= lambda: self.botaoSelecionaEntrada(1))
        button1.grid(row=0,column=0, columnspan=2)
        button2 = Button(lblframe, text="Manual",  width=20,command= lambda: self.botaoSelecionaEntrada(2))
        button2.grid(row=1,column=0,columnspan=2)

        '''define a forma de entrada por arquivo'''
        self.container1.grid(row=0, column=0)
        buttonFile = Button(self.container1, text = 'Ler arquivo', command=self.askopenfilename, padx = 5)
        buttonFile.grid(row=0,column=0,sticky='N')
        self.displayManual()

        '''define a forma de entrada manual'''
        self.container3.grid(row=0, column = 0)
        self.v = StringVar(self.container3)
        self.v.set(value="Vertice")

        

        self.displayEntradaManual()

        self.container2.isgridded = False
        self.container2.grid_forget()

        self.container3.isgridded = False
        self.container3.grid_forget()
    
    def Limpar(self):
        if self.buttonClick == 1:
            self.canvas1.delete(ALL)
        elif self.buttonClick == 2:
            self.canvas2.delete(ALL)
        
    def botaoSelecionaEntrada(self, value):
        """
           @param[in] integer
           @example self.botaoSelecionaEntrada(1)
        """              
        self.buttonClick = value
        self.container1.isgridded = False
        self.container1.grid_forget()
        self.container2.isgridded = False
        self.container2.grid_forget()
        self.container3.isgridded = False
        self.container3.grid_forget()
        if self.buttonClick == 1:
            self.lst = []
            self.container1.isgridded=True
            self.container1.grid(row=0,column=0)
        if self.buttonClick == 2:
            self.container2.isgridded = True
            self.container2.grid(row=0, column = 0)
            self.container3.isgridded = True
            self.container3.grid(row=1, column = 0)

    def askopenfilename(self):
        """
           @example self.askopenfilename()
        """   
        filepath = askopenfilename()
        Graph = SocialGraph(filepath)
        Graph.create()
        self.dg = Graph.dg
        self.desenhaGrafo(self.dg)
    
    
    def desenhaGrafo(self, dg = DiGraph.DiGraph()):
        '''desenha o Grafo conforme entrada manual.'''

        class Circle():
            '''classe círculo'''
            def __init__(self, px, py):
                self.nQuadrantes = (600/120) #define o número de quadrantes que o canvas vai ter (como foi 
                #criado com 600x600 e cada "circulo" vai ocupar 120)
                self.n = len(dg.vertices()) // 5 #numero de vertices do grafo
                if self.n < self.nQuadrantes * 5: #verifica se o grafo cabe dentro do canvas
                    self.px = px #define em qual quadrante o círculo vai ficar (começa com 1)
                    self.py = py
                    self.x = 120 * self.px - 60
                    self.y = 120 * self.py - 60
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
            def retonaDist(self, lst):
                dic = dict()
                for value in lst:
                    dic[value] = self.dist(value.x, value.y)
                return sorted(dic, key=dic.get)
            def __contains__(self, obj):
                return self.x == obj.x and self.y == obj.y
            def __repr__(self):
                return "x= "+str(self.getX())+", y= "+str(self.getY())
        def cria(valor):
            '''método para criar o círculo conforme lado escolhido'''
            px = valor.px + 1
            py = valor.py + 1
            circle = Circle(px, py)
            px, py = 0, 0
            if circle in self.lst or circle.y > 600 or circle.x > 600:
                px = valor.px + 1
                py = valor.py - 1
                circle = Circle(px, py)
                px, py = 0, 0
                if circle in self.lst or circle.x > 600 or circle.y <0:
                    px = valor.px
                    py = valor.py - 1
                    circle = Circle(px, py)
                    px, py = 0, 0
                    if circle in self.lst or circle.y < 0:
                        px = valor.px - 1
                        py = valor.py
                        circle = Circle(px, py)
                        px, py = 0, 0
                        if circle in self.lst or circle.x < 0:
                            px = valor.px + 1
                            py = valor.py 
                            circle = Circle(px, py)
                            cria(circle)
                        else:
                            self.lst.append(circle)
                            return None
                    else:
                        self.lst.append(circle)
                        return None
                else:
                    self.lst.append(circle)
                    return None
            else:
                self.lst.append(circle)
                return None
        
        i = 0
        '''cria e ordena uma lista pela quantidade de arestas que entram e saem do vertice'''
        dicQtdAresta = dict()
        for value in dg.vertices():
            dicQtdAresta[value] = len(dg.adjacentTo(value)) + len(dg.incomingEdges(value))
        dicQtdArestaO = dict()
        for item in sorted(dicQtdAresta, key = dicQtdAresta.get, reverse=TRUE):
            dicQtdArestaO[item] = dicQtdAresta[item]

        '''o primeiro vertice da lista estará no quadrante 3,2'''
        circle = Circle(3, 2)
        self.lst.append(circle)
        while dg.numVertices()>(len(self.lst)):
            '''insere os círculos no canvas'''
            for value in dicQtdArestaO:
                if value not in self.allTags():
                    if len(self.lst)>1:
                        cria(self.lst[i-1])
                    self.canvas1.create_oval(self.lst[i].getX()+self.lst[i].getRaio(), 
                    self.lst[i].getY()-self.lst[i].getRaio(), 
                    self.lst[i].getX()-self.lst[i].getRaio(), 
                    self.lst[i].getY()+self.lst[i].getRaio(),
                                fill="#FFD2A5", tag = value)
                    self.canvas1.create_text(self.lst[i].getX(), self.lst[i].getY(), text = value)
                    i +=1
                    listAdjacent = dg.adjacentTo(value) #lista que retorna todos os vertices adjancentes ao value
                    for item in dg.incomingEdges(value):
                        it = DiGraph.Edge(item, 1)
                        listAdjacent.add(it) #adicionando as arestas incidentes ao value
                    listMaior = dict() #lista que ordena as arestas adjancentes/incidentes ao value
                    while len(listAdjacent):
                        for adjacent in listAdjacent:
                            if adjacent.getVertex() not in self.allTags():
                                listMaior[adjacent]=dicQtdArestaO[adjacent.getVertex()]
                        if len(listMaior) == 0:
                            listAdjacent = dict()
                            break
                        valor = sorted(listMaior, key = listMaior.get, reverse=TRUE)[0]
                        cria(self.lst[i - 1])
                        self.canvas1.create_oval(self.lst[i].getX()+self.lst[i].getRaio(), 
                            self.lst[i].getY()-self.lst[i].getRaio(), 
                            self.lst[i].getX()-self.lst[i].getRaio(), 
                            self.lst[i].getY()+self.lst[i].getRaio(),
                                        fill="#FFD2A5", tag = valor.getVertex())
                        self.canvas1.create_text(self.lst[i].getX(), self.lst[i].getY(), text = valor.getVertex())
                        i +=1
                        listMaior = dict()
                        listAdjacent=dg.adjacentTo(valor.getVertex())
                        for item in dg.incomingEdges(valor.getVertex()):
                            it = DiGraph.Edge(item, 1)
                            listAdjacent.add(it)

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
        coord = self.canvas1.coords(tag)
        coordInver = [coord[2], coord[3], coord[0], coord[1]]
        for v in self.canvas1.find_withtag(ALL):
            coordV = self.canvas1.coords(v)
            for value in (self.canvas1.gettags(v)):
                valueTag = value
            if coordInver == coordV:
                qtdOverlapping += 1
            #pelo raio da circunferência, para calcular o deslocamento 
        for i in range(qtdOverlapping):
            self.canvas1.move(tag, 5, 5)
    def verifyOverlapping(self, inte, inte2, x, y, edge, deslocamento =1):
        '''verifica se a linha está por cima do círculo
        do centro do círculo até o final do círculo'''
        overlapping = False
        for v in  self.canvas1.find_overlapping(inte[0]+2, inte[1]+2, inte[2]+2, inte[3]+2):
            if edge in self.canvas1.gettags(v):
                self.canvas1.delete(edge)
                for v2 in self.canvas1.find_overlapping(inte2[0]+2, inte2[1]+2, inte2[2]+2, inte2[3]+2):
                    if edge in self.canvas1.gettags(v):
                        self.canvas1.create_line(inte[0],inte[1], inte2[0], inte2[1], tag=edge, arrow=FIRST) 
                        overlapping = True
                        break
                self.canvas1.create_line(x, y,  inte[0], inte[1], tag=edge, arrow=FIRST,
                capstyle=BUTT, joinstyle=ROUND)
        if not overlapping:
             for v2 in self.canvas1.find_overlapping(inte2[0]+2, inte2[1]+2, inte2[2]+2, inte2[3]+2):
                 if edge in self.canvas1.gettags(v2):
                        self.canvas1.delete(edge)
                        self.canvas1.create_line(inte2[0],inte2[1], inte[2], inte[3], tag=edge, arrow=FIRST)
                        break  
    
    def calculaInterseccao(self, x, y, x1, y1, paralelo=False, deslocamento=0):
        '''método para calcular os pontos de interseção entre os circles
        @param x: ponto x inicial da reta (centro da circuferência a ser verificada)
        @param y: ponto y inicial da reta (centro da circuferência a ser verificada)
        @param x1: ponto x1 final da reta
        @param y1: ponto y1 final da reta'''
        if x - x1 == 0:
            m = 0
        else:
            m = (y - y1)/(x - x1) #coefiencente angular da reta
        l = y - (m*x) #coeficiente angular da reta
        if paralelo:
            l = deslocamento + l
        a = (1 + m**2) 
        b = (-2*x + 2*m*l - 2*y*m)
        c = x**2 + l**2 - 2*y*l + y**2 - 30**2
        delt = b**2 - (4*a*c)
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
    
    def displayEntradaManual(self):
        self.dgManual = DiGraph.DiGraph()

        self.container2B = LabelFrame(self.container2, text="Visualiza Grafo", padx=10, pady=5)
        self.container2B.grid(row=0, column=1)
        self.canvas2 = Canvas(self.container2B, bg="#FEFFC2", width=600,
        height = 600)
        self.canvas2.configure(scrollregion = self.canvas1.bbox("all"))
        self.canvas2.grid(row=0, column = 2)

        Widget.bind(self.canvas2, "<Button-1>", self.mouseDown)
        Widget.bind(self.canvas2, "<Button1-Motion>", self.mouseMotion)
        Widget.bind(self.canvas2, "<Button1-ButtonRelease>", self.mouseUp)
        Widget.bind(self.container2B, "<Delete>", self.delete)
        #+Widget.bind(self.canvas2, "<Double-Button-1>", self.selectFunc("Select"))

        #ToolBarButton(self.container3, self.toolbar, 'sep', 'sep.gif',width=10, state='disabled')

        self.delete1 = Button(self.container3, text = "Deletar", command = self.delete)
        self.delete1.grid(row=8, column = 0)


        self.rb3 = Radiobutton(self.container3, text="Select", variable=self.v, value="Select",
        command = lambda: self.selectFunc(self.v.get()))
        self.rb3.grid(row=7,column=0, columnspan=2)

        self.valueCB1 = StringVar()
        self.valueCB2 = StringVar()
        self.rb2 = Radiobutton(self.container3, text="Aresta", variable=self.v, value="Aresta",
        command = lambda: self.selectFunc(self.v.get()))
        self.rb2.grid(row=3,column=0, columnspan=2)
        self.labelCB1 = Label(self.container3, text = "Origem")
        self.labelCB1.grid(row=5, column = 0)
        self.CB1 = ttk.Combobox(self.container3, textvariable = self.valueCB1, postcommand = self.updtCB, state = "readonly")
        self.CB1.grid(row=5, column = 1)
        self.labelCB2 = Label(self.container3, text = "Destino")
        self.labelCB2.grid(row=6, column = 0)
        self.CB2 = ttk.Combobox(self.container3, textvariable = self.valueCB2, postcommand = self.updtCB, state="readonly")
        self.CB2.grid(row=6, column = 1)
        self.CB2.bind('<<ComboboxSelected>>', self.addEdge) 
        self.labelE2 = Label(self.container3, text = "Peso:")
        self.labelE2.grid(row=4, column = 0, stick=W)
        self.entry2 = Entry(self.container3)
        self.entry2.grid(row=4, column=1)

        
        self.rb1 = Radiobutton(self.container3, text="Vertice", variable=self.v, value="Vertice",
        command = lambda: self.selectFunc(self.v.get()))
        self.rb1.grid(row=1,column=0, columnspan=2)
        self.labelE1 = Label(self.container3, text = "Vertice:")
        self.labelE1.grid(row=2, column = 0, stick=W)
        self.entry1 = Entry(self.container3)
        self.entry1.grid(row=2, column=1, stick=W)



        
        self.selectFunc(self.v.get())


    def addEdge(self, ent):
        if not self.entry2.get():
            messagebox.showerror('Peso não inserido', 'Inserir o Peso')
        elif not self.CB1.get():
            messagebox.showerror('Origem não inserida', 'Inserir a Origem')
        elif not self.CB2.get():
            messagebox.showerror('Destino não inserido', 'Inserir o Destino')
        else:
            self.dgManual.addEdge(self.CB1.get(), self.CB2.get(), int(self.entry2.get()))

    def updtCB(self):
        retu = []
        retu2 = []
        for value in self.dgManual.vertices():
            if value != self.valueCB1.get():
                retu2.append(value)
            retu.append(value)
        
        self.CB1['values'] = retu
        self.CB2['values'] = retu2

    
    def delete(self):
        coord = self.canvas2.coords(self.selObj)
        self.canvas2.delete(self.canvas2.find_enclosed(coord[0]+10, coord[1]+10, coord[2], coord[3]))
        self.canvas2.delete(self.selObj)
        

        
    
    def selectFunc(self, tag):
        self.currentFunc = self.func[tag]
    
    def mouseDown(self, event):
        try:
            self.currentObject = None
            self.lastx = self.startx = self.canvas2.canvasx(event.x)
            self.lasty = self.starty = self.canvas2.canvasy(event.y)
            if not self.currentFunc:
                self.selObj = self.canvas2.find_closest(self.startx, self.starty)[0]
                if self.canvas2.type(self.selObj) == 'text':
                    self.selObj = None
                self.canvas2.itemconfig(self.selObj, width=2)
                self.canvas2.itemconfig(self.selObjText, width=2)
                self.canvas2.lift(self.selObj)
        except:
            pass

    def mouseMotion(self, event):
        cx = self.canvas2.canvasx(event.x)
        cy = self.canvas2.canvasy(event.y)
        if self.currentFunc:
            self.lastx = cx
            self.lasty = cy
            self.canvas2.delete(self.currentObject)
            self.canvas2.delete(self.selObjText)
            self.currentFunc(self.startx, self.starty, self.lastx, self.lasty)
        else:
            if self.selObj:
                if self.canvas2.type(self.selObj) == 'oval':
                    coord = self.canvas2.coords(self.selObj)
                    for obj in self.canvas2.find_enclosed(coord[0], coord[1], coord[2], coord[3]):
                        if self.canvas2.type(obj) == 'text':
                            self.text = obj
                    tag = self.canvas2.gettags(self.text)
                    self.canvas2.move(self.selObj, cx-self.lastx, cy-self.lasty)
                    self.canvas2.delete(self.text)
                    coord = self.canvas2.coords(self.selObj)
                    self.canvas2.create_text((coord[0]+coord[2])/2, (coord[1]+coord[3])/2, text = tag, tag = tag)
                elif self.canvas2.type(self.selObj) == 'line':
                    coord = self.canvas2.coords(self.selObj)
                    for obj in self.canvas2.find_enclosed(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10):
                        if self.canvas2.type(obj) == 'text':
                            self.text = obj
                    tag = self.canvas2.gettags(self.selObj)
                    self.canvas2.delete(self.text)
                    self.canvas2.move(self.selObj, cx-self.lastx, cy-self.lasty)
                    coord = self.canvas2.coords(self.selObj)
                    self.canvas2.create_text(((coord[0]+coord[2])/2)+10, ((coord[1]+coord[3])/2)+10, text = tag)
                    
                else:
                    if self.canvas2.type(self.selObj) != 'text':
                        self.canvas2.move(self.selObj, cx-self.lastx, cy-self.lasty)
                self.lastx = cx
                self.lasty = cy

    def mouseUp(self, event):
        try:
            self.lastx = self.canvas2.canvasx(event.x)
            self.lasty = self.canvas2.canvasy(event.y)
            self.canvas2.delete(self.currentObject)
            self.currentObject = None
            if self.currentFunc:
                self.currentFunc(self.startx, self.starty, self.lastx, self.lasty)
                todos = self.canvas2.find_all()
                if self.canvas2.type(todos[::-1][0]) == 'line':
                    coord = self.canvas2.coords(self.canvas2.find_all()[len(todos)-1])
                    self.canvas2.create_text(((coord[0]+coord[2])/2)+10, (coord[1]+coord[3])/2+10, text = self.entry2.get())

            else:
                if self.selObj:
                    self.canvas2.itemconfig(self.selObj, width=1)
        except:
            pass
    
    def drawCircle(self, x, y, x2, y2):
        tag = self.entry1.get()
        if tag == '':
            messagebox.showwarning('Vértice', 'Inserir o nome do vértice')
            return None
        elif tag in self.dgManual.vertices() and tag in self.canvas2.gettags(ALL):
            messagebox.showwarning('Vértice', 'Grafo já possui esse vértice')
            return None
        else:
            self.currentObject = self.canvas2.create_oval(x+30, y-30, x2-30, y2+30, fill="#FFD2A5", tag = tag)
            self.canvas2.create_text((x+x2)/2, (y+y2)/2, text = tag, tag = tag)
            self.dgManual.addVertex(tag)
        
    def drawLine(self, x, y, x2, y2):
        try:
            va = int(self.entry2.get())
            self.currentObject = self.canvas2.create_line(x,y,x2,y2, arrow=LAST, tag = self.entry2.get())
        except:
            messagebox.showerror('Erro no peso', 'Inserir um valor válido!')
        #self.canvas2.create_text(((x+x2)/2)+10, (y+y2)/2, text = 2)

if __name__ == '__main__':
    app = Application()
    app.master.title("SocialGraph")
    app.master.geometry("950x900")
    app.mainloop()



