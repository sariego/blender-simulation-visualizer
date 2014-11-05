
from t3dclasses import *
from spagheti import *
from itehgaps import *

root = Tk()
root.resizable(0,0)
root.title('Visor de trayectoria de particulas')
root.iconbitmap('xyz.ico')
note = Notebook(root)
note.pack()

##first = Frame(root)
##directorio = DirectoryGetter(first)
##frames = FramesGetter(first)
##limits = LimitsGetter(first)
##Separator(first).pack(fill=X)
##particles = ParticlesGetter(first,directorio)
##ExAndGo(first, directorio, particles, frames)

fideos = Frame(root)
directorio_f = DirectoryGetter(fideos)
frames_f = FramesGetter(fideos)
detalles = SpaDetails(fideos)
show = Show(fideos, directorio_f, detalles)
Separator(fideos).pack(fill=X)
Go(fideos, directorio_f, frames_f, detalles, show)

soedif = Frame(root)
directorio_s = DirectoryGetter(soedif)
frames_s = FramesGetter(soedif)
detalles_s = SpaDetails(soedif)
show_s = Show(soedif, directorio_s, detalles_s)
Separator(soedif).pack(fill=X)
Og(soedif, directorio_s, frames_s, detalles_s, show_s)

#status = StatusBar(root)


#note.add(first, text='Trayectoria 3D')
note.add(fideos, text='Spagheti')
note.add(soedif, text='itehgapS')

root.mainloop()
