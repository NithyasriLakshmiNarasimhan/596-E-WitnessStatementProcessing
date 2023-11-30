from transformers  import  AutoTokenizer, AutoModelWithLMHead
from transformers import AutoModelForTokenClassification
from transformers import pipeline
import json
import os
model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)
from flask import Flask
from flask import request
import spacy
api = Flask(__name__)
import tensorflow as tf
import json
import openai
from openai import OpenAI
import json
import openai
from graphviz import Digraph
from PIL import Image
from io import BytesIO
import ast
from treelib import Node, Tree
from graphviz import Graph, Digraph
from flask import Flask, request
from flask import Flask, send_file
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import networkx as nx




def compute_usage(response):
    f = open('usage.json')
    data = json.load(f)
    data['input_tokens_used']+=response['usage']["prompt_tokens"]
    data['output_tokens_used']+=response['usage']['completion_tokens']
    with open('usage.json', 'w') as f:
        json.dump(data, f)

    
# def get_openai_response(user_prompt, system_prompt):
#     openai.api_key = "x"
#     response = openai.ChatCompletion.create(
#                   model="gpt-3.5-turbo",
#                   messages=[{"role": "system", "content": system_prompt},
#                             {"role": "user", "content": user_prompt}
#                   ])
#     compute_usage(response)
#     return (response)

def get_openai_response(user_prompt, system_prompt):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    # api_key="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",
    api_key = "x"
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
    # print(response)
    return (response.choices[0].message.content)





@api.route('/getFiles', methods = ['GET', 'POST', 'DELETE'])
def getCaseFiles():
  statements = json.loads(request.data.decode())
  context = statements['fileNum']
  statementsPath = "./Statements"
  fileString = ""
  for fileName in os.listdir(statementsPath):
    fileString += fileName + '\n'
  return os.listdir(statementsPath)

def openAI_QA(context, question):
  system_prompt = """
I will be giving you a few witness statements about a crime. Your task is to answer the follow up question in a clear and concise manner. The accuracy of this task is important and so, refrain from answering the questions whose answers are not mentioned in the statement.
"""
  user_prompt = "The Witness statements are as follows:\n" + context + "\n\n" + "question: \t" + question

  return get_openai_response(user_prompt, system_prompt)



@api.route('/process_text', methods=['POST'])
def process_text():

    dir_name = request.json.get('text')
    question = request.json.get('question')
    content = ""
    path = 'C:/Users/nithy/Documents/GitHub/596-E-WitnessStatementProcessing/FrontEnd/reactapp/src/witnessstatements/'+ dir_name + '/'
    with os.scandir(path) as dir_contents:
      for entry in dir_contents:
        filename = path + entry.name
        with open(filename) as f:
            lines = '\n'.join(f.readlines())
            # print(lines)
            content+=lines
            content+='\n'
    return openAI_QA(content, question)
    # return content
    
    # Process the text_data here and return a response
    # response = {"message": f"Processed text: {text_data}"}
    # return str(response)


@api.route('/getFileContent', methods = ['GET', 'POST', 'DELETE'])
def getFileContent():
  statements = json.loads(request.data.decode())
  fileNum = statements['fileNum']
  filePath = "./Statements/" + fileNum
  returnList = [[], ""]
  if(os.path.isdir(filePath)):
    returnList[0] = os.listdir(filePath)
  if(os.path.isfile(filePath)):
    fileString = os.path.basename(filePath) + '\n' + '\n'
    file=open(filePath,"r")
    fileString += file.read()
    returnList[1] = fileString
  return returnList


