import ollama

def PromptInitial(image_path):
    system_prompt = "除非使用者特別要求，請使用中文回答。\n"
    system_prompt += "你的任務是根據輸入圖片，詳細描述其內容。請盡可能具體、清晰地描述圖片的各個特徵，包含以下幾個方面：\n"
    system_prompt += "1. 情境：整體場景是什麼？例如：餐廳用餐、戶外郊遊、直播中等。\n"
    system_prompt += "2. 人物：若圖片中有人物，請描述他們的外觀、身份、行為或互動關係。\n"
    system_prompt += "3. 動作：人物或其他主體正在做什麼？描述具體的行為與動態。\n"
    system_prompt += "4. 背景：背景中有什麼物件、建築或自然環境？有無特定風格或氛圍？\n"
    system_prompt += "5. 氛圍與情感：整體畫面傳遞出什麼樣的情緒或氛圍？例如：溫馨、緊張、歡樂、孤獨等。\n"
    system_prompt += "6. 其他特徵：任何其他值得注意的細節或特徵，例如顏色、光影、構圖等。\n"
    system_prompt += "請根據上述要點，生成一段完整、具體且符合事實的文字描述。\n"

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