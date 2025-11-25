import tkinter as tk
import random

ANCHO = 400
ALTO = 400
TAM = 20

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Mejorado")

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#1c1c1c")
        self.canvas.pack()

        # Botón de reinicio (invisible al inicio)
        self.btn_reiniciar = tk.Button(root, text="Reiniciar", font=("Arial", 12), command=self.iniciar)
        self.btn_reiniciar.pack(pady=10)
        self.btn_reiniciar.pack_forget()

        self.root.bind("<KeyPress>", self.cambiar_direccion)

        self.iniciar()

    def iniciar(self):
        self.btn_reiniciar.pack_forget()
        self.direccion = "Right"
        self.jugando = True

        self.serpiente = [(100, 100), (80, 100), (60, 100)]
        self.manzana = self.crear_manzana()

        self.canvas.delete("all")
        self.actualizar()

    def crear_manzana(self):
        return (
            random.randrange(0, ANCHO, TAM),
            random.randrange(0, ALTO, TAM)
        )

    def cambiar_direccion(self, event):
        if not self.jugando:
            return

        if event.keysym in ["Up", "Down", "Left", "Right"]:
            # Evitar que se pueda ir hacia atrás directamente
            opuestos = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if opuestos[event.keysym] != self.direccion:
                self.direccion = event.keysym

    def mover(self):
        x, y = self.serpiente[0]

        if self.direccion == "Up":
            y -= TAM
        elif self.direccion == "Down":
            y += TAM
        elif self.direccion == "Left":
            x -= TAM
        elif self.direccion == "Right":
            x += TAM

        nueva_cabeza = (x, y)
        self.serpiente.insert(0, nueva_cabeza)

        # Comer manzana
        if nueva_cabeza == self.manzana:
            self.manzana = self.crear_manzana()
        else:
            self.serpiente.pop()

    def actualizar(self):
        if not self.jugando:
            return

        self.mover()
        x, y = self.serpiente[0]

        # Colisiones
        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO or self.serpiente[0] in self.serpiente[1:]:
            self.game_over()
            return

        self.dibujar()
        self.root.after(100, self.actualizar)

    def dibujar(self):
        self.canvas.delete("all")

        # Dibujar serpiente (cuerpo más claro, cabeza más brillante)
        for i, (x, y) in enumerate(self.serpiente):
            color = "#00ff55" if i == 0 else "#00993a"
            self.canvas.create_rectangle(x, y, x + TAM, y + TAM, fill=color, outline="black")

        # Dibujar manzana
        mx, my = self.manzana
        self.canvas.create_oval(mx, my, mx + TAM, my + TAM, fill="red", outline="darkred")

    def game_over(self):
        self.jugando = False
        self.canvas.create_text(
            ANCHO // 2,
            ALTO // 2 - 20,
            text="GAME OVER",
            fill="white",
            font=("Arial", 28, "bold")
        )
        self.canvas.create_text(
            ANCHO // 2,
            ALTO // 2 + 20,
            text="Presiona el botón para reiniciar",
            fill="gray",
            font=("Arial", 12)
        )

        self.btn_reiniciar.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
