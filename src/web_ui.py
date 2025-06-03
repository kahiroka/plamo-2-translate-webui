import gradio as gr
from translator import PLaMoTranslator
import time


class TranslationWebUI:
    def __init__(self):
        self.translator = PLaMoTranslator()
        self.model_loaded = False
        
    def load_model_handler(self):
        if self.model_loaded:
            return "Model already loaded!"
        
        start_time = time.time()
        success = self.translator.load_model()
        
        if success:
            self.model_loaded = True
            elapsed_time = time.time() - start_time
            return f"Model loaded successfully in {elapsed_time:.2f} seconds!"
        else:
            return "Failed to load model. Check logs for details."
    
    def translate_handler(self, text, source_lang, target_lang):
        if not self.model_loaded:
            return "Please load the model first by clicking 'Load Model'", ""
        
        if len(text.strip()) == 0:
            return "Please enter text to translate", ""
        
        token_count = len(text.split())
        if token_count > 500:
            return f"Text too long ({token_count} words). Please limit to ~500 words for best results.", ""
        
        start_time = time.time()
        translation, error = self.translator.translate(text, source_lang, target_lang)
        elapsed_time = time.time() - start_time
        
        if error:
            return error, ""
        
        status = f"Translation completed in {elapsed_time:.2f} seconds"
        return status, translation
    
    def swap_languages(self, source_lang, target_lang, text, translation):
        return target_lang, source_lang, translation, text
    
    def create_interface(self):
        with gr.Blocks(title="PLaMo-2 Translation") as interface:
            gr.Markdown("# PLaMo-2 Translation Web UI")
            gr.Markdown("English-Japanese translation powered by PLaMo-2 (9.53B parameters)")
            
            with gr.Row():
                with gr.Column(scale=1):
                    load_btn = gr.Button("Load Model", variant="primary")
                    model_status = gr.Textbox(
                        label="Model Status",
                        value="Model not loaded",
                        interactive=False
                    )
            
            gr.Markdown("---")
            
            with gr.Row():
                with gr.Column(scale=1):
                    source_lang = gr.Dropdown(
                        choices=["English", "Japanese"],
                        value="English",
                        label="Source Language"
                    )
                    source_text = gr.Textbox(
                        label="Input Text",
                        placeholder="Enter text to translate...",
                        lines=10
                    )
                
                with gr.Column(scale=0, min_width=50):
                    gr.Markdown("")
                    swap_btn = gr.Button("⇄", scale=0)
                
                with gr.Column(scale=1):
                    target_lang = gr.Dropdown(
                        choices=["English", "Japanese"],
                        value="Japanese",
                        label="Target Language"
                    )
                    translation_output = gr.Textbox(
                        label="Translation",
                        lines=10,
                        interactive=False
                    )
            
            with gr.Row():
                translate_btn = gr.Button("Translate", variant="primary", scale=1)
                clear_btn = gr.Button("Clear", scale=1)
            
            status_output = gr.Textbox(label="Status", interactive=False)
            
            with gr.Accordion("Tips", open=False):
                gr.Markdown("""
                ### Usage Tips:
                - First click 'Load Model' to initialize the PLaMo-2 model
                - Model loading requires a GPU with sufficient memory
                - Keep translations under ~500 words for best performance
                - The model is optimized for English-Japanese translation
                """)
            
            load_btn.click(
                fn=self.load_model_handler,
                outputs=model_status
            )
            
            translate_btn.click(
                fn=self.translate_handler,
                inputs=[source_text, source_lang, target_lang],
                outputs=[status_output, translation_output]
            )
            
            swap_btn.click(
                fn=self.swap_languages,
                inputs=[source_lang, target_lang, source_text, translation_output],
                outputs=[source_lang, target_lang, source_text, translation_output]
            )
            
            clear_btn.click(
                fn=lambda: ("", "", ""),
                outputs=[source_text, translation_output, status_output]
            )
        
        return interface
    
    def launch(self, share=False, server_port=7860):
        interface = self.create_interface()
        interface.launch(share=share, server_port=server_port)