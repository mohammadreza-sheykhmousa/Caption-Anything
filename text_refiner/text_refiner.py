from langchain.llms.openai import OpenAI
import torch
from PIL import Image, ImageDraw, ImageOps
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
import pdb

class TextRefiner:
    def __init__(self, device):
        print(f"Initializing TextRefiner to {device}")
        # self.device = device
        # self.torch_dtype = torch.float16 if 'cuda' in device else torch.float32
        self.llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.prompts = {'length': "convert the sentence to a length of around {length} words, do not change its meaning",
                        "sentiment": "convert the sentence to {sentiment} sentiment, do not change its meaning"
                        }
        self.wiki_prompts = "I want you to act as a Wikipedia page. I will give you a sentence and you will parse the single main object in the sentence and provide a summary of that object in the format of a Wikipedia page. Your summary should be informative and factual, covering the most important aspects of the object. Start your summary with an introductory paragraph that gives an overview of the object. The overall length of the response should be around 100 words. You should not describe the parsing process and only provide the final summary. The sentence is \"{query}\"."

    def parse(self, response):
        out = response.strip()
        return out
    
    def parse2(self, response):
        out = response.strip()
        return out
    
    def prepare_input(self, query, prompts):
        input = '. '.join(prompts) + 'The input sentence is: ' + query
        return input
    
    def inference(self, query: str, controls: dict):
        """
        query: the caption of the region of interest, generated by captioner
        controls: a dict of control singals, e.g., {"length": 5, "sentiment": "positive"}
        """
        prompts = []
        for control, value in controls.items():
            prompts.append(self.prompts[control].format(**{control: value}))
        input = self.prepare_input(query, prompts)
        response = self.llm(input)
        response = self.parse(response)
        
        tmp_configs = {"query": response}
        prompt_wiki = self.wiki_prompts.format(**tmp_configs)  
        response_wiki = self.llm(prompt_wiki)
        response_wiki = self.parse2(response_wiki) 
        out = {
            'raw_caption': query,
            'caption': response,
            'wiki': response_wiki
        }    
        print(out)
        return out
    
if __name__ == "__main__":
    model = TextRefiner(device='cpu')
    controls = {
        "length": 10,
        "sentiment": "positive"
    }
    model.inference(query='a dog is sitting on a bench', controls=controls)
    