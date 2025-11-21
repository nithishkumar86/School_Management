import yaml

def load_config(path: str ="E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Config\\components.yaml")->dict:
    with open(path,'r') as file:
        loader = yaml.safe_load(file)
    return loader


