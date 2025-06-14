# 匯出完整影片功能
from moviepy.editor import concatenate_videoclips, VideoFileClip
from main.approve_button import saved_clips

def export_btn(output_path="final_video.mp4"):
    """
    將所有已儲存片段依序串接並匯出為完整影片
    :param output_path: 匯出影片檔案名稱
    :return: 匯出影片檔案路徑
    """
    if not saved_clips:
        raise Exception("沒有可匯出的片段，請先儲存片段。")
    try:
        clips = [VideoFileClip(path) for path in saved_clips]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path)
        # 關閉所有 clip 以釋放資源
        for c in clips:
            c.close()
        final_clip.close()
        return output_path
    except Exception as e:
        raise Exception(f"影片匯出失敗: {e}")