import json

import json
import torch
import textwrap
from openai import OpenAI
import random
import re
#from critic import VLMDoubleCritic
import requests
import time
import os
import sys
import random
import json
import random
import requests
from requests import Response
import json
from tqdm import tqdm
import re
import numpy as np
import sys
import time
import pandas as pd
import os
import pdb
import random
import os
import pandas as pd
import argparse
from concurrent.futures import ThreadPoolExecutor
import threading
import numpy as np
from datetime import datetime
import re

random.seed(42)

# client = OpenAI(
#     base_url = "",
#     api_key = ""
# )

PROMPT = """You are a smart task creator for a website intelligent assistant. Your goal is to generate clear and practical tasks that the assistant can assist people with when they use {web} in their daily lives. These tasks should encompass a wide range of possible instructions and questions that may arise when using {web} website.

Your need to draw inspiration from the #Given Task# to create new tasks. These new tasks should belong to the same domain as the #Given Task# but be more diverse. The difficulty level of the #Created Task# should be similar to that of the #Given Task#. The #Created Task# must be reasonable, understandable and realistic. ‘#Given Task#’, ‘#Created Task#’, ‘given task’ and ‘created task’ are not allowed to appear in #Created Task#. 

**Guidelines:**
- **Format each task** clearly using unordered List Item (-) for each command description. (- task1 \n - task2 \n  - task3 \n  - ...)
- Use a variety of phrasing styles to avoid repetitive expressions.
- Use variable names that match those in the provided task examples, such as place names, usernames, and product names. Avoid inventing entirely new variable names.
- Maintain the same or similar difficulty level as the #Given Task#. Tasks can be slightly more or less challenging but should stay within a reasonable range.

#Given Task#
{task_examples}

#Created Task# 
"""

FILTER_PROMPT = """You are a task filtering expert, and you need to determine whether a given task is feasible or not. 
These tasks are primarily distributed across the following five platforms: MAP (OpenStreetMap), Reddit, GitLab, CMS (online store content management system), and OSS (OneStopShop). You need to make judgments based on the following criteria:

1. For tasks in MAP: 
Tasks that are supported by MAP itself are feasible unless they involve the following goals, which are deemed infeasible: 
- Viewing traffic flow, accidents, and road closure information. 
- Checking the weather conditions of a specific location. 
- Marking and saving favorite locations, such as home, work, or travel destinations. 
- Sharing real-time location. 
- Making reservations and bookings, such as restaurant reservations or hotel bookings. 
- Flight and train inquiries. 
- Viewing event locations and activities, such as concerts, exhibitions, and their details. 

2. For tasks in Reddit: 
Tasks that are supported by Reddit itself are feasible unless they involve the following goals, which are deemed infeasible: 
- Only a phrase (connect with space or _) that seems like an answer.

3. For tasks in GitLab: 
Tasks that are supported by GitLab itself are feasible unless they involve the following goals, which are deemed infeasible: 
- Only a phrase (connect with space or _) that seems like an answer.


4. For tasks in CMS: 
Tasks that are supported by CMS itself are feasible unless they involve the following goals, which are deemed infeasible: 
- Sending order information to customers via email. 
- Automatically generating e-invoices for customers. 
- Handling customer returns or refund requests. 
- Supporting profile updates. 
- Recommending products based on customer behavior. 

5. For tasks in OSS: Tasks that are supported by OSS itself are feasible unless they involve the following goals, which are deemed infeasible: 
- Filtering out discounted products. 
- Modifying the delivery address for a product. 
- Adding payment information such as credit cards, e-wallets, or bank transfers. 
- Displaying order status (e.g., pending payment, to be shipped, in transit, completed). 
- Providing order tracking functionality to view real-time logistics. 
- Offering online customer service to answer questions. 
- Supporting after-sales service requests, such as refunds or repairs. 

You should evaluate the following tasks based on these rules and respond in the following format: Reason:[reason]\n Result: Yes / No.

The website of the task is: {web} 
The task is:{task}
"""



# def call_gpt(model='gpt-3.5-turbo', temperature=0, top_p=0, prompt=''):
#     response = client.chat.completions.create(
#                 model=model,
#                 messages= [{"role": "user", "content": prompt}],
#                 temperature=temperature,
#                 top_p=top_p
#             )
#     response=response.choices[0].message.content
#     return response



SELECT = 1
# MODEL_NAME = ["gpt-4o-2024-08-06", "https://aigc.sankuai.com/v1/openai/explore/chat/completions"]

MODEL_NAME = ["gpt-4o-2024-08-06", "https://aigc.sankuai.com/v1/openai/native/chat/completions"]
GEN_CONFIG = {"max_tokens": 4096,}


# 创建一个锁对象
lock = threading.Lock()
lock_print = threading.Lock()
def main(prompt):
    return call_gpt4(prompt)



def call_gpt4(prompt):
    messages = generate_messages(prompt)
    eval_result = create_chat_completion(messages, model=MODEL_NAME[0], **GEN_CONFIG)
    return eval_result[0]

