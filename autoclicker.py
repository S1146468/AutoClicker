import time
import threading
import pyautogui
from pynput import keyboard
import tkinter as tk


CLICK_DURATION = 0.15
GREEN_FLASH_DURATION = 1.0
START_DELAY = 10

DEFAULT_WINDOW_WIDTH = 360
DEFAULT_WINDOW_HEIGHT = 220

stop_requested = False
paused = False
last_space_press_time = 0

root = None
status_frame = None
status_label = None
runtime_label = None
countdown_label = None
click_progress_label = None
remaining_label = None
location_label = None

current_status_text = "READY"
current_status_color = "#222222"
flash_id = 0


def format_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}h{minutes:02d}m{secs:02d}s"


def print_progress(current: int, total: int, bar_length: int = 25):
    progress = current / total
    filled = int(bar_length * progress)
    bar = "#" * filled + "-" * (bar_length - filled)
    percent = progress * 100

    print(
        f"\r[{bar}] {percent:5.1f}% ({current}/{total})",
        end="",
        flush=True
    )


def update_window_background(color: str):
    if root is None:
        return

    widgets = [
        status_frame,
        status_label,
        runtime_label,
        countdown_label,
        click_progress_label,
        remaining_label,
        location_label,
    ]

    for widget in widgets:
        if widget is not None:
            widget.config(bg=color)


def set_status(text: str, color: str):
    global current_status_text, current_status_color

    current_status_text = text
    current_status_color = color

    if root is None:
        return

    def update():
        update_window_background(color)
        if status_label is not None:
            status_label.config(text=text)

    root.after(0, update)


def flash_green_for_click():
    global flash_id

    flash_id += 1
    this_flash_id = flash_id

    if root is None:
        return

    def turn_green():
        update_window_background("lime")
        if status_label is not None:
            status_label.config(text="CLICK")

    def restore_color():
        if this_flash_id == flash_id:
            update_window_background(current_status_color)
            if status_label is not None:
                status_label.config(text=current_status_text)

    root.after(0, turn_green)
    root.after(int(GREEN_FLASH_DURATION * 1000), restore_color)


def set_runtime_text(text: str):
    if runtime_label is None or root is None:
        return

    root.after(0, lambda: runtime_label.config(text=text))


def set_countdown_text(text: str):
    if countdown_label is None or root is None:
        return

    root.after(0, lambda: countdown_label.config(text=text))


def set_click_progress_text(current: int, total: int):
    if click_progress_label is None or root is None:
        return

    root.after(
        0,
        lambda: click_progress_label.config(
            text=f"Click: {current} / {total}"
        )
    )


def set_remaining_text(remaining: int):
    if remaining_label is None or root is None:
        return

    root.after(
        0,
        lambda: remaining_label.config(
            text=f"Remaining: {remaining} clicks"
        )
    )


def set_location_text(x: int, y: int):
    if location_label is None or root is None:
        return

    root.after(
        0,
        lambda: location_label.config(
            text=f"Location: x={x}, y={y}"
        )
    )


def on_press(key):
    global stop_requested, paused, last_space_press_time

    if key == keyboard.Key.esc:
        stop_requested = True
        paused = False
        print("\nESC pressed. Stopping safely...")
        set_status("STOPPED", "red")
        return False

    if key == keyboard.Key.space:
        now = time.time()

        if now - last_space_press_time < 1:
            return

        last_space_press_time = now
        paused = not paused

        if paused:
            print("\nPaused. Press SPACE again to resume.")
            set_status("PAUSED", "orange")
            set_countdown_text("Paused")
        else:
            print("\nResumed.")
            set_status("READY", "#222222")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a whole number.")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Enter a number equal to or greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a number, for example 1 or 0.25.")


def live_mouse_position_display(stop_event: threading.Event):
    while not stop_event.is_set():
        x, y = pyautogui.position()
        print(f"\rCurrent mouse coordinates: x={x}, y={y}    ", end="", flush=True)
        time.sleep(0.05)


def select_click_location():
    print("\nMove your mouse to the desired click location.")
    print("Press ENTER to select the current mouse position.")

    stop_event = threading.Event()

    display_thread = threading.Thread(
        target=live_mouse_position_display,
        args=(stop_event,),
        daemon=True
    )
    display_thread.start()

    input()

    stop_event.set()
    display_thread.join(timeout=0.2)

    x, y = pyautogui.position()
    print(f"\nSelected click location: x={x}, y={y}")

    return x, y


def wait_seconds(duration: float, countdown_prefix: str = "Next click in"):
    remaining = duration
    last_time = time.time()

    while remaining > 0:
        if stop_requested:
            return False

        while paused:
            if stop_requested:
                return False
            last_time = time.time()
            time.sleep(0.05)

        now = time.time()
        elapsed = now - last_time
        last_time = now

        remaining -= elapsed
        visible_remaining = max(0, remaining)

        set_countdown_text(f"{countdown_prefix}: {visible_remaining:.1f}s")

        time.sleep(0.05)

    return True


def wait_while_paused():
    while paused:
        if stop_requested:
            return False
        time.sleep(0.05)

    return True


def countdown_before_start():
    set_status("STARTING", "#444444")

    print(f"\nStarting in {START_DELAY} seconds...")
    print("Failsafe: press ESC to stop.")
    print("Pause/resume: press SPACE. Resume only works after at least 1 second.\n")

    for remaining in range(START_DELAY, 0, -1):
        if stop_requested:
            return False

        set_countdown_text(f"Starting in: {remaining}s")
        print(f"\rStarting in: {remaining} seconds ", end="", flush=True)
        time.sleep(1)

    print("\n")
    set_countdown_text("Next click in: 0.0s")
    set_status("READY", "#222222")
    return True


