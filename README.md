# AutoClicker

A simple Windows-only Python autoclicker with a visual status window, fixed click location, progress tracking, pause/resume controls, and an emergency stop key.

This tool is intended for personal desktop automation. Do not use it in games, websites, or applications where autoclicking violates rules, terms of service, or could get your account banned.

## Features

* Choose the total number of clicks before starting
* Choose the interval between clicks
* Select the click location by moving your mouse and pressing `Enter`
* See live mouse coordinates during setup
* 10-second start delay before clicking begins
* Visual status window that can be resized
* Green visual flash when a click happens
* Runtime timer
* Countdown to the next click
* Current click count and total click count
* Remaining click count
* Terminal progress bar
* `Space` to pause/resume
* `Esc` emergency stop

## Requirements

This project is for **Windows only**.

You need:

* Windows 10 or Windows 11
* Python 3.10 or newer
* `pip`

## Install Python on Windows

1. Go to the official Python download page:

   [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. Download the latest stable Windows installer.

3. Run the installer.

4. Very important: enable this checkbox before installing:

   ```text
   Add python.exe to PATH
   ```

5. Click **Install Now**.

6. After installation, open PowerShell and check that Python works:

   ```powershell
   python --version
   ```

   You should see something like:

   ```text
   Python 3.12.x
   ```

7. Check that `pip` works:

   ```powershell
   pip --version
   ```

## Download the Project

Open PowerShell and go to the folder where you want to store the project.

Example:

```powershell
cd $HOME\Documents
```

Clone the repository:

```powershell
git clone https://github.com/S1146468/AutoClicker.git
```

Enter the project folder:

```powershell
cd AutoClicker
```

If you do not have Git installed, download the repository as a ZIP file from GitHub, extract it, then open PowerShell inside the extracted folder.

## Install Dependencies

Install the required Python packages:

```powershell
pip install pyautogui pynput
```

If `pip` does not work, try:

```powershell
python -m pip install pyautogui pynput
```

## Run the AutoClicker

From inside the project folder, run:

```powershell
python autoclicker.py
```

If your script has a different filename, replace `autoclicker.py` with the correct filename.

Example:

```powershell
python main.py
```

## How to Use

When the script starts, it asks:

```text
How many total clicks?
```

Enter the total number of clicks you want.

Example:

```text
20
```

Then it asks:

```text
Click interval in seconds?
```

Enter how long the script should wait between clicks.

Example:

```text
1
```

This means the script will wait 1 second after each click before the next click starts.

Next, the script asks you to choose the click location.

Move your mouse to the location where you want the autoclicker to click. While doing this, the terminal shows your current mouse coordinates.

When your mouse is in the correct location, press:

```text
Enter
```

The script will print the selected coordinates.

Example:

```text
Selected click location: x=850, y=420
```

After setup, a status window opens. You can resize this window before starting.

The script then asks you to press `Enter` one more time:

```text
Press ENTER to start the autoclicker.
```

After pressing `Enter`, the autoclicker waits 10 seconds before it starts clicking.

## Controls

| Key        | Action                          |
| ---------- | ------------------------------- |
| `Enter`    | Confirm setup steps             |
| `Space`    | Pause or resume the autoclicker |
| `Esc`      | Stop the autoclicker safely     |
| `Ctrl + C` | Stop from PowerShell            |

The `Space` key has a 1-second debounce. That means pressing it repeatedly too fast will be ignored.

## Status Window

The status window shows:

* Current state: `READY`, `STARTING`, `CLICK`, `PAUSED`, or `STOPPED`
* Countdown to the next click
* Current click number / total clicks
* Number of clicks remaining
* Runtime
* Selected click location

The window flashes green when a click is triggered.

The actual mouse click duration is fixed in the script:

```python
CLICK_DURATION = 0.15
```

The green visual flash duration is fixed separately:

```python
GREEN_FLASH_DURATION = 1.0
```

The starting delay is:

```python
START_DELAY = 10
```

You can edit these values in the script if needed.

## Example Session

Example input:

```text
How many total clicks? Press Enter after typing: 5
Click interval in seconds? Press Enter after typing: 1
```

Then move your mouse to the target location and press `Enter`.

Example setup summary:

```text
Setup complete.
Total clicks: 5
Click interval: 1.0 seconds
Click duration: 0.15 seconds
Green box flash duration: 1.0 seconds
Starting delay: 10 seconds
Click location: x=850, y=420
```

Then press `Enter` to start.

The script waits 10 seconds, then starts clicking.

At the end, it prints:

```text
Finished.
Total clicks: 5
Total time: 00h00m04s
```

## Troubleshooting

### `python` is not recognized

Python is probably not added to PATH.

Try:

```powershell
py --version
```

If that works, run the script with:

```powershell
py autoclicker.py
```

You can also reinstall Python and make sure this checkbox is enabled:

```text
Add python.exe to PATH
```

### `pip` is not recognized

Try:

```powershell
python -m pip install pyautogui pynput
```

Or:

```powershell
py -m pip install pyautogui pynput
```

### The status window does not appear

Make sure the script is running from a normal Windows desktop session, not from a remote/headless terminal.

The status window uses Python's built-in `tkinter` library. Standard Python installers for Windows normally include it.

### The mouse clicks the wrong location

Run the script again and select the click location carefully.

During setup, watch the live coordinates in the terminal. Move the mouse exactly where you want the script to click, then press `Enter`.

### The progress bar wraps onto multiple lines

Your PowerShell window is too narrow. Make it wider, or reduce the progress bar length inside the script.

Find:

```python
def print_progress(current: int, total: int, bar_length: int = 25):
```

Change `25` to a smaller number, for example:

```python
def print_progress(current: int, total: int, bar_length: int = 15):
```

## Safety Notes

Use this script carefully.

Autoclickers can cause unwanted clicks if you select the wrong location. Always keep the `Esc` key ready.

Do not use this script in software where automation is forbidden. That includes many games, websites, and online services.

## Repository

This README is intended for:

[https://github.com/S1146468/AutoClicker.git](https://github.com/S1146468/AutoClicker.git)
