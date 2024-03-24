import sys
import os
import gradio as gr
from utils import ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
config_loader = ConfigLoader("config.yaml")
config = config_loader.load_config()

#Get the language selection dropdown box
#获取语言选择下拉框
def get_language():
    return gr.Dropdown(choices=["简体中文",
                                "繁体中文",
                                 "法语",
                                 "德语",
                                 "西班牙语"
                                 ], value="中文", label="Select target language")



#Translate the PDF file
#翻译PDF文件
def translate_pdf(pdf_upload_path,target_language,openai_api_key):
    if pdf_upload_path==None:
        pdf_upload_path = config['common']['book']   

    if target_language==None:
        target_language = "简体中文"
    
    LOG.debug(pdf_upload_path+"|"+target_language)
    model_name = config['OpenAIModel']['model']
    LOG.debug(f"___model_name___={model_name}")
    api_key = openai_api_key if openai_api_key else os.environ.get('OPENAI_API_KEY')
    #LOG.debug(f"___api_key___={api_key}")
    model = OpenAIModel(model=model_name, api_key=api_key)


    pdf_file_path = pdf_upload_path if pdf_upload_path else config['common']['book']
    file_format = config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    output_str = translator.translate_pdf(pdf_file_path, file_format, target_language)
    output_str = f"The translated PDF file to markdown document is save to :{output_str}"
    LOG.debug(f"output_str={output_str}")
    return output_str

#Build the Gradio block  
#构建Gradio块  
with gr.Blocks() as app:
    gr.Markdown("""
    # Gradio App of the OpenAI-Translator V2.0
    """)
    with gr.Row():
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    openai_api_key = gr.Textbox(label="Input OpenAI API Key")
                with gr.Column():
                    lang_select = get_language()
            with gr.Row():
                with gr.Column():
                    pdf_upload = gr.File(label="Upload PDF file",height=80)
            with gr.Row():    
                with gr.Column():
                    btn_trans = gr.Button("Translate")
            with gr.Row():                
                with gr.Column():
                    html_display = gr.Textbox(label="Translate PDF result:")

    btn_trans.click(fn=translate_pdf,inputs=[pdf_upload,lang_select,openai_api_key],outputs=[html_display])

#run the app
#运行应用程序 
if __name__ == "__main__":   
    app.launch()