# Import flask and datetime module for showing date and time
from flask import Flask, request
import datetime
# from messages import message
from qanda import q_and_a

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)


# Route for seeing a data
@app.route('/data')
def get_time():
	# Returning an api for showing in reactjs
    source = request.args.get('source')
    return q_and_a(source) 
    # return '''<h1>The source value is: {}</h1>'''.format(source)
	# return {
	# 	'Name':"geek", 
	# 	"Age":"22",
	# 	"Date":x, 
	# 	"programming":"python",
	# 	'value': s['key']
	# 	}

	
# Running app
if __name__ == '__main__':
	app.run(debug=True)