def run_autoclicker(total_clicks_requested: int, click_interval: float, click_x: int, click_y: int):
    global stop_requested

    completed_clicks = 0

    set_click_progress_text(completed_clicks, total_clicks_requested)
    set_remaining_text(total_clicks_requested)

    if not countdown_before_start():
        return

    start_time = time.time()

    try:
        for _ in range(total_clicks_requested):
            if stop_requested:
                break

            if not wait_while_paused():
                break

            elapsed = time.time() - start_time
            set_runtime_text(f"Runtime: {format_time(elapsed)}")
            set_countdown_text("Clicking now")

            pyautogui.moveTo(click_x, click_y)

            flash_green_for_click()

            pyautogui.mouseDown()
            if not wait_seconds(CLICK_DURATION, countdown_prefix="Click held for"):
                pyautogui.mouseUp()
                break
            pyautogui.mouseUp()

            completed_clicks += 1
            remaining_clicks = total_clicks_requested - completed_clicks

            set_click_progress_text(completed_clicks, total_clicks_requested)
            set_remaining_text(remaining_clicks)

            print_progress(completed_clicks, total_clicks_requested)

            elapsed = time.time() - start_time
            set_runtime_text(f"Runtime: {format_time(elapsed)}")

            if completed_clicks < total_clicks_requested:
                if not wait_seconds(click_interval, countdown_prefix="Next click in"):
                    break

    except KeyboardInterrupt:
        print("\nCTRL+C pressed. Stopping safely...")

    finally:
        stop_requested = True
        set_status("STOPPED", "red")

        end_time = time.time()
        total_time = end_time - start_time if "start_time" in locals() else 0

        set_runtime_text(f"Done: {format_time(total_time)}")
        set_countdown_text("Finished")
        set_click_progress_text(completed_clicks, total_clicks_requested)
        set_remaining_text(total_clicks_requested - completed_clicks)

        print("\n\nFinished.")
        print(f"Total clicks: {completed_clicks}")
        print(f"Total time: {format_time(total_time)}")

        if root is not None:
            root.after(2500, root.quit)


def create_status_box(click_x: int, click_y: int):
    global root
    global status_frame
    global status_label
    global runtime_label
    global countdown_label
    global click_progress_label
    global remaining_label
    global location_label

    root = tk.Tk()
    root.title("Autoclicker Status")

    root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}+50+50")
    root.minsize(260, 160)
    root.resizable(True, True)
    root.attributes("-topmost", True)

    status_frame = tk.Frame(root, bg="#222222")
    status_frame.pack(fill="both", expand=True)

    status_label = tk.Label(
        status_frame,
        text="READY",
        bg="#222222",
        fg="white",
        font=("Arial", 26, "bold")
    )
    status_label.pack(fill="x", pady=(12, 4))

    countdown_label = tk.Label(
        status_frame,
        text="Waiting to start",
        bg="#222222",
        fg="white",
        font=("Arial", 15, "bold")
    )
    countdown_label.pack(fill="x", pady=2)

    click_progress_label = tk.Label(
        status_frame,
        text="Click: 0 / 0",
        bg="#222222",
        fg="white",
        font=("Arial", 14, "bold")
    )
    click_progress_label.pack(fill="x", pady=2)

    remaining_label = tk.Label(
        status_frame,
        text="Remaining: 0 clicks",
        bg="#222222",
        fg="white",
        font=("Arial", 14, "bold")
    )
    remaining_label.pack(fill="x", pady=2)

    runtime_label = tk.Label(
        status_frame,
        text="Runtime: 00h00m00s",
        bg="#222222",
        fg="white",
        font=("Arial", 13, "bold")
    )
    runtime_label.pack(fill="x", pady=2)

    location_label = tk.Label(
        status_frame,
        text=f"Location: x={click_x}, y={click_y}",
        bg="#222222",
        fg="white",
        font=("Arial", 11)
    )
    location_label.pack(fill="x", pady=(4, 10))

    return root


def main():
    total_clicks_requested = get_positive_int("How many total clicks? Press Enter after typing: ")
    click_interval = get_non_negative_float("Click interval in seconds? Press Enter after typing: ")

    click_x, click_y = select_click_location()

    create_status_box(click_x, click_y)

    set_click_progress_text(0, total_clicks_requested)
    set_remaining_text(total_clicks_requested)
    set_location_text(click_x, click_y)

    print("\nSetup complete.")
    print(f"Total clicks: {total_clicks_requested}")
    print(f"Click interval: {click_interval} seconds")
    print(f"Click duration: {CLICK_DURATION} seconds")
    print(f"Green box flash duration: {GREEN_FLASH_DURATION} seconds")
    print(f"Starting delay: {START_DELAY} seconds")
    print(f"Click location: x={click_x}, y={click_y}")

    print("\nThe status window is now open.")
    print("You can resize the status window before starting.")
    print("\nPress ENTER to start the autoclicker.")
    print(f"After pressing ENTER, the autoclicker will start after a {START_DELAY}-second delay.")

    start_confirmed = threading.Event()

    def wait_for_enter():
        input()
        start_confirmed.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()

    def check_start():
        if start_confirmed.is_set():
            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            worker = threading.Thread(
                target=run_autoclicker,
                args=(total_clicks_requested, click_interval, click_x, click_y),
                daemon=True
            )
            worker.start()
        else:
            root.after(100, check_start)

    root.after(100, check_start)
    root.mainloop()


if __name__ == "__main__":
    main()