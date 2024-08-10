#!python3

# https://textual.textualize.io/widgets/input/

import sys
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

    def __init__(self, *args, input_file, **kwargs):
        self.input_file = input_file
        self.status_msg = "Initializing..."
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        yield TextArea(
            id="txt_input", text=read_file(self.input_file), tab_behavior="indent"
        )
        yield Static(self.status_msg, id="status_log")
        yield Footer()

    def action_save(self):
        self.set_status("Saving...")
        txt = self.query_one("#txt_input", TextArea).text
        write_file(self.input_file,txt)

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        self.query_one("#status_log", Static).update(msg)  # .write_line(msg)

def main():
    args = sys.argv[1:]
    input_file = "dummy.txt" if len(args) == 0 else args[0]
    app = WriterApp(input_file=input_file)
    app.run()

if __name__ == "__main__":
    main()
