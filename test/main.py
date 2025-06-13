import argparse
import asyncio
import os
import re
import csv
import json
from time import strftime, localtime

from langgraph.errors import GraphRecursionError
from langchain_community.callbacks import get_openai_callback

from src.utils.auto_eval import evaluate_sample_wikitq, evaluate_sample_tabfact, LLM 

async def main():

    qa_data = load_json_file(settings.CONF["data"][settings.CONF["dataset"]])[:10]
    llm = settings.CONF["llm"]
    llm_client = LLM(llm, os.getenv("OPENAI_API_KEY"))
    exception_handler = HandleException(llm)
    wordflow = WorkFlow(llm)
    app = wordflow.compile()
    config = {"recursion_limit": settings.CONF['graph']['recursion_limit']}
    batch_size = settings.CONF['params']['batch_size']
    goldens = []
    predictions = []
    current_eval = []

    if settings.CONF["question_id_condition"] is not None:
        list_of_question_ids = json.load(open(settings.CONF["question_id_condition"]))
        qa_data = [sample for sample in qa_data if sample["id"] in list_of_question_ids]

    # Load existing IDs from CSV to skip re-processing them
    existing_question_ids = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_question_ids.add(row["question_id"])
                current_eval.append(float(row["eval"]))
                predictions.append([row["prediction"]])
                goldens.append(row["answer"])
    
    async def ainvoke_app(sample):
        with get_openai_callback() as cb:
            table_id = sample["table"]["name"]
            header = process_table_header(sample["table"]["header"])
            rows = sample["table"]["rows"]
            table = [header] + rows
            table = add_row_order_column(table)
            if settings.CONF["dataset"] == "wikitq":
                table_cap = header
            else:
                table_cap = sample["table_caption"]
            question = sample["question"]
            if settings.CONF["dataset"] == "wikitq":
                golden = sample["answers"]
            else:
                golden = sample["label"]
            goldens.append(golden)

            input_data = {
                "question": question,
                "table_id": table_id,
                "table": table,
                "table_cap": table_cap,
            }
            try:
                final_state = await asyncio.wait_for(app.ainvoke(input_data, config), timeout=80)
                pattern = r"<answer>(.*?)</answer>"
                match = re.search(pattern, final_state["response"])
                if match:
                    response = match.group(1)
                else:
                    response = final_state["response"]
            except asyncio.TimeoutError:
                final_state = {}
                final_state = {"response": "timeout"}
                response = exception_handler.exception_response(
                    table, table_cap, question
                )
            except GraphRecursionError:
                final_state = {}
                final_state["response"] = "graph_recursion_error"
                response = exception_handler.exception_response(
                    table, table_cap, question
                )
                
            if not response:
                response = exception_handler.exception_response(
                    table, table_cap, question
                )

            # evaluate the response
            if settings.CONF["dataset"] == "wikitq":
                sample_eval = evaluate([[response]], [golden])
            else:
                if isinstance(response, bool):
                    response_normalized = int(response)
                elif response == '1' or response == '0':
                    response_normalized = int(response)
                elif "correct" in str(response.lower()) or "true" in str(response.lower()) or "yes" in str(response.lower()):
                    response_normalized = int(1)
                else:
                    response_normalized = int(0)

                if response_normalized == golden:
                    sample_eval = 1
                else:
                    sample_eval = 0

            print(output_template.format(
                final_state=final_state,
                question=question,
                question_id=sample["id"],
                table_id=table_id,
                response=response,
                golden=golden,
                eval=sample_eval
            ))
            current_eval.append(sample_eval)
            print(f"Current Evaluation: {sum(current_eval)/len(current_eval)}")

            result = {
                "question_id": sample["id"],
                "table": format_markdown(table),
                "question": question,
                "answer": golden,
                "prediction": response,
                "eval": sample_eval,
                "state": final_state,
                "successful_requests": cb.successful_requests,
                "total_cost": cb.total_cost,
                "total_tokens": cb.total_tokens,
            }
            # if eval is not 1, double check the response
            if sample_eval != 1:
                try:
                    result = evaluate_sample_wikitq(
                        result, llm_client
                    ) if settings.CONF["dataset"] == "wikitq" else evaluate_sample_tabfact(
                        result, llm_client
                    )
                except:
                    pass
            return result, sample_eval

    # check if the question id is already processed
    qa_data = [sample for sample in qa_data if sample["id"] not in existing_question_ids]
    
    if batch_size > len(qa_data):
        batch_size = len(qa_data)
   
    for i in range(0, len(qa_data), batch_size):
        # check if the question id is already processed
        batch = qa_data[i : i + batch_size]
        responses = await asyncio.gather(*(ainvoke_app(sample) for sample in batch))
        
        # Write the results to the CSV file after processing the batch
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            for result, sample_eval in responses:
                writer.writerow(result)

        current_eval.extend([sample_eval for _, sample_eval in responses])
        print(f"Current Evaluation: {sum(current_eval) / len(current_eval)}")

    evaluation = current_eval
    print(f"Evaluation: {evaluation}")
    return "ok"

if __name__ == "__main__":
    # load hyper-params
    parser = argparse.ArgumentParser(description="Example of updating Config settings.")
    parser.add_argument(
        "--logging_level",
        type=str,
        default="DEBUG",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--experiment_name",
        type=str,
        help="Name of the experiment",
        default="gpt4omini",
    )
    parser.add_argument(
        "--llm",
        type=str,
        help="Name of the experiment",
        default="gpt-4o-mini",
        choices=["gpt-4o-mini", "gpt-3.5-turbo", "llama8b"],
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        help="Folder to save the logs and models",
        default="runs",
    )
    parser.add_argument(
        "--override_default_config",
        type=str,
        help="Path to the file containing the configuration that overrides the default for each experiment name.",
        default=None,
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="datasetname",
        default="wikitq",
        choices=["wikitq", "tabfact"],
    )

    parser.add_argument(
        "--question_id_condition",
        type=str,
        help="path of file containing question ids to be processed",
        default=None,
    )
    args = parser.parse_args()

    # Update base dir with experiment name and create it if it does not exist
    args.base_dir = os.path.join(args.base_dir, args.experiment_name)
    os.makedirs(args.base_dir, exist_ok=True)

    import logging
    # create logger
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(__name__)
    logger.info(
        f"\n\n\n=============================\n{strftime('%Y-%m-%d %H:%M:%S', localtime())} Running A New Experience: {args.experiment_name}."
    )

    from configs.config import set_config

    set_config(args)

    from configs.config import settings

    for key, value in vars(args).items():
        settings.CONF[key] = value

    # print dataset name
    print(f"Are Testing On Dataset: {settings.CONF['dataset']}")

    from dotenv import load_dotenv
    load_dotenv(override=True)

    csv_file = os.path.join(args.base_dir, "output.csv")
    csv_columns = [
        "question_id",
        "table",
        "question",
        "answer",
        "prediction",
        "eval",
        "state",
        "successful_requests",
        "total_cost",
        "total_tokens",
    ]
    if not os.path.exists(csv_file):
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()

    # run experiments
    from src.utils.table import process_table_header, add_row_order_column, format_markdown
    from src.utils.load_data import load_json_file
    from src.utils.eval import evaluate
    from src.utils.utils import output_template
    from src.graph.workflow import WorkFlow
    from src.agents.exception.agent import HandleException

    asyncio.run(main())
