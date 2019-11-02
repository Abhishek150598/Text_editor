from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from pieceTable import textEditor

class GUI:

    def __init__(self, root):
        self.root = root
        self.root.geometry('500x500')
        self.drawMenu()
        self.drawTextArea()
        self.new()

    def new(self):
        self.root.title("Notepad++++")
        self.string = ""
        self.cursor_pos = 0
        self.end_pos = 0
        self.path = ''
        self.te = textEditor()
        self.display()

    def open(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '.txt'), ('All files', '.*')))
        try:
            with open(path, 'r') as fr:
                self.root.title(path)
                self.string = fr.read()
                self.cursor_pos = len(self.string)
                self.end_pos = len(self.string)
                self.te = textEditor()
                self.te.insert(self.string, 0)
                self.display()
        except FileNotFoundError:
            return 
        except:
            return 

    def save(self):
        try:
            if self.path:
                print('la')
                self.path.write(self.string)
                print('la')
                self.path.close()
            else:
                print(self.string)
                self.path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '.txt'), ('All files', '.*')))
                self.path.write(self.string)
                self.path.close()
        except:
            print('la')
            return 

    def exit(self):
        print("Exit clicked")

    def undo(self):
        self.string = self.te.undo()
        self.end_pos = len(self.string)
        self.cursor_pos = self.end_pos
        self.display()

    def redo(self):
        self.string = self.te.redo()
        self.end_pos = len(self.string)
        self.cursor_pos = self.end_pos
        self.display()

    def onCutClicked(self, index1, index2):
        if index2 < index1:
            messagebox.showerror("Error", "Start index cannot be greater than end index!")
            return

        self.clipboard = self.te.getSubsequence(index1, index2)
        self.string = self.te.delete(index1, index2)
        self.end_pos -= len(self.clipboard)
        self.cursor_pos = self.end_pos
        self.display()
        

    def cut(self):
        cut_window = Tk()
        cut_window.title("Cut")
        # Label to enter starting index 
        Label(cut_window, text = "Enter starting index").pack()
        # Spinbox to enter starting index
        sb1 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb1.pack()
        # Label to enter ending index
        Label(cut_window, text = "Enter ending index").pack()
        # Spinbox to enter ending index
        sb2 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb2.pack()
        Button(cut_window, text = "Cut", command = lambda: self.onCutClicked(int(sb1.get()), int(sb2.get()))).pack()
        cut_window.mainloop()

    def onCopyClicked(self, index1, index2):
        if index2 < index1:
            messagebox.showerror("Error", "Start index cannot be greater than end index!")
            return

        self.clipboard = self.te.getSubsequence(index1, index2)

    def copy(self):
        cut_window = Tk()
        cut_window.title("Copy")
        # Label to enter starting index 
        Label(cut_window, text = "Enter starting index").pack()
        # Spinbox to enter starting index
        sb1 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb1.pack()
        # Label to enter ending index
        Label(cut_window, text = "Enter ending index").pack()
        # Spinbox to enter ending index
        sb2 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb2.pack()
        Button(cut_window, text = "Copy", command = lambda: self.onCopyClicked(int(sb1.get()), int(sb2.get()))).pack()
        cut_window.mainloop()

    def paste(self):
        self.string = self.te.insert(self.clipboard, self.cursor_pos)
        self.end_pos += len(self.clipboard)
        self.cursor_pos += len(self.clipboard)
        self.display()

    def onDeleteClicked(self, index1, index2):
        if index2 < index1:
            messagebox.showerror("Error", "Start index cannot be greater than end index!")
            return

        deleted = self.te.getSubsequence(index1, index2)
        self.string = self.te.delete(index1, index2)
        self.end_pos -= len(deleted)
        self.cursor_pos = self.end_pos
        self.display()

    def delete(self):
        cut_window = Tk()
        cut_window.title("Delete")
        # Label to enter starting index 
        Label(cut_window, text = "Enter starting index").pack()
        # Spinbox to enter starting index
        sb1 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb1.pack()
        # Label to enter ending index
        Label(cut_window, text = "Enter ending index").pack()
        # Spinbox to enter ending index
        sb2 = Spinbox(cut_window, from_ = 0, to = self.end_pos)
        sb2.pack()
        Button(cut_window, text = "Delete", command = lambda: self.onDeleteClicked(int(sb1.get()), int(sb2.get()))).pack()
        cut_window.mainloop()

    def swap(self, c, i, j):
        c = list(c)
        c[i], c[j] = c[j], c[i]
        return ''.join(c)

    def display(self):
        display_string = "|"
        if self.cursor_pos == self.end_pos:
            display_string = self.string + "|"
        else:
            display_string = self.string[:self.cursor_pos] + "|" + self.string[self.cursor_pos:]

        self.var.set(display_string)

    def key(self, event):
        try:
            if 32 <= ord(event.char) <= 126 or event.keysym == 'Return':
                self.string = self.te.insert(event.char, self.cursor_pos)
                self.cursor_pos += 1;
                self.end_pos += 1
                self.display() 
        except:
            pass

        


    def backSpace(self, event):
        if self.cursor_pos == 0:
            return

        self.string = self.te.delete(self.cursor_pos - 1, self.cursor_pos - 1)
        self.cursor_pos -= 1
        self.end_pos -= 1

        self.display()

    def left(self, event):
        if self.cursor_pos != 0:
            self.cursor_pos -= 1
            self.display()

    def right(self, event):
        if self.cursor_pos != self.end_pos:
            self.cursor_pos += 1
            self.display()


    def drawMenu(self):
        self.menubar = Menu(self.root)
        self.root.config(menu = self.menubar)
        self.submenu = Menu(self.menubar,tearoff = 0)

        # Creating the file menu 
        self.menubar.add_cascade(label = 'File', menu = self.submenu)
        self.submenu.add_command(label = 'New', command = self.new)
        self.submenu.add_command(label = 'Open...', command = self.open)
        self.submenu.add_command(label = 'Save', command = self.save)
        self.submenu.add_command(label='Exit', command = self.exit)

        self.submenu = Menu(self.menubar,tearoff = 0)

        # Creating the edit menu
        self.menubar.add_cascade(label= 'Edit' , menu = self.submenu)
        self.submenu.add_command(label = 'Undo', command = self.undo)
        self.submenu.add_command(label = 'Redo', command = self.redo)
        self.submenu.add_command(label = 'Cut', command = self.cut)
        self.submenu.add_command(label = 'Copy', command = self.copy)
        self.submenu.add_command(label = 'Paste', command = self.paste)
        self.submenu.add_command(label = 'Delete', command = self.delete)

    def drawTextArea(self):

        self.var = StringVar()
        self.textArea = Label(root, textvariable = self.var, justify = LEFT)
        self.textArea.place(x = 10, y = 10)
        self.root.bind("<Key>", self.key)
        self.root.bind("<BackSpace>", self.backSpace)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)


        

root = Tk()
gui = GUI(root)
root.mainloop()