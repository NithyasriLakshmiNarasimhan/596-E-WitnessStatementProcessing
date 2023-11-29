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

app = Flask(__name__)


# Route for seeing a data
@app.route('/get_answers')
def get_answers():
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

    # return image    
        
if __name__ == '__main__':
	app.run(debug=True)
