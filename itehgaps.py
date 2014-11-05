
from spagheti import *

class Og:
    def __init__(self,master, directory, fr, details, sow):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.master = master
        self.detalle = details
        
        self.directorio = directory
        self.frames = fr
        self.show = sow

        Label(frame, text="Ingrese los colores con los que desea ver los emisores\nen la animacion. Animacion inversa.\n\nOJO: Debe existir el frame (fmax+1)", anchor=CENTER).pack(side=LEFT)
        Button(frame, text='EMPEZAR', command=self.callback).pack(side=LEFT, ipady=10, ipadx=40, padx=30)

        self.colores = {'':'r', 'rojo':'r', 'azul':'b', 'verde':'g', 'cyan':'c', 'magenta':'m', 'amarillo':'y'}

    def callback(self):
        self.mouse_is_inside = threading.Event()
        self.mouse_is_inside.set()
        self.next = threading.Event()
        self.next.set()
        self.exit_graph = threading.Event()
        self.exit_graph.clear()

        self.w = Toplevel(self.master)
        self.w.resizable(0,0)
        self.w.title('Graficos')
        self.w.iconbitmap('xyz.ico')

        self.top = Toplevel(self.master)
        self.top.resizable(0,0)
        self.top.title('Calculando...')
        self.top.iconbitmap('xyz.ico')

##        self.info = Toplevel(self.master)
##        self.info.resizable(0,0)
##        self.info.title('Informacion')
##        self.info.iconbitmap('xyz.ico')

        self.fig = matplotlib.figure.Figure(figsize=(8,6), dpi=100)
        self.canvas = FigureCanvas(self.fig, master=self.w)
        self.fig.set_canvas(self.canvas)

##        self.toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(self.canvas, self.w)
##        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.frame_label = StringVar()
        Label(self.w, textvariable=self.frame_label).pack(side=BOTTOM, fill=X)

        self.ax = self.fig.add_subplot(111,projection='3d')

        self.ax.mouse_init()
        
        self.progress = ProgressShow(self.top)

        #self.dshow = InfoShow(self.info)
        
        self.w.bind('<Button-1>',self.press_callback)
        self.w.bind('<ButtonRelease-1>',self.release_callback)
        self.w.bind('<space>',self.toggle_callback)
        self.w.bind('<q>',self.exit_callback)


        t = threading.Thread(target=self.graficar, args=())
        t.start()

        
    def graficar(self):
        time.sleep(1)
        current = time.asctime()
        print current

        fmin = int(self.frames.fmin.get().strip())
        fmax = int(self.frames.fmax.get().strip())
        fstep = int(self.frames.fstep.get().strip())

        self.top.focus_force()

        db_pro = []
        for ii in xrange(int(self.detalle.delta.get())):
            for lolo in self.directorio.caches:
                
                porcentaje = 0        
                self.particulas_a_analizar(lolo)
                db = {}
                for r in self.particulas:
                    db[r]=([],[],[],[False],self.colores[self.show.caches[lolo].combo.get()])

                try:
                    archivo = open(lolo+'_'+str(fmax-ii)+'_'+str(fmin)+'_'+str(fstep))
                except IOError:
                    print 'Cache no encontrado. Leyendo frames.'

                    for i in xrange(fmax,fmin-1,-1*fstep):
                        s = self.directorio.var.get() + '/' + lolo + '_' + str(i-ii).zfill(6) +'_00.bphys' 
                        archivo = open(s, 'rb')

                        if (100*(fmax-i))/(fmax+1-fmin) != porcentaje:
                            porcentaje += 1
                            self.progress.update()
                        
                        h = archivo.read(20)
                        n = unpack('i', h[12:16])[0]
                        if n == 0:
                            continue
                        
                        for _ in xrange(n):
                            p = archivo.read(28)
                        
                            m = unpack('i', p[0:4])[0]
                            
                            if m in self.particulas:
                                db[m][0].append(unpack('f', p[4:8])[0])
                                db[m][1].append(unpack('f', p[8:12])[0])
                                db[m][2].append(unpack('f', p[12:16])[0])
                            
                        
                        archivo.close()
                    for m in self.particulas:
                        db[m][0].insert(0,db[m][0][0])
                        db[m][1].insert(0,db[m][1][0])
                        db[m][2].insert(0,db[m][2][0])
                    print 'Creando cache.'
                    archivo = open(lolo+'_'+str(fmax-ii)+'_'+str(fmin)+'_'+str(fstep),'w')
                    for a in db:
                        for i in xrange(len(db[a][0])):
                            archivo.write(str(a)+':'+str(db[a][0][i])+':'+str(db[a][1][i])+':'+str(db[a][2][i])+'\n')
                    archivo.close()
                        

                    print 'Cache listo.'
                    

                else:
                    self.progress.mutate()
                    print 'Cache encontrado. Leyendo cache.'
                    for linea in archivo:
                        datos = linea.strip().split(':')
                        db[int(datos[0])][0].append(float(datos[1]))
                        db[int(datos[0])][1].append(float(datos[2]))
                        db[int(datos[0])][2].append(float(datos[3]))
                    archivo.close()
                    print 'Cache leido'
                db_pro.append(db)

        print current
        print time.asctime()
