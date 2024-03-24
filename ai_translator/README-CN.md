# Gradio App of the OpenAI-Translator V2.0


### **环境：**

Python=3.11

Gradio=4.22.0

运行应用要用：gradio_app.py

### **作业完成情况：**

用Gradio做了**可视化页面**：

- 可以输入OPENAI_API_KEY，不输入默认使用环境变量；
- 可以选择从英语翻译到**多种目标语言**
- 可以选择PDF文档

### **遇到问题：**

gpt-3.5-turbo 表格翻译不稳定，导致汇报错：

```
/openai-translator/ai_translator/translator/writer.py

header = '| ' + ' | '.join(str(column) for column in table.columns) + ' |' + '\n'
                                                        
AttributeError: 'str' object has no attribute 'columns'
```

