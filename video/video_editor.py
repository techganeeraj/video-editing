from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip, AudioFileClip
import os
from moviepy.config import change_settings
import cv2
import numpy as np

# Configure moviepy to use ImageMagick
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def trim_video(input_path, output_path, start_time, end_time):
    """
    Trim a video file based on start and end times (in seconds)
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the trimmed video will be saved
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
    """
    try:
        # Load the video file
        video = VideoFileClip(input_path)
        
        # Trim the video
        trimmed_video = video.subclip(start_time, end_time)
        
        # Write the trimmed video to file
        trimmed_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Close the video files to free up memory
        video.close()
        trimmed_video.close()
        
        print(f"Video trimmed successfully and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def concatenate_videos(video_paths, output_path):
    """
    Concatenate multiple videos in sequence
    
    Args:
        video_paths (list): List of paths to video files in desired sequence
        output_path (str): Path where the final concatenated video will be saved
    """
    try:
        # Load all video clips
        video_clips = []
        for path in video_paths:
            clip = VideoFileClip(path)
            video_clips.append(clip)
        
        # Concatenate the clips
        final_clip = concatenate_videoclips(video_clips)
        
        # Write the final video to file
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Close all clips to free up memory
        for clip in video_clips:
            clip.close()
        final_clip.close()
        
        print(f"Videos concatenated successfully and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def add_text_overlay(input_path, output_path, text, font_size=70, color='white', position='center'):
    """
    Add text overlay to a video file
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the output video will be saved
        text (str): Text to overlay on the video
        font_size (int): Size of the font (default: 70)
        color (str): Color of the text (default: 'white')
        position (str/tuple): Position of text. Can be 'center', 'top', 'bottom' 
                            or tuple of (x,y) coordinates (default: 'center')
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Create text clip with bold and italic styling
        txt_clip = TextClip(
            text, 
            fontsize=font_size, 
            color=color,
            font='Arial-Bold-Italic',  # Use Arial Bold Italic font
            stroke_color='black',      # Add stroke for better visibility
            stroke_width=2             # Stroke width
        )
        
        # Set position
        if position == ('right', 'top'):
            txt_clip = txt_clip.set_position((video.w - txt_clip.w - 5, 5))
        elif position == ('right', 'bottom'):
            txt_clip = txt_clip.set_position((video.w - txt_clip.w - 5, video.h - txt_clip.h - 5))
        elif position == ('left', 'bottom'):
            txt_clip = txt_clip.set_position((5, video.h - txt_clip.h - 5))
        elif position == 'center':
            txt_clip = txt_clip.set_position('center')
        elif position == 'top':
            txt_clip = txt_clip.set_position(('center', 20))
        elif position == 'bottom':
            txt_clip = txt_clip.set_position(('center', video.h - txt_clip.h - 20))
        else:
            txt_clip = txt_clip.set_position(position)
        
        # Set duration to match video
        txt_clip = txt_clip.set_duration(video.duration)
        
        # Combine video and text
        video_with_text = CompositeVideoClip([video, txt_clip])
        
        # Write the result to file
        video_with_text.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        video.close()
        txt_clip.close()
        video_with_text.close()
        
        print(f"Text overlay added successfully and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def add_image_overlay(input_path, output_path, image_path, position='center', size=None):
    """
    Add image/logo overlay to a video file
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the output video will be saved
        image_path (str): Path to the image/logo file
        position (str/tuple): Position of image. Can be 'center', 'top-right', 'bottom-right',
                            'top-left', 'bottom-left' or tuple of (x,y) coordinates (default: 'center')
        size (tuple): Optional (width, height) to resize the image. If None, original size is kept
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Load and create the image clip with duration parameter
        image_clip = ImageClip(image_path).set_duration(video.duration)
        
        # Resize image if size is specified
        if size:
            width, height = size
            image_clip = image_clip.resize(newsize=(width, height))  # Using newsize parameter instead
        
        # Set position
        if position == 'center':
            image_clip = image_clip.set_position('center')
        elif position == 'top-right':
            image_clip = image_clip.set_position((video.w - image_clip.w - 20, 20))
        elif position == 'bottom-right':
            image_clip = image_clip.set_position((video.w - image_clip.w - 20, video.h - image_clip.h - 20))
        elif position == 'top-left':
            image_clip = image_clip.set_position((20, 20))
        elif position == 'bottom-left':
            image_clip = image_clip.set_position((20, video.h - image_clip.h - 20))
        else:
            image_clip = image_clip.set_position(position)
        
        # Combine video and image
        video_with_image = CompositeVideoClip([video, image_clip])
        
        # Write the result to file
        video_with_image.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        video.close()
        image_clip.close()
        video_with_image.close()
        
        print(f"Image overlay added successfully and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def add_logo_cv2(input_path, output_path, logo_path, position='top-left', size=None):
    """
    Add logo overlay to a video file using OpenCV
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the output video will be saved
        logo_path (str): Path to the logo file (preferably PNG with transparency)
        position (str): Position of logo - 'top-left', 'top-right', 'bottom-left', 'bottom-right'
        size (tuple): Optional (width, height) to resize the logo. If None, original size is kept
    """
    try:
        # Read the video
        video = cv2.VideoCapture(input_path)
        
        # Get video properties
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Read the logo
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        
        # Resize logo if size is specified
        if size:
            logo = cv2.resize(logo, size, interpolation=cv2.INTER_AREA)
        
        # Get logo dimensions
        logo_h, logo_w = logo.shape[:2]
        
        # Calculate logo position
        padding = 5  # Reduced padding from 10 to 5 pixels
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
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = video.read()
            if not ret:
                break
                
            # Create ROI for logo
            roi = frame[y:y+logo_h, x:x+logo_w]
            
            # If logo has transparency (4 channels)
            if logo.shape[2] == 4:
                # Separate alpha channel
                alpha = logo[:, :, 3] / 255.0
                # Process each color channel
                for c in range(3):
                    frame[y:y+logo_h, x:x+logo_w, c] = (
                        (1 - alpha) * roi[:, :, c] +
                        alpha * logo[:, :, c]
                    )
            else:
                # If no transparency, simply overlay
                frame[y:y+logo_h, x:x+logo_w] = logo[:, :, :3]
            
            out.write(frame)
        
        # Clean up
        video.release()
        out.release()
        
        print(f"Logo overlay added successfully using OpenCV and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def add_audio_to_video(video_path, audio_path, output_path, video_audio_factor=0.0, music_volume=1.0):
    """
    Add background music to a video file
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the audio file (mp3, wav, etc.)
        output_path (str): Path where the output video will be saved
        video_audio_factor (float): Volume factor for original video audio (0.0 to 1.0, default 0.0 - mute)
        music_volume (float): Volume factor for added music (0.0 to 1.0, default 1.0)
    """
    try:
        # Load the video
        video = VideoFileClip(video_path)
        
        # Load the audio
        audio = AudioFileClip(audio_path)
        
        # Get original video audio if needed and if it exists
        original_audio = None
        if video_audio_factor > 0 and video.audio is not None:
            original_audio = video.audio.volumex(video_audio_factor)
        
        # If audio is shorter than video, loop it
        if audio.duration < video.duration:
            # Calculate how many times to loop
            repeats = int(video.duration / audio.duration) + 1
            audio = concatenate_videoclips([audio] * repeats)
        
        # Trim audio if it's longer than video
        audio = audio.subclip(0, video.duration)
        
        # Adjust music volume
        audio = audio.volumex(music_volume)
        
        # Combine original audio with music if needed
        if original_audio:
            final_audio = CompositeVideoClip([original_audio, audio])
        else:
            final_audio = audio
        
        # Set the audio to the video
        final_video = video.set_audio(final_audio)
        
        # Write the result to file
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        video.close()
        audio.close()
        if original_audio:
            original_audio.close()
        final_video.close()
        
        print(f"Audio added successfully and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Base paths
    base_dir = r"C:\data\hero"
    logo_path = r"C:\data\hero\hero-logo.png"
    
    # Verify logo file exists
    # if not os.path.exists(logo_path):
    #     print(f"Error: Logo file not found at {logo_path}")
    #     exit(1)
    
    # # Process each video file (s1 through s12)
    # for i in range(1, 13):
    #     if i == 2:  # Skip s2
    #         continue
            
    #     input_video = fr"{base_dir}\trim-s{i}.mp4"
        
    #     # Verify input video exists
    #     if not os.path.exists(input_video):
    #         print(f"Warning: Input video not found: {input_video}")
    #         continue
            
    #     try:
    #         # First add text
    #         temp_output = fr"{base_dir}\temp-s{i}.mp4"
    #         add_text_overlay(
    #             input_video,
    #             temp_output,
    #             "Hero Xoom 160",
    #             font_size=70,
    #             color='Red',
    #             position=('right', 'top')  # Changed to top-right
    #         )
            
    #         # Verify temp file was created
    #         if not os.path.exists(temp_output):
    #             raise Exception(f"Failed to create temporary file: {temp_output}")
            
    #         # Then add logo
    #         final_output = fr"{base_dir}\final-s{i}.mp4"
    #         add_logo_cv2(
    #             temp_output,
    #             final_output,
    #             logo_path,
    #             position='top-left',
    #             size=(100, 100)
    #         )
            
    #         # Verify final file was created
    #         if not os.path.exists(final_output):
    #             raise Exception(f"Failed to create final file: {final_output}")
            
    #         # Clean up temporary file
    #         try:
    #             os.remove(temp_output)
    #         except Exception as e:
    #             print(f"Warning: Could not remove temporary file {temp_output}: {str(e)}")
            
    #         print(f"Successfully processed video s{i}")
            
    #     except Exception as e:
    #         print(f"Error processing video s{i}: {str(e)}")
    #         # Try to clean up temp file if it exists
    #         if os.path.exists(temp_output):
    #             try:
    #                 os.remove(temp_output)
    #             except:
    #                 pass
    #         continue
    
    # print("Processing complete!")
    
    # Example of trimming a video
    # input_video = r"C:\data\hero\s23.mp4"
    # output_trimmed = r"C:\data\hero\trim-s23.mp4"
    # trim_video(input_video, output_trimmed, 1,3)
    
    # Example of concatenating videos
    video_list = [
       r"C:\data\hero\temp_trim-s1.mp4",
    #    r"C:\data\hero\temp_trim-s2.mp4",
    #    r"C:\data\hero\temp_trim-s3.mp4",
    #    r"C:\data\hero\temp_trim-s4.mp4",
    #    r"C:\data\hero\temp_trim-s5.mp4",
    #    r"C:\data\hero\temp_trim-s6.mp4",
    #    r"C:\data\hero\temp_trim-s7.mp4",
    #    r"C:\data\hero\temp_trim-s8.mp4",
    #    r"C:\data\hero\temp_trim-s9.mp4",
    #    r"C:\data\hero\temp_trim-s10.mp4",
    #    r"C:\data\hero\temp_trim-s11.mp4",
       r"C:\data\hero\temp_trim-s12.mp4"
    ]
    output_concatenated = r"C:\data\hero\concat-all-text11.mp4"
    concatenate_videos(video_list, output_concatenated)
    
    # Example of adding text overlay
    # input_video = r"C:\data\hero\trim-s1.mp4"
    # output_video = r"C:\data\hero\trim-s1-text.mp4"
    # add_text_overlay(
    #     input_video,
    #     output_video,
    #     "Hero Xoom 160",
    #     font_size=70,
    #     color='Red',
    #     position=('right', 'bottom')
    # )
    
    # Example of adding background music
    # input_video = r"C:\data\hero\final_video.mp4"
    # output_video = r"C:\data\hero\final_video_with_music.mp4"
    # music_path = r"C:\data\hero\audio.mp3"
    # add_audio_to_video(
    #     input_video,
    #     music_path,
    #     output_video,
    #     video_audio_factor=0.3,  # Keep some original audio at 30% volume
    #     music_volume=0.9         # Background music at 70% volume
    # )
    
    # Add text to individual files at bottom-left
    # text_overlays = {
    #      'trim-s7.mp4': "Twin Rear Suspension"
    # }
    
    # Process each file with its specific text
    # for input_file, text in text_overlays.items():
    #     input_path = fr"{base_dir}\{input_file}"
    #     temp_output = fr"{base_dir}\temp_{input_file}"
        
    #     # Add the specific text at bottom-left with bold italic
    #     add_text_overlay(
    #         input_path,
    #         temp_output,
    #         text,
    #         font_size=50,
    #         color='White',
    #         position=('left', 'bottom')
    #     )
        
    #     # Add "Hero Xoom 160" text at top-right with bold italic
    #     final_output = fr"{base_dir}\final_{input_file}"
    #     add_text_overlay(
    #         temp_output,
    #         final_output,
    #         "Hero Xoom 160",
    #         font_size=70,
    #         color='Red',
    #         position=('right', 'top')
    #     )
        
        # Clean up temporary file
        # try:
        #     os.remove(temp_output)
        # except:
        #     pass
        
        # print(f"Processed {input_file} with text: {text}")
    
    # Rest of your existing code... 