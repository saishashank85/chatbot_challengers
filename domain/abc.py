import yaml
with open('./responses.yml','w') as f:
    print(yaml.safe_load(f))