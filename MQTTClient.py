from tkinter import *

WIDTH = 1280
HEIGHT = 720

connected_user = "GUEST"
incoming_messages = []
subscribed_topics = []

font1 = ("Roboto", 9, 'bold')

root = Tk()
dashboard_autoscroll = IntVar()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = ((screen_width / 2) - (WIDTH / 2))
y = ((screen_height / 2) - (HEIGHT / 2))

root.geometry(f'{WIDTH}x{HEIGHT}+{int(x)}+{int(y) - 30}')

root.title("MQTT Client")
root.resizable(False, False)
root.configure(bg="#ECF0F5")


#####################################################
# ******************FUNCTIONS***********************#
#####################################################
def load_dashboard():
    dashboard_selected_label.configure(image=dashboard_selected_img)
    subscribe_selected_label.configure(image=subscribe_unselected_img)
    publish_selected_label.configure(image=publish_unselected_img)

    subscribe_content_parent_frame.place_forget()
    publish_content_parent_frame.place_forget()
    dashboard_content_parent_frame.place(x=0, y=130, relwidth=1, relheight=0.809)


def load_subscribe():
    dashboard_selected_label.configure(image=dashboard_unselected_img)
    subscribe_selected_label.configure(image=subscribe_selected_img)
    publish_selected_label.configure(image=publish_unselected_img)

    dashboard_content_parent_frame.place_forget()
    publish_content_parent_frame.place_forget()
    subscribe_content_parent_frame.place(x=0, y=130, relwidth=1, relheight=0.809)


def load_publish():
    dashboard_selected_label.configure(image=dashboard_unselected_img)
    subscribe_selected_label.configure(image=subscribe_unselected_img)
    publish_selected_label.configure(image=publish_selected_img)

    dashboard_content_parent_frame.place_forget()
    subscribe_content_parent_frame.place_forget()
    publish_content_parent_frame.place(x=0, y=130, relwidth=1, relheight=0.809)


def on_frame1_configure():
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox("all"))


def display_message():
    result_frame = Frame(inner_dashboard_content_frame, bg="#ECF0F5")
    result_frame.grid(row=display_message.message_y, column=display_message.message_x)
    Label(result_frame, image=result_img).grid(row=0, column=0)
    Label(result_frame, text=f"Result {display_message.counter}", bg="#3725AB", fg="white",
          font=font1).place(x=20, y=20,
                            anchor=NW)
    Label(result_frame, text=f"Path/path", bg="#3725AB", fg="white", font=font1).place(x=230, y=90,
                                                                                       anchor=NE)
    incoming_messages.append(result_frame)

    if display_message.message_x < 2:
        display_message.message_x += 1
    elif display_message.message_x == 2:
        display_message.message_y += 1
        display_message.message_x = 0
    else:
        display_message.message_y += 1
        display_message.message_x = 0

    display_message.counter += 1


def clear_message():
    for message in incoming_messages:
        inner_dashboard_content_frame.update()
        message.destroy()
        display_message.message_x = 0
        display_message.message_y = 0
        display_message.counter = 0


def adjust_scrollbar():
    dashboard_canvas.update_idletasks()
    if dashboard_autoscroll.get() == 1:
        dashboard_canvas.yview_moveto(1.0)

    # update the scroll region of the canvas
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox('all'))


def on_frame2_configure():
    subscribe_canvas.configure(scrollregion=subscribe_canvas.bbox("all"))


def delete_topic(event):
    event.widget.master.destroy()


def display_message1():
    if topic_txt.get().strip() == "":
        return
    topic_frame = Frame(inner_subscribe_content_frame, bg="#ECF0F5")
    topic_frame.grid(row=display_message1.message_y, column=0)
    Label(topic_frame, image=topic_result_img).grid(row=0, column=0)

    Label(topic_frame, text=f"{topic_txt.get()}", bg="#3725AB", fg="white",
          font=("Times New Roman", 24), anchor=NW).place(x=20, y=15, width=330)
    delete_label = Label(topic_frame, image=bin_img, bg="#3725AB")
    delete_label.place(x=369, y=25)
    delete_label.bind("<Button-1>", delete_topic)

    subscribed_topics.append(topic_frame)
    display_message1.message_y += 1


def on_frame3_configure():
    publish_canvas.configure(scrollregion=publish_canvas.bbox("all"))


def display_message2():
    if topic_txt1.get().strip() == "" or message_txt.get().strip() == "":
        return
    topic_frame = Frame(inner_publish_content_frame, bg="#ECF0F5")
    topic_frame.grid(row=display_message1.message_y, column=0)
    Label(topic_frame, image=topic_result_img).grid(row=0, column=0)

    Label(topic_frame, text=f"{topic_txt1.get()}", bg="#3725AB", fg="white",
          font=("Times New Roman", 24), anchor=NW).place(x=20, y=15, width=200)
    Label(topic_frame, text=f"{message_txt.get()}", bg="#3725AB", fg="white",
          font=("Times New Roman", 24), anchor=E).place(x=280, y=15, width=80)
    delete_label = Label(topic_frame, image=bin_img, bg="#3725AB")
    delete_label.place(x=369, y=25)
    delete_label.bind("<Button-1>", delete_topic)

    subscribed_topics.append(topic_frame)
    display_message1.message_y += 1



