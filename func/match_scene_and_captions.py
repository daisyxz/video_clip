
def replaceSymble(text):
    replace_symbol = [",", "?", "!", "，", "？", "！", "。"]
    for s in replace_symbol:
        text = text.replace(s, "")
    return text

def matchCaptions(clip,captions):
    clip_text = replaceSymble(clip.caption_text)
    match_cap_list = []
    for cap in captions:
        text = replaceSymble(cap.text)
        if text in clip_text:
            match_cap_list.append(cap)
        else:
            break
    return match_cap_list

def matchSceneAndCaptions(scene_clip_list, captions):
    scene_clip_id_to_captions = dict()
    start_idx = 0
    for clip in scene_clip_list:
        match_cap_list = matchCaptions(clip,captions[start_idx:] )
        scene_clip_id_to_captions[clip.id] = match_cap_list
        start_idx += len(match_cap_list)
    return scene_clip_id_to_captions
