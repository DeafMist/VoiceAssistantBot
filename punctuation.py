import torch
import yaml


torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                               'models/latest_silero_models.yml',
                               progress=False)

with open('models/latest_silero_models.yml', 'r', errors='ignore') as yaml_file:
    models = yaml.load(yaml_file, Loader=yaml.SafeLoader)
model_conf = models.get('te_models').get('latest')

model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                  model='silero_te')


def get_punctuation(text: str):
    return apply_te(text, lan='ru')
