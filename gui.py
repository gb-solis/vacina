from plot import plot_aux
from vacinação import perfis
from functools import partial
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import ctypes

# cataloga o processo
myappid = 'vacina.v0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Create window and frames
window = tk.Tk()
window.title('vacina')

# set the taskbar and window icons
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='ícone_vacina.png'))

buttonFrame = tk.Frame(window)
buttonFrame.pack()

plotFrame = tk.Frame(window)
plotFrame.pack(side = tk.BOTTOM)

# List of person to be shown in the plot
pessoas = []

# Create canvas and toolbar
fig = Figure(figsize=(5, 4), dpi=100)
plot_aux(fig.add_subplot(), pessoas, linhas=True)
canvas = FigureCanvasTkAgg(fig, master=plotFrame)  # A tk.DrawingArea.
canvas.draw()
toolbar = NavigationToolbar2Tk(canvas, plotFrame, pack_toolbar=False)
toolbar.update()
canvas.mpl_connect("key_press_event", key_press_handler)

toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

def toggle_pessoa(pessoa):                                 
    if pessoa in pessoas:
        pessoas.remove(pessoa)
    else:
        pessoas.append(pessoa)
    update_plot()

var_linhas = tk.BooleanVar(window)

def update_plot():
    fig.clear()
    plot_aux(fig.add_subplot(), pessoas, linhas=var_linhas.get())
    canvas.draw()

check = tk.Checkbutton(buttonFrame, text='Linhas', variable=var_linhas, command=update_plot)
check.pack(side=tk.LEFT)

for perfil in perfis:
    nome = perfil['name']
    btn = tk.Button(buttonFrame, text=nome, command=partial(toggle_pessoa, nome))
    btn.pack(side=tk.LEFT)

# inicializa a primeira pessoa da lista no plot
try:
    toggle_pessoa(perfis[0]['name'])
except:
    pass

window.mainloop()