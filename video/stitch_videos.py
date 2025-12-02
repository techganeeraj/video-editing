from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

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
            # Verify file exists before adding
            if not os.path.exists(path):
                print(f"Warning: Video file not found, skipping: {path}")
                continue
            clip = VideoFileClip(path)
            video_clips.append(clip)

        if not video_clips:
            print("Error: No valid video files found to concatenate.")
            return

        # Concatenate the clips
        final_clip = concatenate_videoclips(video_clips, method="compose") # Use compose for better compatibility

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

if __name__ == "__main__":
    # Example usage
    video_list = [
        r"C:\data\zomato\receipe\Noodles\clip1-trim.mp4",  # Assuming these files exist after individual processing
        r"C:\data\zomato\receipe\Noodles\clip2-trim.mp4",  
        r"C:\data\zomato\receipe\Noodles\clip3-trim.mp4",
        r"C:\data\zomato\receipe\Noodles\clip4-trim.mp4",
        r"C:\data\zomato\receipe\Noodles\clip5-trim.mp4",  
        r"C:\data\zomato\receipe\Noodles\clip6-trim.mp4",  
        r"C:\data\zomato\receipe\Noodles\clip7-trim.mp4"
        ]
    output_concatenated = r"C:\data\zomato\receipe\Noodles\concatenated_final.mp4"

    concatenate_videos(video_list, output_concatenated) 