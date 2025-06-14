import os
import gradio as gr

# 全域片段列表
saved_clips = []

def approve_btn(current_clip_path):
    """
    將當前片段路徑加入片段列表
    :param current_clip_path: 當前生成的影片片段路徑 (str or tuple)
    :return: None
    """
    if current_clip_path:
        # 處理路徑，確保取得正確的字串路徑
        if isinstance(current_clip_path, tuple):
            path = current_clip_path[0]  # 取得tuple中的路徑
        else:
            path = current_clip_path
            
        # 確保路徑存在且未重複儲存
        if os.path.exists(path) and path not in saved_clips:
            saved_clips.append(path)
            clip_count = len(saved_clips)
            total_duration = clip_count * 5  # 每個片段 5 秒
            
            gr.Warning(
                message=f"已儲存片段至: {path}\n"
                       f"目前已儲存 {clip_count} 個片段\n"
                       f"總時長: {total_duration} 秒",
                duration=15
            )
        else:
            gr.Warning(message="無效的影片路徑或重複的片段", duration=5)
    else:
        gr.Warning(message="沒有可儲存的影片片段", duration=5)