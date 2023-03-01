from tkinter import *

WIDTH = 1280
HEIGHT = 720

connected_user = "IdrisFallout"
incoming_messages = []

root = Tk()

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

    dashboard_content_frame.pack(side='left', fill='both', expand=True)


def load_subscribe():
    dashboard_selected_label.configure(image=dashboard_unselected_img)
    subscribe_selected_label.configure(image=subscribe_selected_img)
    publish_selected_label.configure(image=publish_unselected_img)


def load_publish():
    dashboard_selected_label.configure(image=dashboard_unselected_img)
    subscribe_selected_label.configure(image=subscribe_unselected_img)
    publish_selected_label.configure(image=publish_selected_img)


def on_frame1_configure(event):
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox("all"))


def display_message():
    result_frame = Frame(inner_dashboard_content_frame, bg="#ECF0F5")
    result_frame.pack()
    Label(result_frame, image=result_img).pack()
    Label(result_frame, text=f"Result", bg="#3725AB", fg="white", font=("Roboto", 9, 'bold')).place(x=20, y=20,
                                                                                                    anchor=NW)
    Label(result_frame, text=f"Result", bg="#3725AB", fg="white", font=("Roboto", 9, 'bold')).place(x=230, y=90,
                                                                                                    anchor=NE)
    incoming_messages.append(result_frame)


def clear_message():
    for message in incoming_messages:
        message.destroy()


#####################################################
# ******************END***********************#
#####################################################


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
options_frame.pack(side=TOP, fill=X)

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

dashboard_content_frame = Frame(content_frame, bg="#ECF0F5", height=107, width=940)
# dashboard_content_frame.pack(side='left', fill='both', expand=True)

# Create a canvas and scrollbar for the first frame
dashboard_canvas = Canvas(dashboard_content_frame, bg="#ECF0F5")
dashboard_canvas.pack(side="left", fill="both", expand=True)

inner_dashboard_content_frame = Frame(dashboard_canvas, bg="#ECF0F5")
inner_dashboard_content_frame.pack(side='left', fill='both', expand=True)

dashboard_scrollbar = Scrollbar(dashboard_content_frame, command=dashboard_canvas.yview)
dashboard_scrollbar.pack(side="left", fill="y")

dashboard_canvas.configure(yscrollcommand=dashboard_scrollbar.set)

dashboard_canvas.create_window((0, 0), window=inner_dashboard_content_frame, anchor="nw")


inner_dashboard_content_frame.bind("<Configure>", on_frame1_configure)

add_button_button1 = Button(inner_dashboard_content_frame, text="Add Message", command=lambda: display_message())
add_button_button1.pack()

add_button_button2 = Button(inner_dashboard_content_frame, text="Delete Messages", command=lambda: clear_message())
add_button_button2.pack()

root.mainloop()
