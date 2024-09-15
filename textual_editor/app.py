#!python3

# https://textual.textualize.io/widgets/input/
import sys
import os
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import TextArea, Header, Footer, Static, DirectoryTree
from textual.binding import Binding


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


class TextEditor(App):
    """A simple Textual text editor."""

    #####################
    ### Textual setup ###
    #####################

    TITLE = "Text Editor"
    BINDINGS = [
        Binding(key="ctrl+s", action="save", description="Save"),
        ("ctrl+o", "open", "Open"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, *args, input_file, **kwargs):
        self.current_file = input_file # might be None
        self.current_dir = os.path.dirname(input_file)  if input_file else os.getcwd()
        self.status_msg = "Initializing..."
        self.language = "markdown"  # default language
        self.file_panel_width = 40
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
#        with Horizontal():
        file_panel = DirectoryTree(path=self.current_dir, id="file_panel")
        file_panel.styles.dock = "left"
        file_panel.styles.width =  self.file_panel_width
        yield file_panel
        yield TextArea.code_editor(id="text_area", text="Please select a file...", disabled=True)
        yield Static(self.status_msg, id="status_area")
        # yield Log(self.status_msg, id="status_area", auto_scroll=True)
        yield Footer()

    #################
    ### On_ hooks ###
    #################

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.load_file(event.path)

    def on_mount(self) -> None:
        self.load_file(self.current_file)

    def on_ready(self) -> None:
        self.set_status(f"Editing {self.current_file} - Language: {self.language}")
        if self.current_file is None:
            self.query_one("#file_panel", DirectoryTree).focus()
        else:
            self.query_one("#text_area", TextArea).focus()


    #################
    ###  actions  ###
    #################

    def action_save(self):
        self.set_status(f"Saving {self.current_file}...", False)
        text_content = self.query_one("#text_area", TextArea).text
        write_file(self.current_file, text_content)
        self.set_status()

    def action_open(self):
        self.show_file_panel()

    #################
    ###  methods  ###
    #################

    def show_file_panel(self):
        """show directory tree panel"""
        self.query_one("#file_panel", DirectoryTree).styles.width =  self.file_panel_width

    def hide_file_panel(self):
        """hide directory tree panel"""
        self.query_one("#file_panel", DirectoryTree).styles.width =  0

    def load_file(self, file_path):
        if file_path is not None :
            self.current_file = file_path
            self.current_dir  = os.path.dirname(file_path) 
            self.hide_file_panel()
            text_area = self.query_one("#text_area", TextArea)
            self.language = self.detect_file_language(text_area, file_path)
            text_area.language = self.language
            text_area.disabled = False
            if os.path.exists(file_path):
                # read file
                text_area.text = read_file(file_path)
                self.set_status(f"{file_path} loaded")
            else:
                # create new file
                text_area.text = ""
                self.set_status(f"Creating {file_path}")
    
    def detect_file_language(self, text_area: TextArea, file_path: str):
        filename, file_extension = os.path.splitext(file_path)
        languages = {"." + e: e for e in text_area.available_languages}
        extensions = {
            ".yml": "yaml",
            ".py": "python",
            ".js": "javascript",
            ".md": "markdown",
            ".sh": "bash",
        }
        if file_extension in languages:
            return languages[file_extension]
        if file_extension in extensions:
            return extensions[file_extension]
        return "markdown"

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        # timestamp = datetime.now().strftime("%H:%M:%S")
        # self.query_one("#status_area", Log).write_line(f"{timestamp}: {msg}")
        self.query_one("#status_area", Static).update(msg)  # .write_line(msg)

def main():
    args = sys.argv[1:]
    arg_file = None if len(args) == 0 else args[0]
    app = TextEditor(input_file=arg_file)
    app.run()


if __name__ == "__main__":
    main()
