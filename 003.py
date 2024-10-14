import tkinter as tk
from tkinter import filedialog, messagebox
from zhipuai import ZhipuAI
def zhipu(tittle,api_key):
    # 初始化ZhipuAI客户端
    client = ZhipuAI(api_key=api_key)

    # 配置工具
    tools = [{
        "type": "web_search",
        "web_search": {
            "enable": True
        }
    }]

    # 定义提示词和初始消息内容
    initial_prompt = "你现在是一个中国的高二学生，正在完成本周的语文议论文写作作业。文章需要有实际事例，内容完整连贯符合高考作文标准，不要出现分点。多运用古代诗词或者典故文章更受人喜欢，可以使用搜索功能查找相关内容，作文写的好有助于更高的得分。"
    messages = [
        {"role": "system", "content": initial_prompt},
        {"role": "user", "content": "这是本次的作文题目，祝你写出优秀的文章。"},
        {"role": "user", "content": tittle}
    ]

    # 第一次生成作文内容
    response1 = client.chat.completions.create(
        model='glm-4-plus',
        messages=messages,
        tools=tools,
        temperature=0.75
    )

    # 获取第一次输出的内容
    initial_output = response1.choices[0].message.content

    # 为优化作文准备新的提示词和消息
    optimization_prompt = f"你已经写了一篇文章，内容如下：{initial_output}请根据以下反馈对文章进行优化，确保文章包含更多真实事例和古代诗词或典故，事例不得自己捏造，如果不确定可以使用搜索功能进行查找，提高文章质量。"

    optimization_messages = [
        {"role": "system", "content": optimization_prompt},
        {"role": "user", "content": "你写的文章已经非常好了，但是仍然有一点点的小问题需要优化，相信你可以做到的"}
    ]
    optimization_messages = [
        {"role": "system", "content": initial_prompt},
        {"role": "user", "content": "这是本次的作文题目，祝你写出优秀的文章。"},
        {"role": "user", "content": tittle},
        {"role": "assistant", "content": initial_output},
        {"role": "user", "content": optimization_prompt}
    ]


    # 第二次生成优化后的作文内容
    response2 = client.chat.completions.create(
        model='glm-4-plus',
        messages=optimization_messages,
        tools=tools,
        temperature=0.75
    )

    # 打印优化后的作文内容
    print(response1.choices[0].message.content)
    print('---------')
    print(response2.choices[0].message.content)
    return(response2.choices[0].message.content)

def button_click():
    auth_key = text_paikey.get("1.0","end").replace('\n','').replace(' ','')
    if not auth_key:
        messagebox.showwarning('警告','请输入密钥')
        return 0
    text_in = text_input.get("1.0","end")
    result = zhipu(text_in)
    text_out = result
    text_output.delete(0.0,tk.END)
    text_output.insert(tk.INSERT,text_out)
    text_output.update

root = tk.Tk()
root.title("高中作文小工具alpha0.1")
root.geometry("600x600")
text_input = tk.Text(root,width=500,height=20)
text_paikey = tk.Text(root,width=500,height=2)
button = tk.Button(root, text="开始生成", command=button_click)
text_output = tk.Text(root,width=500,height=20)

text_paikey.pack()
text_input.pack()
button.pack()
text_output.pack()

root.mainloop()