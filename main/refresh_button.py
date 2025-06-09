import gradio as gr

def refresh_btn(output_gallery):
    """
    清空現有gallery並顯示提示信息
    """
    # 清空gallery
    empty_gallery = []
    
    # 顯示提示信息
    gr.Warning(message="更新提示詞效果更好")
    
    return [] #, gr.Warning(message="更新提示詞效果更好")