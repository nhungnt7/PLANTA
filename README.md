# Planta: Table Understanding with LLM Long-Term Planning

## Overview

PLANTA is a powerful agent system for complex table reasoning, built around a long-term planning framework where each step is tightly connected and contributes directly to the final goal.

🏆 **State-of-the-art performance**: PLANTA achieves SOTA results on the WikiTableQuestions and TabFact benchmarks.

## Project Architecture

The Planta project is structured as follows:

```
.
├── configs/                    # Configuration files
├── data/                       # Dataset management scripts
├── logs/                       # Logging output
├── settings/                   # YAML configuration files
├── src/                        # Source code
│   ├── agents/                 # Specialized agents
│   ├── graph/                  # Graph-based workflow management
│   └── utils/                  # Utility functions
├── test/                       # Testing scripts
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
└── run.sh                      # Script for running experiments
```

## Installation

To set up the Planta project, follow these steps:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/nhungnt7/planta
    cd planta
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**

    Create a `.env` file in the project root with your OpenAI API key:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Configuration

The system is configured using YAML files located in the `settings` directory:

*   **`settings/config.yml`:** Contains dataset paths, model settings, task-specific parameters, and graph execution settings.
*   **`settings/logging.yml`:** Configures logging settings.

Key configuration sections in `config.yml`:

```yaml
data:
  wikitq: data/datasets/wikitq/test.json
  tabfact: data/datasets/tab_fact/small_test.jsonl

model:
  gpt-4o-mini: "gpt-4o-mini"
  gpt-3.5-turbo: "gpt-3.5-turbo"

params:
  batch_size: 1
  default_temperature: 0
  high_temperature: 0
  search_temperature: 0.4
```

## Usage

### Running Experiments

Experiments can be run using the `run.sh` script or by directly executing the `test/main.py` file.

#### Using `run.sh` Script

```bash
bash run.sh [experiment_name] [dataset] [llm]
```

Parameters:

*   `experiment_name`: Name for the experiment (default: `gpt4omini`)
*   `dataset`: Dataset to use (`wikitq` or `tabfact`, default: `tabfact`)
*   `llm`: Language model to use (`gpt-4o-mini`, `gpt-3.5-turbo`, default: `gpt-4o-mini`)

Example: Running `gpt-4o-mini` on WikiTableQuestions:

```bash
bash run.sh wtq_experiment wikitq gpt-4o-mini
```

This will:

*   Test on the WikiTableQuestions dataset.
*   Use the `gpt-4o-mini` model.
*   Save results in `runs/wtq_experiment/`.
*   Output evaluation metrics for table question answering.

#### Direct Python Execution

```bash
python test/main.py \
  --dataset wikitq \
  --experiment_name custom_run \
  --llm gpt-3.5-turbo \
  --logging_level DEBUG
```

Command-line arguments:

*   `--dataset`: Choose dataset (`wikitq` or `tabfact`)
*   `--experiment_name`: Name for the experiment run
*   `--llm`: Model to use (`gpt-4o-mini`, `gpt-3.5-turbo`)
*   `--base_dir`: Output directory (default: `runs`)
*   `--logging_level`: Debug level (default: `DEBUG`)
*   `--override_default_config`: Custom config file path
*   `--question_id_condition`: Path to file containing specific question IDs to process

### Dataset Setup

1.  **Create Dataset Directories:**

    ```bash
    mkdir -p data/datasets/wikitq
    mkdir -p data/datasets/tab_fact
    ```

2.  **Download and Prepare Datasets:**

    ```bash
    python data/download_dataset.py
    ```

The datasets will be automatically loaded and processed during experiment runs based on the configuration in `settings/config.yml`.

## Output Structure

Experiment results are saved in the `runs` directory:

```
runs/
└── {experiment_name}/
    ├── app.log        # Experiment logs
    └── output.csv     # Results containing:
        - Question IDs
        - Tables
        - Questions
        - Answers
        - Predictions
        - Evaluation metrics
        - Model statistics
```

## Citation

If you use this code in your research, please cite our paper:

```bibtex
@inproceedings{
  nguyen2025planning,
  title={Planning for Success: Exploring {LLM} Long-term Planning Capabilities in Table Understanding},
  author={Thi-Nhung Nguyen and Hoang Ngo and Dinh Phung and Thuy-Trang Vu and Dat Quoc Nguyen},
  booktitle={The SIGNLL Conference on Computational Natural Language Learning},
  year={2025}
}
```
