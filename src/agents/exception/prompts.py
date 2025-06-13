from langchain_core.prompts import ChatPromptTemplate
examples = {
    "wikitq": """
Table:
| row order | Year| Division | League | Reg__Season | Playoffs | National_Cup |
|---|---|----|---|---|---|---|
| 7| 1935/36| N/A | ASL | 1st | Champion (no playoff) | ? |
| 8| 1936/37| N/A | ASL | 5th, National | Did not qualify | Champion |
| 24| 1952/53| N/A | ASL | 6th | No playoff | Semifinals |
| 25| 1953/54| N/A | ASL | 1st | Champion (no playoff) | Champion |
| 26| 1954/55| N/A | ASL | 8th | No playoff | ? |

Question: How long did it take for the New York Americans to win the National Cup after 1936?
Plan:
**Step 1: Identify the relevant columns**
- We need to focus on the **"Year"** and **"National_Cup"** columns.

**Step 2: Find the National Cup wins after 1936**
- **1936/37 Season:** National_Cup = **Champion**
- **1953/54 Season:** National_Cup = **Champion**

**Step 3: Calculate the time difference between the wins**
- The team won the National Cup in the **1936/37** season.
- Their next National Cup win was in the **1953/54** season.
- **Time difference:**
  - From **1936/37** to **1953/54** is **17 years**.

**Step 4: Response to user**
It took **17 years** for the New York Americans to win the National Cup after 1936.
""",
    "tabfact": """
Example 2:
Table:
| Team 1 | Score | Team 2 | 1st Round | 2nd Round |
|---|---|----|------|
| FC Nantes (D1) | 1 - 2  | AS Monaco (D1) | 0 - 0 | 1 - 2 |
| Olympique de Marseille (D1) | 3 - 2  | Sporting Toulon Var (D1) | 1 - 1 | 2 - 1 |
| OGC Nice (D1) | 1 - 5  | AJ Auxerre (D1) | 1 - 2 | 0 - 3     |
| Lille OSC (D1) | 2 - 3  | FC Mulhouse (D2) | 0 - 0 | 2 - 3     |
| FC Sochaux-Montbéliard (D1) | 2 - 1  | Olympique Lyonnais (D2) | 1 - 0 | 1 - 1 |
| AS Beauvais (D2) | 4 - 1  | SM Caen (D1) | 1 - 0 | 3 - 1 |
| Paris SG (D1) | 3 - 7  | US Orléans (D2) | 0 - 4 | 3 - 3 |
| Stade Rennais (D2) | 4 - 1  | Angers SCO (D1) | 1 - 0 | 3 - 1 |

Table Caption: 1988-89 Coupe de France
Question: The New York Americans won the National Cup in 1953/54.
Plan:
Step 1. **Define the Objective:** Verify the claim "Only 1 team from 'team 1' scored 0 points during the 2nd round."

Step 2. **Understand the Data:** The data includes a table with columns 'team 1', 'score', 'team 2', '1st round', '2nd round'.

Step 3. **Extract Relevant Information:** Focus on 'team 1' and their '2nd round' scores.

Step 4. **Plan Verification Steps:** List all 'team 1' teams and their '2nd round' scores.

Step 5. **Execute the Verification:** Identify which teams scored 0 points in the '2nd round'.

Step 6. **Analyze Results:** Only 'ogc nice (d1)' scored 0 points in the '2nd round'.

Step 7. **Conclusion:** The claim is **true** based on the provided data. response to user in the defined template.
""",
}

exception_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
"""Your task is answer the question based on the givent table. You need to return answer in tag <answer>...</answer> format, with reason in tag <reason>...</reason> format.
""",
        ),
        ("placeholder", "{messages}"),
    ]
)

exception_message_prompt = """
Consider the table below:
{table}
Table caption: {table_cap}
Please follow the reasoning template below:
{examples}
Please answer the question: {question}
"""