import gradio as gr

def refresh_with_message(output_gallery, *gen_inputs):
    """
    顯示提示消息並重新生成
    
    Args:
        output_gallery: 當前的輸出畫廊 
        gen_inputs: 生成所需的輸入參數
    """
    # 顯示提示消息
    gr.Info("若是影片生成結果不佳，重新修改提示詞，生成效果更好")
    return gen_inputs[0](*gen_inputs[1:])