@api.route('/StaticGraph', methods = ['GET', 'POST', 'DELETE'])
@app.route('/get_answers')
def get_answers():

    system_prompt = """
    I will be giving you a few witness statements about a crime. Your task is to answer the follow up questions in a clear and concise manner. The accuracy of this task is important and so, refrain from answering the questions whose answers are not mentioned in the statement.

    These are the questions that you must answer based on the witness statements. Please limit your answer to 3 words or less.

    What was the crime being discussed?
    What is the gender of the criminal?,
    What does the vehicle used in the crime look like?,
    What did the criminal look like?,
    What did the criminal wear?,
    What did the criminal use to commit the crime?,
    What was the criminal's ethnicity?,
    What was the criminal's age?,
    What did the victim look like?,
    What did the victim wear?,
    What was the victim's ethnicity?,
    What was the gender of the victim?,
    What was the age of the victim?

    Return the answer as a python list.\\
    If the answer to that question is not in the passage, leave it empty:

    """

    keys = ['crime', 'criminal gender', 'crime vehicle', 'criminal\'s appearance', 'criminal\'s clothes', 'criminal accessasory', 'crinimal\'s ethnicity', 'criminal\'s age', 'victim\'s appearance', 'victim\'s clothes', 'victim\'s ethnicity', 'victim\'s gender', 'victim\'s age']



    user_prompt = request.args.get('user_prompt')
    answers = []
    # for i in range(len(user_prompt)):
    response = get_openai_response(user_prompt, system_prompt)
    answer = ast.literal_eval(response['choices'][0]['message']['content'])
    answers.append(answer)    
    description_of_the_crime = {}
    for k, v in zip(keys, answer):
        description_of_the_crime[k]=v
    
    nodes = []
    
    crime_desc = description_of_the_crime['crime']
    nodes.append(crime_desc)
    edges = []
    for key in description_of_the_crime.keys():
        # edges.append()

        # s = key+":\n"+description_of_the_crime[key]
        if 'crime'==key:
            continue
        nodes.append(key)
        
        if len(description_of_the_crime[key])>0 and  "not mentioned" not in str.lower(description_of_the_crime[key]):
            nodes.append(description_of_the_crime[key])
            edges.append((key, description_of_the_crime[key]))
        
        if 'victim' in key:
            edges.append((key,crime_desc))
        else:
            edges.append((crime_desc, key))  

    G = nx.DiGraph()

    G.add_nodes_from(nodes)

    G.add_edges_from(edges)


    nx.draw(G, with_labels=True, font_weight='bold', node_color='skyblue', edge_color='gray', node_size=800)
        
    dot = Graph(comment='Tree Visualization')

    for node in nodes:
        dot.node(str(node), str(node))

    for edge in list(edges):
        dot.edge(str(edge[0]), str(edge[1]))

    
    
    dot_format = 'png'  # Choose the desired image format (e.g., png, pdf, svg, etc.)
    graph_bytes = dot.pipe(format=dot_format)
    
    graph_bytesio = BytesIO(graph_bytes)
    image = Image.open(graph_bytesio)
    img_stream = BytesIO()
    image.save(img_stream, format='PNG')
    img_stream.seek(0)

    # Serve the image to the front end
    return send_file(img_stream, mimetype='image/png')
  



@api.route('/QandA', methods = ['GET', 'POST', 'DELETE'])
def my_QandA():

  if request.method == 'POST':
    questions = ["What was the crime being discussed?", "What is the gender of the criminal?", "Was there a vehicle mentioned in the statements?", "What does the vehicle look like?", "What did the criminal look like?", "What did the criminal wear?", "What did the criminal use to commit the crime?", "What was the criminal's ethnicity?", "What was the criminal's age?", "What did the victim look like?", "What did the victim wear?", "What was the victim's ethnicity?", "What was the gender of the victim?", "What was the age of the victim?"]

    statements = json.loads(request.data.decode())
    context = statements['statement']
    for newQ in (statements['questions']):
      questions.append(newQ)
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
    return "Error"
  


