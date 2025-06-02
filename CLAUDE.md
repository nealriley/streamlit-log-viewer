# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Focus on project root when performing your actions. The following files are meant to guide you while developing:
- .vibe/docs
- .vibe/tasks
- .vibe/ERRORS.md
- .vibe/INSTRUCTIONS.md
- .vibe/LINKS.md

Your instructions you will follow are in INSTRUCTIONS.md. If INSTRUCTIONS.md is empty, check .vibe/tasks for any open tasks, determine which task is best to complete next and ask the user for permission to continue with the task in question. If there are no INSTRUCTIONS or TASKS, continue with your assumption of what the user is looking to achieve. 

Any errors that occured in a previous development iteration are stored in ERRORS.md. If no errors are found,it is either the first iteration or no errors have occurred. 

Add any tasks that need actioning are in the tasks/ folder. By default there will be one TASKS.md file, however there may be more taks in this folder, read all tasks in the folder.  When a task is complete, update the relevant task file showing that this task is completed. Do so in a way that makes it easy to scan later for open and closed tasks. 

Relevant documentation can be found in the folder .vibe/docs. You will find different formats of document there, use this to supplement your approach, your understanding, and your actions. You may choose to use these documents if you need more context or guidance. Not every task will require this action. 

There are a set of external documentation, in the form of a Title and Link, in the LINKS.md file. This list will allow you to quickly navigate to relevant documentation, guides, information to perform your action in the best possible way. 

## Architecture

No specific architecture has been established yet. This template is ready for any type of project setup.

## Development Commands

No build, test, or lint commands have been configured yet. These should be added as the project evolves with specific technologies and frameworks.