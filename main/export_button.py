import os
import shutil
import gradio as gr
from moviepy.editor import concatenate_videoclips, VideoFileClip
from main.approve_button import saved_clips

def export_btn():
    """
    將所有已儲存片段依序串接並匯出為完整影片，完成後清除暫存的影片檔案
    :return: None
    """
    if not saved_clips:
        gr.Warning(message="沒有可匯出的片段，請先儲存片段。")
        return None

    try:
        # 設定輸出路徑
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, "final_video.mp4")
        
        # 驗證並載入影片片段
        valid_clips = []
        for path in saved_clips:
            try:
                if os.path.exists(path):
                    clip = VideoFileClip(path)
                    valid_clips.append(clip)
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
        
        # 清除暫存的影片檔案
        for path in saved_clips:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"已刪除暫存檔案: {path}")
            except Exception as e:
                print(f"刪除檔案失敗 {path}: {str(e)}")
                continue
        
        # 清除 cache 目錄
        cache_dir = os.path.join(os.getcwd(), "cache")
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print("已清除 cache 目錄")
                # 重新創建空的 cache 目錄
                os.makedirs(cache_dir)
            except Exception as e:
                print(f"清除 cache 目錄失敗: {str(e)}")
        
        # 清空 saved_clips 列表
        saved_clips.clear()
        
        total_duration = len(valid_clips) * 5  # 每個片段 5 秒
        gr.Warning(
            message=f"影片已成功匯出到: {output_path}\n"
                   f"合併了 {len(valid_clips)} 個片段\n"
                   f"總時長: {total_duration} 秒\n",
            duration=15
        )
        
    except Exception as e:
        gr.Warning(message=f"影片匯出失敗: {str(e)}")
        print(f"Export error: {str(e)}")
        return None