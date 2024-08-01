import os
from flask import Flask, render_template, request, url_for, redirect, session, Response

import logger

app = Flask(__name__, template_folder="html_templates")
app.secret_key = os.urandom(24) 

os.environ.setdefault("LOG_LEVEL", "INFO")
logger = logger.get_logger(__name__)



@app.route('/')
def index():

    session['availableAgents'] = ['Jimmy', 'Ravi', 'Steve', 'Ajay'] # to update agents list , we should use db/redis

    isAgentRejected = session.pop('isAgentRejected', False) 
    isAgentRepsonded = session.pop('isAgentRepsonded', True)
    nextAgent = session.get('nextAgent', "")

    if not isAgentRepsonded or isAgentRejected:
        session['nextAgent'] = ""

    logger.info("Rendering index page")

    return render_template('index.html', availableAgents = session['availableAgents'], isAgentRejected = isAgentRejected, nextAgent = nextAgent, isAgentRepsonded = isAgentRepsonded)




@app.route('/triggerCall', methods=['GET', 'POST'])
def triggerIncomingCall():

    nextAgent = request.form['agent']
    provider = request.form['provider']
    instance = request.form['instance']

    session['nextAgent'] = nextAgent
    session['provider'] = provider
    session['instance'] = instance


    customerName = "Test_Customer"  # Replace this with actual customer name if available
    session['customerName'] = customerName

    logger.info(f"Making call to agent {nextAgent} from the customer {customerName}.")

    return render_template('incoming_call.html', nextAgent=nextAgent, customerName=customerName)




@app.route('/noResponse', methods=['GET', 'POST'])
def noResponseFromAgent():

    session['isAgentRepsonded'] = False
    
    logger.info(f"Agent {session['nextAgent']} has not responded to call from customer {session['customerName']}.")

    return redirect(url_for('index'))




@app.route('/ongoingcall', methods=['GET', 'POST'])
def handleIncomingCallActions():
    action = request.form['call-actions']
    if action == 'accept':

        session['currentAgent'] = session['nextAgent']
        session['nextAgent'] = ""

        metadata = {
        'agent' : session['currentAgent'],
        'provider' : session['provider'],
        'instance' : session['instance']
        }

        # call the Platform Load Tester api here by passing metadata

        logger.info(f"Agent {session['currentAgent']} has accepted the call from the customer {session['customerName']}.")

        return render_template('ongoing_call.html', isConferenceCall = False, currentAgent = session['currentAgent'], availableAgents = session['availableAgents'], customerName = session['customerName'])
    
    else:

        session['isAgentRejected'] = True

        logger.info(f"Agent {session['nextAgent']} has rejected the call from the customer {session['customerName']}.")

        return redirect(url_for('index'))

   

@app.route('/toggleHoldResume', methods=['POST'])
def toggleHoldResume():

    data = request.json
    call_status = data.get('status')

    if call_status == 'HOLD':
        # pause audio streaming here

        logger.info(f"Call of agent {session['currentAgent']} with customer {session['customerName']} is on hold.")
    elif call_status == 'RESUME':
        # resume the audio stream

        logger.info(f"Call of agent {session['currentAgent']} with customer {session['customerName']} has resumed.")

    return Response(status=204)




@app.route('/endCall', methods=['GET', 'POST'])
def endCall():
    try:
        callDuration = request.form['callDuration']

        isConferenceCall = session.pop('isConferenceCall', False)

        conferenceAgents = session.pop('conferenceAgents', None)

        # call api to stop streaming the audio to audio-connector

        logger.info(f"Call of agent {session['currentAgent']} with customer {session['customerName']} has ended.")

        return render_template('call_ended.html', callDuration=callDuration, isConferenceCall = isConferenceCall, conferenceAgents = conferenceAgents, currentAgent = session['currentAgent'])
    finally:
        session.clear()





if __name__ == '__main__':
    app.run(debug=True)