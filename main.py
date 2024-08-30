from configuration.configuration import Configuration
from element.clip_manager import ClipManager


if __name__ == '__main__':
    # 加载配置
    conf_path = "/Users/xinzi_z/Desktop/工作/xhs_video/20240820【宠物科普】猫咪长寿/【宠物科普】猫咪长寿.xlsx"
    conf = Configuration(conf_path)
    conf.frame_sheet = "脚本及对应视频"
    conf.parseConfig()
    #读取视频控制
    clip_manager = ClipManager()
    clip_manager.setVideoControl(conf.video_control_dict)
    # 读取主控脚本文件等
    clip_manager.initSceneClipList(conf)
    # 读取字幕文件
    clip_manager.loadCaptions(conf.captions_file_path)
    # 剪辑处理
    clip_manager.process(conf)

