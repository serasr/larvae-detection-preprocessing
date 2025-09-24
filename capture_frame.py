import cv2
import os
import random

def extract_frames_from_video(input_video, output_folder, num_frames):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load video and get total no. of frames
    video = cv2.VideoCapture(input_video)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Select random frames
    random_frame_ids = random.sample(range(total_frames), min(num_frames, total_frames))

    count = 0

    # Save frames to output folder
    for fid in random_frame_ids:
        video.set(cv2.CAP_PROP_POS_FRAMES, fid)  # Jump to randomly selected frame id
        success, frame = video.read()            # read video

        if success:
            image_path = os.path.join(output_folder, f"frame_{count:04d}.jpg")
            cv2.imwrite(image_path, frame)
            count += 1
    video.release()

    
extract_frames_from_video("video_00.avi", "output_frames/video_00", 5)
extract_frames_from_video("video_01.mp4", "output_frames/video_01", 7)




    