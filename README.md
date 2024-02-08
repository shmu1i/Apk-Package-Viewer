# APK Package Viewer

## Introduction
APK Package Viewer is a simple tool built with PyQt5 and Androguard to facilitate the exploration and management of Android application packages (APK files). This tool allows users to view essential information about APK files, such as file names, package names, and file paths. Additionally, it provides functionality for opening files, exploring folders, copying file paths, and renaming files directly within the application.

## Features
- Browse and view information for multiple APK files within a specified folder.
- Open individual APK files or explore the containing folder.
- Copy the file path of selected APK files with the option to include double quotes.
- Rename APK files directly within the application.
- User-friendly interface with a responsive progress bar for loading files.

## Usage
1. Click the "Select Folder" button to choose a folder containing APK files.
2. View the list of APK files with details such as file name, package name, and file path.
3. Double-click on an item to open the corresponding file or right-click to access additional options.
4. Use the context menu to open files, explore folders, copy file paths, and rename files.

## Requirements
- Python 3.x
- PyQt5
- Androguard

## Installation
1. Install required Python packages:
   
   `pip install PyQt5 androguard`

2. Run the application:

     `python apk_package_viewer.py`

## Acknowledgments

- Androguard: https://github.com/androguard/androguard