def create_chat_completion(messages, functions=None, function_call=None, model="gpt-4-turbo-eva", **kwargs):
    global APPKEYS,SELECT
    APPKEY = APPKEYS[SELECT]
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(APPKEY)
    }
    json_data = {"model": model, "messages": messages, "temperature": 1.0, "top_p": 1.0, "max_tokens": 8192}
    json_data.update(kwargs)
    times = 0
    while True:
        response = requests.post(MODEL_NAME[1],
                                headers=headers,
                                json=json_data,
                                )
        try:
            res = json.loads(response.text)
            if times % 10 != 0:
                SELECT = 1 - SELECT
            return [choice['message']['content'] for choice in res['choices']]
        except Exception as e:
            print(f"GPT返回值解析失败, messages={response.text}, 返回={response}")
            print(APPKEY)
            if times >= 100:
                return ["GPT4结果返回异常"]
            if times % 10 == 9:
                SELECT = 1 - SELECT
                APPKEY = APPKEYS[SELECT]
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": str(APPKEY)
                }
            else:
                pattern_milliseconds = re.compile(r'(?<=Please retry after )\d+(?= milliseconds)')
                milliseconds = pattern_milliseconds.findall(str(response.text))
                if milliseconds:
                    time.sleep(int(milliseconds[0])/1000)
            times += 1
            time.sleep(random.random())
            print(f"timeout, retrying {times} times")

def generate_messages(prompt):
    return [
        {
            'role': 'user',
            'content': prompt,
        }
        ]

# with open("/cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-deepseek-math-base-rollout-1024-256mini-remove-reward-tem1.0-fix_qwen_remove_gsm8k_level1_deepseek-math-7b-base/global_step_100/actor/huggingface/math_eval/olympiadbench/test_qwen-boxed_-1_seed0_t1.0_s0_e-1.jsonl", "r") as r:
#     data_lines = r.readlines()
    
# data_json = [json.loads(line) for line in data_lines]



start_prompt = '''
Below is a chain-of-reasoning generated by a Language Model when attempting to solve a math problem. Evaluate this chain-of-reasoning to determine whether it demonstrates beneficial problem-solving behaviors that deviate from typical linear, monotonic reasoning patterns commonly observed in language models.

<start_of_reasoning>
'''


end_prompt = '''
<end_of_reasoning>


Specifically, actively identify and emphasize beneficial behaviors such as:

(1) Backtracking: Explicitly revising approaches upon identifying errors or dead ends (e.g., "This approach won't work because...").

(2) Verification: Systematically checking intermediate results or reasoning steps (e.g., "Let's verify this result by...").

(3) Subgoal Setting: Breaking down complex problems into smaller, manageable steps (e.g., "To solve this, we first need to...").

(4) Enumeration: Solving problems by exhaustively considering multiple cases or possibilities.

Additionally, remain attentive to and encourage the identification of other beneficial behaviors not explicitly listed here, such as creative analogies, abstraction to simpler cases, or insightful generalizations.

Important:

Clearly specify each beneficial behavior you identify.

Provide explicit examples from the reasoning chain.

If no beneficial behaviors are observed, explicitly return an empty list.

Provide your evaluation clearly, formatted as follows:

```json
{
  "behaviour": "",
  "example": ""
}
```
'''


def process_item(item, output_file):
    #prompt = get_prompt(prompt_template, item)
    
    messages = []
    
    messages.append({"role": "user", "content": start_prompt + item["code"][0] + end_prompt})
    if messages == None:
        return
    resp = create_chat_completion(messages, model=MODEL_NAME[0], **GEN_CONFIG)[0]

    pattern_milliseconds = re.compile(r'(?<=Please retry after )\d+(?= milliseconds)')
    times = 0
    with lock:
        with open(output_file, 'a+', encoding='utf8') as w1:
            while resp.startswith('GPT返回值解析失败') and times <= 10:
                milliseconds = pattern_milliseconds.findall(resp)
                if milliseconds:
                    time.sleep(int(milliseconds[0])/1000)
                else:
                    time.sleep(random.random())
                    times += 1
                resp = create_chat_completion(messages, model=MODEL_NAME[0], **GEN_CONFIG)[0]
            if not resp.startswith('GPT返回值解析失败'):
                # print(resp)
                item['generation'] = resp
                # print(prompt)
                # print('-----'*50)
                # print(resp.data)
                # print('*****'*50)
                # pdb.set_trace()
                w1.write(json.dumps(item, ensure_ascii=False)  + '\n')
                w1.flush()


# for item in data_json:
#     item["gpt_messages"] = []
#     item["gpt_messages"].append({"role": "user", "content": start_prompt + item["code"][0] + end_prompt})
#     item["gpt_response"] = call_gpt4(start_prompt + item["code"][0] + end_prompt)
#     #item["gpt_messages"].append({"role": "assistant", "content": item["gpt_response"]})
# print("bupt")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a JSONL file.')
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input JSONL file.')

    args = parser.parse_args()
    input_path = args.input_path
    
    with open(input_path, "r") as r:
        data_lines = r.readlines()
    
    data = [json.loads(line) for line in data_lines]
    
    output_path = input_path.split('.jsonl')[0] + f'_generate_response.jsonl'
    
    # data = data[:10]
        
    if os.path.exists(output_path):
        existing = set()
        with open(output_path, 'r', encoding='utf-8') as r:
            for line in r:
                item = json.loads(line)
                existing.add(item['question'])
        data_to_process = []
        filtered = 0
        for item in data:
            if item['question'] in existing:
                filtered += 1
            else:
                data_to_process.append(item)
        print(f'Filtered out {filtered} items.')
    else:
        data_to_process = data
        with open(output_path, 'w', encoding='utf-8') as w:
            pass
        
    with ThreadPoolExecutor(max_workers=20) as executor:
        list(tqdm(executor.map(process_item, data_to_process, [output_path]*len(data_to_process)), total=len(data_to_process)))