#####################################################
# ******************END***********************#
#####################################################

display_message.message_x = 0
display_message.message_y = 0
display_message.counter = 0
display_message1.message_y = 0

top_bar = Frame(root, bg="#3725AB", width=WIDTH, height=40)
top_bar.pack(side=TOP, fill=X)

connected_user_label = Label(top_bar, text=f"{connected_user.upper()}", bg="#3725AB", fg="white",
                             justify=LEFT, font=("Roboto", 12, 'bold'))
connected_user_label.place(x=1260, y=10, anchor=NE)

sidebar_img = PhotoImage(file="images/sidebar.png")
connect_img = PhotoImage(file="images/connect.png")
option_back_img = PhotoImage(file="images/options_back.png")
subscribe_selected_img = PhotoImage(file="images/subscribe_selected.png")
subscribe_unselected_img = PhotoImage(file="images/subscribe_unselected.png")
publish_selected_img = PhotoImage(file="images/publish_selected.png")
publish_unselected_img = PhotoImage(file="images/publish_unselected.png")
dashboard_selected_img = PhotoImage(file="images/dashboard_selected.png")
dashboard_unselected_img = PhotoImage(file="images/dashboard_unselected.png")
result_img = PhotoImage(file="images/result_feedback.png")
topic_img = PhotoImage(file="images/topic.png")
subscribe_img = PhotoImage(file="images/subscribe_btn.png")
topic_result_img = PhotoImage(file="images/topic_frame.png")
bin_img = PhotoImage(file="images/bin.png")
message_img = PhotoImage(file="images/messagebox.png")
save_img = PhotoImage(file="images/save.png")
publish_img = PhotoImage(file="images/publish.png")

side_bar = Frame(root, bg="#D9D9D9", width=340, height=HEIGHT, border=0.5, relief="ridge")
side_bar.pack(side=LEFT, fill=Y)

sidebar_label = Label(side_bar, image=sidebar_img, bg="#D9D9D9")
sidebar_label.place(x=18, y=42.37)

connect_btn = Button(side_bar, image=connect_img, bg="#D9D9D9", bd=0, activebackground="#D9D9D9")
connect_btn.place(x=207, y=437.86)

host_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
host_txt.place(x=30, y=125, height=30)

port_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
port_txt.place(x=30, y=190, height=30)

username_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
username_txt.place(x=30, y=318, height=30)

password_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
password_txt.place(x=30, y=382, height=30)

# Content panel
content_frame = Frame(root, bg="#ECF0F5")
content_frame.pack(side=LEFT, fill=BOTH, expand=True)

options_frame = Frame(content_frame, bg="#ECF0F5", height=107)
options_frame.place(x=0, y=0, relwidth=1)

option_back_label = Label(options_frame, image=option_back_img, bg="#ECF0F5")
option_back_label.place(x=36, y=22)

dashboard_selected_label = Label(options_frame, image=dashboard_selected_img, bg="#ECF0F5")
dashboard_selected_label.place(x=40, y=28)
dashboard_selected_label.bind("<Button-1>", lambda e: load_dashboard())

subscribe_selected_label = Label(options_frame, image=subscribe_unselected_img, bg="#ECF0F5")
subscribe_selected_label.place(x=332, y=28)
subscribe_selected_label.bind("<Button-1>", lambda e: load_subscribe())

publish_selected_label = Label(options_frame, image=publish_unselected_img, bg="#ECF0F5")
publish_selected_label.place(x=624, y=28)
publish_selected_label.bind("<Button-1>", lambda e: load_publish())

# Dashboard content

dashboard_content_parent_frame = Frame(content_frame, bg="#ECF0F5", width=940)
dashboard_content_parent_frame.place(x=0, y=130, relwidth=1, relheight=0.809)

dashboard_content_frame = Frame(dashboard_content_parent_frame, bg="#ECF0F5")
dashboard_content_frame.pack(side="top", fill="both", expand=True)

# Create a canvas and scrollbar for the first frame
dashboard_canvas = Canvas(dashboard_content_frame, bg="#ECF0F5")
dashboard_canvas.pack(side="left", fill="both", expand=True)

inner_dashboard_content_frame = Frame(dashboard_canvas, bg="#ECF0F5", width=940, height=469.49)
# inner_dashboard_content_frame.grid(row=0, column=0)

dashboard_scrollbar = Scrollbar(dashboard_content_frame, command=dashboard_canvas.yview)
dashboard_scrollbar.pack(side="left", fill="y")

