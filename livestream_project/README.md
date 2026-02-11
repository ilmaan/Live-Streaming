# 🎥 Django Live Video Streaming

A simple Django web application for live video streaming using WebRTC. Hosts can start a stream and share a unique link with anyone to join and watch in real-time.

## Features

- ✅ **Start Live Stream** - Host can start streaming with one click
- ✅ **Shareable Links** - Unique link generated for each stream
- ✅ **Real-time Viewing** - Anyone with the link can watch instantly
- ✅ **WebRTC P2P** - Peer-to-peer streaming for low latency
- ✅ **No Account Required** - Simple and easy to use
- ✅ **Responsive Design** - Works on desktop and mobile

## Tech Stack

- **Backend**: Django 4.2 + Django Channels (WebSockets)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Video**: WebRTC (Peer-to-Peer)
- **Signaling**: WebSocket via Django Channels

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Step 1: Clone/Download the Project

```bash
cd livestream_project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

### Step 5: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run the Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Usage

### For Hosts

1. Go to the home page
2. Enter your stream title and name
3. Click "Start Streaming"
4. Allow camera/microphone access when prompted
5. Copy and share the generated link with your audience
6. Click "Stop Stream" when you're done

### For Viewers

1. Click the shared link or go to `/watch/<stream_id>/`
2. The stream will automatically connect
3. Enjoy watching the live stream!

## Project Structure

```
livestream_project/
├── livestream_project/      # Django project settings
│   ├── __init__.py
│   ├── asgi.py             # ASGI config for Channels
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
├── streams/                 # Main Django app
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── consumers.py        # WebSocket consumers
│   ├── models.py           # Stream model
│   ├── routing.py          # WebSocket routing
│   ├── urls.py             # App URL patterns
│   ├── views.py            # View functions
│   └── tests.py            # Tests
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── streams/
│       ├── home.html       # Home page
│       ├── host.html       # Host streaming page
│       └── watch.html      # Viewer watching page
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## How It Works

### WebRTC Signaling Flow

1. **Host starts stream**:
   - Host opens camera and creates a WebSocket connection
   - Host waits for viewers to join

2. **Viewer joins**:
   - Viewer opens the stream link
   - Creates a WebSocket connection to the signaling server
   - Signaling server notifies host of new viewer

3. **Peer Connection**:
   - Host creates an RTCPeerConnection and sends an "offer" to viewer
   - Viewer receives offer and sends back an "answer"
   - Both exchange ICE candidates for NAT traversal
   - Direct P2P connection established

4. **Video Streaming**:
   - Host's video is sent directly to viewer via WebRTC
   - Low latency, no server processing required for video

## Configuration

### Using Redis (Production)

For production, configure Redis as the channel layer:

1. Install Redis:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # macOS
   brew install redis
   ```

2. Update `settings.py`:
   ```python
   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               'hosts': [('127.0.0.1', 6379)],
           },
       },
   }
   ```

3. Install Redis support:
   ```bash
   pip install channels-redis
   ```

### Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Generate a new secret key
3. Configure allowed hosts
4. Use HTTPS (required for WebRTC camera access)
5. Use a production ASGI server like Daphne

```bash
# Run with Daphne
daphne -b 0.0.0.0 -p 8000 livestream_project.asgi:application
```

## Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari (14+)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

**Note**: Camera access requires HTTPS in production environments.

## Troubleshooting

### Camera not working

- Make sure you've granted camera/microphone permissions
- Use HTTPS in production (required for camera access)
- Check that no other app is using the camera

### Stream not connecting

- Check browser console for errors
- Ensure WebSocket connection is established
- Try refreshing the page
- Check firewall settings (STUN servers should work through most firewalls)

### Video quality issues

- Check internet connection speed
- Close other bandwidth-heavy applications
- Reduce video resolution if needed

## Security Considerations

- This app uses public STUN servers for NAT traversal
- For production, consider using a TURN server for relaying when direct P2P fails
- Always use HTTPS in production for secure WebRTC connections
- Implement rate limiting to prevent abuse

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork and submit pull requests!

---

**Happy Streaming! 🎥**
