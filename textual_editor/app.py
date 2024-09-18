#!python3

# https://textual.textualize.io/widgets/input/
import sys
from pathlib import Path, PurePath
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import TextArea, Header, Footer, Static, DirectoryTree, Log
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

    def __init__(self, *args, arg_file_or_path, **kwargs):
        self.arg_file_or_path = arg_file_or_path
        self.current_file = None
        self.current_dir = None
        self.status_msg = "Initializing..."
        self.language = "markdown"  # default language
        self.file_panel_width = 40
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        file_panel = DirectoryTree(path=".", id="file_panel")
        file_panel.styles.dock = "left"
        file_panel.styles.width =  self.file_panel_width
        yield file_panel
        yield TextArea.code_editor(id="text_area", text="Please select a file...", disabled=True)
        yield Static(self.status_msg, id="status_area")
        yield Log("Loading...", id="log_area", auto_scroll=True)
        yield Footer()

    #################
    ### On_ hooks ###
    #################

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.load_file(event.path)

    def on_mount(self) -> None:
        # calculate starting file and dir
        start_file = None
        start_dir = Path.cwd()
        if self.arg_file_or_path is not None:
            fp = Path(self.arg_file_or_path)
            if fp.is_dir():# only true if exists and is a directory
                start_file = None
                start_dir = fp
            elif fp.is_file():# only true if exists and is a file
                start_file = fp
                start_dir = fp.parent
            elif not fp.exists():
                try:
                    write_file(fp, "")
                    start_file = fp
                    start_dir = fp.parent
                except IOError as e:
                    self.write_to_log("Error creating file", e, "error")            
        # store the current file and directory
        self.current_file = start_file.resolve() if start_file is not None else None
        self.current_dir = start_dir.resolve()
        # set the directory tree start dir
        self.query_one("#file_panel", DirectoryTree).path = str(self.current_dir)
        # load the file
        if self.current_file is not None:
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
        if Path(file_path).exists():
            self.current_file = file_path
            self.current_dir  = PurePath(file_path).parent()
            self.hide_file_panel()
            # detect language from extension
            text_area = self.query_one("#text_area", TextArea)
            self.language = self.detect_file_language(text_area, file_path)
            text_area.language = self.language
            text_area.disabled = False    
            # read file
            text_area.text = read_file(file_path)
            self.set_status(f"{file_path} loaded")
    
    def detect_file_language(self, text_area: TextArea, file_path: str):
        file_extension = PurePath(file_path).suffix
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

    def write_to_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.query_one("#log_area", Log).write_line(f"{timestamp}: {msg}")

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        self.query_one("#status_area", Static).update(msg)

def main():
    args = sys.argv[1:]
    arg_file_or_path = None if len(args) == 0 else args[0]
    app = TextEditor(arg_file_or_path=arg_file_or_path)
    app.run()


if __name__ == "__main__":
    main()
