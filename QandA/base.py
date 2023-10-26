from  transformers  import  AutoTokenizer, AutoModelWithLMHead, pipeline
import json
model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)
from flask import Flask
from flask import request
api = Flask(__name__)











@api.route('/QandA', methods = ['GET', 'POST', 'DELETE'])
def my_QandA():

  if request.method == 'POST':
    questions = ["What was the crime being discussed?", "What is the gender of the criminal?", "Was there a vehicle mentioned in the statements?", "What does the vehicle look like?", "What did the criminal look like?", "What did the criminal wear?", "What did the criminal use to commit the crime?", "What was the criminal's ethnicity?", "What was the criminal's age?", "What did the victim look like?", "What did the victim wear?", "What was the victim's ethnicity?", "What was the gender of the victim?", "What was the age of the victim?"]

    statements = json.loads(request.data.decode())
    context = statements['statement']
    
    responses = []
    for question in questions:
      # question = "What was the age of the victim?"

      input = f"question: {question} context: {context}"
      encoded_input = tokenizer([input],
                                  return_tensors='pt',
                                  max_length=2048,
                                  truncation=True)
      output = model.generate(input_ids = encoded_input.input_ids,
                                  attention_mask = encoded_input.attention_mask)
      response = tokenizer.decode(output[0], skip_special_tokens=True)
      responses.append(response)
    output = questions[0] + ": " + responses[0]
    for i in range(1, len(questions)):
      output += "\n" + questions[i] + ": " + responses[i]
    return output
  else:
    context = request.data.statement
    print("hello")
    print(context)
    return context
# # print(context)
# print(q_and_a(context))




# from flask import Flask

# api = Flask(__name__)

# @api.route('/profile')
# def my_profile():
#     response_body = {
#         "name": "Nagato",
#         "about" :"Hello! I'm a full stack developer that loves python and javascript"
#     }

#     return response_body