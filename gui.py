from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from textEditor import textEditor
import pandas as pd

class GUI:

    def __init__(self, root):
        self.root = root
        self.root.geometry('600x500')
        self.drawMenu()
        self.drawTextArea()
        self.drawFooter()
        self.keyBind()
        self.new()

    def new(self):
        self.root.title("Notepad++++")
        self.string = ""
        self.cursor_pos = 0
        self.end_pos = 0
        self.path = ""
        self.te = textEditor()
        self.display()

    def open(self):

        self.path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '.txt'), ('All files', '.*')))
        
        try:
            with open(self.path, 'r') as fr:
                self.root.title(os.path.basename(self.path))
                self.string = fr.read()
                self.cursor_pos = len(self.string)
                self.end_pos = len(self.string)
                self.te = textEditor(self.string)
                self.display()
        except FileNotFoundError:
            return 
        except:
            return 
        
    def save(self):
        try:
            if not self.path:
                self.path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '.txt'), ('All files', '.*'))).name
                
            fw = open(str(self.path), 'w')
            fw.write(self.string)   
            fw.close()
        except:
            return


    def saveAs(self):
        try:
            self.path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '.txt'), ('All files', '.*'))).name
            fw = open(str(self.path), 'w')
            fw.write(self.string)   
            fw.close()
        except:
            return 

    def exit(self):
        try:    
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
            if mbox is True:
                self.save()
                root.destroy()
            else:
                root.destroy()
        except:
            return 

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

    def help(self):
        messagebox.showinfo('Help', '- Use right and left arrows to navigate\n- Use up and down arrows to change font size\n\nShortcuts\nCtrl+N\t\t\tNew\nCtrl+O\t\t\tOpen\nCtrl+S\t\t\tSave\nCtrl+Z\t\t\tUndo\nCtrl+Y\t\t\tRedo\nCtrl+X\t\t\tCut\nCtrl+C\t\t\tCopy\nCtrl+V\t\t\tPaste')

    def about(self):
        messagebox.showinfo('About Notepad','Project made using python tkinter by Abhideep, Abhishek, Sourav, Debadyuti, Praneet')

    def swap(self, c, i, j):
        c = list(c)
        c[i], c[j] = c[j], c[i]
        return ''.join(c)

    # Function to display string in text area alongwith cursor
    def display(self):
        display_string = "|"
        if self.cursor_pos == self.end_pos:
            display_string = self.string + "|"
        else:
            display_string = self.string[:self.cursor_pos] + "|" + self.string[self.cursor_pos:]

        self.var.set(display_string)
        self.var2.set("Cursor position: " + str(self.cursor_pos) + "\t\t\tEnd position: " + str(self.end_pos))

        # Display the piece table on the terminal
        os.system("clear")
        #print(display_string)
        print("Original buffer: " + self.te.original_buffer)
        print("Add buffer: " + self.te.add_buffer)
        print("Piece table: ")
        print(pd.DataFrame(self.te.piece_table))

    # Keyboard event when any key is pressed
    def key(self, event):
        try:
            if 32 <= ord(event.char) <= 126 or event.keysym == 'Return':
                self.string = self.te.insert(event.char, self.cursor_pos)
                self.cursor_pos += 1;
                self.end_pos += 1
                self.display() 
        except:
            pass

    # Keyboard event when backspace is pressed
    def backSpace(self, event):
        if self.cursor_pos == 0:
            return

        self.string = self.te.delete(self.cursor_pos - 1, self.cursor_pos - 1)
        self.cursor_pos -= 1
        self.end_pos -= 1

        self.display()

    # Keyboard event when left arrow is pressed
    def left(self, event):
        if self.cursor_pos != 0:
            self.cursor_pos -= 1
            self.display()

    # Keyboard event when right arrow is pressed
    def right(self, event):
        if self.cursor_pos != self.end_pos:
            self.cursor_pos += 1
            self.display()

    def fontUp(self, event):
        self.fontSize += 2
        self.textArea.config(font=('Courier', self.fontSize))

    def fontDown(self, event):
        if self.fontSize >= 0:
            self.fontSize -= 2
            self.textArea.config(font=('Courier', self.fontSize))

    # Function to draw themenu bar
    def drawMenu(self):
        self.menubar = Menu(self.root)
        self.root.config(menu = self.menubar)
        

        # Creating the file menu 
        self.submenu = Menu(self.menubar,tearoff = 0)
        self.menubar.add_cascade(label = 'File', menu = self.submenu)
        self.submenu.add_command(label = 'New', command = self.new)
        self.submenu.add_command(label = 'Open...', command = self.open)
        self.submenu.add_command(label = 'Save', command = self.save)
        self.submenu.add_command(label = 'Save As', command = self.saveAs)
        self.submenu.add_command(label='Exit', command = self.exit)

        

        # Creating the edit menu
        self.submenu = Menu(self.menubar,tearoff = 0)
        self.menubar.add_cascade(label= 'Edit' , menu = self.submenu)
        self.submenu.add_command(label = 'Undo', command = self.undo)
        self.submenu.add_command(label = 'Redo', command = self.redo)
        self.submenu.add_command(label = 'Cut', command = self.cut)
        self.submenu.add_command(label = 'Copy', command = self.copy)
        self.submenu.add_command(label = 'Paste', command = self.paste)
        self.submenu.add_command(label = 'Delete', command = self.delete)

        # Creating the help menu
        self.submenu = Menu(self.menubar,tearoff = 0)
        self.menubar.add_cascade(label= 'Help' , menu = self.submenu)
        self.submenu.add_command(label = 'Help', command = self.help)
        self.submenu.add_command(label = 'About Notepad', command = self.about)

    # Function to draw the text area
    def drawTextArea(self):
        self.var = StringVar()
        self.fontSize = 14
        self.textArea = Label(root, textvariable = self.var, justify = LEFT, font=('Courier', self.fontSize))
        self.textArea.place(x = 10, y = 10)

    # Function to bind keys with events
    def keyBind(self):
        self.root.bind("<Key>", self.key)
        self.root.bind("<BackSpace>", self.backSpace)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Up>", self.fontUp)
        self.root.bind("<Down>", self.fontDown)
        self.root.bind("<Control-n>", lambda x: self.new())
        self.root.bind("<Control-o>", lambda x: self.open())
        self.root.bind("<Control-s>", lambda x: self.save())
        self.root.bind("<Control-z>", lambda x: self.undo())
        self.root.bind("<Control-y>", lambda x: self.redo())
        self.root.bind("<Control-x>", lambda x: self.cut())
        self.root.bind("<Control-c>", lambda x: self.copy())
        self.root.bind("<Control-v>", lambda x: self.paste())

    # Function to draw footer which shows the cursor position and end position
    def drawFooter(self):
        self.var2 = StringVar()
        self.footer = Label(root, relief = RAISED, textvariable = self.var2, justify = LEFT, height = 2)
        self.footer.pack(side = BOTTOM, fill = X)


root = Tk()
gui = GUI(root)
root.mainloop()