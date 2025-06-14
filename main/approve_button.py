import gradio as gr
# 儲存當前片段功能
# 全域片段列表
saved_clips = []

def approve_btn(current_clip_path):
    """
    將當前片段路徑加入片段列表
    :param current_clip_path: 當前生成的影片片段路徑 (str)
    :return: 已儲存片段列表
    """
    if current_clip_path and current_clip_path not in saved_clips:
        saved_clips.append(current_clip_path)
        
    gr.Warning(
        message="當前片段以儲存到" + str(current_clip_path) + "目前已儲存片段數量: " + str(len(saved_clips)),
        duration= 15
    )
    return saved_clips