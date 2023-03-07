import json
import os
from tkinter import *
from mqtt_backend import *

WIDTH = 1280
HEIGHT = 720

connected_user = "GUEST"
subscribed_topics = []
subscribed_topics_dict = []

SERVER_ADDRESS = "test.mosquitto.org"
SERVER_PORT = 1883

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

def prepare_environment():
    if os.path.isfile("resources/subscribed_topics.json"):
        pass
    else:
        open("resources/subscribed_topics.json", "w").close()

    host_txt.insert(0, f"{SERVER_ADDRESS}")
    port_txt.insert(0, f"{SERVER_PORT}")
    load_subscribed_topics()
    prepare_environment.is_startup = False


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


def load_subscribed_topics():
    try:
        with open('resources/subscribed_topics.json', 'r') as f:
            data = json.load(f)
        for message in data:
            subscribed_topics_dict.append(message)
        for topic in subscribed_topics_dict:
            display_message1(topic)
            load_subscribed_topics.count += 1
    except:
        pass


def on_frame1_configure():
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox("all"))


def toggle_result_frame(event):
    toggle_result_frame.is_active = not toggle_result_frame.is_active
    # print(toggle_result_frame.is_active)


def display_message(message, topic):
    result_frame = Frame(inner_dashboard_content_frame, bg="#ECF0F5")
    result_frame.grid(row=display_message.message_y, column=display_message.message_x)
    img_label = Label(result_frame, image=result_img)
    img_label.grid(row=0, column=0)
    result_lbl = Label(result_frame, text=f"{message}", bg="#3725AB", fg="white",
                       font=font1)
    result_lbl.place(x=20, y=20, anchor=NW)

    path_lbl = Label(result_frame, text=f"{topic}", bg="#3725AB", fg="white", font=font1)
    path_lbl.place(x=230, y=90, anchor=NE)

    if display_message.message_x < 2:
        display_message.message_x += 1
    elif display_message.message_x == 2:
        display_message.message_y += 1
        display_message.message_x = 0
    else:
        display_message.message_y += 1
        display_message.message_x = 0


def clear_message():
    for widget in inner_dashboard_content_frame.winfo_children():
        widget.destroy()
    inner_dashboard_content_frame.update()
    display_message.message_x = 0
    display_message.message_y = 0


def adjust_scrollbar():
    dashboard_canvas.update_idletasks()
    if dashboard_autoscroll.get() == 1:
        dashboard_canvas.yview_moveto(1.0)

    # update the scroll region of the canvas
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox('all'))


def on_frame2_configure():
    subscribe_canvas.configure(scrollregion=subscribe_canvas.bbox("all"))


def delete_topic(event):
    parent_widget = event.widget.winfo_parent()
    result_frame_widget = event.widget.nametowidget(parent_widget)
    topic_lbl = result_frame_widget.winfo_children()[1]
    subscribed_topics.remove(topic_lbl.cget("text"))

    global subscribed_topics_dict

    subscribed_topics_dict = [d for d in subscribed_topics_dict if d["topic"] != f"{topic_lbl.cget('text')}"]
    try:
        connect_to_server.client.unsubscribe(topic_lbl.cget("text"))
        connect_to_server.client.update_topics(subscribed_topics)
    except:
        pass
    event.widget.master.destroy()


def on_img_label_click(parent_widget):
    result_frame_widget = root.nametowidget(parent_widget)
    img_lbl = result_frame_widget.winfo_children()[0]
    topic_lbl = result_frame_widget.winfo_children()[1]
    delete_label = result_frame_widget.winfo_children()[2]

    if img_lbl.cget("image") == str(topic_result_img):
        img_lbl.config(image=result_inactive_img)
        topic_lbl.config(fg="black", bg="#D3D3D3")
        delete_label.config(fg="black", bg="#D3D3D3")
        [sub_topic.update({"state": 0}) for sub_topic in subscribed_topics_dict if sub_topic.get("topic") == topic_lbl.cget("text")]
        if connect_to_server.is_connected:
            connect_to_server.client.unsubscribe(topic_lbl.cget("text"))
    else:
        img_lbl.config(image=topic_result_img)
        topic_lbl.config(fg="white", bg="#3725AB")
        delete_label.config(fg="white", bg="#3725AB")
        [sub_topic.update({"state": 1}) for sub_topic in subscribed_topics_dict if
         sub_topic.get("topic") == topic_lbl.cget("text")]
        if connect_to_server.is_connected:
            connect_to_server.client.subscribe_to_topic(topic_lbl.cget("text"))



