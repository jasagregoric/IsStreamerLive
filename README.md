# IsStreamerLive

IsStreamerLive is a Twitch streamer monitoring application built with Python and Tkinter. It checks if specified streamers are live and displays alerts. You can add, delete, mute, and view information about streamers.

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
    git clone https://github.com/jasagregoric/IsStreamerLive.git
    cd IsStreamerLive
    ```

2. **Create a `.env` file**

    ```bash
    touch .env
    ```

    Add your Twitch API credentials to the `.env` file:

    ```env
    client_id=your_twitch_client_id
    api_key=your_twitch_api_key
    ```

## Usage

Run the application:

```bash
python main.py
