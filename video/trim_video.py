from moviepy.editor import VideoFileClip
import os

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

if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\zomato\receipe\noodles\clip6.mp4"
    output_trimmed = r"C:\data\zomato\receipe\noodles\clip6-trim.mp4"

    # Trim video from 3 seconds to 6 seconds
    trim_video(input_video, output_trimmed, 6, 8) 