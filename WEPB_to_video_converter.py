import os
from PIL import Image
import cv2
import numpy as np

def webp_to_mp4_preserve_fps(webp_path, mp4_path, out_fps=50):
    img = Image.open(webp_path)
    frames = []
    durations = []

    # Extract all frames and their durations (in ms)
    try:
        while True:
            frames.append(np.array(img.convert('RGB')))
            durations.append(img.info.get('duration', 100))  # Default 100ms if not specified
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    if not frames:
        print(f"No frames found in {webp_path}. Skipping.")
        return

    # Build video frames according to durations
    video_frames = []
    for i, frame in enumerate(frames):
        duration = durations[i] / 1000  # duration in seconds
        count = max(1, int(round(duration * out_fps)))
        for _ in range(count):
            video_frames.append(frame)

    height, width, _ = video_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(mp4_path, fourcc, out_fps, (width, height))
    for frame in video_frames:
        video.write(frame[..., ::-1])  # RGB to BGR
    video.release()
    print(f"Converted {webp_path} -> {mp4_path} | Out FPS: {out_fps}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    webp_dir = os.path.join(script_dir, 'webp')
    mp4_dir = os.path.join(script_dir, 'video')
    os.makedirs(mp4_dir, exist_ok=True)

    for fname in os.listdir(webp_dir):
        if fname.lower().endswith('.webp'):
            webp_path = os.path.join(webp_dir, fname)
            mp4_name = os.path.splitext(fname)[0] + '.mp4'
            mp4_path = os.path.join(mp4_dir, mp4_name)
            webp_to_mp4_preserve_fps(webp_path, mp4_path)

if __name__ == '__main__':
    main()
