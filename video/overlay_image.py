import cv2
import numpy as np
import os
from tqdm import tqdm

def add_logo_cv2(input_path, output_path, logo_path, position='top-left', size=None, padding=5):
    """
    Add logo overlay to a video file using OpenCV

    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the output video will be saved
        logo_path (str): Path to the logo file (preferably PNG with transparency)
        position (str): Position of logo - 'top-left', 'top-right', 'bottom-left', 'bottom-right'
        size (tuple): Optional (width, height) to resize the logo. If None, original size is kept
        padding (int): Padding from edges in pixels (default: 5)
    """
    try:
        # Verify logo file exists
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found: {logo_path}")

        # Read the video
        video = cv2.VideoCapture(input_path)
        if not video.isOpened():
             raise IOError(f"Cannot open video file: {input_path}")

        # Get video properties
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Read the logo
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        if logo is None:
            raise IOError(f"Cannot read logo file: {logo_path}")

        # Resize logo if size is specified
        if size:
            logo = cv2.resize(logo, size, interpolation=cv2.INTER_AREA)

        # Get logo dimensions
        logo_h, logo_w = logo.shape[:2]

        # Calculate logo position
        if position == 'top-left':
            x = padding
            y = padding
        elif position == 'top-right':
            x = width - logo_w - padding
            y = padding
        elif position == 'bottom-left':
            x = padding
            y = height - logo_h - padding
        elif position == 'bottom-right':
            x = width - logo_w - padding
            y = height - logo_h - padding
        else: # Default to top-left if position is invalid
             print(f"Warning: Invalid position '{position}'. Defaulting to 'top-left'.")
             x = padding
             y = padding

        # Ensure logo fits within frame boundaries
        x = max(0, min(x, width - logo_w))
        y = max(0, min(y, height - logo_h))

        # Create video writer (try different codecs)
        codecs = [('mp4v', '.mp4'), ('XVID', '.avi')]
        writer = None
        for codec, ext in codecs:
            try:
                 fourcc = cv2.VideoWriter_fourcc(*codec)
                 # Adjust output path extension if needed
                 current_output_path = output_path if output_path.endswith(ext) else output_path.rsplit('.', 1)[0] + ext
                 writer = cv2.VideoWriter(current_output_path, fourcc, fps, (width, height))
                 if writer.isOpened():
                     print(f"Using codec {codec} for output: {current_output_path}")
                     break
                 else:
                     writer.release()
                     writer = None
            except:
                 if writer: writer.release()
                 writer = None

        if not writer:
            raise IOError("Could not open video writer. Check codec availability.")


        pbar = tqdm(total=frame_count, desc='Adding logo')
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Define region of interest (ROI)
            roi = frame[y:y+logo_h, x:x+logo_w]

            # Blend logo with transparency
            if logo.shape[2] == 4: # Check for alpha channel
                alpha = logo[:, :, 3] / 255.0
                for c in range(0, 3):
                    frame[y:y+logo_h, x:x+logo_w, c] = (alpha * logo[:, :, c] +
                                                     (1.0 - alpha) * roi[:, :, c])
            else: # No alpha channel, just overlay
                frame[y:y+logo_h, x:x+logo_w] = logo[:,:,:3]

            writer.write(frame)
            pbar.update(1)

        # Clean up
        pbar.close()
        video.release()
        writer.release()

        print(f"Logo overlay added successfully using OpenCV and saved to: {current_output_path}")

    except Exception as e:
        print(f"An error occurred in add_logo_cv2: {str(e)}")
        # Release resources if they were opened
        if 'video' in locals() and video.isOpened(): video.release()
        if 'writer' in locals() and writer and writer.isOpened(): writer.release()


if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\hero\some_input_video.mp4" # Input video path
    output_video = r"C:\data\hero\output_with_logo.mp4" # Output video path
    logo_path = r"C:\data\hero\hero-logo.png"    # Logo file path

    add_logo_cv2(
        input_path=input_video,
        output_path=output_video,
        logo_path=logo_path,
        position='top-left', # e.g., 'top-left', 'bottom-right'
        size=(100, 100)     # Optional: resize logo to 100x100 pixels
    ) 