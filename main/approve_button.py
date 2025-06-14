import os
import gradio as gr
import shutil

# 全域片段列表
saved_clips = []

# 設定完整路徑
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_dir = os.path.join(base_dir, 'cache', 'video_clips')

def approve_btn(current_clip_path):
    """
    將當前片段路徑加入片段列表並移動到正確的儲存位置
    :param current_clip_path: 當前生成的影片片段路徑 (str or tuple)
    :return: None
    """
    # 確保目標資料夾存在
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception as e:
            gr.Warning(message=f"建立資料夾失敗: {str(e)}", duration=5)
            return

    if current_clip_path:
        # 處理路徑，確保取得正確的字串路徑
        if isinstance(current_clip_path, tuple):
            temp_path = current_clip_path[0]
        else:
            temp_path = current_clip_path
            
        if os.path.exists(temp_path):
            # 生成新的檔案名稱
            filename = os.path.basename(temp_path)
            new_path = os.path.join(save_dir, filename)
            
            try:
                # 複製檔案到正確的位置
                shutil.copy2(temp_path, new_path)
                
                # 只有成功複製後才加入列表
                if new_path not in saved_clips:
                    saved_clips.append(new_path)
                    clip_count = len(saved_clips)
                    total_duration = clip_count * 5  # 每個片段 5 秒
                    
                    gr.Warning(
                        message=f"已儲存片段至: {new_path}\n"
                               f"目前已儲存 {clip_count} 個片段\n"
                               f"總時長: {total_duration} 秒",
                        duration=15
                    )
            except Exception as e:
                gr.Warning(message=f"儲存片段時發生錯誤: {str(e)}", duration=5)
        else:
            gr.Warning(message=f"找不到影片檔案: {temp_path}", duration=5)
    else:
        gr.Warning(message="沒有可儲存的影片片段", duration=5)