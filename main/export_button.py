import os
import shutil
import gradio as gr
from moviepy.editor import concatenate_videoclips, VideoFileClip
import datetime

def export_btn():
    """
    將 cache/video_clips 目錄中的所有影片依序串接並匯出為完整影片，完成後清除暫存的影片檔案
    :return: None
    """
    # 設定 video_clips 目錄路徑
    video_clips_dir = os.path.join(os.getcwd(), "cache", "video_clips")
    
    if not os.path.exists(video_clips_dir):
        gr.Warning(message="找不到 video_clips 目錄，請先儲存片段。")
        return None
    
    # 獲取目錄中的所有 mp4 檔案
    video_files = []
    try:
        for filename in os.listdir(video_clips_dir):
            if filename.lower().endswith('.mp4'):
                video_files.append(os.path.join(video_clips_dir, filename))
    except Exception as e:
        gr.Warning(message=f"讀取 video_clips 目錄失敗: {str(e)}")
        return None
    
    if not video_files:
        gr.Warning(message="video_clips 目錄中沒有找到任何影片檔案，請先儲存片段。")
        return None
    
    # 按檔名排序，確保順序正確
    video_files.sort()

    try:
        # 設定輸出路徑
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        name = '{0:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())    
        output_path = os.path.join(output_dir, f"gallery_{name}.mp4")
        
        # 驗證並載入影片片段
        valid_clips = []
        for path in video_files:
            try:
                if os.path.exists(path):
                    clip = VideoFileClip(path)
                    valid_clips.append(clip)
                    print(f"載入影片: {os.path.basename(path)}")
                else:
                    print(f"找不到影片檔案: {path}")
            except Exception as e:
                print(f"載入影片失敗 {path}: {str(e)}")
                continue
        
        if not valid_clips:
            gr.Warning(message="無法載入任何有效的影片片段，請確認檔案是否存在。")
            return None
            
        # 串接並輸出
        print(f"開始合併 {len(valid_clips)} 個影片片段...")
        final_clip = concatenate_videoclips(valid_clips, method="compose")
        
        print(f"正在輸出到 {output_path}")
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=16,
            threads=4,
            verbose=False,
            logger=None
        )
                                 
        # 關閉所有 clip 以釋放資源
        for c in valid_clips:
            c.close()
        final_clip.close()
        
        # 清除 video_clips 目錄中的檔案
        for path in video_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"已刪除暫存檔案: {os.path.basename(path)}")
            except Exception as e:
                print(f"刪除檔案失敗 {path}: {str(e)}")
                continue
        
        # 如果 video_clips 目錄為空，可以選擇刪除該目錄
        try:
            if not os.listdir(video_clips_dir):
                os.rmdir(video_clips_dir)
                print("已刪除空的 video_clips 目錄")
        except Exception as e:
            print(f"刪除 video_clips 目錄失敗: {str(e)}")
        
        total_duration = len(valid_clips) * 5  # 每個片段 5 秒（根據實際情況調整）
        gr.Warning(
            message=f"影片已成功匯出到: {output_path}\n"
                   f"合併了 {len(valid_clips)} 個片段\n"
                   f"總時長: 約 {total_duration} 秒\n",
            duration=15
        )
        
    except Exception as e:
        gr.Warning(message=f"影片匯出失敗: {str(e)}")
        print(f"Export error: {str(e)}")
        return None