import argparse
import matplotlib
import matplotlib.pyplot
# Only use Agg backend if not displaying interactively
import sys
import platform

if '--no-display' in sys.argv:
    matplotlib.use('Agg')
else:
    # Use macosx backend on macOS, fallback to Qt5Agg on other platforms
    if platform.system() == 'Darwin':
        matplotlib.use('macosx')
    else:
        try:
            matplotlib.use('Qt5Agg')
        except ImportError:
            print("Warning: Interactive display not available. Using non-interactive mode.")
            matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.animation
import A_GIS.Visual.Clock.render
from datetime import datetime, timedelta
import os
from tqdm import tqdm
import time
import subprocess
import tempfile
import numpy as np


def parse_time(time_str):
    """Parse HH:MM:SS format into hour, minute, second components."""
    try:
        hour, minute, second = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise ValueError("Time values out of range")
        return hour, minute, second
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid time format. Use HH:MM:SS. Error: {str(e)}")


def resize_to_even_dimensions(image):
    """Resize image to even dimensions."""
    height, width = image.shape[:2]
    new_height = height + (height % 2)
    new_width = width + (width % 2)
    if new_height != height or new_width != width:
        return np.resize(image, (new_height, new_width, *image.shape[2:]))
    return image


def save_raw_frame(frame, output_file):
    """Save a frame as raw RGB data."""
    if frame.shape[-1] == 4:  # RGBA
        frame = frame[..., :3]
    if frame.dtype == np.float32 or frame.max() <= 1.0:
        frame = (frame * 255).astype(np.uint8)
    else:
        frame = frame.astype(np.uint8)
    frame = resize_to_even_dimensions(frame)
    frame.tofile(output_file)



def main():
    try:
        parser = argparse.ArgumentParser(description="Render a clock face with time-lapse animation")
        parser.add_argument("start_time", type=str, help="Start time in HH:MM:SS format")
        parser.add_argument("--duration", type=int, default=3600, help="Duration in seconds (default: 3600)")
        parser.add_argument("--speed", type=float, default=1.0, help="Speed factor (seconds per animation second) (default: 1.0)")
        parser.add_argument("--output", type=str, default="clock_animation.mp4", help="Output file path for the animation (default: clock_animation.mp4)")
        parser.add_argument("--no-display", action="store_true", default=True,help="Don't display frames while generating")
        parser.add_argument("--step", action="store_true", help="Step through frames with spacebar")

        args = parser.parse_args()
        
        # Ensure output file has .mp4 extension
        if not args.output.endswith('.mp4'):
            args.output = os.path.splitext(args.output)[0] + '.mp4'
        
        # Parse start time
        hour, minute, second = parse_time(args.start_time)
        start_time = datetime(2000, 1, 1, hour, minute, second)  # Using arbitrary date
        
        print(f"Starting animation from {args.start_time}")
        print(f"Duration: {args.duration} seconds")
        print(f"Speed factor: {args.speed}x")
        print(f"Output file: {args.output}")

        # Calculate number of frames needed (one per second)
        total_frames = args.duration  # One frame per second, regardless of speed
        
        # Create figure and axis
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Create progress bar
        pbar = tqdm(total=total_frames, desc="Generating frames", unit="frame")
        
        # Generate frames sequentially
        frame_times = []
        frames = []
        generation_start = time.time()
        
        for frame_num in range(total_frames):
            frame_start = time.time()
            
            # Calculate time for this frame (one second per frame)
            current_time = start_time + timedelta(seconds=frame_num)
            hour = current_time.hour
            minute = current_time.minute
            second = current_time.second

            result = A_GIS.Visual.Clock.render(
                hour=hour,
                minute=minute,
                second=second,
            )

            if result.error:
                print(f"Error: {result.error}")
                continue

            frame_time = time.time() - frame_start
            frames.append(result.image)
            frame_times.append(frame_time)
            
            # Display frame if not in no-display mode
            if not args.no_display:
                plt.clf()  # Clear the current figure
                plt.imshow(result.image)
                plt.title(f"{hour:02d}:{minute:02d}:{second:02d}")
                plt.draw()
                plt.pause(0.001)  # Small pause to allow display to update
                if args.step:
                    print("Press spacebar to continue, 'q' to quit...")
                    while True:
                        key = plt.waitforbuttonpress()
                        if key:
                            if plt.get_current_fig_manager().canvas.key_press_handler_id == 'q':
                                print("\nQuitting...")
                                sys.exit(0)
                            break
            
            pbar.update(1)
        
        generation_time = time.time() - generation_start
        avg_frame_time = sum(frame_times) / len(frame_times) if frame_times else 0
        
        # Create animation
        print("\nCreating animation...")
        animation_start = time.time()
        anim = matplotlib.animation.ArtistAnimation(
            fig,
            [[plt.imshow(frame)] for frame in frames],
            interval=1000,  # Update every 1000ms (1 second)
            blit=True,
            repeat=False
        )
        animation_time = time.time() - animation_start
        
        # Save frames as raw video
        print("Saving frames...")
        save_start = time.time()
        
        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_file = os.path.join(temp_dir, "raw_frames.raw")
            frame_save_start = time.time()
            
            # Save all frames to a single raw file
            with open(raw_file, 'wb') as f:
                for frame in frames:
                    save_raw_frame(frame, f)
            frame_save_time = time.time() - frame_save_start
            
            # Get frame dimensions
            height, width = frames[0].shape[:2]
            
            # Convert raw video to MP4 using FFmpeg with high quality settings
            print("Converting to MP4...")
            convert_start = time.time()
            cmd = [
                'ffmpeg', '-y',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-s', f'{width}x{height}',
                '-pix_fmt', 'rgb24',
                '-r', str(args.speed),  # Playback speed (e.g. speed=10 means 10 fps = 10x faster)
                '-i', raw_file,
                '-c:v', 'libx264',
                '-preset', 'medium',  # Better quality than ultrafast
                '-crf', '17',  # Lower CRF = higher quality (range 0-51, lower is better)
                '-pix_fmt', 'yuv420p',  # Required for compatibility
                '-movflags', '+faststart',  # Enable fast start for web playback
                args.output
            ]
            
            # Run FFmpeg with error output
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("FFmpeg error output:", result.stderr, file=sys.stderr)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                
            convert_time = time.time() - convert_start
            
            save_time = time.time() - save_start
            
            # Print timing statistics
            print("\nTiming Statistics:")
            print(f"Total frames generated: {len(frames)}")
            print(f"Frame generation time: {generation_time:.2f} seconds")
            print(f"Average time per frame: {avg_frame_time*1000:.2f} ms")
            print(f"Animation creation time: {animation_time:.2f} seconds")
            print(f"Frame save time: {frame_save_time:.2f} seconds")
            print(f"Video conversion time: {convert_time:.2f} seconds")
            print(f"Total save time: {save_time:.2f} seconds")
            print(f"Total processing time: {(generation_time + animation_time + save_time):.2f} seconds")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up matplotlib resources
        plt.close('all')
        if 'pbar' in locals():
            pbar.close()


if __name__ == "__main__":
    main()
