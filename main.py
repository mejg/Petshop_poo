from package.controllers.gui import PetShopGUI
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = PetShopGUI(root)
    root.mainloop()