def save_subscribed_topics():
    with open("resources/subscribed_topics.json", "w") as file:
        json.dump(subscribed_topics_dict, file)


def display_message1(the_topic):
    the_message = None
    if the_topic == "":
        return
    if prepare_environment.is_startup:
        the_message = the_topic
        the_topic = the_topic['topic']

    topic_frame = Frame(inner_subscribe_content_frame, bg="#ECF0F5")
    topic_frame.grid(row=display_message1.message_y, column=0)

    topic_bg_lbl = Label(topic_frame, image=topic_result_img)
    topic_bg_lbl.grid(row=0, column=0)
    topic_lbl = Label(topic_frame, text=f"{the_topic}", bg="#3725AB", fg="white",
                      font=("Times New Roman", 24), anchor=NW)
    topic_lbl.place(x=20, y=15, width=330)
    delete_label = Label(topic_frame, image=bin_img, bg="#3725AB")
    delete_label.place(x=369, y=25)
    delete_label.bind("<Button-1>", delete_topic)

    topic_bg_lbl.bind('<Button-1>', lambda event: on_img_label_click(str(event.widget.winfo_parent())))
    topic_lbl.bind('<Button-1>', lambda event: on_img_label_click(str(event.widget.winfo_parent())))


    # during startup
    if prepare_environment.is_startup:
        if the_message["state"] == 1:
            pass
        elif the_message["state"] == 0:
            # simulate a click on the topic label
            parent_frame = f".!frame3.!frame3.!frame.!canvas.!frame.!frame2.!frame{'' if load_subscribed_topics.count == 1 else load_subscribed_topics.count}"
            on_img_label_click(parent_frame)
    else:
        pass
    # print(subscribed_topics_dict)

    try:
        if not prepare_environment.is_startup:
            subscribed_topics_dict.append({"topic": f"{topic_lbl.cget('text')}", "state": 1})
        subscribed_topics.append(topic_lbl.cget("text"))
        connect_to_server.client.update_topics(subscribed_topics)
        # Subscribe to topic and print received messages
        connect_to_server.client.subscribe_to_topic(topic_lbl.cget("text"))
    except:
        pass
    display_message1.message_y += 1


def on_frame3_configure():
    publish_canvas.configure(scrollregion=publish_canvas.bbox("all"))


def delete_publish(event):
    # print("Deleting...")
    event.widget.master.destroy()


def on_img_label_click1(event):
    parent_widget = event.widget.winfo_parent()
    result_frame_widget = event.widget.nametowidget(parent_widget)
    topic_lbl = result_frame_widget.winfo_children()[1]
    msg_lbl = result_frame_widget.winfo_children()[2]

    # topic_txt1.delete(0, END)
    # topic_txt1.insert(0, topic_lbl.cget("text"))
    #
    # message_txt.delete(0, END)
    # message_txt.insert(0, msg_lbl.cget("text"))

    publish_message(topic_lbl.cget("text"), msg_lbl.cget("text"))


def publish_message(topic, message):
    if topic.strip() == "" or message.strip() == "":
        return
    if not connect_to_server.is_connected:
        return
    # Publish message to topic
    connect_to_server.client.publish(topic, message)


def display_message2():
    if topic_txt1.get().strip() == "" or message_txt.get().strip() == "":
        return
    topic_frame = Frame(inner_publish_content_frame, bg="#ECF0F5")
    topic_frame.grid(row=display_message1.message_y, column=0)
    bg_label = Label(topic_frame, image=topic_result_img)
    bg_label.grid(row=0, column=0)

    topic_lbl = Label(topic_frame, text=f"{topic_txt1.get()}", bg="#3725AB", fg="white",
                      font=("Times New Roman", 24), anchor=NW)
    topic_lbl.place(x=20, y=15, width=200)
    msg_lbl = Label(topic_frame, text=f"{message_txt.get()}", bg="#3725AB", fg="white",
                    font=("Times New Roman", 24), anchor=E)
    msg_lbl.place(x=280, y=15, width=80)
    delete_label = Label(topic_frame, image=bin_img, bg="#3725AB")
    delete_label.place(x=369, y=25)
    delete_label.bind("<Button-1>", delete_publish)

    bg_label.bind('<Button-1>', on_img_label_click1)
    topic_lbl.bind('<Button-1>', on_img_label_click1)
    msg_lbl.bind('<Button-1>', on_img_label_click1)

    # subscribed_topics.append(topic_frame)
    display_message1.message_y += 1


