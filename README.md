# IsStreamerLive

IsLive is a Twitch streamer monitoring application built with Python and Tkinter. It checks if specified streamers are live and displays alerts. You can add, delete, mute, and view information about streamers.

## Features

- **Live Status Monitoring**: Check if streamers are live on Twitch.
- **Blinking Popup Alerts**: Display a blinking popup when a streamer goes live.
- **Streamer Management**: Add, delete, and mute streamers.
- **Streamer Info**: View detailed information about a streamer, including the current game, stream title, tags, and duration.

## Requirements

- Python 3.7 or higher
- Required Python packages:
  - `requests`
  - `python-dotenv`
  - `Pillow`
  - `configparser`
  - `tkinter` (should be included with Python)

## Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/islive.git
    cd islive
    ```

2. **Install required packages**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file**

    ```bash
    touch .env
    ```

    Add your Twitch API credentials to the `.env` file:

    ```env
    client_id=your_twitch_client_id
    api_key=your_twitch_api_key
    ```

4. **Create a `streamers.ini` file**

    ```bash
    touch streamers.ini
    ```

    Add initial streamers and muted lists:

    ```ini
    [DEFAULT]
    names=pokimane,ironmouse
    muted=
    ```

5. **Prepare asset folders**

    Create necessary directories and add required assets:

    ```bash
    mkdir -p assets/logos
    mkdir -p assets/img
    ```

    Add a `close.png` image to `assets/img` for the popup close button.

## Usage

Run the application:

```bash
python main.py
