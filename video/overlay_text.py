from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import os

# Configure moviepy to use ImageMagick (adjust path if necessary)
try:
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
except Exception as e:
    print(f"Warning: Could not configure ImageMagick. Text overlay might fail. Error: {e}")


def add_text_overlay(input_path, output_path, text, font_size=70, color='white', position='center', font='Arial-Bold-Italic', stroke_color='black', stroke_width=2):
    """
    Add text overlay to a video file

    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the output video will be saved
        text (str): Text to overlay on the video
        font_size (int): Size of the font (default: 70)
        color (str): Color of the text (default: 'white')
        position (str/tuple): Position of text. Can be 'center', 'top-right', 'bottom-left' etc. or tuple of (x,y) coordinates (default: 'center')
        font (str): Font name (default: 'Arial-Bold-Italic')
        stroke_color (str): Outline color for text (default: 'black')
        stroke_width (int): Outline width (default: 2)
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)

        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=font_size,
            color=color,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )

        # Set position
        padding = 5 # Pixels from edge
        if position == ('right', 'top'):
            txt_clip = txt_clip.set_position((video.w - txt_clip.w - padding, padding))
        elif position == ('left', 'bottom'):
            txt_clip = txt_clip.set_position((padding, video.h - txt_clip.h - padding))
        elif position == 'center':
             txt_clip = txt_clip.set_position('center')
        # Add more positions as needed (e.g., 'top-left', 'bottom-right')
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

if __name__ == "__main__":
    # Example usage: Add text to a specific file
    input_video = r"C:\data\hero\trim-s1.mp4" # Example input
    output_video = r"C:\data\hero\text_overlay_s1.mp4" # Example output

    add_text_overlay(
        input_path=input_video,
        output_path=output_video,
        text="Scooter Reimagined",
        font_size=50,
        color='White',
        position=('left', 'bottom') # Bottom-left position
    )

    # Example usage: Add different text to another file
    input_video_2 = r"C:\data\zomato\receipe\Channamasala\clip8-trim.mp4" # Use previous output as input
    output_video_2 = r"C:\data\zomato\receipe\Channamasala\clip8-trim-text.mp4"

    add_text_overlay(
        input_path=input_video_2,
        output_path=output_video_2,
        #text="Saute the Onion, Wholespices,\n Ginger-Garlic Paste in Oil \n Till Golden Brown at Medium Flame",
        #text="Boil the Chickpeas until soft \n 15-18 Minutes",
        #text="Add spices \n and cook for 2-3 Minutes",
        #text="Add the cut tomatoes to the pan \n Cook for 3-4 Minutes",
        #text="Finally, Add the chickpeas \n Cook for 15-20 Minutes",   
        #text="On Low flame.....",  
        text="Garnish and Serve",
        font_size=50,
        color='White',
        position=('center', 'bottom') # Top-right position
    ) 