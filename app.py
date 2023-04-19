# Using flask to make an api
# import necessary libraries and functions
from datetime import datetime
from flask import Flask, jsonify, request, Response

from flask_cors import CORS, cross_origin
import json
import openai
import re
import os

openai.api_key = os.environ['OPENAI_API_KEY']

# creating a Flask app
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'




system_message = open('system_message.txt', 'r').read()

user_message = open('user_message.txt', 'r').read()

chords_file = json.loads(open('chord-fingerings.json', 'r').read())
  
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
    
def minify_json(json_data):
    # check if json_data is a string
    # print(type(json_data), json_data)
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    return json.dumps((json_data), separators=(',', ':'), indent=None)
  
def save_to_log(request_ip, request_time, progression, success, error, response, openai_response={}):
    # with open('./_logs/log.txt', 'a') as f:
        # f.write('\n'+str(request_time) + '|' + request_ip + '|' + progression + '|' + str(success) + '|' + re.sub(r"[\n\t]*", "", error) + '|' + str((datetime.now()-request_time).seconds) + '|' + re.sub(r"[\n\t]*", "", str(response)))        
    print((str(request_time) + '|' + request_ip + '|' + progression + '|' + str(success) + '|' + re.sub(r"[\n\t]", " ", error) + '|' + str((datetime.now()-request_time).seconds) + '|' + minify_json((response))) + '|' + minify_json((openai_response)))

@app.route('/api/reharmonize', methods = ['GET', 'OPTIONS'])
def disp():
    progression = request.args.get('progression')
    # print(progression)

    request_ip = request.remote_addr
    request_time = datetime.now()
    # print(request_time, request_ip, progression)


    # make sure the progression string is not empty
    if len(progression) == 2 or progression == None or progression == '':
        save_to_log(request_ip, request_time, progression, False, 'empty progression', 'Error 400: Bad Request')
        return Response('Bad Request', status=400, mimetype='application/json')
    
    # ensure that the progression string is of the correct format (eg [Gmaj, Emin, Cmaj, Dmaj])
    if progression[0] != '[' or progression[-1] != ']':
        save_to_log(request_ip, request_time, progression, False, 'invalid progression format', 'Error 400: Bad Request')
        return Response('Bad Request', status=400, mimetype='application/json')
    
    # extract the chord progression from the request
    progression_t = progression[1:-1]
    progression_t = progression_t.split(', ')

    if (len(progression_t) > 5):
        save_to_log(request_ip, request_time, progression, False, 'progression contains more than 5 chords '+str(len(progression_t)), 'Error 400: Bad Request')
        return Response('Bad Request', status=400, mimetype='application/json')
    
    for chord in progression_t: 
        if re.match(r'^[A-G][#]?(m|maj|min|dim|aug|7|maj7|min7|dim7|add9)?$', chord) == None:
            # print('Chord is invalid ', chord)
            save_to_log(request_ip, request_time, progression, False, 'invalid chord '+chord, '')
            return Response('Bad Request', status=400, mimetype='application/json')
    
    if (progression == '[G, Em, C, D]'):
        res = json.loads(open('response.json', 'r').read())
        # res = res.choices[0]['message']['content']
        res = append_chord_fingerings(res)
        save_to_log(request_ip, request_time, progression, True, '', res)
        return (res)
        # return json.loads(open('response.json', 'r').read()) # return pre-defined response for testing
    
    styles = '[jazz, funk, rnb]'
    passing_chords = 'true'
    number = '3'
    
    # replace global user_message variable value with the user input
    user_message_local = str(user_message)
    user_message_local = user_message_local.replace('<progression>', progression)
    user_message_local = user_message_local.replace('<style>', styles)
    user_message_local = user_message_local.replace('<passing>', passing_chords)
    user_message_local = user_message_local.replace('<number>', number)
    


    # return json.loads(open('response.json', 'r').read()) # return pre-defined response for testing
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message_local},
            ]
        )
        if (response.choices[0].finish_reason == 'stop'):
            # print(response.choices[0]['message']['content'])
            # save_to_log(request_ip, request_time, progression, True, '', re.sub(r"[\n\t]*", "", str(response)))

            res = json.loads(response.choices[0]['message']['content'])
            res = append_chord_fingerings(res)

            save_to_log(request_ip, request_time, progression, True, '', res, response)
            return (res)
        else:
            save_to_log(request_ip, request_time, progression, False, 'API error', 'Error 400: Bad Request')
            return Response('Bad Request', status=400, mimetype='application/json')
    except Exception as e:
        # print(e)
        save_to_log(request_ip, request_time, progression, False, 'openai error exception: '+str(e), 'Error 400: Bad Request')
        return Response('Bad Request', status=400, mimetype='application/json')
    

def append_chord_fingerings(response):
    chord_list = []
    for alternates in response['alternates']:
        chord_list.extend(alternates['reharmonized'])
        chord_list.extend(alternates['new_passing_chords'])

    chord_list = list(set(chord_list))
    # print(len(chord_list), len(set(chord_list)))

    chord_fingerings = dict()
    for chord in chord_list:
        # if chord contains 'minor' replace it with 'm'
        modified_chord = ''
        if 'minor' in chord:
            modified_chord = chord.replace('minor', 'm')
            # chord = modified_chord
        elif 'min' in chord:
            modified_chord = chord.replace('min', 'm')
            # chord = modified_chord
        elif 'maj' == chord[-3:len(chord)]:
            modified_chord = chord.replace('maj', '')
        elif '°' in chord:
            modified_chord = chord.replace('°', 'dim')
        elif 'ø' in chord:
            if 'ø7' in chord:
                modified_chord = chord.replace('ø7', 'dim7')
            else:
                modified_chord = chord.replace('ø', 'm7b5')
                
        else:
            modified_chord = chord

        for key in chords_file.keys():
            
            if chord == key or modified_chord == key:
                # print(key, chord)
                for position in chords_file[key]:
                    if chord not in chord_fingerings:
                        chord_fingerings[chord] = []
                    chord_fingerings[chord].append(position)
                break

    for k,v in chord_fingerings.items():
        # print(k, len(v))
        chord_fingerings[k] = v[0:3]

    # for k,v in chord_fingerings.items():
    #     print(k, v)

    response['chord_fingerings'] = chord_fingerings

    return response
    
    
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)