def create_client():
    if connect_to_server.is_connected:
        return
    connect_to_server.client = MqttClient(connect_to_server.broker_address, connect_to_server.broker_port)
    connect_to_server.client.update_topics(subscribed_topics)
    connect_to_server.client.subscribe(subscribed_topics)
    # print(subscribed_topics)

    connect_to_server.client.set_display_message(display_message=[display_message, adjust_scrollbar])
    connect_to_server.client.set_disconnection_callback(disconnection_callback=handle_disconnection)

    connect_to_server.broker_address = host_txt.get().strip()
    connect_to_server.broker_port = int(port_txt.get().strip())
    connect_to_server.client.update_logins(connect_to_server.broker_address, connect_to_server.broker_port)


def connect_to_server():
    if host_txt.get().strip() == "" or port_txt.get().strip() == "":
        return

    create_client()

    if connect_to_server.is_connected:
        connect_to_server.client.disconnect()
        # del client
        if not connect_to_server.client.is_connected:
            connect_to_server.is_connected = False
        disable_logins()
        return

    connect_to_server.client.connect()
    # print(connect_to_server.client.is_connected)
    if connect_to_server.client.is_connected:
        connect_to_server.is_connected = True

    disable_logins()


def disable_logins():
    if connect_to_server.is_connected:
        host_txt.config(state=DISABLED)
        port_txt.config(state=DISABLED)
        username_txt.config(state=DISABLED)
        password_txt.config(state=DISABLED)
        connect_btn.config(image=disconnect_img)
        connection_status_label.config(image=good_network_img)
    else:
        host_txt.config(state=NORMAL)
        port_txt.config(state=NORMAL)
        username_txt.config(state=NORMAL)
        password_txt.config(state=NORMAL)
        connect_btn.config(image=connect_img)
        connection_status_label.config(image=bad_network_img)


def handle_disconnection():
    if not connect_to_server.client.is_connected:
        connect_to_server.is_connected = False
    disable_logins()


def on_closing():
    try:
        save_subscribed_topics()
        connect_to_server.client.disconnect()
    except:
        pass
    root.destroy()


#####################################################
# ******************END***********************#
#####################################################

display_message.message_x = 0
display_message.message_y = 0

display_message1.message_y = 0
connect_to_server.is_connected = False
connect_to_server.broker_address = ""
connect_to_server.broker_port = 0
toggle_result_frame.is_active = True

connect_to_server.client = None
connect_to_server.the_count = 0

prepare_environment.is_startup = True

load_subscribed_topics.count = 1

sidebar_img = PhotoImage(file="images/sidebar.png")
connect_img = PhotoImage(file="images/connect.png")
disconnect_img = PhotoImage(file="images/disconnect.png")
option_back_img = PhotoImage(file="images/options_back.png")
subscribe_selected_img = PhotoImage(file="images/subscribe_selected.png")
subscribe_unselected_img = PhotoImage(file="images/subscribe_unselected.png")
publish_selected_img = PhotoImage(file="images/publish_selected.png")
publish_unselected_img = PhotoImage(file="images/publish_unselected.png")
dashboard_selected_img = PhotoImage(file="images/dashboard_selected.png")
dashboard_unselected_img = PhotoImage(file="images/dashboard_unselected.png")
result_img = PhotoImage(file="images/result_feedback.png")
result_inactive_img = PhotoImage(file="images/result_feedback_inactive.png")
click_area_topic_img = PhotoImage(file="images/click_area_topics.png")
topic_img = PhotoImage(file="images/topic.png")
subscribe_img = PhotoImage(file="images/subscribe_btn.png")
topic_result_img = PhotoImage(file="images/topic_frame.png")
bin_img = PhotoImage(file="images/bin.png")
message_img = PhotoImage(file="images/messagebox.png")
save_img = PhotoImage(file="images/save.png")
publish_img = PhotoImage(file="images/publish.png")
good_network_img = PhotoImage(file="images/good_network.png")
bad_network_img = PhotoImage(file="images/bad_network.png")

top_bar = Frame(root, bg="#3725AB", width=WIDTH, height=40)
top_bar.pack(side=TOP, fill=X)

connected_user_label = Label(top_bar, text=f"{connected_user.upper()}", bg="#3725AB", fg="white",
                             justify=LEFT, font=("Roboto", 12, 'bold'))
connected_user_label.place(x=1260, y=10, anchor=NE)

connection_status_label = Label(top_bar, image=bad_network_img, bg="#3725AB")
connection_status_label.place(x=8, y=8, anchor=NW)

side_bar = Frame(root, bg="#D9D9D9", width=340, height=HEIGHT, border=0.5, relief="ridge")
side_bar.pack(side=LEFT, fill=Y)

sidebar_label = Label(side_bar, image=sidebar_img, bg="#D9D9D9")
sidebar_label.place(x=18, y=42.37)

