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
  Samplecontext = """
Statement 1:
My name is Amanda Wells. On Tuesday afternoon around 3:30pm, I was walking my dog in the park when I heard a child scream. I looked over and saw a man grabbing a young boy who looked about 10 years old. The boy was yelling "Help, help!" but the man put his hand over the boy's mouth and dragged him towards a white van. He forced the boy into the side door of the van and then got into the driver's seat and quickly drove off. I immediately called 911 to report what I saw. I really hope they find that poor boy.

Statement 2:
My name is Mark Jones. On Tuesday around 3:45pm, I was driving down Elm Street when I noticed some commotion in the park. I pulled over and saw a man pulling a young boy into a white van. The boy was crying and trying to get away but the man was too strong. He shoved the boy into the van and sped off. I tried to get the license plate number but couldn't see it clearly. The boy looked about 10 years old with brown hair and a red shirt. I called 911 and reported the incident as a likely kidnapping. I hope they find him soon.

Statement 3:
My name is Sarah Davis. I was in the park with my children on Tuesday afternoon when I witnessed a kidnapping. Around 3:30pm, a man in a black hoodie grabbed a young boy who was playing on the swings. The boy screamed "Let me go!" but the man covered his mouth and dragged him toward a white van parked nearby. He forced the boy into the van and drove off quickly. The boy appeared to be about 10 years old with blond hair and was wearing a blue t-shirt. I immediately pulled out my phone, dialed 911, and told them what I saw. I hope the police can rescue that poor child.

Statement 4:
My name is Jack Wilson. On Tuesday at approximately 3:35pm, I witnessed a kidnapping at the park on Oak Street. I saw a man wearing a black ski mask jump out of a white van, grab a young boy off the sidewalk, and force him into the van. The boy looked about 10 years old with brown hair and was crying for help. I yelled at the man to stop but he drove off quickly with the boy in his van. I called the police immediately and reported the license plate number as ABC-1234. I really hope they find that kid soon. The police need to catch this criminal.

Statement 5:
My name is Lisa Chen. I was walking through the park on Tuesday afternoon when I saw a frightening scene. A man in a gray sweatshirt and jeans was forcibly dragging a young boy toward a white van. The boy was screaming "Help me!" but the man put a hand over his mouth and shoved him into the side door of the van. The boy looked about 10 years old with sandy blonde hair. I tried to intervene but the man drove off in a hurry before I could do anything. I immediately took out my cell phone and called the police to report the kidnapping. I really hope they can find the boy and arrest whoever took him. It was an incredibly disturbing thing to witness."
"""

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