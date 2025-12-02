import cv2
import numpy as np
from tqdm import tqdm
import os

def upscale_video(input_path, output_path, target_height=2160):
    """
    Upscale a video to a target resolution while maintaining aspect ratio
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to save the upscaled video
        target_height (int): Target height in pixels (default: 2160 for 4K)
    """
    try:
        # Open the video
        video = cv2.VideoCapture(input_path)
        
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate new dimensions maintaining aspect ratio
        scale = target_height / height
        new_width = int(width * scale)
        new_height = target_height
        
        # Ensure dimensions are divisible by 2 (required by some codecs)
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)
        
        print(f"Original resolution: {width}x{height}")
        print(f"New resolution: {new_width}x{new_height}")
        
        # Calculate target bitrate (higher for better quality)
        target_bitrate = int(new_width * new_height * fps * 0.2)  # 0.2 bits per pixel
        
        # Try different codecs in order of preference
        codecs = [
            ('mp4v', '.mp4'),  # Added this as first option
            ('XVID', '.avi'),
            ('MJPG', '.avi'),
            ('DIVX', '.avi'),
            ('avc1', '.mp4'),
            ('H264', '.mp4')
        ]
        
        # Try each codec until one works
        writer = None
        for codec, ext in codecs:
            try:
                if output_path.endswith('.mp4') and not ext.endswith('.mp4'):
                    current_output = output_path.rsplit('.', 1)[0] + ext
                else:
                    current_output = output_path
                
                fourcc = cv2.VideoWriter_fourcc(*codec)
                writer = cv2.VideoWriter(
                    current_output,
                    fourcc,
                    fps,
                    (new_width, new_height),
                    isColor=True
                )
                
                if writer.isOpened():
                    print(f"Using codec: {codec}")
                    # Set bitrate if codec supports it
                    try:
                        writer.set(cv2.VIDEOWRITER_PROP_QUALITY, 100)  # Highest quality
                        writer.set(cv2.VIDEOWRITER_PROP_BITRATE, target_bitrate)
                    except:
                        pass
                    break
                else:
                    writer.release()
                    writer = None
                    
            except Exception as e:
                print(f"Codec {codec} failed: {str(e)}")
                if writer is not None:
                    writer.release()
                    writer = None
        
        if writer is None:
            raise Exception("No working codec found")
        
        # Process each frame
        pbar = tqdm(total=frame_count, desc='Upscaling video')
        while True:
            ret, frame = video.read()
            if not ret:
                break
            
            # Upscale the frame using Lanczos interpolation
            upscaled = cv2.resize(
                frame, 
                (new_width, new_height), 
                interpolation=cv2.INTER_LANCZOS4
            )
            
            # Apply sharpening
            kernel = np.array([[-1,-1,-1],
                             [-1, 9,-1],
                             [-1,-1,-1]]) / 9
            upscaled = cv2.filter2D(upscaled, -1, kernel)
            
            # Write the frame
            writer.write(upscaled)
            
            pbar.update(1)
        
        # Clean up
        pbar.close()
        video.release()
        writer.release()
        
        print(f"Video upscaled successfully and saved to: {current_output}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'video' in locals():
            video.release()
        if 'writer' in locals() and writer is not None:
            writer.release()

if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\hero\concat-all-text.mp4"
    output_video = r"C:\data\hero\concat-all-4k.avi"  # Changed to .avi
    
    # Upscale to different resolutions:
    # 2160 for 4K (3840x2160)
    # 4320 for 8K (7680x4320)
    upscale_video(
        input_video,
        output_video,
        target_height=2160  # Change to 4320 for 8K
    ) 