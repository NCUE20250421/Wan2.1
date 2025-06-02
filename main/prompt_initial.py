import ollama

def PromptInitial(image_path):
    system_prompt = "除非特別要求，請使用中文。\n"
    system_prompt += "你需要盡可能地描述圖片的特徵。描述要求:\n"
    system_prompt += "1. 情境 (例如：直播、餐桌場景等)\n"
    system_prompt += "2. 人物 (如果有，描述人物的角色或行為)\n"
    system_prompt += "3. 動作 (如果有，描述正在進行的動作)\n"
    system_prompt += "4. 背景 (描述背景環境或設置)\n"
    system_prompt += "請給出滿足條件的提示詞：\n"

    response = ollama.chat(
        model="qwen2.5vl:3b",
        messages=[
            {
                "role": "user",
                "content": system_prompt,
                "images": [image_path]  # Pass the image file path
            }
        ]
    )
    return response['message']['content']