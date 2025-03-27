import argparse
import matplotlib
import matplotlib.pyplot as plt
import A_GIS.Visual.Clock.render
from datetime import datetime, timedelta
import sys
import platform
import numpy as np
import io
import cairosvg
from PIL import Image
import time

# Use macosx backend on macOS, fallback to Qt5Agg on other platforms
if platform.system() == 'Darwin':
    try:
        matplotlib.use('macosx')
    except ImportError:
        print("Warning: macosx backend not available, trying Qt5Agg...")
        try:
            matplotlib.use('Qt5Agg')
        except ImportError:
            print("Warning: Qt5Agg backend not available, using Agg...")
            matplotlib.use('Agg')
else:
    try:
        matplotlib.use('Qt5Agg')
    except ImportError:
        print("Warning: Qt5Agg backend not available, using Agg...")
        matplotlib.use('Agg')

def svg_to_array(svg_data):
    """Convert SVG data to numpy array."""
    try:
        print("Converting SVG to array...")
        # Convert SVG to PNG using cairosvg
        png_data = cairosvg.svg2png(bytestring=svg_data)
        print("SVG converted to PNG")
        
        # Convert PNG data to PIL Image
        image = Image.open(io.BytesIO(png_data))
        print(f"PNG loaded as PIL Image: {image.size}")
        
        # Convert to numpy array
        array = np.array(image)
        print(f"Converted to numpy array: {array.shape}")
        return array
    except Exception as e:
        print(f"Error converting SVG to array: {e}")
        return None

def parse_time(time_str):
    """Parse HH:MM:SS format into hour, minute, second components."""
    try:
        hour, minute, second = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise ValueError("Time values out of range")
        return hour, minute, second
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid time format. Use HH:MM:SS. Error: {str(e)}")

def show_static_clock(hour, minute, second):
    """Show a static clock face."""
    print(f"Showing static clock at {hour:02d}:{minute:02d}:{second:02d}")
    
    # Create figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Render clock face
    print("Rendering clock face...")
    result = A_GIS.Visual.Clock.render(
        hour=hour,
        minute=minute,
        second=second,
    )
    
    if result.error:
        print(f"Error: {result.error}")
        return
    
    # Convert SVG to array and display
    image_array = svg_to_array(result.svg)
    if image_array is not None:
        print("Displaying clock face...")
        ax.imshow(image_array)
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        ax.set_title(f"Time: {time_str}")
        
        plt.show(block=True)
        plt.close('all')

def show_animated_clock(hour, minute, second, duration, speedup=1.0):
    """Show an animated clock face.
    
    Args:
        hour: Starting hour
        minute: Starting minute
        second: Starting second
        duration: Duration in seconds
        speedup: Speed multiplier (1.0 = real time, >1 = faster, <1 = slower)
    """
    print(f"Starting animation from {hour:02d}:{minute:02d}:{second:02d}")
    print(f"Duration: {duration} seconds")
    print(f"Speedup: {speedup}x")
    
    # Calculate target frame interval
    target_interval = 1.0 / speedup
    print(f"Target frame interval: {target_interval:.3f} seconds")
    
    # Create figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Set start time
    start_time = datetime(2000, 1, 1, hour, minute, second)
    start_wall_time = time.time()
    
    try:
        while True:
            try:
                # Calculate how much time has passed in wall clock time
                wall_time_elapsed = time.time() - start_wall_time
                
                # Calculate target time based on wall time and speedup
                target_seconds = int(wall_time_elapsed * speedup)
                target_time = start_time + timedelta(seconds=target_seconds)
                
                # Get current time components
                hour = target_time.hour
                minute = target_time.minute
                second = target_time.second
                
                print(f"\nRendering frame at {hour:02d}:{minute:02d}:{second:02d}")
                
                # Clear previous frame
                ax.clear()
                ax.axis('off')
                
                # Render new frame
                result = A_GIS.Visual.Clock.render(
                    hour=hour,
                    minute=minute,
                    second=second,
                )
                
                if result.error:
                    print(f"Error: {result.error}")
                    continue
                
                # Convert SVG to array and display
                image_array = svg_to_array(result.svg)
                if image_array is not None:
                    print("Displaying clock face...")
                    ax.imshow(image_array)
                    time_str = target_time.strftime("%H:%M:%S")
                    ax.set_title(f"Time: {time_str} (Speed: {speedup}x)")
                    
                    # Update display
                    plt.draw()
                    
                    # Sleep for the target interval
                    plt.pause(target_interval)
                
                # Check if we've reached the duration
                if target_seconds >= duration:
                    break
                
            except Exception as e:
                print(f"Error updating frame: {e}")
                time.sleep(target_interval)  # Wait a bit before retrying
                
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    finally:
        plt.close('all')

def main():
    try:
        parser = argparse.ArgumentParser(description="Render a clock face")
        parser.add_argument("start_time", type=str, help="Start time in HH:MM:SS format")
        parser.add_argument("--duration", type=int, default=0, help="Duration in seconds (0 for static, default: 0)")
        parser.add_argument("--speedup", type=float, default=1.0, help="Speed multiplier (1.0 = real time, >1 = faster, <1 = slower)")
        
        args = parser.parse_args()
        
        # Validate speedup
        if args.speedup <= 0:
            print("Error: Speedup must be positive", file=sys.stderr)
            sys.exit(1)
        
        # Parse start time
        hour, minute, second = parse_time(args.start_time)
        
        # Show static or animated clock
        if args.duration == 0:
            show_static_clock(hour, minute, second)
        else:
            show_animated_clock(hour, minute, second, args.duration, args.speedup)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        plt.close('all')

if __name__ == "__main__":
    main()
