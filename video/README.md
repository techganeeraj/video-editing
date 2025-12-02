## Video Tools & Web App

This folder contains a small Flask web app and a set of Python utilities for basic video editing tasks, built on top of MoviePy and OpenCV.

### Features

- **Web UI (`app.py`)**
  - Upload videos (and audio) through a browser.
  - **Trim** a single video between a start and end time.
  - **Stitch** multiple videos together into one.
  - **Add text overlay** to a video with configurable text, size, color, and position.
  - **Add background audio** to a video with independent volume controls for original audio and music.

- **CLI / script utilities**
  - **`video_editor.py`**: Core helpers for:
    - Trimming videos.
    - Concatenating multiple videos.
    - Adding styled text overlays.
    - Adding image/logo overlays (MoviePy or OpenCV based).
    - Adding background music to existing clips.
  - **`stitch_videos.py`**: Stand‑alone script to concatenate multiple video files.
  - **`add_audio.py`**: Stand‑alone script to add or mix background music with a video.
  - **`overlay_text.py`**: Stand‑alone script to render text over a video using ImageMagick.
  - **`overlay_image.py`**: Stand‑alone script to overlay a logo/image using OpenCV.
  - **`video_upscaler_cv2.py`**: Upscale videos (e.g. to 4K) using OpenCV, with optional sharpening.
  - **Other upscaler variants**: `video_upscaler.py`, `video_upscaler_ffmpeg.py`, `video_upscaler_simple.py` (implementation and usage are similar: upscale an input video and write a higher‑resolution output).
  - **`trim_video.py`**: Helper used by the web app to trim a single video.

### Requirements

- Python 3.9+ (recommended).
- **Libraries**:
  - `moviepy`
  - `opencv-python`
  - `numpy`
  - `flask`
  - `tqdm`
- **For text overlays**:
  - ImageMagick installed and available at the path configured in `video_editor.py` / `overlay_text.py`
    (by default something like `C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe` on Windows).

You can install the Python dependencies with:

```bash
pip install moviepy opencv-python numpy flask tqdm
```

### Folder Layout (key files)

- `app.py` – Flask web app for browser‑based trimming, stitching, text overlay, and audio overlay.
- `video_editor.py` – Collection of reusable video editing functions used from scripts or other code.
- `stitch_videos.py` – Simple entry point for concatenating multiple videos.
- `add_audio.py` – Add or mix audio tracks into a video file.
- `overlay_text.py` – Add text captions/labels to an existing video.
- `overlay_image.py` – Add a logo/watermark using OpenCV.
- `video_upscaler_cv2.py` – Resolution upscaling with OpenCV and progress display.
- `trim_video.py` – Utility for trimming a single video; used by `app.py`.

### Running the Web App

From the `video` folder:

```bash
python app.py
```

Then open your browser at `http://127.0.0.1:5000/` and use the UI to:

- Upload a video (and optionally audio).
- Choose an operation (trim, stitch, text overlay, audio overlay).
- Download the processed result from the link shown after processing.

> **Note**: The app saves uploads under an `uploads/` subfolder and processed videos under `processed/` (both are created automatically).

### Using the Scripts Directly

Each script includes an example usage block under:

```python
if __name__ == "__main__":
    ...
```

To adapt them:

- Update the hard‑coded Windows paths (`C:\data\...`) to point to your own input/output video, audio, and logo files.
- Run a script directly, e.g.:

```bash
python video_editor.py
python stitch_videos.py
python video_upscaler_cv2.py
```

These are intended as templates/snippets—copy the relevant functions into your own pipelines or adjust the paths and parameters to suit your project.