host_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
host_txt.place(x=30, y=125, height=30)

port_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
port_txt.place(x=30, y=190, height=30)

username_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
username_txt.place(x=30, y=318, height=30)

password_txt = Entry(side_bar, width=47, bg="#D9D9D9", bd=0, relief="flat")
password_txt.place(x=30, y=382, height=30)

connect_btn = Button(side_bar, image=connect_img, bg="#D9D9D9", bd=0, activebackground="#D9D9D9",
                     command=lambda: connect_to_server())
connect_btn.place(x=207, y=437.86)

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

inner_dashboard_content_parent_frame = Frame(dashboard_canvas, bg="#ECF0F5", width=940, height=469.49)

inner_dashboard_content_sibling_frame = Frame(inner_dashboard_content_parent_frame, bg="#ECF0F5", width=85,
                                              height=469.49)
inner_dashboard_content_sibling_frame.pack(side="left", fill="both", expand=True)

inner_dashboard_content_frame = Frame(inner_dashboard_content_parent_frame, bg="#ECF0F5", width=940, height=469.49)
inner_dashboard_content_frame.pack(side="left", fill="both", expand=True)

dashboard_scrollbar = Scrollbar(dashboard_content_frame, command=dashboard_canvas.yview)
dashboard_scrollbar.pack(side="left", fill="y")

dashboard_canvas.configure(yscrollcommand=dashboard_scrollbar.set)

dashboard_canvas.create_window((0, 0), window=inner_dashboard_content_parent_frame, anchor="nw")

inner_dashboard_content_frame.bind("<Configure>", lambda e: on_frame1_configure())

####################################################PARSER####################################################
# connect_to_server.client.set_display_message(display_message=[display_message, adjust_scrollbar])
# connect_to_server.client.set_disconnection_callback(disconnection_callback=handle_disconnection)

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
                          activebackground="#ECF0F5", command=lambda: display_message1(topic_txt.get()))
subscribe_button.place(x=521, y=80)

# Create a canvas and scrollbar for the first frame
subscribe_canvas = Canvas(subscribe_content_frame, bg="#ECF0F5")
subscribe_canvas.pack(side="left", fill="both", expand=True)

inner_subscribe_content_parent_frame = Frame(subscribe_canvas, bg="#ECF0F5", width=940, height=469.49)

inner_subscribe_content_sibling_frame = Frame(inner_subscribe_content_parent_frame, bg="#ECF0F5", width=263,
                                              height=469.49)
inner_subscribe_content_sibling_frame.pack(side="left", fill="both", expand=True)

inner_subscribe_content_frame = Frame(inner_subscribe_content_parent_frame, bg="#ECF0F5", width=940, height=469.49)
inner_subscribe_content_frame.pack(side="left", fill="both", expand=True)

subscribe_scrollbar = Scrollbar(subscribe_content_frame, command=subscribe_canvas.yview)
subscribe_scrollbar.pack(side="left", fill="y")

subscribe_canvas.configure(yscrollcommand=subscribe_scrollbar.set)

subscribe_canvas.create_window((0, 0), window=inner_subscribe_content_parent_frame, anchor="nw")

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
                        activebackground="#ECF0F5",
                        command=lambda: publish_message(topic_txt1.get(), message_txt.get()))
publish_button.place(x=521, y=145)

# Create a canvas and scrollbar for the first frame
publish_canvas = Canvas(publish_content_frame, bg="#ECF0F5")
publish_canvas.pack(side="left", fill="both", expand=True)

inner_publish_content_parent_frame = Frame(publish_canvas, bg="red", width=940, height=469.49)

inner_publish_content_sibling_frame = Frame(inner_publish_content_parent_frame, bg="#ECF0F5", width=263, height=469.49)
inner_publish_content_sibling_frame.pack(side="left", fill="both", expand=True)

inner_publish_content_frame = Frame(inner_publish_content_parent_frame, bg="#ECF0F5", width=940, height=469.49)
inner_publish_content_frame.pack(side="left", fill="both", expand=True)

publish_scrollbar = Scrollbar(publish_content_frame, command=publish_canvas.yview)
publish_scrollbar.pack(side="left", fill="y")

publish_canvas.configure(yscrollcommand=publish_scrollbar.set)

publish_canvas.create_window((0, 0), window=inner_publish_content_parent_frame, anchor="nw")

inner_publish_content_frame.bind("<Configure>", lambda e: on_frame3_configure())

prepare_environment()

root.protocol("WM_DELETE_WINDOW", lambda: on_closing())
root.mainloop()
