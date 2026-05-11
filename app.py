from tkinter import *
from just_playback import Playback
import time

# Audio Setup
playback = Playback()
timer_id = None 

def play_alarm():
    try:
        playback.load_file('alarm.mp3')
        playback.play()
    except Exception as e:
        print(f"Error loading sound: {e}")

def stop_alarm():
    try:
        playback.stop()
    except:
        pass

# --- Interaction Logic ---
def on_enter(e):
    e.widget['bg'] = "#333333"

def on_leave(e):
    if e.widget == btn_start:
        e.widget['bg'] = "#ea3548"
    elif e.widget == btn_reset:
        e.widget['bg'] = "#222"
    else:
        e.widget['bg'] = "#1e1e1e"

root = Tk()
root.title("Modern Timer")
root.geometry("450x700")
root.config(bg="#121212")
root.resizable(False, False)


# --- UI Elements ---
heading = Label(root, text="TIMER", font=("Impact", 40), bg="#121212", fg="#ea3548")
heading.pack(pady=(50, 5))

def clock(): 
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)

current_time = Label(root, font=("Consolas", 20, "bold"), text="", fg="#6B7B76", bg="#121212")
current_time.pack()
clock()

input_frame = Frame(root, bg="#121212")
input_frame.pack(pady=40)

entry_cfg = {
    "font": ("Helvetica", 55, "bold"), "bg": "#121212", "fg": "#ffffff", 
    "bd": 0, "highlightthickness": 0, "insertbackground": "white", "justify": CENTER
}

hrs, mins, sec = StringVar(value="00"), StringVar(value="00"), StringVar(value="00")

Entry(input_frame, textvariable=hrs, width=2, **entry_cfg).grid(row=0, column=0)
Label(input_frame, text=":", font=("Helvetica", 40), bg="#121212", fg="#ea3548").grid(row=0, column=1)
Entry(input_frame, textvariable=mins, width=2, **entry_cfg).grid(row=0, column=2)
Label(input_frame, text=":", font=("Helvetica", 40), bg="#121212", fg="#ea3548").grid(row=0, column=3)
Entry(input_frame, textvariable=sec, width=2, **entry_cfg).grid(row=0, column=4)

lbl_cfg = {"font": ("Arial", 9, "bold"), "bg": "#121212", "fg": "#444"}
Label(input_frame, text="HOURS", **lbl_cfg).grid(row=1, column=0)
Label(input_frame, text="MINUTES", **lbl_cfg).grid(row=1, column=2)
Label(input_frame, text="SECONDS", **lbl_cfg).grid(row=1, column=4)

# --- Functions ---

def update_timer(total_seconds):
    global timer_id
    if total_seconds >= 0:
        h, m, s = total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60
        hrs.set(f"{h:02d}"); mins.set(f"{m:02d}"); sec.set(f"{s:02d}")
        timer_id = root.after(1000, update_timer, total_seconds - 1)
    else:
        play_alarm()

def start_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
    try:
        total = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(sec.get())
        if total > 0:
            update_timer(total)
    except: pass

def reset_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
    stop_alarm()
    hrs.set("00"); mins.set("00"); sec.set("00")

def set_preset(h, m, s):
    hrs.set(f"{h:02d}"); mins.set(f"{m:02d}"); sec.set(f"{s:02d}")

# --- Presets ---
preset_frame = Frame(root, bg="#121212")
preset_frame.pack(pady=10)

btn_p_cfg = {"bg": "#1e1e1e", "fg": "white", "bd": 0, "highlightthickness": 0, "width": 8, "height": 2, "font": ("Arial", 10, "bold"), "cursor": "hand2"}

# Fallback text buttons if icons aren't found
try:
    img1 = PhotoImage(file="brush.png")
    b1 = Button(preset_frame, image=img1, bg="#121212", bd=0, highlightthickness=0, command=lambda: set_preset(0, 2, 0))
except:
    b1 = Button(preset_frame, text="BRUSH", command=lambda: set_preset(0, 2, 0), **btn_p_cfg)
b1.grid(row=0, column=0, padx=10)

try:
    img2 = PhotoImage(file="face.png")
    b2 = Button(preset_frame, image=img2, bg="#121212", bd=0, highlightthickness=0, command=lambda: set_preset(0, 15, 0))
except:
    b2 = Button(preset_frame, text="FACE", command=lambda: set_preset(0, 5, 0), **btn_p_cfg)
b2.grid(row=0, column=1, padx=10)

try:
    img3 = PhotoImage(file="eggs.png")
    b3 = Button(preset_frame, image=img3, bg="#121212", bd=0, highlightthickness=0, command=lambda: set_preset(0, 10, 0))
except:
    b3 = Button(preset_frame, text="EGGS", command=lambda: set_preset(0, 10, 0), **btn_p_cfg)
b3.grid(row=0, column=2, padx=10)

# --- Control Buttons ---

btn_start = Button(root, text="START TIMER", font=("Arial", 14, "bold"), bg="#ea3548", fg="white", 
                   bd=0, highlightthickness=0, width=20, height=2, cursor="hand2", command=start_timer)
btn_start.pack(pady=(40, 10))
btn_start.bind("<Enter>", lambda e: btn_start.config(bg="#ff5e6e"))
btn_start.bind("<Leave>", lambda e: btn_start.config(bg="#ea3548"))

btn_reset = Button(root, text="RESET", font=("Arial", 12, "bold"), bg="#222", fg="#fff", 
                   bd=0, highlightthickness=0, width=15, height=1, cursor="hand2", command=reset_timer)
btn_reset.pack(pady=5)
btn_reset.bind("<Enter>", on_enter)
btn_reset.bind("<Leave>", on_leave)

btn_stop = Button(root, text="STOP ALARM", font=("Arial", 11, "bold"), bg="#FF3D4D", fg="white", 
                  bd=0, highlightthickness=0, cursor="hand2", command=stop_alarm)
btn_stop.pack(pady=10)
btn_stop.bind("<Enter>", lambda e: btn_stop.config(fg="#0a2a55ff"))
btn_stop.bind("<Leave>", lambda e: btn_stop.config(fg="#444"))


line = Frame(root, bg="#1e1e1e", height=1, bd=0, highlightthickness=0)
line.pack(side=BOTTOM, fill=X, padx=100, pady=(0, 5))

# Copyright text
footer = Label(root, text="© 2026 Musfiquer Prottoy. All Rights Reserved", 
               font=("Arial", 9), bg="#121212", fg="#B8E0CB")
footer.pack(side=BOTTOM)

root.mainloop()