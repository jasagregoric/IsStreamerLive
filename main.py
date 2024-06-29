import os
import requests
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv
from addUser import adduser  # Assuming this function is used to add a new user
import configparser
from PIL import Image, ImageTk
from logos import get_logos, get_logo  # Assuming these functions handle logos retrieval
from getData import get_data  # Assuming this function retrieves data for a streamer
import datetime

# Function to load environment variables
def configure():
    load_dotenv()

def main():
    configure()

main()

# Track streamers that have already triggered the live popup
notified_live_streamers = set()
popup_windows = {}  # Dictionary to keep track of popup windows

# Function to create a blinking popup window
def create_blinking_popup(streamer_name):
    popup = tk.Toplevel(root)
    popup.geometry("300x170")
    popup.title("Streamer Live Alert")
    popup.overrideredirect(True)  # Remove window decorations
    popup.wm_attributes("-topmost", True)

    # Set the position of the popup in the top right corner of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    image_path = "assets/logos/"+streamer_name+".jpg"
    image = Image.open(image_path).resize((60, 60))
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(popup, text=f"  {streamer_name} is live!", font=("Helvetica", 25), image=photo, compound='left')
    label.image=photo
    label.pack(pady=20, expand=True)
    
    popup.update()

    # Calculate the dimensions and coordinates
    label_width = label.winfo_width()
    window_width = label_width + 180
    window_height = 140
    x_coordinate = screen_width - window_width - 20
    y_coordinate = 20

    # Set the geometry of the popup window
    popup.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    close_img = tk.PhotoImage(file="assets/img/close.png").subsample(3, 3)
    close_button = tk.Button(popup, image=close_img, command=popup.destroy, borderwidth=0)
    close_button.image = close_img  # Keep a reference to the image
    close_button.place(x=window_width - close_button.winfo_width() - 30, y=15)  # Place at top right corner

    def blink():
        bg_color = label.cget("background")
        fg_color = label.cget("foreground")
        label.config(background=fg_color, foreground=bg_color)
        popup.after(500, blink)

    blink()

    def on_close():
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    # Store the popup in the dictionary
    popup_windows[streamer_name] = popup
