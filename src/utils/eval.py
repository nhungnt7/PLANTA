from typing import List
from src.utils.wikitq_evaluator import to_value_list, check_denotation


def evaluate(predictions: List[List], goldens: List[List]):
    scores = []
    for pred_answer, gold_answer in zip(predictions, goldens):
        pred_answer_val = to_value_list(pred_answer)
        gold_answer_val = to_value_list(gold_answer)
        correct = check_denotation(pred_answer_val, gold_answer_val)
        scores.append(correct)
    return sum(scores) / len(scores)
