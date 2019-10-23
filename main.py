from flask import Flask, render_template, request, Response
from flask import jsonify, make_response
import time

app = Flask(__name__)

push_data = ['hello there']

message_id = 0

@app.route('/stream')
def stream():
    global push_data
    def eventStream():
        global push_data
        while True:
            yield 'data: {}\n\n'.format(push_data[0])
            push_data = []
            break
    while(len(push_data) != 0):
        time.sleep(1)
        return Response(eventStream(), mimetype="text/event-stream")
    return Response('', mimetype="text/event-stream")

@app.route('/get_reply', methods=['GET','POST'])
def get_reply():
    global push_data, message_id
    # chat_msg, display_cards
    recieved_data = request.form.to_dict()
    print('Message sent by client: ', recieved_data)
# =============================================================================
#     scrapped_data = scrap_data('Bangalore', 'asdfasdfsf', 'Doctor Name', 0)
#     data = {'message': scrapped_data, 'msg_type': 'display_cards'}
#     print(scrapped_data)
# =============================================================================
# =============================================================================
#     scrapped_data = ['Reply from the bot']
#     data = {'message': scrapped_data, 'msg_type': 'chat_msg'}
# =============================================================================
    
    scrapped_data = [{'headline':'This is first headline', 'body': 'This is first body'}, {'headline':'This is second headline', 'body': 'This is second body'}]
    data = {'message': scrapped_data, 'msg_type': 'ask_options', 'id': message_id}
    message_id+=1
    print('About to push again...')
    push_data.append('Push data again...')
# =============================================================================
#     scrapped_data = scrap_data('Bangalore', 'Psychiatrist', 'Doctor', 0)
#     data = {'message': scrapped_data, 'msg_type': 'display_cards'}
#     
#     scrapped_data = scrap_data('Bangalore', 'Apollo', 'Hospital', 0)
#     data = {'message': scrapped_data, 'msg_type': 'display_cards'}
#     
#     scrapped_data = scrap_data('Bangalore', 'Apollo', 'Clinic', 0)
#     data = {'message': scrapped_data, 'msg_type': 'display_cards'}
# =============================================================================
    
    return make_response(jsonify(data), 201)
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["REDIS_URL"] = "redis://localhost"
    app.register_blueprint(sse, url_prefix='/stream')