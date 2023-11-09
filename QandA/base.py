from transformers  import  AutoTokenizer, AutoModelWithLMHead
from transformers import AutoModelForTokenClassification
from transformers import pipeline
import json
model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)
from flask import Flask
from flask import request
import spacy
api = Flask(__name__)
import tensorflow as tf
print(tf.__version__)
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
  print("we got here instead")
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
