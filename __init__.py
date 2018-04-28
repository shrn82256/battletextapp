from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/getword',methods = ['GET'])
def result():
	rargs = request.args
	if rargs['start'][0].isalpha():
		start = rargs['start'][0].lower()
	else:
		start = 'a'
	if 'avoid' in rargs.keys() and len(rargs['avoid']) >= 1:
		avoid = [i.lower() for i in rargs['avoid']]
		avoidFlag = True
	else:
		avoid = []
		avoidFlag = False
	if 'end' in rargs.keys() and len(rargs['end']) >= 1:
		end = rargs['end'].lower()
		endFlag = True
	else:
		end = ""
		endFlag = False

	try:
		filePath = "/home/ubuntu/battletextapp/static/words/"
		data = list(json.load(open(filePath + start + ".json")))
	except:
		filePath = "F:\\battletextapp\\static\\words\\"
		data = list(json.load(open(filePath + start + ".json")))

	data.sort(key=len, reverse=True)

	if 'num' in rargs.keys() and len(rargs['num']) >= 1:
		n = int(rargs['num'])
	else:
		n = 20
	words = []
	for i in data:
		flag = True
		if avoidFlag:
			for j in avoid:
				if j in i:
					flag = False
					break
		if endFlag:
			if not i.endswith(end):
				flag = False
		if flag and len(i) <= 24:
			words.append(i)
		else:
			continue
		if len(words) == n:
			break

	return render_template('index.html', result=words, avoid=rargs['avoid'])

if __name__ == '__main__':
	app.run(host="0.0.0.0")
	# app.run(debug=True)