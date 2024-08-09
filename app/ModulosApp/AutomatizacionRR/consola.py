import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys

__version__ = 1.01

class frame(ttk.Frame):
	def __init__(self, master, **kwargs):
	    super().__init__(master, padding=10, **kwargs)
	    ttk.Style().configure("TButton", font="TkFixedFont 12")
	    self.root = master
	    self.widtgets()

	def widtgets(self):
		# Crear y posicionar elementos en la ventana
		label_usuario = ttk.Label(self.root, text="Usuario:")
		label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky=ttk.E)

		entry_usuario = ttk.Entry(self.root)
		entry_usuario.grid(row=0, column=1, padx=10, pady=10)

		label_clave = ttk.Label(self.root, text="Clave:")
		label_clave.grid(row=1, column=0, padx=10, pady=10, sticky=ttk.E)

		entry_clave = ttk.Entry(self.root, show="*")
		entry_clave.grid(row=1, column=1, padx=10, pady=10)


		label_ciudad = ttk.Label(self.root, text="Ciudad.")
		label_ciudad.grid(row=3,column=0)
		self.selCiudad = ttk.Combobox(master=self.root, state="readonly", values=["Bogota","Bucaramanga","Cali"])
		self.selCiudad.grid(row=3,column=1,padx=10, pady=10, sticky=ttk.E)
        
		btn_iniciar = ttk.Button(self.root, text="Iniciar Sesión",bootstyle="success-outline")#, command=iniciar_sesion)
		btn_iniciar.grid(row=4, column=0)

		btn_cancelar = ttk.Button(self.root, text="Cancelar", bootstyle="danger-outline", command=lambda:sys.exit())
		btn_cancelar.grid(row=4, column=1)


		

if __name__ == "__main__":
    app = ttk.Window(
        title="Bot cancelaciones razones v %s"%__version__,
        themename="solar",
        size=(300, 350),
        resizable=(False, False),
    )
    frame(app)
    app.mainloop()