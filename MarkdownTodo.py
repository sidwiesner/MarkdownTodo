import datetime
import os
import sublime
import sublime_plugin

class MarkdownTodoBase(sublime_plugin.TextCommand):
    """Base class for Markdown Todo actions"""
    def configure(self):
        self.settings = sublime.load_settings('MarkdownTodo.sublime-settings')
        self.archive_file = self.get_filename("archive_file")
        self.todo_file    = self.get_filename("todo_file")
        self.waiting_file = self.get_filename("waiting_file")
        self.someday_file = self.get_filename("someday_file")

    def get_filename(self, key):
        if self.settings is None:
            return ""
        return os.path.join(self.find_root_directory(), self.settings.get(key))

    def find_root_directory(self):
        # FIXME: this is too simplistic. Should do a downward directory search
        # done to make sure this is actually the right directory to use.
        if self.root_directory is not None and self.root_directory != "":
            return self.root_directory
        self.root_directory = os.path.dirname(self.view.file_name())
        return self.root_directory

    def valid_markdown_extension(self, filename):
        allowed_filetypes = ('.md', '.markdown', '.mdown')
        if filename is None:
            return False
        return filename.endswith(allowed_filetypes)

    def run(self, edit):
        self.configure()
        if not valid_file_extension(self.view.file_name()):
            return False
        self.runCommand(edit)

class MarkdownTodoAddCommand(MarkdownTodoBase):
    """Description"""
    def runCommand(self, edit):
        # FIXME: this isn't implemented
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                # don't add a newline when creating new item with cursor is at
                # an empty line
                if not line:
                    line_contents = '- '
                    self.view.insert(edit, line.begin(), line_contents)
                # add a newline when creating new item when cursor is at another
                # line
                else:
                    line_contents = self.view.substr(line) + '\n- '
                    self.view.replace(edit, line, line_contents)

class MarkdownTodoDoneCommand(MarkdownTodoBase):
    """Mark item as done, prepending the @done and current date/time. Can also
       be used to reverse its own effects."""
    def runCommand(self, edit):
        # Only pay attention to current selection
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                line_head = self.view.find("[-\+]", line.begin())
                line_contents = self.view.substr(line).strip()
                # prepend @done if item is ongoing
                if line_contents.startswith('-'):
                    self.view.replace(edit, line_head, "+ @done (%s)" %
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                # undo @done
                elif line_contents.startswith('+'):
                    subfix = self.view.find('\s*@done \([^)]+\)', line.begin())
                    self.view.erase(edit, subfix)
                    self.view.replace(edit, line_head, "-")

class MarkdownTodoArchiveCommand(MarkdownTodoBase):
    """Move done items to the archive file."""
    def runCommand(self, edit):
        # FIXME: should be looking only at specific files to archive
        # FIXME: would like to put the lines in archive file in sorted order
        archive_lines = self.view.find_all('\s*\+ @done.+$')
        archive_lines.reverse() # reverse because it is destructive change
        # print ("Matches =", len(archive_lines))
        with open(self.archive_file, "a") as archive_file:
            for line in archive_lines:
                # print ("Region found =", line)
                line_contents = self.view.substr(line).strip()
                # FIXME: handle any type of line endings
                # self.view.line_endings()
                archive_file.write(line_contents + "\n")
                # FIXME: delete new line from old file too
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
