from Tkinter import *
from ttk import *

import tkFileDialog as tfd
import os

import threading
from struct import unpack

class ProgressShow:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.var = StringVar()
        self.var.set('0% completado')

        self.bar = Progressbar(frame, orient='horizontal', length=500, mode='determinate')
        self.bar.pack(side=LEFT, pady=5, padx=5)
        Label(frame, textvariable=self.var).pack(side=LEFT)

    def update(self, n):
        self.bar.step(n)
        self.var.set('{0}% completado'.format(int(self.var.get().split('%')[0])+n))

class DirectoryGetter:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.var = StringVar()
        self.caches = []

        Label(frame, text='DIRECTORIO DEL CACHE').pack(anchor=W)
        Entry(frame, state=DISABLED, textvariable=self.var, width=70).pack(side=LEFT)
        Button(frame, text='Explorar', command=self.callback).pack(side=LEFT, padx=5)

    def callback(self):
        self.var.set(tfd.askdirectory())
        self.caches = []
        files = map(str,os.listdir(self.var.get()))
        for f in files:
            c = f.strip().split('_')
            if c[-2] == '000000' and '_'.join(c[:-2]) not in self.caches:
                self.caches.append('_'.join(c[:-2]))

        self.minmax_caches = {}
        for cch in self.caches:
            self.minmax_caches[cch] = [999999,0]

        for f in files:
            c = f.split('_')
            p = int(c[-2])
            cch = '_'.join(c[:-2])
            #print cch, p
            if self.minmax_caches[cch][0] > p and p != 0:
                self.minmax_caches[cch][0] = p
            if self.minmax_caches[cch][1] < p :
                self.minmax_caches[cch][1] = p
                
        self.particles.total_remove()
        self.particles.crear_entrada()

    def set_particles(self,part):
        self.particles = part

class FramesGetter:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.fmin = StringVar()
        self.fmax = StringVar()
##        self.delta = StringVar()
##        self.delta.set('1')

        Label(frame, text='FRAMES').pack(anchor=W)
        Label(frame, text='Min').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.fmin).pack(side=LEFT)
        Label(frame, text='Max').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.fmax).pack(side=LEFT)
##        Label(frame, text='Delta').pack(side=LEFT)
##        Entry(frame, width=6, textvariable = self.delta).pack(side=LEFT)

class DetailsGetter:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.factor = StringVar()
        self.factor.set('100')

        Label(frame, text='DETALLES').pack(anchor=W)
        Label(frame, text='Factor de Busqueda').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.factor).pack(side=LEFT)

class ShowAndGo:
    def __init__(self,master, directory, fr):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.master = master

        self.caches = StringVar()
        self.caches.set('<ninguno>')
        self.directorio = directory
        self.frames = fr

        self.directorio.set_particles(self)
        self.trabajando = False

        Label(frame, text='CACHES DETECTADOS').pack(anchor=W)
        Label(frame, textvariable=self.caches, width=50).pack(side=LEFT)
        Button(frame, text='EMPEZAR', command=self.callback).pack(side=LEFT, ipady=10, ipadx=40, padx=30)

    def crear_entrada(self):
        #self.caches.set('-'+'\n-'.join(self.directorio.caches))
        s=''
        for cch in self.directorio.caches:
            s= s+'-Cache: {0} Frames: de {1} a {2}\n'.format(cch, self.directorio.minmax_caches[cch][0], self.directorio.minmax_caches[cch][1])
        self.caches.set(s)

    def total_remove(self):
        pass

    def callback(self):
        if self.trabajando:
            return
        self.trabajando = True
        
        self.top = Toplevel(self.master)
        self.top.resizable(0,0)
        self.top.title('Cargando...')

        self.progress = ProgressShow(self.top)
        self.top.focus_force()

        t = threading.Thread(target=self.gogogo, args=())
        t.start()

    def get_particles(self):
        fmin = int(self.frames.fmin.get())
        fmax = int(self.frames.fmax.get())

        self.particulas = {}
        for cache in self.directorio.caches:
            self.particulas[cache] = {}
            pan = []
            pac = []
            
            for i in xrange(fmin,fmax):
                archivo = open(self.directorio.var.get() + '/' + cache + '_' + str(i).zfill(6) + '_00.bphys','rb')
                h = actual.read(20)
                n = unpack('i', h[12:16])[0]
                if n == 0:
                    continue
                for _ in xrange(n):
                    p = archivo.read(28)
                    m = unpack('i', p[0:4])[0]

                    pac.append(m)

                if i != fmin:
                    self.particulas[cache][i-1] = list(set(pac)-set(pan))

                archivo.close()
                pan = pac

            self.particulas[cache][fmax] = []

        self.all_particles = []
        for d in self.particulas:
            


    def gogogo(self):

        self.get_particles()
        
        fmin = int(self.frames.fmin.get())
        fmax = int(self.frames.fmax.get())
        #fstep = int(self.frames.fstep.get())

        anterior = 0
        largo = len(self.directorio.caches)

        dire = './CACHES/'+self.directorio.var.get().split('/')[-1]

        if not os.path.exists(dire):
            os.makedirs(dire)

        for cache in self.directorio.caches:
            
            for i in xrange(fmin,fmax):

                actual = ((100*(i-fmin))/(fmax-fmin))/largo
                dif = actual - anterior
                if  dif > 0:
                    anterior = actual
                    self.progress.update(dif)

            archivo = open(self.directorio.var.get() + '/' + cache + '_' + str(i).zfill(6) + '_00.bphys','rb')
            h = archivo.read(20)
            n = unpack('i', h[12:16])[0]
            if n == 0:
                continue

            sapbe = open (dire+'/'+cache.split('/')[-1]+'_'+str(i).zfill(6)+'.csv','w')

            for _ in xrange(n):
                p = archivo.read(28)
            
                m = unpack('i', p[0:4])[0]
                if m in 
                
                px = unpack('f', p[4:8])[0]
                py = unpack('f', p[8:12])[0]
                pz = unpack('f', p[12:16])[0]

            

root = Tk()
root.resizable(0,0)
root.title('Crear caches para ITEHGAPS')

directorio = DirectoryGetter(root)
frames = FramesGetter(root)
detalles = DetailsGetter(root)
Separator(root).pack(fill=X)
ShowAndGo(root, directorio, frames)

root.mainloop()
