import csv
import os
from openai import OpenAI
import re
import time
import sys
import traceback


wikitq_prompt = """  
You are an AI evaluator tasked with assessing the accuracy of predictions made by another AI model. Given a prediction and a ground truth answer, determine whether they refer to the same entity, number, or concept, regardless of wording, synonyms, or phrasing differences.  

### Evaluation Criteria:  
1. Correct if: The prediction and the answer convey the same meaning, even if they use different words, synonyms, formats, or phrasing. Minor differences in wording or grammar do not affect correctness.  
2. Incorrect if: The prediction refers to a different entity, number, or concept than the Answer

### Output Format:  
Respond with one of the following labels and an explanation:  
- "Correct": (Explanation of how the prediction and answer match)  
- "Incorrect": (Explanation of the mismatch)  

### Examples:  
#### Example 1  
- Prediction: "three hundred and fifty"  
- Answer: "350"  
- Evaluation: <evalation>Correct</evalation>(Both refer to the same number.)  

#### Example 2  
- Prediction: "New York City"  
- Answer: "NYC"  
- Evaluation: <evaluation>Correct</evalation> (NYC is a common abbreviation for New York City.)  

#### Example 3  
- Prediction: "5"  
- Answer: "50"  
- Evaluation: <evalation>Incorrect</evaluation> (The numbers are different)

Your tasks:
Prediction: {prediction}
Answer: {answer}
Evaluation:
"""

tabfact_prompt = """Claim: {question} 
Label: {answer}
AI Prediction: {prediction}

Based on the provided Claim, Label, and AI Prediction, determine if the AI's Prediction aligns with the Label. Explain your reasoning.

Your final answer must conclude with either `<evaluation>Correct</evaluation>` if the AI's prediction aligns with the label, or `<evaluation>Incorrect</evaluation>` if it does not."""

class LLM:
    def __init__(self, model_name, key):
        self.model_name = model_name
        self.client = OpenAI(api_key=key)

    def get_model_options(
        self,
        temperature=0,
        per_example_max_decode_steps=150,
        per_example_top_p=1,
        n_sample=1,
    ):
        return dict(
            temperature=temperature,
            n=n_sample,
            top_p=per_example_top_p,
            max_tokens=per_example_max_decode_steps,
        )

    def generate(self, question, pred, label, eval_prompt):
        prompt = eval_prompt.format(question=question, prediction=pred, answer=label)
        messages = [
            # {"role": "system", "content": "You are a logical reasoning assistant."},
            {"role": "user", "content": prompt},
        ]

        response = None
        retry_num = 0
        retry_limit = 2
        while response is None:
            try:
                response = self.client.chat.completions.create(
                                messages=messages,
                                model=self.model,
                                **self.get_model_options()
                            )

            except Exception as e:
                print(str(e), flush=True)
                if retry_num > retry_limit:
                    break
                else:
                    time.sleep(10)
                retry_num += 1
        
        # print(response)
        if response:
            response_text = response["choices"][0]["message"]["content"].strip()
            match = re.search(r"\<evaluation\>(.*?)\</evaluation\>", response_text, re.IGNORECASE)
            return match.group(1).lower() if match else "error" 
        else:
            return "error"

def exact_match_check(pred, label):
    def normalize(text):
        text = re.sub(r"\s+", " ", text)  # Normalize all spaces
        text = re.sub(r"[\W_]+", "", text)  # Remove punctuation
        return text.strip().lower()

    return normalize(pred) == normalize(label)

def evaluate_sample_tabfact(sample, llm, eval_prompt=tabfact_prompt):
    try:
        label = "True" if sample['answer'] else "False"
        pred = sample['prediction']
        question = sample['question']
        response = llm.generate(question, pred, label, eval_prompt)
        result = 1 if response == "correct" else 0
        
        sample["eval"] = result
    except Exception as err:
        print(err)
        print(traceback.format_exc())
        sys.exit(1)
        sample["eval"] = 0
    return sample

def evaluate_sample_wikitq(sample, llm, eval_prompt=wikitq_prompt):
    try:
        label = sample['answer']
        pred = sample['prediction']
        question = sample['question']
        response = llm.generate(question, pred, label, eval_prompt)
        result = 1 if response == "correct" else 0
        
        sample["eval"] = result
    except Exception as err:
        print(err)
        print(traceback.format_exc())
        sys.exit(1)
        sample["eval"] = 0
    return sample

def save_to_file(output, output_path):
    csv_columns = [
        "question_id","table","question","answer","prediction","eval","state","successful_requests","total_cost","total_tokens"
    ]
    if not os.path.exists(output_path):
        with open(output_path, mode="w", newline="") as fout:
            writer = csv.DictWriter(fout, fieldnames=csv_columns)
            writer.writeheader()
    
    with open(output_path, mode="a", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=csv_columns)
        writer.writerows(output)

def load_processed_data(output_path):
    if not os.path.exists(output_path):
        return 0, 0
    else:
        n_samples, n_correct_samples = 0, 0
        with open(output_path, mode="r", newline="") as fout:
            reader = csv.DictReader(fout)
            for row in reader:
                n_samples += 1
                if int(row['eval']) == 1:
                    n_correct_samples += 1
        return n_samples, n_correct_samples

def read_csv(data_path):
    data = []
    with open(data_path, mode="r", newline="") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            data.append(row)
    return data 

# if __name__ == "__main__":
#     # eval prompt is either wikitq prompt or tabfact_prompt
#     sample = evaluate_sample_wikitq(sample, llm, eval_prompt)
#     print(sample['eval'])