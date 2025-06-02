import ollama
import sys
import random
import datetime

def return_random_prompt():
    system_prompt = "你需要盡可能給出不同型態的憂鬱問題和對應的答案。要求:\n"

    # Generate random topics
    topic_list = ["感情", "健康", "工作", "人際關係", "學業", "家庭", "生活", "金錢"]
    system_prompt += "1. 憂鬱問題主題多樣化，涵蓋各個領域，例如：" + "、".join(random.sample(topic_list, 1)) + "等。\n"

    # Other requirements
    system_prompt += "2. 除非特別要求，請使用中文，指令可以是命令句、疑問句、或其他合適的類型。\n"
    system_prompt += "3. 為指令生成一個適當且涉及真實情況的<input>，不應該只包含簡單的佔位符。<input>應提供實質性的內容，具有挑戰性。字數不超過" + str(random.randint(80, 120)) + "字。\n"
    system_prompt += "4. <output>應該是對指令的適當且真實的回應，不能只回覆答應或拒絕請求。如果需要額外資訊才能回覆時，請努力預測用戶意圖並嘗試回覆。<output>的內容應少於" + str(random.randint(128, 512)) + "字。\n\n"

    system_prompt += "請給出滿足條件的20條JSON格式資料：\n"
    return system_prompt

if __name__ == "__main__":
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/home/yuchi/Artificial_Intelligence_Chatbot/Alpaca/output_{current_time}.txt"
    MAX_EPOCHS = 1  # Number of iterations to generate data

    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(MAX_EPOCHS):
            response = ollama.chat(
                model="qwen2.5:3b",  
                messages=[{"role": "user", "content": return_random_prompt()}]
            )
            f.write(response['message']['content'] + '\n')
    f.close()
    print(f"生成的內容已儲存至 {output_file}")

class PromptOptimizer:
    def __init__(self):
        self.base_prompts = {
            "quality": "masterpiece, best quality, high quality, highly detailed",
            "style": "realistic, photorealistic",
            "lighting": "professional lighting, natural lighting"
        }
    
    def optimize_prompt(self, original_prompt):
        """優化使用者輸入的提示詞"""
        if not original_prompt:
            return self.base_prompts["quality"]
            
        # 移除多餘空格並整理格式
        prompt = original_prompt.strip()
        
        # 檢查是否已包含品質相關詞彙
        has_quality = any(q in prompt.lower() for q in ["masterpiece", "best quality", "high quality"])
        
        # 如果沒有品質相關詞彙，添加基礎品質描述
        if not has_quality:
            prompt = f"{self.base_prompts['quality']}, {prompt}"
            
        return prompt