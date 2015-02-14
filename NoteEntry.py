import Tkinter as tk
import tkFont
from enchant.checker import SpellChecker
import tkMessageBox

class NoteEntry(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Set to full screen mode
        self.attributes('-fullscreen', True)

        # Note input frame
        note_frame = tk.Frame(borderwidth=1, relief="sunken")
        note_frame.pack(side="bottom", fill="both", expand=True)

        # Actual note text field
        self.note = tk.Text(wrap="word", background="white", 
                            borderwidth=0, highlightthickness=0)
        # Misspelled tag to colour word red and underline it
        self.note.tag_configure("misspelled", foreground="red", underline=True)

        # Scroll bar to be placed on note input field
        self.scrollBar = tk.Scrollbar(orient="vertical", borderwidth=0,
                                command=self.note.yview)
        self.scrollBar.pack(in_=note_frame,side="right", fill="y", expand=False)
        self.note.configure(yscrollcommand=self.scrollBar.set)
        self.note.pack(in_=note_frame, side="left", fill="both", expand=True)

        # Watch keystrokes on note input field and initialise focus to it
        self.note.bind("<Key>", self.spellcheck)
        self.note.focus()

        self.protocol("WM_DELETE_WINDOW", self.closeCallback)

    def closeCallback(self):
        if tkMessageBox.askokcancel("Save", "Save note?"):
            # Implement encrypt and save not here
            tkMessageBox.showinfo("Success", "Note successfully saved.")
        self.destroy()

    def spellcheck(self, event):
        # Set spell checker language to British English
        chkr = SpellChecker("en_UK")
        index = self.note.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "" or not " " in self.note.get("1.0", 'end'):
            index ="1.0"
        else:
            index = self.note.index("%s+1c" % index)
        word = self.note.get(index, "insert")

        if word is not None and len(word) > 0:
            if chkr.check(word):
                self.note.tag_remove("misspelled", index, "%s+%dc" % (index, len(word)))
            else:
                self.note.tag_add("misspelled", index, "%s+%dc" % (index, len(word)))

if __name__ == "__main__":
    app=NoteEntry()
    app.mainloop()