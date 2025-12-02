from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips
import os

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
            num_loops = int(video.duration // audio.duration) + 1
            audio = concatenate_audioclips([audio] * num_loops)


        # Trim audio if it's longer than video
        if audio.duration > video.duration:
             audio = audio.subclip(0, video.duration)

        # Adjust music volume
        audio = audio.volumex(music_volume)

        # Combine original audio with music if needed
        if original_audio:
            # Use CompositeAudioClip for combining
            final_audio = CompositeAudioClip([original_audio, audio])
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
        # final_audio might be the same object as audio or original_audio, no separate close needed
        final_video.close()

        print(f"Audio added successfully and saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\zomato\receipe\Noodles\concatenated_final.mp4" # Video without audio or with audio to adjust
    output_video = r"C:\data\zomato\receipe\Noodles\final_video_with_music.mp4" # Final output path
    music_path = r"C:\data\zomato\receipe\Noodles\s2.wav" # Path to your music file

    add_audio_to_video(
        video_path=input_video,
        audio_path=music_path,
        output_path=output_video,
        video_audio_factor=0.0,  # Keep some original audio at 30% volume (if it exists)
        music_volume=0.5        # Background music at 70% volume
    ) 