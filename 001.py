from zhipuai import ZhipuAI
client = ZhipuAI(api_key='****')
response = client.chat.completions.create(
    model='glm-4',
    messages=[
        {"role": "system","content":"你现在是一个中国的高二学生，现在正在参加新时代好少年“礼赞新中国，奋进新时代”主题教育读书征文活动，根据一下要求完成文章"},
        {"role": "user","content":"新时代好少年“礼赞新中国，奋进新时代”主题教育读书征文活动一、主题理解本次征文以“礼赞新中国，奋进新时代”为主题，旨在引导新时代好少年通过阅读相关书籍、资料，深入了解新中国成立以来特别是改革开放以来取得的辉煌成就，感受祖国的强大与繁荣，激发爱国热情，树立远大理想，积极投身到新时代中国特色社会主义的伟大实践中去。二、写作内容作为新时代好少年，文章应体现出新时代少年的精神风貌和价值取向。写作内容：致敬为社会、国家做出贡献的家乡英雄，表达对英雄的缅怀，展现继承英雄精神，砥砺前行的新时代青年精神风貌。简要回顾新中国七十五年的重要历史节点和标志性事件，如改革开放、经济特区建设、科技创新、脱贫攻坚等，展现祖国在各个领域取得的巨大成就，提出自己对新时代发展的独到见解和建议。分析当前国家面临的机遇与挑战，如全球化背景下的国际合作与竞争、科技革命带来的变革等，体现高中生对时事政治的关注和思考。三、写作要求1.主题鲜明，紧扣时代：文章必须紧密围绕“礼赞新中国，奋进新时代”这一主题展开，突出展现新中国的发展历程、重大成就以及新时代下的新气象、新作为。2.内容真实，情感真挚：文章内容应基于真实的历史事实和个人感悟，通过具体事例、数据等展现新中国的巨大变化和新时代少年的精神风貌。情感表达要真挚自然，能够触动人心。3.结构清晰，逻辑严密：文章结构要合理，逻辑要严密，条理要清晰。4.语言生动，富有感染力：写作时要注重语言的运用，力求生动形象、富有感染力。可以适当运用比喻、拟人等修辞手法，增强文章的表现力。同时，要注意语言的准确性和规范性。字数要求1000字左右"},
        {"role": "user","content":"文章需要有实际事例，内容完整连贯，不要出现分点"}]
)
print(response.choices[0].message.content)