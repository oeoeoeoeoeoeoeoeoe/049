import turtle
import time
import tkinter as tk
from tkinter import OptionMenu, StringVar
import os
import pygame
import pytz
import datetime
pygame.init()

music = [
    "a-short-piano-intermezzo-218315.wav",
    "dramatic-background-music-piano-for-short-video-vlog-60-second-182221.wav",
    "epic-music-background-instrumental-for-video-dramatic-hip-hop-beat-176723.wav",
    "lilix27s-dream-116990.wav",
    "ordinary-day-8025.wav",
    "piano-guitar-duetensemble-slow-tempo-and-short-119063.wav",
    "skylight-240800.wav"
] # Danh sách nhạc đã tải sẵn ở máy.

utc = [f"GMT+{i}" for i in range(1, 13)]
utc.extend([f"GMT{i}" for i in range(-1, -13, -1)]) # Tạo danh sách các múi giowf
cur_tz = "GMT-7"

screen = turtle.Screen()
screen.setup(700, 700)
screen.title("Đồng hồ")
screen.tracer(0)

clk = turtle.Turtle()
clk.hideturtle()
clk.speed(0)
clk.width(1)
clk.color("blue")


def draw_clock_face(dd): # Vẽ đồng hồ
    cur_time = datetime.datetime.now(pytz.timezone(f"Etc/{cur_tz}")) # Lấy giờ hiện tại theo múi giờ đã chọn
    clk.clear()
    clk.up()
    clk.goto(0, 210)
    clk.setheading(180)
    clk.color("black")
    clk.pendown()
    clk.circle(210)
    clk.goto(0, 210)

    a = 1
    b = 12
    for i in range(0, 60):
        if a % 5 == 0:
            b -= 1
            if b == 0:
                b = 12
            clk.circle(210, 6)
            clk.left(90)
            clk.width(3)
            clk.forward(40)
            clk.backward(40)
            clk.penup()
            clk.backward(35)
            clk.write((int(b)),font=("Verdana", 12))
            clk.forward(35)
            clk.pendown()
            clk.right(90)
            clk.width(1)
        else:
            clk.circle(210, 6)
            clk.left(90)
            clk.forward(10)
            clk.backward(10)
            clk.right(90)
        a += 1
    clk.shape("arrow")
    clk.penup()
    clk.width(5)
    clk.goto(0, 0)
    clk.setheading(90)
    clk.rt((int(cur_time.strftime("%I")) / 12) * 360 + (int(cur_time.strftime("%M")) / 60) * 30)
    clk.pendown()
    clk.forward(80)
    clk.color("black")

    clk.penup()
    clk.width(3)
    clk.goto(0, 0)
    clk.setheading(90)
    clk.rt((int(cur_time.strftime("%M")) / 60) * 360)
    clk.color("blue")
    clk.pendown()
    clk.forward(120)

    clk.penup()
    clk.width(1)
    clk.goto(0, 0)
    clk.setheading(90)
    clk.rt((int(cur_time.strftime("%S")) / 60) * 360)
    clk.color("red")
    clk.pendown()
    clk.forward(160)

    hours = cur_time.strftime("%I")
    minutes = cur_time.strftime("%M")
    hour, minute = read_time_from_file()
    times2 = []


    if os.path.exists("test.txt"):
        with open("test.txt", "r") as file:
            times2 = [line.strip().split(": ")[1] for line in file.readlines()]

    current_time_str = f"{hours:02}:{minutes:02}"

    if current_time_str in times2:
        if dd == 0:
            dd = 1
            if os.path.exists("test2.txt"):
                with open("test2.txt", "r") as file:
                    content = file.read().strip()
                pygame.mixer.music.load(content)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        dd = 0

    screen.tracer(0)
    screen.update()
    screen.ontimer(lambda: draw_clock_face(dd), 1000)

def read_time_from_file(): # Đọc thời gian trong file đã tạo để kiểm tra hẹn giờ
    try:
        with open("test.txt", "r") as file:
            content = file.read().strip()
            time_str = content.split(": ")[1]
            hour, minute = map(int, time_str.split(":"))
            return hour, minute
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None



