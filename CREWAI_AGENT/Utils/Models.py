from CREWAI_AGENT.Config.configfile import load_config
import os
from dotenv import load_dotenv
from crewai import LLM

class ModelLoader:
    def __init__(self) -> None:
        self.config = load_config()
        self._load_environment()
    
    def _load_environment(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        if OPENAI_API_KEY:
            os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        else:
            raise EnvironmentError("There is no OPENAI_API_KEY is found")
    
    def model_loading1(self):
        # llm = LLM(
        #     model = self.config['model']['provider'] + '/' + self.config['model']['model'],
        #     base_url="https://openrouter.ai/api/v1",
        #     temperature=self.config['model']['temperature'],
        #     max_tokens=self.config['model']['max_tokens'],
        #     timeout=self.config['model']['timeout']
        # )

        llm = LLM(
            model=self.config['model']['provider'] + '/' + self.config['model']['model'],
            temperature=0.7,
            max_tokens=4000
        )
        return llm
    
    def model_loading2(self):
        llm = LLM(
            model=self.config["model2"]["provider"] + "/" +self.config["model2"]["model"],
            base_url=self.config["model2"]["baseurl"]
        )
        print(self.config["model2"]["provider"] + "/" +self.config["model2"]["model"])
        return llm
  
    

# if __name__ == "__main__":
#     model = ModelLoader()
#     print(model.model_loading1())




        