import cv2
import numpy as np
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from basicsr.utils import img2tensor, tensor2img
from realesrgan import RealESRGANer
import os
from tqdm import tqdm

def upscale_video(input_path, output_path, scale=4, model_name='RealESRGAN_x4plus'):
    """
    Upscale a video to higher resolution using RealESRGAN
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to save the upscaled video
        scale (int): Upscaling factor (default: 4)
        model_name (str): Name of the model to use. Options:
                         - RealESRGAN_x4plus (default)
                         - RealESRGAN_x4plus_anime_6B
                         - realesr-animevideov3
    """
    try:
        # Initialize the model
        if model_name == 'RealESRGAN_x4plus':
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
        elif model_name == 'RealESRGAN_x4plus_anime_6B':
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']
        elif model_name == 'realesr-animevideov3':
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=9, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
        
        # Load the model
        upsampler = RealESRGANer(
            scale=netscale,
            model_path=None,
            model=model,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=True,
            gpu_id=0
        )
        
        # Download the model weights if not exists
        model_path = load_file_from_url(url=file_url[0], 
                                      model_dir='weights', 
                                      progress=True, 
                                      file_name=None)
        upsampler.model.load_state_dict(torch.load(model_path)['params'], strict=True)
        
        # Open the video
        video = cv2.VideoCapture(input_path)
        
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate new dimensions
        new_width = width * scale
        new_height = height * scale
        
        # Ensure dimensions are divisible by 2 (required by some codecs)
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)
        
        # Initialize video writer with high quality settings
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (new_width, new_height),
            isColor=True
        )
        
        # Process each frame
        pbar = tqdm(total=frame_count, desc='Upscaling video')
        while True:
            ret, frame = video.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Upscale the frame
            output, _ = upsampler.enhance(frame_rgb, outscale=scale)
            
            # Convert back to BGR for OpenCV
            output_bgr = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
            
            # Write the frame
            out.write(output_bgr)
            
            pbar.update(1)
        
        # Clean up
        pbar.close()
        video.release()
        out.release()
        
        print(f"Video upscaled successfully and saved to: {output_path}")
        print(f"New resolution: {new_width}x{new_height}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_video = r"C:\data\hero\concat-all.mp4"
    output_video = r"C:\data\hero\concat-all-8k.mp4"
    
    # Upscale video to 8K (assuming input is 1080p)
    # Scale factor of 4 on 1080p will give approximately 8K resolution
    upscale_video(
        input_video,
        output_video,
        scale=4,
        model_name='RealESRGAN_x4plus'  # This model works best for real-world videos
    ) 