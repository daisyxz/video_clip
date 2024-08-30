from element.captions import Captions
import pandas as pd

from element.scene_clip import SceneClip
from element.captions import Captions
from element.video_control import VideoControl
from configuration.configuration import Configuration
from func.video_process import *
from func.image_process import *
from func.match_scene_and_captions import matchSceneAndCaptions
import os


class ClipManager:
    def __init__(self):
        self.captions = None
        self.scene_clip_list = list()
        self.video_control = None


    def setVideoControl(self,video_control_dict):
        video_control = VideoControl()
        video_control.mode = video_control_dict['模式']
        video_control.fps = video_control_dict['帧率']
        video_control.width = video_control_dict['分辨率的宽']
        video_control.height = video_control_dict['分辨率的高']

        video_control.video_merge  = True
        video_control.clip_save  = False
        video_control.clip_more_save = False
        if video_control.mode == "精剪":
            video_control.clip_save = True
            video_control.clip_more_save = True
            video_control.before_sec = video_control_dict['切片视频前留时间']
            video_control.after_sec = video_control_dict['切片视频后留时间']
        self.video_control = video_control
        return


    def initSceneClip(self,id, line, field_idx,orign_video_dir):
        clip = SceneClip()
        clip.id = id
        clip.caption_text = line[field_idx["caption"]]
        clip.orign_video_name = line[field_idx["origin_video_name"]]
        clip.origin_video_path = os.path.join(orign_video_dir, clip.orign_video_name) \
            if not pd.isnull(clip.orign_video_name) else ""
        clip.start_sec_in_origin_video = float(line[field_idx["start_time_sec"]]) if not pd.isnull(
            line[field_idx["start_time_sec"]]) else 0
        clip.end_sec_in_origin_video = float(line[field_idx["end_time_sec"]]) if not pd.isnull(
            line[field_idx["end_time_sec"]]) else 0
        clip.duration_sec = clip.end_sec_in_origin_video - clip.start_sec_in_origin_video
        clip.clip_type = line[field_idx["clip_type"]]
        clip.end_time_calcu_manner = line[field_idx["end_time_calcu_manner"]]
        return clip


    def initSceneClipList(self,conf):
        frame_data =  conf.frame_data_mat.data_mat
        field_idx = {f:conf.frame_data_mat.filed_idx_map[conf.frame_data_title_map[f]] for f in conf.frame_data_title_map.keys()}
        clip_list = list()
        for i in range(len(frame_data)):
            line = frame_data[i]
            clip = self.initSceneClip(i + 1, line, field_idx,conf.orign_video_dir)
            clip_list.append(clip)
        self.scene_clip_list = clip_list
        return


    def loadCaptions(self,path):
        self.captions = Captions(path)
        return

    def calcuClipEndTime(self):
        clip_id_to_cap = matchSceneAndCaptions(self.scene_clip_list, self.captions.cap_list)
        for clip in self.scene_clip_list:
            if not clip.end_time_calcu_manner == "字幕推算":
                continue
            duration = sum([cap.duration_sec for cap in  clip_id_to_cap[clip.id]])
            clip.end_sec_in_origin_video = clip.start_sec_in_origin_video + duration
            clip.duration_sec = duration
        return



    def makeImageClip(self, clip_save_dir):
        for clip in self.scene_clip_list:
            save_path = os.path.join(clip_save_dir, str(clip.id) + "_" + clip.orign_video_name + ".mp4")
            if clip.clip_type =="图片":
                img = cv2.imread(clip.origin_video_path)
                imageToVideo(img,self.video_control.fps, clip.duration_sec,save_path)
            elif clip.clip_type == "空白":
                emptyVideo(self.video_control.width,self.video_control.height,self.video_control.fps, clip.duration_sec,save_path)
        return

    def makeClipAndSave(self, clip_save_dir):
        for clip in self.scene_clip_list:
            save_path = os.path.join(clip_save_dir, str(clip.id) + "_" + clip.orign_video_name + ".mp4")
            if clip.clip_type == "视频":
                make_clip(clip.origin_video_path,clip.start_sec_in_origin_video, clip.end_sec_in_origin_video, \
                      save_path)
        self.makeImageClip(clip_save_dir)
        return

    def makeClipWithMoreTime(self, clip_save_dir):
        for clip in self.scene_clip_list:
            save_path = os.path.join(clip_save_dir, str(clip.id) + "_" + clip.orign_video_name + ".mp4")
            if clip.clip_type == "视频":
                start_time_sec = clip.start_sec_in_origin_video - self.video_control.before_sec\
                    if clip.start_sec_in_origin_video - self.video_control.before_sec>0 else 0
                end_time_sec = clip.end_sec_in_origin_video  + self.video_control.after_sec
                make_clip(clip.origin_video_path,start_time_sec,end_time_sec, \
                      save_path)
        return

    def mergeVideo(self, output_filename):
        merge_img_list = list()
        print("剪辑拼接视频中")
        for clip in self.scene_clip_list:
            clip.loadImageList()
            image_list = clip.image_list
            image_list = [imageResize(img, self.video_control.height, self.video_control.width) for img in image_list]
            if clip.clip_type == "视频":
                reset_fps_image_list = changeFpsForVideoImageList(image_list, clip.fps, self.video_control.fps)
            else:
                reset_fps_image_list = imageToVideoImgList(image_list[0], self.video_control.fps\
                                                           ,clip.duration_sec)

            merge_img_list += reset_fps_image_list
        writeVideoFromImageList(merge_img_list,self.video_control.fps, self.video_control.width, self.video_control.height\
                            ,output_filename)


    def process(self,conf):
        self.calcuClipEndTime()
        # 拼接
        if self.video_control.video_merge:
            self.mergeVideo(conf.final_video_path)

        # 剪辑视频为切片
        if self.video_control.clip_save:
            self.makeClipAndSave(conf.clip_save_dir)
        if self.video_control.clip_more_save:
            self.makeClipWithMoreTime(conf.clip_more_save_dir)
        return