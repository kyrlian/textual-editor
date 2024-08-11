#!python3

# https://textual.textualize.io/widgets/input/

import sys
import os
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Header, Footer, Static

def read_file(filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
        return "\n".join(lines)
    except FileNotFoundError:
        return ""

def write_file(filename, s):
    f = open(filename, "w")
    f.write(s)
    f.close()

# custom commands
# https://textual.textualize.io/guide/command_palette/


# custom text area hook
# https://textual.textualize.io/widgets/text_area/#hooking-into-key-presses


class WriterApp(App):
    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def detect_language(self,input_file):
        filename, file_extension = os.path.splitext(input_file)
        languages =  {"."+e : e for e in TextArea().available_languages}
        extensions = { ".yml": "yaml",".py": "python",".js":"javascript",".md":"markdown",".sh":"bash"}
        if file_extension in languages:
            return languages[file_extension]
        if file_extension in extensions:
            return extensions[file_extension]

    def __init__(self, *args, input_file, **kwargs):
        self.input_file = input_file
        self.status_msg = "Initializing..."
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        self.language=self.detect_language(self.input_file)
        yield TextArea.code_editor(id="txt", text="Loading...", language=self.language)#, tab_behavior="indent")
        yield Static(self.status_msg, id="status")
        # yield Log(self.status_msg, id="status", auto_scroll=True)
        yield Footer()

    def action_save(self):
        self.set_status(f"Saving {self.input_file}...",False)
        txt = self.query_one("#txt", TextArea).text
        write_file(self.input_file,txt)
        self.set_status()

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        # timestamp = datetime.now().strftime("%H:%M:%S")
        # self.query_one("#status", Log).write_line(f"{timestamp}: {msg}")
        self.query_one("#status", Static).update(msg)  # .write_line(msg)

    def on_ready(self) -> None:
        ta = self.query_one("#txt", TextArea)
        #ta.language = self.detect_language(self.input_file)
        ta.text=read_file(self.input_file)
        self.set_status(f"Editing {self.input_file} - Language: {self.language}")

def main():
    args = sys.argv[1:]
    input_file = "dummy.txt" if len(args) == 0 else args[0]
    app = WriterApp(input_file=input_file)
    app.run()

if __name__ == "__main__":
    main()
