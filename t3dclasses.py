from Tkinter import *
from ttk import *

import tkFileDialog as tfd

import os
import random

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
        self.fmin.set('1')
        self.fmax = StringVar()
        self.fmax.set('200')
        self.fstep = StringVar()
        self.fstep.set('1')

        Label(frame, text='FRAMES').pack(anchor=W)
        Label(frame, text='Inicio').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.fmin).pack(side=LEFT)
        Label(frame, text='Final').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.fmax).pack(side=LEFT)
        Label(frame, text='Step').pack(side=LEFT)
        Entry(frame, width=6, textvariable = self.fstep).pack(side=LEFT)

class LimitsGetter:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.check = IntVar()

        Label(frame, text='LIMITES').grid()
        Label(frame, text='Eje X').grid()
        Label(frame, text='Min').grid(row=1, column=1)
        self.xmin = Entry(frame, width=4, state=DISABLED)
        self.xmin.grid(row=1, column=2, pady=1)
        Label(frame, text='Max').grid(row=1, column=3)
        self.xmax = Entry(frame, width=4, state=DISABLED)
        self.xmax.grid(row=1, column=4, pady=1)
        Label(frame, text='Eje Y').grid()
        Label(frame, text='Min').grid(row=2, column=1)
        self.ymin = Entry(frame, width=4, state=DISABLED)
        self.ymin.grid(row=2, column=2, pady=1)
        Label(frame, text='Max').grid(row=2, column=3)
        self.ymax = Entry(frame, width=4, state=DISABLED)
        self.ymax.grid(row=2, column=4, pady=1)
        Label(frame, text='Eje Z').grid()
        Label(frame, text='Min').grid(row=3, column=1)
        self.zmin = Entry(frame, width=4, state=DISABLED)
        self.zmin.grid(row=3, column=2, pady=1)
        Label(frame, text='Max').grid(row=3, column=3)
        self.zmax = Entry(frame, width=4, state=DISABLED)
        self.zmax.grid(row=3, column=4, pady=1)
        Checkbutton(frame, text='Usar limites', variable=self.check, onvalue=True, offvalue=False, command=self.callback).grid(columnspan=5, sticky=W)

    def callback(self):
        if self.check.get():
            self.xmin.config(state=NORMAL)
            self.xmax.config(state=NORMAL)
            self.ymin.config(state=NORMAL)
            self.ymax.config(state=NORMAL)
            self.zmin.config(state=NORMAL)
            self.zmax.config(state=NORMAL)
        else:
            self.xmin.config(state=DISABLED)
            self.xmax.config(state=DISABLED)
            self.ymin.config(state=DISABLED)
            self.ymax.config(state=DISABLED)
            self.zmin.config(state=DISABLED)
            self.zmax.config(state=DISABLED)

class ComboOption:
    def __init__(self,master, clist,directory,part):
        self.frame = Frame(master)
        self.frame.pack(anchor=W)

        self.csel = StringVar()
        self.directorio = directory
        self.particles = part
        clist.append(self.csel)

        Combobox(self.frame, state = 'readonly', textvariable=self.csel, values = self.directorio.caches).pack(side=LEFT)
        self.button = Button(self.frame, text='Agregar', command=self.agregar_callback)
        self.button.pack(side=LEFT)

    def agregar_callback(self):
        self.button.pack_forget()

        self.psel = StringVar()
        self.particles.plist.append(self.psel)
        Entry(self.frame, width=50, textvariable=self.psel).pack(side=LEFT)
        Button(self.frame, text='Quitar', command=self.quitar_callback).pack(side=LEFT)
        self.particles.crear_entrada()

    def quitar_callback(self):
        self.frame.pack_forget()
        self.particles.clist.remove(self.csel)
        self.particles.plist.remove(self.psel)


class ParticlesGetter:
    def __init__(self,master,directory):
        self.frame = Frame(master)
        self.frame.pack(anchor=W, padx=5, pady=5)

        self.clist = []
        self.plist = []
        self.oplist = []
        self.directorio = directory

        self.directorio.set_particles(self)

        Label(self.frame, text='PARTICULAS PARA ANALISIS').pack(anchor=W)
        op = ComboOption(self.frame, self.clist,self.directorio,self)
        self.oplist.append(op)
        #Entry(frame, width=70, textvariable=self.var).pack(anchor=W)

    def crear_entrada(self):
        op = ComboOption(self.frame, self.clist,self.directorio,self)
        self.oplist.append(op)

    def total_remove(self):
        for op in self.oplist:
            op.frame.pack_forget()
        self.clist = []
        self.plist = []
        self.oplist = []

class ExAndGo:
    def __init__(self,master, directory, part, fr):
        frame = Frame(master)
        frame.pack(anchor=W, padx=5, pady=5)

        self.directorio = directory
        self.particles = part
        self.frames = fr

        Label(frame, text="Ingrese los numeros de las particulas que desee visualizar.\n\tEj: '1 30 58' analiza esas tres particulas", anchor=CENTER).pack(side=LEFT)
        Button(frame, text='EMPEZAR', command=self.callback).pack(side=LEFT, ipady=10, ipadx=40, padx=30)

    def callback(self):
        for c in self.particles.clist[:-1]:
            print c.get()
        print '------------------------'
        for p in self.particles.plist:
            print p.get()
        print '------------------------'


class StatusBar:
    def __init__(self,master):
        frame = Frame (master)
        frame.pack(side=BOTTOM, fill=X)

        self.var = StringVar()
        self.var.set('Esperando datos...')
        

        Label(frame, textvariable=self.var, relief=RIDGE, anchor=W, width=80).pack(side=LEFT)
        Label(frame, text='NSX v1.0', relief=RIDGE, anchor=E).pack(side=RIGHT, ipadx=10)