dashboard_canvas.configure(yscrollcommand=dashboard_scrollbar.set)

dashboard_canvas.create_window((0, 0), window=inner_dashboard_content_frame, anchor="nw")

inner_dashboard_content_frame.bind("<Configure>", lambda e: on_frame1_configure())

add_button_button1 = Button(dashboard_content_parent_frame, text="Add Message",
                            command=lambda: (display_message(), adjust_scrollbar()))
add_button_button1.pack()

add_button_button2 = Button(dashboard_content_parent_frame, text="Delete Messages", command=lambda: clear_message())
add_button_button2.pack()

checkbox = Checkbutton(dashboard_content_parent_frame, text="Autoscroll", variable=dashboard_autoscroll, font=font1,
                       onvalue=1, offvalue=0)
checkbox.select()
checkbox.pack()

# Subscribe content

subscribe_content_parent_frame = Frame(content_frame, bg="#ECF0F5", width=940)

subscribe_content_frame = Frame(subscribe_content_parent_frame, bg="#ECF0F5")
subscribe_content_frame.pack(side="top", fill="both", expand=True)

subscribe_content_top_frame = Frame(subscribe_content_frame, bg="#ECF0F5", height=150)
subscribe_content_top_frame.pack(fill="x")

topic_label = Label(subscribe_content_top_frame, image=topic_img, font=font1, bg="#ECF0F5")
topic_label.place(x=308, y=14)

topic_txt = Entry(subscribe_content_top_frame, width=51, bg="#ECF0F5", bd=0, relief="flat")
topic_txt.place(x=320, y=31, height=30)

subscribe_button = Button(subscribe_content_top_frame, image=subscribe_img, bg="#ECF0F5", bd=0, relief="flat",
                          activebackground="#ECF0F5", command=lambda: display_message1())
subscribe_button.place(x=521, y=80)

# Create a canvas and scrollbar for the first frame
subscribe_canvas = Canvas(subscribe_content_frame, bg="#ECF0F5")
subscribe_canvas.pack(side="left", fill="both", expand=True)

inner_subscribe_content_frame = Frame(subscribe_canvas, bg="#ECF0F5", width=940, height=469.49)
# inner_subscribe_content_frame.grid(row=0, column=0)

subscribe_scrollbar = Scrollbar(subscribe_content_frame, command=subscribe_canvas.yview)
subscribe_scrollbar.pack(side="left", fill="y")

subscribe_canvas.configure(yscrollcommand=subscribe_scrollbar.set)

subscribe_canvas.create_window((0, 0), window=inner_subscribe_content_frame, anchor="nw")

inner_subscribe_content_frame.bind("<Configure>", lambda e: on_frame2_configure())

# Publish content

publish_content_parent_frame = Frame(content_frame, bg="#ECF0F5", width=940)

publish_content_frame = Frame(publish_content_parent_frame, bg="#ECF0F5")
publish_content_frame.pack(side="top", fill="both", expand=True)

publish_content_top_frame = Frame(publish_content_frame, bg="#ECF0F5", height=195)
publish_content_top_frame.pack(fill="x")

topic_label1 = Label(publish_content_top_frame, image=topic_img, font=font1, bg="#ECF0F5")
topic_label1.place(x=308, y=14)

topic_txt1 = Entry(publish_content_top_frame, width=51, bg="#ECF0F5", bd=0, relief="flat")
topic_txt1.place(x=320, y=31, height=30)

message_label = Label(publish_content_top_frame, image=message_img, font=font1, bg="#ECF0F5")
message_label.place(x=308, y=80)

message_txt = Entry(publish_content_top_frame, width=51, bg="#ECF0F5", bd=0, relief="flat")
message_txt.place(x=320, y=97, height=30)

save_button = Button(publish_content_top_frame, image=save_img, bg="#ECF0F5", bd=0, relief="flat",
                        activebackground="#ECF0F5", command=lambda: display_message2())
save_button.place(x=395, y=145)

publish_button = Button(publish_content_top_frame, image=publish_img, bg="#ECF0F5", bd=0, relief="flat",
                        activebackground="#ECF0F5")
publish_button.place(x=521, y=145)

# Create a canvas and scrollbar for the first frame
publish_canvas = Canvas(publish_content_frame, bg="#ECF0F5")
publish_canvas.pack(side="left", fill="both", expand=True)

inner_publish_content_frame = Frame(publish_canvas, bg="#ECF0F5", width=940, height=469.49)
# inner_publish_content_frame.grid(row=0, column=0)

publish_scrollbar = Scrollbar(publish_content_frame, command=publish_canvas.yview)
publish_scrollbar.pack(side="left", fill="y")

publish_canvas.configure(yscrollcommand=publish_scrollbar.set)

publish_canvas.create_window((0, 0), window=inner_publish_content_frame, anchor="nw")

inner_publish_content_frame.bind("<Configure>", lambda e: on_frame3_configure())

root.mainloop()
