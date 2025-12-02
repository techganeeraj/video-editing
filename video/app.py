import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

# Import your existing functions (make sure these files are in the same directory or accessible)
from trim_video import trim_video
from stitch_videos import concatenate_videos
from overlay_text import add_text_overlay
from add_audio import add_audio_to_video
# from overlay_image import add_logo_cv2 # Import if you add the image tab later

# --- Configuration ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PROCESSED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processed')
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
ALLOWED_EXTENSIONS_AUDIO = {'mp3', 'wav', 'aac', 'ogg'}
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'gif'} # For logo if added later

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.secret_key = 'your_very_secret_key' # Change this for production

# Create upload/processed folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_extensions):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, allowed_extensions):
    """Saves an uploaded file with a unique name."""
    if file and allowed_file(file.filename, allowed_extensions):
        filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None

# --- Routes ---

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/process/<task>', methods=['POST'])
def process_task(task):
    """Handles the processing for different tasks."""
    output_filename = None
    output_filepath = None
    error_message = None
    processed_video_url = None

    try:
        # --- Trim Task ---
        if task == 'trim':
            if 'video_file' not in request.files:
                raise ValueError("No video file part")
            file = request.files['video_file']
            start_time = float(request.form.get('start_time', 0))
            end_time = float(request.form.get('end_time', 0))

            if file.filename == '':
                raise ValueError("No selected video file")
            if start_time >= end_time:
                 raise ValueError("Start time must be less than end time")

            input_filepath = save_uploaded_file(file, ALLOWED_EXTENSIONS_VIDEO)
            if not input_filepath:
                 raise ValueError("Invalid file type")

            output_filename = f"trimmed_{str(uuid.uuid4())}.mp4"
            output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            trim_video(input_filepath, output_filepath, start_time, end_time)

        # --- Stitch Task ---
        elif task == 'stitch':
            files = request.files.getlist('video_files') # Get multiple files
            if not files or all(f.filename == '' for f in files):
                raise ValueError("No video files selected")

            input_filepaths = []
            for file in files:
                 filepath = save_uploaded_file(file, ALLOWED_EXTENSIONS_VIDEO)
                 if filepath:
                     input_filepaths.append(filepath)

            if len(input_filepaths) < 2:
                raise ValueError("Need at least two valid video files to stitch")

            output_filename = f"stitched_{str(uuid.uuid4())}.mp4"
            output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            concatenate_videos(input_filepaths, output_filepath)

        # --- Text Overlay Task ---
        elif task == 'text':
            if 'video_file' not in request.files:
                raise ValueError("No video file part")
            file = request.files['video_file']
            text = request.form.get('overlay_text', 'Default Text')
            font_size = int(request.form.get('font_size', 70))
            color = request.form.get('text_color', 'white')
            position = request.form.get('position', 'center')

            # Handle tuple positions like ('right', 'top') if needed
            if position == 'right_top': position = ('right', 'top')
            elif position == 'left_bottom': position = ('left', 'bottom')
            # Add other positions as needed

            if file.filename == '':
                 raise ValueError("No selected video file")

            input_filepath = save_uploaded_file(file, ALLOWED_EXTENSIONS_VIDEO)
            if not input_filepath:
                 raise ValueError("Invalid file type")

            output_filename = f"text_{str(uuid.uuid4())}.mp4"
            output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            add_text_overlay(input_filepath, output_filepath, text, font_size, color, position)

        # --- Audio Overlay Task ---
        elif task == 'audio':
            if 'video_file' not in request.files or 'audio_file' not in request.files:
                raise ValueError("Missing video or audio file")

            video_file = request.files['video_file']
            audio_file = request.files['audio_file']
            video_volume = float(request.form.get('video_volume', 0.0)) / 100.0 # Convert percentage
            music_volume = float(request.form.get('music_volume', 100.0)) / 100.0 # Convert percentage

            if video_file.filename == '' or audio_file.filename == '':
                raise ValueError("No selected video or audio file")

            input_video_path = save_uploaded_file(video_file, ALLOWED_EXTENSIONS_VIDEO)
            input_audio_path = save_uploaded_file(audio_file, ALLOWED_EXTENSIONS_AUDIO)

            if not input_video_path or not input_audio_path:
                 raise ValueError("Invalid file type for video or audio")

            output_filename = f"audio_{str(uuid.uuid4())}.mp4"
            output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            add_audio_to_video(input_video_path, input_audio_path, output_filepath, video_volume, music_volume)

        else:
            raise ValueError("Invalid task specified")

        # --- Success ---
        if output_filename and os.path.exists(output_filepath):
            processed_video_url = url_for('serve_processed', filename=output_filename)
            flash(f"Task '{task}' completed successfully!", "success")
        else:
             raise ValueError(f"Processing failed or output file not found for task '{task}'.")

    except Exception as e:
        error_message = f"Error processing task '{task}': {str(e)}"
        flash(error_message, "error")
        print(f"Error: {error_message}") # Log error to console

    # Clean up uploaded files (optional) - consider doing this in a background task
    # for file_to_remove in request.files.values():
    #     if file_to_remove and file_to_remove.filename != '':
    #          try:
    #              # Be careful here, ensure you only delete from uploads
    #              # uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], ...) # reconstruct path safely
    #              # os.remove(uploaded_path)
    #              pass # Implement safe cleanup if needed
    #          except OSError as e:
    #              print(f"Error removing uploaded file: {e}")

    return render_template('index.html', processed_video_url=processed_video_url)


@app.route('/processed/<filename>')
def serve_processed(filename):
    """Serves the processed video file."""
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True) # Turn off debug mode for production 