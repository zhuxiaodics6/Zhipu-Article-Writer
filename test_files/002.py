from zhipuai import ZhipuAI

# 初始化ZhipuAI客户端
client = ZhipuAI(api_key='****')

# 配置工具
tools = [{
    "type": "web_search",
    "web_search": {
        "enable": True
    }
}]

# 定义提示词和初始消息内容
initial_prompt = "你现在是一个中国的高二学生，正在完成本周的语文议论文写作作业。文章需要有实际事例，内容完整连贯符合高考作文标准，不要出现分点。多运用古代诗词或者典故文章更受人喜欢，可以使用搜索功能查找相关内容，作文写的好有助于更高的得分。"
tittle = "新时代好少年“礼赞新中国，奋进新时代”主题教育读书征文活动一、主题理解本次征文以“礼赞新中国，奋进新时代”为主题，旨在引导新时代好少年通过阅读相关书籍、资料，深入了解新中国成立以来特别是改革开放以来取得的辉煌成就，感受祖国的强大与繁荣，激发爱国热情，树立远大理想，积极投身到新时代中国特色社会主义的伟大实践中去。二、写作内容作为新时代好少年，文章应体现出新时代少年的精神风貌和价值取向。写作内容：致敬为社会、国家做出贡献的家乡英雄，表达对英雄的缅怀，展现继承英雄精神，砥砺前行的新时代青年精神风貌。简要回顾新中国七十五年的重要历史节点和标志性事件，如改革开放、经济特区建设、科技创新、脱贫攻坚等，展现祖国在各个领域取得的巨大成就，提出自己对新时代发展的独到见解和建议。分析当前国家面临的机遇与挑战，如全球化背景下的国际合作与竞争、科技革命带来的变革等，体现高中生对时事政治的关注和思考。三、写作要求1.主题鲜明，紧扣时代：文章必须紧密围绕“礼赞新中国，奋进新时代”这一主题展开，突出展现新中国的发展历程、重大成就以及新时代下的新气象、新作为。2.内容真实，情感真挚：文章内容应基于真实的历史事实和个人感悟，通过具体事例、数据等展现新中国的巨大变化和新时代少年的精神风貌。情感表达要真挚自然，能够触动人心。3.结构清晰，逻辑严密：文章结构要合理，逻辑要严密，条理要清晰。4.语言生动，富有感染力：写作时要注重语言的运用，力求生动形象、富有感染力。可以适当运用比喻、拟人等修辞手法，增强文章的表现力。同时，要注意语言的准确性和规范性。字数要求1000字左右"
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