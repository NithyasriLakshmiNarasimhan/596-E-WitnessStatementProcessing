import json
import openai
import ast

from openai import OpenAI

def get_openai_response(user_prompt, system_prompt):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
              
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    model="gpt-3.5-turbo",
)
    # compute_usage(response)
    return (response)


@app.route('/get_answers_dynamic')
def get_answers():
    user_prompt = request.args.get('user_prompt')
    crime = request.args.get('crime')
    answers = []
    system_prompt = "You will be given a few witness statements about a " + crime + "identify a comprehensive set of questions that can be answered from the statements and that will be benificial to the investigators. Return a python list of questions."
    questions = get_openai_response("", system_prompt)
    questions = questions.choices[0].message.content
    part_2 = """
    [{question:,
      answer:}, ]"
    If the answer to that question is not in the passage, leave it empty:

    """
    
    system_prompt = "I will be giving you a few witness statements about a crime. Your task is to answer the follow up questions in a clear and concise manner. The accuracy of this task is important and so, refrain from answering the questions whose answers are not mentioned in the statement. These are the questions that you must answer based on the witness statements. Please limit your answer to 3 words or less." + questions + "return the answer as a json of questions and answers in the following format: " + part_2
   

    answers = get_openai_response("", system_prompt)
    answers = answers.choices[0].message.content
    answer = ast.literal_eval(answer)
    return answers