##        self.dshow.change_min(fmin)
##        self.dshow.change_part(' '.join(map(str,self.particulas)))
##        self.dshow.change_muertas(' '.join(map(str,self.particulas)))

        for b in db_pro:
            for a in b:
                self.ax.plot(b[a][0],b[a][1],b[a][2])
        print time.asctime()
        self.ax.set_xlim3d(-10,10)
        self.ax.set_ylim3d(-10,10)
        self.ax.set_zlim3d(0,12)
        self.fig.canvas.draw()
        
        self.next.clear()
        self.next.wait()
        self.ax.clear()
        for b in db_pro:
            for a in b:
                self.ax.plot(b[a][0],b[a][1],b[a][2],'k')
        self.ax.set_xlim3d(-10,10)
        self.ax.set_ylim3d(-10,10)
        self.ax.set_zlim3d(0,12)
        self.fig.canvas.draw()

        self.next.clear()
        self.next.wait()

        self.mouse_is_inside.set()

        vidas = []
        for b in db_pro:
            for a in b:
                vidas.append(len(b[a][0]))
        vml = max(vidas)

##        muertes = {}
##        for b in db_pro.:
##            muertes[b] = ([])

        c_part = set(self.particulas)
        rr = int(self.detalle.largo.get())
        
        for i in xrange(int(self.detalle.inicio.get()),vml,int(self.detalle.step.get())):
            if self.exit_graph.isSet():
                break
            #print i
            self.frame_label.set('Frame '+str(fmax-i*fstep))
            time.sleep(0.05)
            self.mouse_is_inside.wait()
            self.ax.clear()
            for b in db_pro:
                for a in b:
                    if b[a][3][0]:
                        continue
                    self.mouse_is_inside.wait()
                    self.ax.plot(b[a][0],b[a][1],b[a][2],'k', alpha=0.1)
                    self.ax.plot(b[a][0][i-rr:i],b[a][1][i-rr:i],b[a][2][i-rr:i],b[a][4])
                    if len(b[a][0]) < i:
                        b[a][3][0] = True
##                        self.dshow.change_m(a,fmin+i)
##                        vivas = list(c_part - set(muertes))
##                        vivas.sort()
##                        self.dshow.change_muertas(' '.join(map(str,vivas)))
            self.ax.set_xlim3d(-10,10)
            self.ax.set_ylim3d(-10,10)
            self.ax.set_zlim3d(0,12)
            self.fig.canvas.draw()
        self.frame_label.set('Terminado. Frame Final: '+str(fmax-i*fstep))

        self.w.unbind('<Button-1>')
        self.w.unbind('<ButtonRelease-1>')
        self.w.unbind('<space>')
        self.w.unbind('<q>')
        
        self.next.clear()
        self.next.wait()
##        self.ax.clear()
##        for b in db_pro:
##            for a in b:
##                self.ax.plot(b[a][0],b[a][1],b[a][2])
##        self.fig.canvas.draw()
       
    def exit_callback(self,event):
        print 'EXIT'
        self.exit_graph.set()
        time.sleep(0.5)
        
    def press_callback(self,event):
        print 'PRESS'
        self.mouse_is_inside.clear()
        time.sleep(0.5)

    def release_callback(self,event):
        print 'RELEASE'
        time.sleep(0.5)
        self.mouse_is_inside.set()

    def toggle_callback(self,event):
        print 'TOGGLE'
        if self.mouse_is_inside.isSet():
            self.mouse_is_inside.clear()
        else:
            self.mouse_is_inside.set()

        if self.next.isSet():
            self.next.clear()
        else:
            self.next.set()

    def particulas_a_analizar(self, direc):
        pre = []
        paa = []

        f = int(self.frames.fmax.get().strip())

        s = self.directorio.var.get() + '/' + direc + '_' + str(f+1).zfill(6) +'_00.bphys'
        archivo = open(s, 'rb')

        h = archivo.read(20)
        n = unpack('i', h[12:16])[0]
        if n == 0:
            return

        for _ in xrange(n):
            p = archivo.read(28)
            pre.append(unpack('i', p[0:4])[0])

        archivo.close()

        s = self.directorio.var.get() + '/' + direc + '_' + str(f).zfill(6) +'_00.bphys'
        archivo = open(s, 'rb')

        h = archivo.read(20)
        n = unpack('i', h[12:16])[0]
        if n == 0:
            return

        for _ in xrange(n):
            p = archivo.read(28)
            paa.append(unpack('i', p[0:4])[0])

        archivo.close()

        self.particulas = list(set(paa)-set(pre))
        self.particulas.sort()
        
            

            

    
