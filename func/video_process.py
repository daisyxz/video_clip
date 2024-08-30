import os.path

import cv2
import numpy as np

def checkDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def readVideoImageList(origin_video_path, start_sec, end_sec):
    image_list = list()
    # 打开视频文件
    cap = cv2.VideoCapture(origin_video_path)
    # 获取视频的帧率、总帧数和时长
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    # 计算裁剪时间段的起始帧和结束帧
    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)
    if end_sec > duration:
        print("【错误】截止时间超过了视频长度：视频路径为" + str(origin_video_path) + ",视频长度" \
              + str(duration) + "秒,计划截取至" + str(end_sec) + "秒" )
        return
    # 跳转到裁剪时间段的起始帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 读取并写入裁剪时间段内的每一帧
    for i in range(start_frame, end_frame):
        ret, frame = cap.read()
        if ret:
            image_list.append(frame)
        else:
            break
    return image_list,fps



def make_clip(origin_video_path, start_sec, end_sec, output_filename):
    # 打开视频文件
    cap = cv2.VideoCapture(origin_video_path)
    # 获取视频的帧率、总帧数和时长
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    print("clip video，" \
          # +"fps="+str(fps)+","+str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) +\
          # ","+str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\
         + origin_video_path + ",开始时间=" \
          + str(round(start_sec,2)) + ",结束时间=" + str(round(end_sec,2)) )
    # 计算裁剪时间段的起始帧和结束帧
    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)
    if end_sec > duration:
        print("【错误】截止时间超过了视频长度：视频路径为" + str(origin_video_path) + ",视频长度" \
              + str(duration) + "秒,计划截取至" + str(end_sec) + "秒" )
        return

    # 设置裁剪后输出视频的文件名和编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # 设置输出视频的帧率和分辨率
    out_fps = fps
    out_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    out_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建输出视频的对象
    checkDir(os.path.dirname(output_filename))
    out = cv2.VideoWriter(output_filename, fourcc, out_fps, (out_width, out_height))

    # 跳转到裁剪时间段的起始帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 读取并写入裁剪时间段内的每一帧
    for i in range(start_frame, end_frame):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    # 释放对象并关闭窗口
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return


def imageToVideo(image, fps, duration, output_filename):
    out_height = image.shape[0]
    out_width = image.shape[1]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # 创建输出视频的对象
    out = cv2.VideoWriter(output_filename, fourcc, fps, (out_width, out_height))
    total_frames = int(fps*duration)
    for i in range(total_frames):
        out.write(image)
    # 释放对象并关闭窗口
    out.release()
    cv2.destroyAllWindows()
    return

def emptyVideo( out_width, out_height, fps, duration, output_filename):
    blank_image = np.zeros((out_height, out_width, 3),dtype=np.uint8)
    imageToVideo(blank_image, fps, duration, output_filename)
    return

def imageToVideoImgList(image, fps, duration):
    total_frames = int(fps*duration)
    img_list = list()
    for i in range(total_frames):
        img_list.append(image)
    # 释放对象并关闭窗口
    return img_list

def emptyVideoImgList( out_width, out_height, fps, duration):
    blank_image = np.zeros((out_height, out_width, 3),dtype=np.uint8)
    imageToVideoImgList(blank_image, fps, duration)
    return


# 视频长度不变，修改帧率（采样或插值）
def changeFpsForVideoImageList(image_list, current_fps, target_fps):
    duration = len(image_list)/current_fps
    scale = target_fps/current_fps
    target_frame_cnt = int(duration*target_fps)
    target_image_list = list()
    for i in range(target_frame_cnt):
        origin_idx = round(i/scale)
        target_image_list.append(image_list[origin_idx])
    return target_image_list


def writeVideoFromImageList(image_list, fps, width, height, filename):
    # 创建输出视频的对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    for img in  image_list:
        out.write(img)

    # 释放对象并关闭窗口
    out.release()
    cv2.destroyAllWindows()