def BaoThuc_va_BamGio(x,y):
    if 80 <= x <= 180 and -280 <= y <= -220: # Cửa sổ hẹn giờ
        root = tk.Tk()
        root.withdraw()

        times = []

        if os.path.exists("test.txt"):
            with open("test.txt", "r") as file:
                times = [line.strip().split(": ")[1] for line in file.readlines()]

        def add_time():
            hour_var = tk.StringVar(root)
            minute_var = tk.StringVar(root)
            hour_var.set("0")
            minute_var.set("0")

            top = tk.Toplevel(root)
            top.geometry("200x200")
            top.title("??")

            tk.Label(top, text="Chọn giờ:").pack()
            hour_menu = tk.OptionMenu(top, hour_var, *range(24))
            hour_menu.pack()

            tk.Label(top, text="Chọn phút:").pack()
            minute_menu = tk.OptionMenu(top, minute_var, *range(60))
            minute_menu.pack()

            def on_ok():
                selected_hour = hour_var.get()
                selected_minute = minute_var.get()
                formatted_time = f"{int(selected_hour):02}:{int(selected_minute):02}"
                times.append(formatted_time)

                with open("test.txt", "w") as file:
                    for time in times:
                        file.write(f"Selected Time: {time}\n")

                update_times_display()
                tk.messagebox.showinfo("??", "Thành công!")
                top.destroy()

            ok_button = tk.Button(top, text="OK", command=on_ok)
            ok_button.pack()

        def update_times_display():
            times_label.config(text="\n".join(times))

        def delete_time():
            delete_top = tk.Toplevel(root)
            delete_top.geometry("200x200")
            delete_top.title("??")

            tk.Label(delete_top, text="Chon giờ muốn xóa:").pack()
            time_var = tk.StringVar(delete_top)
            time_var.set(times[0] if times else "")

            time_menu = tk.OptionMenu(delete_top, time_var, *times)
            time_menu.pack()

            def on_delete():
                selected_time = time_var.get()
                if selected_time in times:
                    times.remove(selected_time)
                    with open("test.txt", "w") as file:
                        for time in times:
                            file.write(f"Selected Time: {time}\n")

                    update_times_display()
                tk.messagebox.showinfo("??", "Thành công!")
                delete_top.destroy()

            delete_button = tk.Button(delete_top, text="Xóa", command=on_delete)
            delete_button.pack()

        top = tk.Toplevel(root)
        top.geometry("200x150")
        top.title("Hẹn giờ")

        times_label = tk.Label(top, text="", justify="left")
        times_label.pack()

        add_time_button = tk.Button(top, text="Thêm", command=add_time)
        add_time_button.pack()

        delete_time_button = tk.Button(top, text="Xóa", command=delete_time)
        delete_time_button.pack()

        update_times_display()

        root.mainloop()
    elif -190 <= x <= -90 and -280 <= y <= -220: # Cửa sổ bấm giờ
        root = tk.Tk()
        root.title("Đồng Hồ Bấm Giờ")
        root.geometry("700x300")

        running = False
        start_time = 0
        elapsed_time = 0
        laps = []

        time_label = tk.Label(root, text="00:00:00.000", font=("Arial", 30), fg="black")
        time_label.pack(pady=10)

        def start():
            nonlocal running, start_time, elapsed_time
            if not running:
                start_time = time.time() - elapsed_time
                running = True

        def stop():
            nonlocal running
            if running:
                running = False

        def lap():
            nonlocal elapsed_time, laps
            if running:
                lap_time = format_time(elapsed_time)
                laps.append(lap_time)
                lap_listbox.insert(tk.END, f"Cột mốc {len(laps)}: {lap_time}")
                lap_listbox.see(tk.END)

        def reset():
            nonlocal running, elapsed_time, laps
            running = False
            elapsed_time = 0
            time_label.config(text="00:00:00.000")
            laps.clear()
            lap_listbox.delete(0, tk.END)

        start_button = tk.Button(root, text="Bắt đầu", font=("Arial", 12), command=start)
        start_button.pack(side="left", padx=10, pady=10)

        stop_button = tk.Button(root, text="Dừng", font=("Arial", 12), command=stop)
        stop_button.pack(side="left", padx=10)

        lap_button = tk.Button(root, text="Dừng cột mốc", font=("Arial", 12), command=lap)
        lap_button.pack(side="left", padx=10)

        reset_button = tk.Button(root, text="Đặt lại", font=("Arial", 12), command=reset)
        reset_button.pack(side="left", padx=10)

        # Hiển thị danh sách cột mốc
        lap_listbox = tk.Listbox(root, font=("Arial", 12), height=10, width=30)
        lap_listbox.pack(pady=10)

        def format_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds - int(seconds)) * 1000)
            return f"{h:02}:{m:02}:{s:02}.{ms:03}"

        def update_display():
            nonlocal elapsed_time
            if running:
                elapsed_time = time.time() - start_time
            time_label.config(text=format_time(elapsed_time))
            root.after(10, update_display)

        update_display()
        root.mainloop()


    elif 200 <= x <= 300 and 300 <= y <= 350: # Cửa sổ chọn nhạc
        root = tk.Tk()
        root.withdraw()

        music_var = StringVar(root)
        music_var.set(music[0])

        top = tk.Toplevel(root)
        top.title("??")

        tk.Label(top, text="Chọn nhạc:").pack()
        music_menu = OptionMenu(top, music_var, *music)
        music_menu.pack()

        def on_ok():
            selected_music = music_var.get()
            with open("test2.txt", "w") as file:
                file.write(f"{selected_music}")
            top.destroy()
        ok_button = tk.Button(top, text="OK", command=on_ok)
        ok_button.pack()
        root.mainloop()
    elif -320 <= x <= -180 and 300 <= y <= 330: # Cửa sổ đổi múi giờ
        root = tk.Tk()
        tz = tk.StringVar(root)
        op = tk.OptionMenu(root, tz, *utc)
        op.pack()
        def shift_timezone():
            global cur_tz
            cur_tz = tz.get()
        ok_button = tk.Button(root, text="OK", font=("Arial", 12), command=shift_timezone)
        ok_button.pack()
        op.pack()

