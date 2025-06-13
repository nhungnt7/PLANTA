from datasets import load_dataset

if __name__ == '__main__':
    wtq = load_dataset('Stanford/wikitablequestions', trust_remote_code=True)
    wtq['test'].to_json('data/datasets/wikitq/test.json', force_ascii=False)

    tabfact = load_dataset('ibm/tab_fact', trust_remote_code=True)
    tabfact['test'].to_json('data/datasets/tab_fact/test.json', force_ascii=False)