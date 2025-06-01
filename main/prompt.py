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