@api.route('/NER', methods = ['GET', 'POST', 'DELETE'])
def doNer():
  statements = json.loads(request.data.decode())
  statement = statements['statement']
  # import usaddress

  tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
  model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
  tokenizer_address = AutoTokenizer.from_pretrained("ctrlbuzz/bert-addresses")
  model_address = AutoModelForTokenClassification.from_pretrained("ctrlbuzz/bert-addresses")
  # spacy.cli.download("en_core_web_sm")
  NER = spacy.load("en_core_web_sm")
  def apt_no(trial_token, ner):
    apt=''
    iter=1
    while iter<=5:
      if trial_token[ner['index']-iter].isdigit():
        apt = trial_token[ner['index']-iter] + apt
      #   print(trial_token[ner['index']-iter])
      elif trial_token[ner['index']-iter][2:].isdigit():
        apt = trial_token[ner['index']-iter][2:] + apt
      #   print(trial_token[ner['index']-iter][2:])
      else:
        if apt=='':
          return ner['word']
        else:
          return apt + ' ' + ner['word']
      iter+=1
  #   print(type(apt))
  nlp = pipeline("ner", model=model, tokenizer=tokenizer)
  nlp_address = (pipeline("ner", model=model_address, tokenizer=tokenizer_address))

  def NER_func(doc):

    ner_res = nlp(doc)
  #   for ner in ner_res:
  #     print('entity = ', ner['entity'], " word = ",ner['word'])
    inputs = tokenizer(doc, return_tensors="pt")
    # print(inputs["input_ids"][0])
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    # print(tokens)
    trial_token = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    for ner in ner_res:
      if ner['entity'] == 'B-LOC':
        ner['word'] = apt_no(trial_token, ner)
      #   print(ner['word'])
      #   if trial_token[ner['index']-1].isdigit():
      #     ner['word'] = trial_token[ner['index']-1] + ' ' + ner['word']
      #   if trial_token[ner['index']-1].startswith('##'):
      #     if trial_token[ner['index']-1][2:].isdigit():
      #       # # h_no = find_house_no(1,trial_token[ner['index']-5],'')
      #       ner['word'] = trial_token[ner['index']-2] + trial_token[ner['index']-1][2:] + ' ' + ner['word']
    per=[]
    loc=[]
    misc=[]
    idk=[]
    for ner in ner_res:
      # print('entity = ', ner['entity'], " word = ",ner['word'])
      if ner['entity'] =='B-PER' or ner['entity'] == 'I-PER':
        per.append([ner['word'], ner['entity']])
      elif ner['entity'] =='B-LOC' or ner['entity'] == 'I-LOC':
        loc.append([ner['word'], ner['entity']])
      elif ner['entity'] =='B-MISC' or ner['entity'] == 'I-MISC':
        misc.append([ner['word'], ner['entity']])
      else:
        idk.append([ner['word'], ner['entity']])
      
  #   print(per)
  #   print()
  #   print(loc)
  #   print()
  #   print(misc)
  #   print()
  #   print(idk)
    entity_arr = [per]+[loc]+[misc]+[idk]
    # print(entity_arr)

    flag=0
    begin_flag=0
    temp=''
    per_final=[]
    entity_final=[]
    for ent in entity_arr:
      # print(ent)
      ent_len=len(ent)
      temp=''
      per_final=[]
      for i,val in enumerate(ent):
        if val[1].startswith('B'):
          begin_flag=1
          per_final.append(temp)
          temp=val[0]
        else:
          begin_flag=0
          if val[0].startswith('##'):
            temp=temp+val[0][2:]
          elif not val[0][0].isalpha():
            temp=temp+val[0]
            flag=1
          else:
            if flag==1:
              flag=0
              temp=temp+val[0]
            else:
              temp=temp+' '+val[0]
          if i==ent_len-1:
            per_final.append(temp)
      if begin_flag==1:
        per_final.append(temp)

      entity_final.append(per_final[1:]) 
    entity_dict = {'Names': entity_final[0], 'Improper addresses and Locations': entity_final[1], 'Vehicles': entity_final[2] , 'Organizations': entity_final[3]}
    # for key,val in entity_dict.items():
    #   print(key,' : ', val)
    var_date = {(ent.text.strip(), ent.label_) for ent in NER(doc).ents if ent.label_ == 'DATE'}
    # print(var_date)
    date_dict = {}
    for text, label in var_date:
        if label not in date_dict:
            date_dict[label] = []
        if not text.isdigit():
          date_dict[label].append(text)
    # print(date_dict)
    entity_dict.update(date_dict)
    return entity_dict
  d = NER_func(statement)
  output = ""
  for k,v in d.items():
    output += k +": "
    v = set(v)
    for name in v:
      output += name + ", "
    output += "\n"
  return output
