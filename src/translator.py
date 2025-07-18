import vllm
from typing import Optional, Dict, Tuple
import torch
from transformers import AutoTokenizer


class PLaMoTranslator:
    def __init__(self, model_name: str = "pfnet/plamo-2-translate"):
        self.model_name = model_name
        self.llm = None
        self.is_loaded = False
        self.tokenizer = None
        
    def load_model(self) -> bool:
        try:
            if torch.cuda.is_available():
                print(f"Loading {self.model_name} on GPU...")
            else:
                print("Warning: No GPU detected. Model loading may fail or be very slow.")
            
            self.llm = vllm.LLM(
                model=self.model_name,
                trust_remote_code=True,
                max_model_len=2000,
                max_num_batched_tokens=2000,
                max_num_seqs=16
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            self.is_loaded = True
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def _create_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        prompt = f'''<|plamo:op|>dataset
translation
<|plamo:op|>input lang={source_lang}
{text}
<|plamo:op|>output lang={target_lang}
'''
        return prompt
    
    def translate(self, text: str, source_lang: str = "English", target_lang: str = "Japanese") -> Tuple[str, Optional[str], Dict[str, int]]:
        if not self.is_loaded:
            return "", "Model not loaded. Please load the model first.", {"input_tokens": 0, "output_tokens": 0}
        
        if not text.strip():
            return "", "Please provide text to translate.", {"input_tokens": 0, "output_tokens": 0}
        
        try:
            prompt = self._create_prompt(text, source_lang, target_lang)
            
            input_tokens = len(self.tokenizer.encode(prompt))
            
            sampling_params = vllm.SamplingParams(
                temperature=0,
                max_tokens=1024,
                stop=["<|plamo:op|>"]
            )
            
            responses = self.llm.generate([prompt], sampling_params=sampling_params)
            
            if responses and len(responses) > 0:
                translation = responses[0].outputs[0].text.strip()
                output_tokens = len(self.tokenizer.encode(translation))
                
                token_counts = {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                }
                
                return translation, None, token_counts
            else:
                return "", "No translation generated.", {"input_tokens": input_tokens, "output_tokens": 0}
                
        except Exception as e:
            return "", f"Translation error: {str(e)}", {"input_tokens": 0, "output_tokens": 0}
    
    def get_model_info(self) -> Dict[str, any]:
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "max_tokens": 2000,
            "supported_languages": ["English", "Japanese"]
        }
