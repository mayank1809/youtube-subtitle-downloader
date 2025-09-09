Here’s the **ready-to-save `README.md` file** in proper Markdown format (no extra wrapping fences, just clean `.md` text):

---

# 🎬 YouTube Subtitle Downloader

A simple Python-based tool to **download subtitles from YouTube videos**.
This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to fetch metadata and subtitle files, and is packaged into a standalone `.exe` so that **non-developers can use it easily**.

---

## ✨ Features

* Download subtitles from any YouTube video (if available).
* Supports multiple subtitle formats (default: `.srt`).
* Fetch video metadata (title, duration, etc.).
* Works as a **Python script** or as a **standalone Windows `.exe`** (no Python needed).

---

## 🛠 Requirements

If running from **Python source code**:

* Python 3.8 or later
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* `requests` library

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Running with Python

Clone this repository:

```bash
git clone https://github.com/mayank1809/youtube-subtitle-downloader.git
cd youtube-subtitle-downloader
```

Run the script:

```bash
python main.py
```

You will be prompted to enter a YouTube URL:

```
Enter YouTube URL: https://www.youtube.com/watch?v=xxxxxxx
Fetching metadata and downloading subtitles...
Download complete! Subtitles saved in: video_title.srt
```

---

### 2. Running the `.exe` (Windows)

If you don’t have Python installed, you can use the pre-built `.exe` inside the `dist/` folder:

```bash
dist\main.exe
```

Then paste the YouTube URL when asked.

---

## 🏗 Building the Executable Yourself

To package the script into an `.exe`:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

The `.exe` will be created in the `dist/` folder.

---

## 📂 Project Structure

```
youtube_subtitle/
│── main.py           # Main script
│── .gitignore        # Ignore build/cache files
│── README.md         # Project documentation
│── requirements.txt  # Python dependencies
└── dist/             # Auto-created when building .exe
```

---

## ⚠️ Notes

* Subtitles will only download if the video actually has them.
* Some videos may have **auto-generated subtitles** only.
* Ensure you have a stable internet connection.

---

## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

---

## 👨‍💻 Author

**Mayank (mayank1809)**
Built as a learning project to practice Python, GitHub, and packaging.

---

👉 Save this content as `README.md` inside your project folder.
Then run:

```bash
git add README.md
git commit -m "Added detailed README"
git push
```

---

Do you also want me to generate a **requirements.txt** file with `yt-dlp` and `requests` so others can set up quickly?
