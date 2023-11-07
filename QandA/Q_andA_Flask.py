import json
import openai
from graphviz import Digraph
from PIL import Image
from io import BytesIO
import ast
from treelib import Node, Tree
from graphviz import Digraph
from flask import Flask, request
from flask import Flask, send_file
from PIL import Image
from io import BytesIO


def compute_usage(response):
    f = open('usage.json')
    data = json.load(f)
    data['input_tokens_used']+=response['usage']["prompt_tokens"]
    data['output_tokens_used']+=response['usage']['completion_tokens']
    with open('usage.json', 'w') as f:
        json.dump(data, f)

    
def get_openai_response(user_prompt, system_prompt):
    openai.api_key = "#"
    response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                  ])
    compute_usage(response)
    return (response)

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
Incase an answer is not mentioned in the witness statements, give an empty string for that question:

"""

user_prompt = [
"""
Statement 1:
My name is Amanda Clark. I manage a motel just off the highway. A few weeks ago, I noticed a room had been booked for over a month under one man's name. However, I saw a different man coming and going from the room with three young women. They rarely ventured out and looked very scared and thin. I thought it seemed suspicious and called the police to report possible trafficking. Officers investigated and found the women had been kidnapped and were being forced into sex work against their will. I'm glad I spoke up before the situation got worse.

Statement 2:
My name is Officer James Wilson. I helped raid a motel room where three trafficking victims were being held captive. The young women were lured from vulnerable backgrounds with promises of jobs and security, then transported across state lines and forced into prostitution. The traffickers employed coercion, abuse and controlled their access to food, shelter and medical care. We arrested the ringleaders and provided support services to help the victims. Sadly this is just one example of human trafficking networks exploiting the vulnerable.

Statement 3:
My name is Amanda Lopez. I thought I had met a nice man online who cared about me. But he convinced me to travel far from home, took my phone, and forced me to have sex with strangers for money. There were two other girls in the same situation who were always under watch. When we didn't obey, we were beaten and starved. They said if we tried to escape our families would pay. I felt totally trapped and scared until the police raided and rescued us. I'm so thankful but the trauma still haunts me.

Statement 4:
My name is Dr. Sarah Mills. I volunteer with an organization providing medical services to human trafficking survivors. The victims we see have extensive trauma from prolonged abuse - physical injuries, malnutrition, PTSD and more. Restoring their health and trust is extremely difficult. Traffickers often deny them healthcare, control them with forced drug use, and leave victims with long-term medical issues. Sadly there are many still suffering in abusive situations with no access to help. We must keep fighting this criminal exploitation.

Statement 5:
My name is Mark Caruso. I'm a social worker that assists human trafficking victims after they escape or are rescued. The psychological impact cannot be overstated. Most deal with severe depression, anxiety, substance abuse and suicidal thoughts from the cruelty inflicted upon them. I help connect survivors to counseling, medical care, housing services and vocational training so they can heal and build a better life. It's a long difficult journey but incredibly rewarding to see their strength and resilience.
""" 
]
keys = ['crime', 'criminal gender', 'crime vehicle', 'criminal\'s appearance', 'criminal\'s clothes', 'criminal accessasory', 'crinimal\'s ethnicity', 'criminal\'s age', 'victim\'s appearance', 'victim\'s clothes', 'victim\'s ethnicity', 'victim\'s gender', 'victim\'s age']

app = Flask(__name__)


# Route for seeing a data
@app.route('/get_answers')
def get_answers():
    user_prompt = request.args.get('user_prompt')
    description_of_the_crime={}
    answers = []
    # for i in range(len(user_prompt)):
    response = get_openai_response(user_prompt, system_prompt)
    answer = ast.literal_eval(response['choices'][0]['message']['content'])
    answers.append(answer)    
    description_of_the_crime = {}
    for k, v in zip(keys, answer):
        description_of_the_crime[k]=v
    tree = Tree()
    tree.create_node(description_of_the_crime['crime'], description_of_the_crime['crime'])  # root node
    
    
    for key in description_of_the_crime:
        if key!='crime':
            tree.create_node(key+"\n"+description_of_the_crime[key], key+"\n"+description_of_the_crime[key], parent=description_of_the_crime['crime'])
    dot = Digraph(comment='Tree Visualization')

    for node in tree.all_nodes():
        dot.node(node.identifier, node.tag)
    
    for node in tree.all_nodes():
        parent = tree.parent(node.identifier)
        if parent:
            dot.edge(parent.identifier, node.identifier)
    
    dot_format = 'png'  # Choose the desired image format (e.g., png, pdf, svg, etc.)
    graph_bytes = dot.pipe(format=dot_format)
    
    graph_bytesio = BytesIO(graph_bytes)
    image = Image.open(graph_bytesio)
    img_stream = BytesIO()
    image.save(img_stream, format='PNG')
    img_stream.seek(0)

    # Serve the image to the front end
    return send_file(img_stream, mimetype='image/png')

    # return image    
        
if __name__ == '__main__':
	app.run(debug=True)
