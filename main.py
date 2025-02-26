# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
from typing import Optional
from zhipuai import ZhipuAI
from functools import partial

class ArticleGenerator:
    """作文生成器类，处理与智谱AI的交互"""
    
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        self.tools = [{
            "type": "web_search",
            "web_search": {"enable": True}
        }]
        
    async def generate_article(self, title: str, model: str) -> Optional[str]:
        """生成并优化作文"""
        initial_prompt = "你现在是一个中国的高二学生，正在完成本周的语文议论文写作作业。文章需要有实际事例，内容完整连贯符合高考作文标准，不要出现分点。多运用古代诗词或者典故文章更受人喜欢，可以使用搜索功能查找相关内容，作文写的好有助于更高的得分。"
        
        # 第一轮生成
        messages = [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": "这是本次的作文题目，祝你写出优秀的文章。"},
            {"role": "user", "content": title}
        ]
        
        try:
            loop = asyncio.get_event_loop()
            response1 = await loop.run_in_executor(
                None,
                partial(
                    self.client.chat.completions.create,
                    model=model,
                    messages=messages,
                    tools=self.tools,
                    temperature=0.75
                )
            )
            initial_output = response1.choices[0].message.content
            
            # 第二轮优化
            optimization_prompt = f"你已经写了一篇文章，内容如下：{initial_output}请根据以下反馈对文章进行优化，确保文章包含更多真实事例和古代诗词或典故，事例不得自己捏造，如果不确定可以使用搜索功能进行查找，提高文章质量。"
            
            optimization_messages = [
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": "这是本次的作文题目，祝你写出优秀的文章。"},
                {"role": "user", "content": title},
                {"role": "assistant", "content": initial_output},
                {"role": "user", "content": optimization_prompt},
                {"role": "user", "content": f"你写的文章已经非常好了，但是仍然有一点点的小问题需要优化,首先不要有自身的的事例，全部事例都要是可查的，语言要流畅不要有首先然后这种过于刻意的连词，这里是高考议论文的改卷标准，参考改卷要求对你自己写的文章进行优化调整，确保文章包含更多真实事例和古代诗词或典故，事例不得自己捏造，如果不确定可以使用搜索功能进行查找，提高文章质量。相信你可以做到的。高考改卷标准：{self.GRADING_STANDARD}"}
            ]
            
            response2 = await loop.run_in_executor(
                None,
                partial(
                    self.client.chat.completions.create,
                    model=model,
                    messages=optimization_messages,
                    tools=self.tools,
                    temperature=0.75
                )
            )
            
            return response2.choices[0].message.content
            
        except Exception as e:
            messagebox.showerror('生成失败', f"生成失败: {str(e)}")
            return None
    
    GRADING_STANDARD = """
    全国高考作文的批改标准主要包括：内容要全面、观点要明确、论证要有力、语言要流畅、结构要合理、规范要准确等方面。 
    1.内容要全面 作文的内容要贴近题目要求，全面展现自己的观点和思考。要注意对主题的理解和拓展，避免偏题或跑题，同时要注意内容的层次性和连贯性。 
    2.观点要明确 作文的观点要明确，立意要鲜明，能够清晰地表达自己的思想和看法。不同的观点应该有适当的论证和分析，以增强文章的可读性和说服力。 
    3.论证要有力 作文中的论证要有逻辑性和说服力，要能够举一反三，有充分的事实和例证来支持观点。同时，还要注意适度的理论知识和引用，但不宜过多和过分生硬。 
    4.语言要流畅 作文的语言要通顺、得体、地道。要注意遣词造句的准确性和多样性，避免重复和冗余。同时，还要注意语言的连贯性和层次性，做到篇章结构合理、段落衔接自然。 
    5.结构要合理 作文的结构要合理，包括开头、主体和结尾三个部分。开头要引人入胜，引发读者的兴趣；主体要有适当的分段和论述，层次分明；结尾要简洁有力，点明主题。 
    6.规范要准确 作文要遵循规范的写作要求，包括字数要求、格式要求等。同时，还要注意标点符号的使用、书写的规范等方面，准确无误地表达自己的思想和意图。
    """

class ArticleWriterGUI:
    """作文生成器的GUI界面类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("高中作文小工具alpha0.1")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.setup_gui()
        
        # 创建事件循环
        self.loop = asyncio.new_event_loop()
        self.thread = None
        
    def setup_gui(self):
        """设置GUI界面元素"""
        # API密钥输入框
        self.text_apikey = tk.Text(self.root, width=83, height=2)
        self.text_apikey.grid(row=0, column=0, padx=5, pady=4, sticky=tk.W, columnspan=5)
        
        # 题目输入框
        self.text_input = tk.Text(self.root, width=83, height=20)
        self.text_input.grid(row=1, column=0, padx=5, pady=4, sticky=tk.W, columnspan=5)
        
        # 生成按钮
        self.generate_button = tk.Button(self.root, text="开始生成", command=self.generate_article)
        self.generate_button.grid(row=2, column=1, padx=5, pady=4, sticky=tk.W)
        
        # 模型选择
        self.model_var = tk.StringVar(value="glm-4-flash")
        tk.Radiobutton(self.root, text="glm-4-plus", variable=self.model_var, 
                      value="glm-4-plus").grid(row=2, column=2, padx=5, pady=4, sticky=tk.W)
        tk.Radiobutton(self.root, text="glm-4-flash", variable=self.model_var,
                      value="glm-4-flash").grid(row=2, column=3, padx=5, pady=4, sticky=tk.W)
        
        # 输出框
        self.text_output = tk.Text(self.root, width=83, height=20)
        self.text_output.grid(row=3, column=0, padx=5, pady=4, sticky=tk.W, columnspan=5)
        
        # 添加状态标签
        self.status_label = tk.Label(self.root, text="就绪")
        self.status_label.grid(row=2, column=0, padx=5, pady=4, sticky=tk.W)
    
    def update_status(self, text: str):
        """更新状态标签"""
        self.status_label.config(text=text)
        self.root.update()

    async def async_generate_article(self):
        """异步生成文章"""
        api_key = self.text_apikey.get("1.0", "end").strip()
        if not api_key:
            messagebox.showwarning('警告', '请输入密钥')
            return
            
        title = self.text_input.get("1.0", "end")
        self.generate_button.config(state=tk.DISABLED)
        self.update_status("正在生成中...")
        
        try:
            generator = ArticleGenerator(api_key)
            result = await generator.generate_article(title, self.model_var.get())
            
            if result:
                self.text_output.delete("1.0", tk.END)
                self.text_output.insert(tk.INSERT, result)
        finally:
            self.generate_button.config(state=tk.NORMAL)
            self.update_status("生成完成")
    
    def start_async_generation(self):
        """启动异步生成过程"""
        if self.thread and self.thread.is_alive():
            return
            
        async def run_async():
            await self.async_generate_article()
            
        def run_in_thread():
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(run_async())
            
        self.thread = threading.Thread(target=run_in_thread, daemon=True)
        self.thread.start()
    
    def generate_article(self):
        """处理生成按钮点击事件"""
        self.start_async_generation()
    
    def run(self):
        """启动GUI程序"""
        self.root.mainloop()
        
    def __del__(self):
        """清理事件循环"""
        if self.loop and not self.loop.is_closed():
            self.loop.close()

if __name__ == "__main__":
    app = ArticleWriterGUI()
    app.run()