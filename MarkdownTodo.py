import datetime
import os
import sublime
import sublime_plugin

class MarkdownTodoBase(sublime_plugin.TextCommand):
    """Base class for Markdown Todo actions"""
    def configure(self):
        self.settings = sublime.load_settings('MarkdownTodo.sublime-settings')
        self.files = {
            "todo"   : self.get_filename("todo_file"),
            "archive": self.get_filename("archive_file"),
            "waiting": self.get_filename("waiting_file"),
            "someday": self.get_filename("someday_file"),
        }

    def run(self, edit):
        self.configure()
        if not self.valid_markdown_extension(self.view.file_name()):
            return False
        self.runCommand(edit)

    def get_filename(self, key):
        return os.path.join(self.find_root_directory(), self.settings.get(key))

    def find_root_directory(self):
        if hasattr(self, 'root_directory'):
            return self.root_directory
        else:
            key_file = self.settings.get("todo_file")
            # Want to search downward in in directory tree to find key file that
            # marks the actual root directory of the project
            current_root = os.path.dirname(self.view.file_name())
            path_found = False
            while not (path_found or current_root == ""):
                if os.path.exists(os.path.join(current_root, key_file)):
                    path_found = True
                else:
                    (current_root, filename) = os.path.split(current_root)
            if current_root == "":
                raise AttributeError
            self.root_directory = current_root
            return self.root_directory

    def valid_markdown_extension(self, filename):
        allowed_filetypes = ('.md', '.markdown', '.mdown')
        if filename is None:
            return False
        return filename.endswith(allowed_filetypes)

    def is_primary_todo_file(self):
        # check if currently open file is in special todo file list
        return self.view.file_name() in self.files.values()

    def get_line_ending(self):
        line_endings = {
            "Unix"   : '\n',
            "Windows": '\r\n',
            "CR"     : '\r',
        }
        return line_endings[self.view.line_endings()]

class MarkdownTodoAddCommand(MarkdownTodoBase):
    """Append todo items to the todo file."""
    def runCommand(self, edit):
        # Only pay attention to current selection(s)
        with open(self.files["todo"], "a") as todo_file:
            for region in self.view.sel():
                lines = self.view.lines(region)
                for line in lines:
                    line_contents = self.view.substr(line).strip()
                    todo_file.write(line_contents + self.get_line_ending())

class MarkdownTodoDoneCommand(MarkdownTodoBase):
    """Mark item as done, prepending the @done and current date/time. Can also
       be used to reverse its own effects."""
    def runCommand(self, edit):
        # Only pay attention to current selection(s)
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                line_head = self.view.find("[-\+]", line.begin())
                line_contents = self.view.substr(line).strip()
                # prepend @done if item is ongoing
                if line_contents.startswith('-'):
                    self.view.replace(edit, line_head, "+ @done (%s)" %
                        datetime.datetime.now().strftime("%Y-%m-%d"))
                # undo @done
                elif line_contents.startswith('+'):
                    subfix = self.view.find('\s*@done \([^)]+\)', line.begin())
                    self.view.erase(edit, subfix)
                    self.view.replace(edit, line_head, "-")

class MarkdownTodoArchiveCommand(MarkdownTodoBase):
    """Move done items to the archive file."""
    def runCommand(self, edit):
        # Only archive lines if file is one of the primary todo files
        if not self.is_primary_todo_file():
            return False
        # FIXME: would like to put the lines in archive file in sorted order
        archive_lines = self.view.find_all('\s*\+ @done.+$')
        archive_lines.reverse() # reverse because it is destructive change
        # print ("Matches =", len(archive_lines))
        with open(self.files["archive"], "a") as archive_file:
            for line in archive_lines:
                # print ("Region found =", line)
                line_contents = self.view.substr(line).strip()
                archive_file.write(line_contents + self.get_line_ending())
                self.view.erase(edit, line)

class MarkdownTodoWaitCommand(MarkdownTodoBase):
    """Description"""
    # FIXME: this isn't implemented
    def runCommand(self, edit):
        pass

class MarkdownTodoSomedayCommand(MarkdownTodoBase):
    """Description"""
    # FIXME: this isn't implemented
    def runCommand(self, edit):
        pass