live_data = []
# Function to check if streamers are live
def isLive():
    def check_streamers():
        live_data = []
        for name in name_list:
            if isMuted(name):
                live_data.append((name, False, True))  # Append (name, False, True) for muted
                continue

            url = f'https://api.twitch.tv/helix/streams?user_login={name}'
            headers = {
                'Authorization': 'Bearer ' + os.getenv('api_key'),
                'Client-Id': os.getenv('client_id')
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            is_live = bool(data['data'])
            live_data.append((name, is_live, False))  # Append (name, is_live, False) for normal

            if is_live and name not in notified_live_streamers:
                create_blinking_popup(name)
                notified_live_streamers.add(name)
            elif not is_live and name in notified_live_streamers:
                notified_live_streamers.remove(name)
                if name in popup_windows:
                    popup_windows[name].destroy()
                    del popup_windows[name]

        update_table(live_data)
        threading.Timer(2, check_streamers).start()

    check_streamers()  # Start the initial check

# Function to update the table with live status
def update_table(live_data):
    if live_data is None:
        return

    selected_item = tree.selection()
    selected_name = tree.item(selected_item)['values'][0] if selected_item else None

    for item in tree.get_children():
        tree.delete(item)

    for name, status, muted in live_data:
        status_text = 'Muted' if muted else ('Live' if status else 'Offline')
        tags = ('muted' if muted else ('live' if status else 'offline'),)
        tree.insert('', 'end', values=(name, status_text), tags=tags)
        
    if selected_name:
        for item in tree.get_children():
            if tree.item(item, 'values')[0] == selected_name:
                tree.selection_set(item)
                tree.focus(item)
                break

# Function to add a new streamer
def add_streamer_action():
    streamer_name = entry_streamer.get().strip()
    if streamer_name:
        result = adduser(streamer_name)
        if result == 0:
            get_logo(streamer_name)
            messagebox.showinfo('Success', f'Streamer "{streamer_name}" added successfully.')
            name_list.append(streamer_name)  # Add new streamer to list
            update_table(name_list)  # Update table with new streamer
            entry_streamer.delete(0, tk.END)  # Clear entry field after adding

def delete_streamer_action():
    selected_item = tree.selection()
    if selected_item:
        streamer_name = tree.item(selected_item)['values'][0]
        confirmed = messagebox.askyesno('Delete Streamer', f'Are you sure you want to delete "{streamer_name}"?')
        if confirmed:
            os.remove(f"assets/logos/{streamer_name}.jpg")
            name_list.remove(streamer_name)
            if streamer_name in muted_list:
                muted_list.remove(streamer_name)
            update_ini_file()  # Update the ini file
            update_table(name_list)  # Update table after deletion
            messagebox.showinfo('Deleted', f'Streamer "{streamer_name}" deleted successfully.')
            
def show_streamer_info():
    selected_item = tree.selection()
    if selected_item:
        name = tree.item(selected_item)['values'][0]
        data = get_data(name)
        
        if not data:
            messagebox.showerror('Error', f'No data found for streamer "{name}".')
            return

        streamer_data = data[0]

        # Convert the started_at timestamp to a readable format
        started_at = streamer_data['started_at']
        duration_str=''
        if started_at:
            now = datetime.datetime.utcnow()
            started_at_datetime = datetime.datetime.strptime(started_at, "%Y-%m-%dT%H:%M:%SZ")
            duration = now - started_at_datetime
            duration_str = str(duration).split('.')[0]

        # Create a new window
        info_window = tk.Toplevel()
        info_window.title(f"{streamer_data['display_name']}'s Info")
        info_window.geometry('490x370')

        # Load and display the streamer's image
        image_path = f"assets/logos/{name}.jpg"
        image = Image.open(image_path).resize((130, 130))  # Resize as needed
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(info_window, image=photo)
        image_label.image = photo  # Keep a reference to the image
        image_label.grid(row=0, column=0, padx=19, pady=10, sticky="nw")

        # Display streamer's data
        text_info = f"Name: {streamer_data['display_name']}\n" \
                    f"Game: {streamer_data['game_name']}\n" \
                    f"Title: {streamer_data['title']}\n" \
                    f"Tags: {', '.join(streamer_data['tags'])}\n" \
                    f"Duration: {duration_str}"
        
        info_text = tk.Text(info_window, wrap="word", width=50, height=6, spacing2=6, font=("Helvetica", 12))
        info_text.insert(tk.END, text_info)
        info_text.config(state=tk.DISABLED)  # Disable editing
        info_text.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nw")
        info_text.config(spacing1=7)
        info_text.config(spacing2=7)
        info_text.config(spacing3=7)

        # Run the new window's main loop
        info_window.mainloop()
        
def isMuted(name):
    return name in muted_list

def mute_streamer_action():
    selected_item = tree.selection()
    if selected_item:
        streamer_name = tree.item(selected_item)['values'][0]
        if isMuted(streamer_name):
            muted_list.remove(streamer_name)
        else:
            muted_list.append(streamer_name)
        update_ini_file()  # Update the ini file
        update_table(isLive())  # Update table after muting/unmuting
        status = "muted" if isMuted(streamer_name) else "unmuted"
        messagebox.showinfo('Mute/Unmute', f'Streamer "{streamer_name}" has been {status}.')


# Function to update the ini file
def update_ini_file():
    config['DEFAULT']['names'] = ','.join(name_list)
    config['DEFAULT']['muted'] = ','.join(muted_list)
    with open('streamers.ini', 'w') as configfile:
        config.write(configfile)

# Read the configuration file
config = configparser.ConfigParser()
config.read('streamers.ini')

names = config['DEFAULT'].get('names', '')
name_list = [name.strip() for name in names.split(',') if name.strip()]

muted = config['DEFAULT'].get('muted', '')
muted_list = [mut.strip() for mut in muted.split(',') if mut.strip()]

# Create the main application window
root = tk.Tk()
root.geometry('800x500')
root.title('IsLive')

# Create a frame to hold the treeview and add streamer input
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the treeview
columns = ('Streamer Name', 'Status')
tree = ttk.Treeview(frame, columns=columns, show='headings')
tree.heading('Streamer Name', text='Streamer Name', anchor='w')
tree.heading('Status', text='Status', anchor='w')

# Adjust the columns' text anchor
tree.column('Streamer Name', anchor='w', stretch=tk.YES, width=300, minwidth=100)
tree.column('Status', anchor='w', stretch=tk.YES, width=200, minwidth=100)

# Add a vertical scrollbar to the treeview
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# Place the treeview and scrollbar
tree.grid(row=0, column=0, sticky='nsew')
vsb.grid(row=0, column=1, sticky='ns')

style = ttk.Style()
style.configure('Treeview', rowheight=25)
style.configure('Treeview', background='white')
style.map('Treeview', background=[('selected', 'light blue')])
style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

# Apply custom tag styles with lighter colors for a transparent effect
style.configure('live.Treeview', background='#ccffcc', )  # Light green
style.configure('offline.Treeview', background='#ffcccc')  # Light red

# Ensure the tags are applied
tree.tag_configure('live', background='#ccffcc')
tree.tag_configure('offline', background='#ffcccc')

# Create a frame for delete button on the left
frame_dlt_streamer = tk.Frame(root)
frame_dlt_streamer.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

# Create a frame for adding new streamers on the right
frame_add_streamer = tk.Frame(root)
frame_add_streamer.pack(side=tk.RIGHT, fill=tk.X, padx=30, pady=10)

# Delete Streamer button
button_delete = tk.Button(frame_dlt_streamer, text='Delete Selected', command=delete_streamer_action)
button_delete.pack(side=tk.LEFT, padx=(0, 10))

button_mute = tk.Button(frame_dlt_streamer, text='Mute/Unmute', command=mute_streamer_action)
button_mute.pack(side=tk.LEFT, padx=(0, 0))

button_info = tk.Button(frame_dlt_streamer, text='Info', command=show_streamer_info)
button_info.pack(side=tk.LEFT, padx=(10, 0))

# Add streamer input label and entry
label_streamer = tk.Label(frame_add_streamer, text='Add Streamer:')
label_streamer.pack(side=tk.LEFT, padx=(0, 10))

entry_streamer = tk.Entry(frame_add_streamer, width=40)
entry_streamer.pack(side=tk.LEFT, padx=(0, 10))

# Add Streamer button
button_add = tk.Button(frame_add_streamer, text='Add Streamer', command=add_streamer_action)
button_add.pack(side=tk.LEFT, padx=(10, 0))

# Configure the frame to expand with the window
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Function to check if streamers are live initially
isLive()

# Start the main event loop
root.mainloop()