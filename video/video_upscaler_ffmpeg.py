import subprocess
import os
from tqdm import tqdm
import time

# Add at the top of the file
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

def upscale_video_ffmpeg(input_path, output_path, target_height=2160):
    """
    Upscale a video using FFmpeg with high-quality settings
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to save the upscaled video
        target_height (int): Target height in pixels (default: 2160 for 4K)
    """
    try:
        # Print debug information
        print(f"FFmpeg path: {FFMPEG_PATH}")
        print(f"FFprobe path: {FFPROBE_PATH}")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        
        # Get video information using FFprobe
        probe_cmd = [
            FFPROBE_PATH,
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-of', 'csv=p=0',
            input_path
        ]
        
        print("Running FFprobe command...")
        try:
            probe_output = subprocess.check_output(probe_cmd, stderr=subprocess.PIPE)
            print(f"FFprobe output: {probe_output.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            print(f"FFprobe error: {e.stderr.decode('utf-8')}")
            raise
        
        probe_output = probe_output.decode('utf-8').strip().split(',')
        width, height = map(float, probe_output[:2])  # Only convert width and height to float
        
        # Handle fractional frame rate properly
        fps_fraction = probe_output[2]
        if '/' in fps_fraction:
            num, den = map(int, fps_fraction.split('/'))
            fps = num / den
        else:
            fps = float(fps_fraction)
        
        # Calculate new width maintaining aspect ratio
        scale = target_height / height
        new_width = int(width * scale)
        new_width = new_width - (new_width % 2)  # Ensure even number
        
        print(f"Original resolution: {int(width)}x{int(height)}")
        print(f"New resolution: {new_width}x{target_height}")
        
        # FFmpeg command with high-quality settings
        ffmpeg_cmd = [
            FFMPEG_PATH,
            '-i', input_path,
            '-vf', f'scale={new_width}:{target_height}:flags=lanczos,unsharp=5:5:1.5:5:5:0.0',
            '-c:v', 'libx264',  # Use H.264 codec
            '-preset', 'slow',   # Slower encoding = better quality
            '-crf', '18',       # High quality (lower = better, range 0-51)
            '-c:a', 'aac',      # Copy audio codec
            '-b:a', '192k',     # Audio bitrate
            '-movflags', '+faststart',  # Enable streaming
            '-y',               # Overwrite output file if exists
            output_path
        ]
        
        # Start FFmpeg process
        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Calculate total duration
        duration_cmd = [
            FFPROBE_PATH,
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_path
        ]
        duration = float(subprocess.check_output(duration_cmd).decode('utf-8').strip())
        total_frames = int(duration * fps)
        
        # Setup progress bar
        pbar = tqdm(total=total_frames, desc='Upscaling video')
        last_frame_count = 0
        
        # Monitor progress
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
                
            # Try to parse frame number from FFmpeg output
            if 'frame=' in line:
                try:
                    current_frame = int(line.split('frame=')[1].split()[0])
                    pbar.update(current_frame - last_frame_count)
                    last_frame_count = current_frame
                except:
                    pass
        
        pbar.close()
        
        # Check if process was successful
        if process.returncode == 0:
            print(f"Video upscaled successfully and saved to: {output_path}")
        else:
            raise Exception("FFmpeg encoding failed")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Clean up output file if it exists
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass

if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\hero\concat-all-text.mp4"
    output_video = r"C:\data\hero\concat-all-4k-ff.mp4"
    
    # Add debug checks
    print("\nChecking files and paths:")
    print(f"Input file exists: {os.path.exists(input_video)}")
    print(f"Input file size: {os.path.getsize(input_video) if os.path.exists(input_video) else 'N/A'} bytes")
    print(f"FFmpeg exists: {os.path.exists(FFMPEG_PATH)}")
    print(f"FFprobe exists: {os.path.exists(FFPROBE_PATH)}")
    print("\nStarting upscaling process...")
    
    upscale_video_ffmpeg(
        input_video,
        output_video,
        target_height=2160
    ) 