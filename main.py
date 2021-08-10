from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"

# GLOBALS
REPS = 0
TIMER = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(TIMER)
    # set heading back to timer
    timer_label.config(text="Timer")
    # remove all check marks
    check_label.config(text="")
    # set timer to 00:00
    canvas.itemconfig(canvas_timer_text, text="00:00")
    # reset REPS to 0
    global REPS
    REPS = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    # access global REPS
    global REPS
    REPS += 1

    # if REPS = ODD -> Work
    # if REPS is divisible by 8 -> Long Break
    # if REPS = EVEN -> Short Break

    # EVEN Rep - break
    if REPS % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(LONG_BREAK_MIN * 60)
    elif REPS % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        timer_label.config(text="Break", fg=PINK)
    # ODD Rep - work
    else:
        timer_label.config(text="Work", fg=GREEN)
        count_down(WORK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(seconds):
    # format the seconds to look like time - mm:ss
    mins = str(seconds // 60)
    secs = str(seconds % 60)
    time_remaining = f"{mins.zfill(2)}:{secs.zfill(2)}"
    # grab the canvas object and update timer value
    canvas.itemconfig(canvas_timer_text, text=time_remaining)
    if seconds > 0:
        # decrement the counter until its zero after each second
        global TIMER
        TIMER = window.after(1000, count_down, seconds - 1)
    if seconds == 0:
        get_checks = check_label.cget("text")
        global REPS
        if REPS % 16 == 0:
            get_checks += "\n"
        if REPS % 2 == 1:
            get_checks += CHECK_MARK
        check_label.config(text=get_checks, fg=GREEN, font=(FONT_NAME, 12, "bold"), bg=YELLOW)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=110, pady=50, background=YELLOW)

# Setup the Canvas() to display tomato image and timer text
canvas = Canvas(width=200, height=224, background=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
canvas_timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 24, "bold"))
canvas.grid(row=1, column=1)

# create the application label
# timer - can have value either Timer, Work or Break
timer_label = Label(text="Timer", bg=YELLOW, font=(FONT_NAME, 36, "bold"))
timer_label.config(fg=GREEN)
timer_label.grid(row=0, column=1)

# check mark - depends on logic
# put it at row=3, col=1
check_label = Label(text="", fg=GREEN, font=(FONT_NAME, 12, "bold"), bg=YELLOW)
check_label.grid(row=3, column=1)

# create application buttons - Start and Reset
# Start
start_btn = Button(text="Start", command=start_timer)
start_btn.grid(row=2, column=0)

# Reset
reset_btn = Button(text="Reset", command=reset_timer)
reset_btn.grid(row=2, column=2)

window.mainloop()
