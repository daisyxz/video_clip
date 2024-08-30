from func.video_process import *

class SceneClip:
    def __init__(self):
        self.id = -1
        self.caption_text = ""
        self.clip_type = ""
        self.orign_video_name = ""
        self.origin_video_path = ""
        self.start_sec_in_origin_video = 0
        self.end_sec_in_origin_video = 0
        self.duration_sec = 0
        self.fps = 0
        self.img_list = list()
        self.end_time_calcu_manner = ""


    def loadImageList(self):
        if self.clip_type == "视频":
            image_list, self.fps = readVideoImageList(self.origin_video_path\
                                                     ,self.start_sec_in_origin_video,self.end_sec_in_origin_video)
        elif self.clip_type == "图片":
            img = cv2.imread(self.origin_video_path)
            image_list = [img]
        else:
            blank_image = np.zeros((300, 400, 3), dtype=np.uint8)
            image_list = [blank_image]

        self.image_list = image_list


    


