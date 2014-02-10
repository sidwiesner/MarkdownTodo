# Markdown todo plugin for Sublime Text

This is focused on my personal workflow using separate markdown files for a GTD workflow.

## Files used

- todo.md - current tasks and work for today and this week
- archive.md - completed tasks
- waiting.md - waiting for task list
- someday.md - someday/maybe list

In addition, I use subfolders (e.g. project, reference) for other GTD related files. I want the same commands to work there, but push to the relevant root level files.

## Commands and actions

- add_todo -- copy item from current file to todo.md (append line)
- done     -- mark item as done with formatting
- archive  -- move all done items in current file to archive.md file
- wait     -- add wait formatting, and if in special files, move to waiting
- someday  -- if in special files, move to someday
