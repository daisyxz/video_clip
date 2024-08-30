from element.caption import Caption
class Captions:
    def __init__(self, path):
        self.cap_list = self.loadCaptions(path)
        self.len = len(self.cap_list)



    def loadCaptions(self,path):
        cap_list = list()

        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            clip_info_dict = {}
            for line in lines:
                line = line.strip()
                if not line:
                    if 'text' in clip_info_dict:
                        cap = Caption(clip_info_dict)
                        cap_list.append(cap)
                        clip_info_dict = {}
                else:
                    if line.isdigit():
                        clip_info_dict['id'] = int(line)
                    elif '-->' in line:
                        parts = line.split('-->')
                        clip_info_dict['start_time'] = parts[0].strip()
                        clip_info_dict['end_time'] = parts[1].strip()
                    else:
                        if 'text' not in clip_info_dict:
                            clip_info_dict['text'] = line
                        else:
                            clip_info_dict['text'] += '\n' + line
        for i in range(len(cap_list)):
            if i == len(cap_list) - 1:
                continue
            cap_list[i].end_time_sec = cap_list[i+1].start_time_sec
            cap_list[i].end_time = cap_list[i + 1].start_time
            cap_list[i].duration_sec = cap_list[i].end_time_sec - cap_list[i].start_time_sec
        return cap_list

