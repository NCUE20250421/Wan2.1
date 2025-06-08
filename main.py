# -*- coding: utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.

import argparse
import datetime
import os
import sys

import imageio
import numpy as np
import torch

import gradio as gr
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main.prompt_initial import PromptInitial
from main.prompt_optimize import PromptOptimize

sys.path.insert(
    0, os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2]))
import wan
from wan import WanVace, WanVaceMP
from wan.configs import SIZE_CONFIGS, WAN_CONFIGS


class FixedSizeQueue:
    
    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []

    def add(self, item):
        self.queue.insert(0, item)
        if len(self.queue) > self.max_size:
            self.queue.pop()

    def get(self):
        return self.queue

    def __repr__(self):
        return str(self.queue)


class VACEInference:

    def __init__(self,
                 cfg,
                 skip_load=False,
                 gallery_share=True,
                 gallery_share_limit=5):
        self.cfg = cfg
        self.save_dir = cfg.save_dir
        self.gallery_share = gallery_share
        self.gallery_share_data = FixedSizeQueue(max_size=gallery_share_limit)
        if not skip_load:
            if not args.mp:
                self.pipe = WanVace(
                    config=WAN_CONFIGS[cfg.model_name],
                    checkpoint_dir=cfg.ckpt_dir,
                    device_id=0,
                    rank=0,
                    t5_fsdp=False,
                    dit_fsdp=False,
                    use_usp=False,
                )
            else:
                self.pipe = WanVaceMP(
                    config=WAN_CONFIGS[cfg.model_name],
                    checkpoint_dir=cfg.ckpt_dir,
                    use_usp=True,
                    ulysses_size=cfg.ulysses_size,
                    ring_size=cfg.ring_size)

    def create_ui(self, *args, **kwargs):
        gr.Markdown("""
                    <div style="text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 15px;">
                        <a href="https://ali-vilab.github.io/VACE-Page/" style="text-decoration: none; color: inherit;">帶貨直播 Demo</a>
                    </div>
                    """)
        with gr.Row(variant='panel', equal_height=True):
            with gr.Column(scale=1, min_width=0):
                self.src_video = gr.Video(
                    label="src_video",
                    sources=['upload'],
                    value=None,
                    interactive=True)
            with gr.Column(scale=1, min_width=0):
                self.src_mask = gr.Video(
                    label="src_mask",
                    sources=['upload'],
                    value=None,
                    interactive=True)
        #
        with gr.Row(variant='panel', equal_height=True):
            with gr.Column(scale=1, min_width=0):
                with gr.Row(equal_height=True):
                    self.src_ref_image_1 = gr.Image(
                        label='src_ref_image_1',
                        height=200,
                        interactive=True,
                        type='filepath',
                        image_mode='RGB',
                        sources=['upload'],
                        elem_id="src_ref_image_1",
                        format='png')
                    self.src_ref_image_2 = gr.Image(
                        label='src_ref_image_2',
                        height=200,
                        interactive=True,
                        type='filepath',
                        image_mode='RGB',
                        sources=['upload'],
                        elem_id="src_ref_image_2",
                        format='png')
                    self.src_ref_image_3 = gr.Image(
                        label='src_ref_image_3',
                        height=200,
                        interactive=True,
                        type='filepath',
                        image_mode='RGB',
                        sources=['upload'],
                        elem_id="src_ref_image_3",
                        format='png')
        with gr.Row(variant='panel', equal_height=True):
            with gr.Column(scale=1):
                with gr.Row(equal_height=True):
                    self.prompt = gr.Textbox(
                        show_label=False,
                        placeholder="positive_prompt_input",
                        elem_id='positive_prompt',
                        container=True,
                        autofocus=True,
                        elem_classes='type_row',
                        visible=True,
                        lines=2)
                    self.initial_prompt_btn = gr.Button(
                        value="初始化提示詞",
                        scale=0.15, # type: ignore
                        )
                    self.optimize_prompt_btn = gr.Button(
                        value="優化提示詞",
                        scale=0.15, # type: ignore
                        )
                self.negative_prompt = gr.Textbox(
                    show_label=False,
                    value=self.pipe.config.sample_neg_prompt, # type: ignore
                    placeholder="negative_prompt_input",
                    elem_id='negative_prompt',
                    container=True,
                    autofocus=False,
                    elem_classes='type_row',
                    visible=True,
                    interactive=True,
                    lines=1)
        #
        with gr.Row(variant='panel', equal_height=True):
            with gr.Column(scale=1, min_width=0):
                with gr.Row(equal_height=True):
                    self.shift_scale = gr.Slider(
                        label='Shift Scale',
                        minimum=0.0,
                        maximum=100.0,
                        step=1.0,
                        value=16.0,
                        interactive=True,
                        info="控制移動幅度的參數，值越大移動越明顯 (建議值: 16.0)")
                    self.sample_steps = gr.Slider(
                        label='Sampling Steps',
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=20,
                        interactive=True,
                        info="生成時的採樣步數，步數越多品質越好但耗時更長 (建議值: 20)")
                    self.context_scale = gr.Slider(
                        label='Context Scale',
                        minimum=0.0,
                        maximum=2.0,
                        step=0.1,
                        value=1.0,
                        interactive=True,
                        info="控制上下文關聯性的參數，值越大關聯性越強 (建議值: 1.0)")
                    self.guide_scale = gr.Slider(
                        label='Guidance Scale',
                        minimum=1,
                        maximum=10,
                        step=0.5,
                        value=5.0,
                        interactive=True,
                        info="提示詞引導強度，值越大越接近提示詞描述但可能影響品質 (建議值: 5.0)")
                    self.infer_seed = gr.Slider(
                        minimum=-1,
                        maximum=10000000,
                        value=2025,
                        label="Seed",
                        info="隨機種子數，相同的種子會產生相同的結果，-1為隨機")

        with gr.Accordion(label="Advanced Settings", open=False):
            with gr.Row(equal_height=True):
                self.output_height = gr.Textbox(
                    label='Output Height',
                    value=480, # type: ignore
                    interactive=True,
                    info="輸出影片的高度 (像素)")
                self.output_width = gr.Textbox(
                    label='Output Width',
                    value=832, # type: ignore
                    interactive=True,
                    info="輸出影片的寬度 (像素)")
                self.frame_rate = gr.Textbox(
                    label='Frame Rate',
                    value=24, # type: ignore
                    interactive=True,
                    info="影片的每秒幀數 (FPS)")
                self.num_frames = gr.Textbox(
                    label='Number of Frames',
                    value=240, # type: ignore
                    interactive=True,
                    info="生成影片的總幀數")
        #
        with gr.Row(equal_height=True):
            with gr.Column(scale=5):
                self.generate_button = gr.Button(
                    value='Run',
                    elem_classes='type_row',
                    elem_id='generate_button',
                    visible=True)
            
        #
        self.output_gallery = gr.Gallery(
            label="output_gallery",
            value=[],
            interactive=False,
            allow_preview=True,
            preview=True)

        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                self.approve_button = gr.Button(
                    value='✅ 確認保存', 
                    elem_classes='type_row',
                    elem_id='approve_button',
                )
            with gr.Column(scale=1):
                self.refresh_button = gr.Button(
                    value='🔄 重新生成', 
                    elem_classes='type_row',
                    elem_id='refresh_button',
                )

    def generate(self, output_gallery, src_video, src_mask, src_ref_image_1,
                 src_ref_image_2, src_ref_image_3, prompt, negative_prompt,
                 shift_scale, sample_steps, context_scale, guide_scale,
                 infer_seed, output_height, output_width, frame_rate,
                 num_frames):
        output_height, output_width, frame_rate, num_frames = int(
            output_height), int(output_width), int(frame_rate), int(num_frames)
        src_ref_images = [
            x for x in [src_ref_image_1, src_ref_image_2, src_ref_image_3]
            if x is not None
        ]
        src_video, src_mask, src_ref_images = self.pipe.prepare_source(
            [src_video], [src_mask], [src_ref_images],
            num_frames=num_frames,
            image_size=SIZE_CONFIGS[f"{output_width}*{output_height}"],
            device=self.pipe.device)
        video = self.pipe.generate(
            prompt,
            src_video,
            src_mask,
            src_ref_images,
            size=(output_width, output_height),
            context_scale=context_scale,
            shift=shift_scale,
            sampling_steps=sample_steps,
            guide_scale=guide_scale,
            n_prompt=negative_prompt,
            seed=infer_seed,
            offload_model=True)

        name = '{0:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())
        video_path = os.path.join(self.save_dir, f'gallery_{name}.mp4')
        video_frames = (
            torch.clamp(video / 2 + 0.5, min=0.0, max=1.0).permute(1, 2, 3, 0) * # type: ignore
            255).cpu().numpy().astype(np.uint8) 

        try:
            writer = imageio.get_writer(
                video_path,
                fps=frame_rate,
                codec='libx264',
                quality=8,
                macro_block_size=1)
            for frame in video_frames:
                writer.append_data(frame)
            writer.close()
            print(video_path)
        except Exception as e:
            raise gr.Error(f"Video save error: {e}")

        if self.gallery_share:
            self.gallery_share_data.add(video_path)
            return self.gallery_share_data.get()
        else:
            return [video_path]

    def initial_prompt_callback(self, prompt, src_ref_image_1, src_ref_image_2, src_ref_image_3):
        image_inputs = {
            'src_ref_image_1': src_ref_image_1,
            'src_ref_image_2': src_ref_image_2,
            'src_ref_image_3': src_ref_image_3
        }
        # Filter out None images
        available_images = {label: path for label, path in image_inputs.items() if path is not None}
        if not available_images:
            return prompt if prompt else "無圖片輸入，請上傳至少一張參考圖片。"
        
        # Generate prompts for each available image
        prompts = []
        for label, image_path in available_images.items():
            try:
                description = PromptInitial(image_path)
                prompts.append(f"{label}: {description}")
            except Exception as e:
                prompts.append(f"{label}: 無法分析圖片，錯誤: {str(e)}")
        
        # Combine prompts or use existing prompt if no new descriptions
        result_prompt = "\n".join(prompts) if prompts else prompt
        return result_prompt if result_prompt else "無法生成提示詞，請檢查圖片輸入。"
        
    def optimize_prompt_callback(self, prompt):
        if not prompt:
            return "無提示詞輸入，請上傳提示詞。"
            
        try:
            # Send prompt to optimize_prompt function
            optimized_prompt = PromptOptimize(prompt)
            return optimized_prompt
        except Exception as e:
            return f"無法生成提示詞: {str(e)}"    

    def set_callbacks(self, **kwargs):
        self.gen_inputs = [
            self.output_gallery, self.src_video, self.src_mask,
            self.src_ref_image_1, self.src_ref_image_2, self.src_ref_image_3,
            self.prompt, self.negative_prompt, self.shift_scale,
            self.sample_steps, self.context_scale, self.guide_scale,
            self.infer_seed, self.output_height, self.output_width,
            self.frame_rate, self.num_frames
        ]
        self.gen_outputs = [self.output_gallery]
        
        # 生成按鈕回調
        self.generate_button.click(
            self.generate,
            inputs=self.gen_inputs,
            outputs=self.gen_outputs,
            queue=True)
        
        # 刷新按鈕回調
        self.refresh_button.click(
            lambda x: self.gallery_share_data.get()
            if self.gallery_share else x,
            inputs=[self.output_gallery],
            outputs=[self.output_gallery])
        
        # 初始化提示詞按鈕回調    
        self.initial_prompt_btn.click(
            fn=self.initial_prompt_callback,  # 添加回調函數
            inputs=[
                self.prompt,
                self.src_ref_image_1,
                self.src_ref_image_2,
                self.src_ref_image_3
            ],
            outputs=[self.prompt],
            queue=True)
        
        # 優化提示詞按鈕回調
        self.optimize_prompt_btn.click(
            fn=self.optimize_prompt_callback,
            inputs=[self.prompt],
            outputs=[self.prompt],
            queue=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Argparser for VACE-WAN Demo:\n')
    parser.add_argument(
        '--server_port', dest='server_port', help='', type=int, default=7860)
    parser.add_argument(
        '--server_name', dest='server_name', help='', default='127.0.0.1')
    parser.add_argument('--root_path', dest='root_path', help='', default=None)
    parser.add_argument('--save_dir', dest='save_dir', help='', default='cache')
    parser.add_argument(
        "--mp",
        action="store_true",
        help="Use Multi-GPUs",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="vace-14B",
        choices=list(WAN_CONFIGS.keys()),
        help="The model name to run.")
    parser.add_argument(
        "--ulysses_size",
        type=int,
        default=1,
        help="The size of the ulysses parallelism in DiT.")
    parser.add_argument(
        "--ring_size",
        type=int,
        default=1,
        help="The size of the ring attention parallelism in DiT.")
    parser.add_argument(
        "--ckpt_dir",
        type=str,
        # default='models/VACE-Wan2.1-1.3B-Preview',
        # default='models/Wan2.1-VACE-14B/',
        default='Wan2.1-VACE-1.3B',
        help="The path to the checkpoint directory.",
    )
    parser.add_argument(
        "--offload_to_cpu",
        action="store_true",
        help="Offloading unnecessary computations to CPU.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir, exist_ok=True)

    with gr.Blocks() as demo:
        infer_gr = VACEInference(
            args, skip_load=False, gallery_share=True, gallery_share_limit=5)
        infer_gr.create_ui()
        infer_gr.set_callbacks()
        allowed_paths = [args.save_dir]
        demo.queue(status_update_rate=1).launch(
            server_name=args.server_name,
            server_port=args.server_port,
            root_path=args.root_path,
            allowed_paths=allowed_paths,
            show_error=True,
            debug=True,
            share=True)
        