draw_clock_face(0)

clk.penup()
clk.setpos(-60, -180)

text_writer = turtle.Turtle()
text_writer.hideturtle()

def display_current_time(): # Biểu diễn ngày giờ theo múi giờ đã chọn
    text_writer.color('blue')
    current_time = datetime.datetime.now(pytz.timezone(f"Etc/{cur_tz}"))
    formatted_time = current_time.strftime("%H:%M:%S")
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    text_writer.clear()
    text_writer.penup()
    text_writer.setpos(-90, 300)
    text_writer.pendown()
    text_writer.write(f"{formatted_time}, {day}/{month}/{year}", font=("Arial", 16, "normal"))
    screen.ontimer(display_current_time, 1000)

# Vẽ các nút và kết thúc chương trình
button = turtle.Turtle()
button.penup()
button.goto(90, -270)
button.color("darkblue")
button.write("Hẹn giờ", font=("Arial", 18, "normal"))
button.hideturtle()

button2 = turtle.Turtle()
button2.penup()
button2.goto(-180, -270)
button2.color("darkblue")
button2.write("Bấm giờ", font=("Arial", 18, "normal"))
button2.hideturtle()

button3 = turtle.Turtle()
button3.penup()
button3.goto(200, 300)
button3.color("darkblue")
button3.write("Chọn nhạc", font=("Arial", 18, "normal"))
button3.hideturtle()

button4 = turtle.Turtle()
button4.penup()
button4.goto(-300, 300)
button4.color("darkblue")
button4.write("Đổi múi giờ", font=("Arial", 18, "normal"))
button4.hideturtle()

display_current_time()
screen.onclick(BaoThuc_va_BamGio)
turtle.done()

