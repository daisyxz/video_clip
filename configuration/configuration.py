from common.read_excel import *
FRAME_SHEET = "脚本及对应视频"
FILE_PATH_SHEET = "文件路径"
VIDEO_CONTROL_SHEET = "视频配置"

ORIGIN_VIDEO = "原始视频文件夹"
CAPTIONS = "字幕脚本文件"
CLIP_SAVE = "切片视频保存文件夹"
CLIP_MORE_SAVE = "切片视频保存文件夹（前后预留时长）"
FINAL_VIDEO_PATH = "剪辑拼接视频路径"

class Configuration:
    def __init__(self, path):
        self.path = path
        self.frame_data_mat = None
        self.frame_data_title_map = dict()
        self.orign_video_dir = ""
        self.captions_file_path = ""
        self.final_video_path = ""
        self.clip_save_dir = ""
        self.clip_more_save_dir = ""
        self.frame_data_title_map = dict({"caption":"小场景（脚本、字幕）","origin_video_name":"实际找到的素材内容",\
                                     "start_time_sec":"起始时间（秒）","end_time_sec":"结束时间（秒）",\
                                          "clip_type":"片段类型","end_time_calcu_manner":"结束时间获取途径"})
        self.video_control_dict = dict()
        self.frame_sheet = FRAME_SHEET

    def parseConfig(self):
        # 解析脚本框架
        self.frame_data_mat = readExcelMatrix(self.path, self.frame_sheet)
        # 读取文件路径
        data = readExcelMatrix(self.path, FILE_PATH_SHEET)
        path_dict = {line[0]:line[1] for line in data.data_mat}
        self.orign_video_dir = path_dict[ORIGIN_VIDEO]
        self.captions_file_path =  path_dict[CAPTIONS]
        self.final_video_path = path_dict[FINAL_VIDEO_PATH]
        self.clip_save_dir = path_dict[CLIP_SAVE]
        self.clip_more_save_dir = path_dict[CLIP_MORE_SAVE]
        # 读取视频配置
        data = readExcelMatrix(self.path, VIDEO_CONTROL_SHEET)
        self.video_control_dict = {line[0]:line[1] for line in data.data_mat}




