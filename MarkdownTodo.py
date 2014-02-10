import sublime, sublime_plugin
from datetime import datetime

class MarkdownTodoBase(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        # list of allowed filetypes
        allowed_filetypes = ('.md', '.markdown', '.mdown')
        if filename is None or not filename.endswith(allowed_filetypes):
            return False
        self.runCommand(edit)

class TodoAddCommand(MarkdownTodoBase):
    # FIXME - this isn't implemented
    def runCommand(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                # don't add a newline when creating new item with cursor is at an empty line
                if not line:
                    line_contents = '- '
                    self.view.insert(edit, line.begin(), line_contents)
                # add a newline when creating new item when cursor is at another line
                else:
                    line_contents = self.view.substr(line) + '\n- '
                    self.view.replace(edit, line, line_contents)

class TodoDoneCommand(MarkdownTodoBase):
    def runCommand(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                line_head = self.view.find("[-\+]", line.begin())
                line_contents = self.view.substr(line).strip()
                # prepend @done if item is ongoing
                if line_contents.startswith('-'):
                    self.view.replace(edit, line_head, "+ @done (%s)" % datetime.now().strftime("%Y-%m-%d %H:%M"))
                # undo @done
                elif line_contents.startswith('+'):
                    subfix = self.view.find('(\s)*@done \([^)]+\)', line.begin())
                    self.view.erase(edit, subfix)
                    self.view.replace(edit, line_head, "-")

class TodoArchiveCommand(MarkdownTodoBase):
    def runCommand(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                line_head = self.view.find("[-\+]", line.begin())
                line_contents = self.view.substr(line).strip()
                if line_contents.startswith('+'):
                    if line_contents.find('(\s)*@done(.)+\)$', line.begin()):
                        # FIXME: line deleted from current file, but also need to delete newline,
                        # and need to append line to archive.md
                        subfix = self.view.find('(\s)*@done(.)+\)$', line.begin())
                        self.view.erase(edit, line)

class TodoWaitCommand(MarkdownTodoBase):
    # FIXME - this isn't implemented
    def runCommand(self, edit):
        pass

class TodoSomedayCommand(MarkdownTodoBase):
    # FIXME - this isn't implemented
    def runCommand(self, edit):
        pass
