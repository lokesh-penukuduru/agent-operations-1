import os,json
from flask import Flask, render_template, request, url_for, redirect, session
import redis

app = Flask(__name__, template_folder="html_templates")
app.secret_key = os.urandom(24) 

# global redis_client
redis_client = redis.Redis(host='localhost', port=6379, db=0)
initailAgents = ['agent-1','agent-2','agent-3','agent-4','agent-5','agent-6','agent-7','agent-8','agent-9']
redis_client.set('availableAgents',json.dumps(initailAgents))
# edit from here, working fine

@app.route('/')
def index():
    print("In index")
    
    # session['agents_list'] = ['Jimmy', 'Ravi', 'Steve', 'Ajay']
    # global availableAgents
    
    isAgentRejected = session.pop('isAgentRejected', False) 
    isAgentRepsonded = session.pop('isAgentRepsonded', True)
    nextAgent = session.get('nextAgent', "")     
    return render_template('agent-simulation.html',availableAgents = sorted(json.loads(redis_client.get('availableAgents'))), isAgentRejected = isAgentRejected, nextAgent = nextAgent, isAgentRepsonded = isAgentRepsonded)

@app.route('/triggerIncomingCall', methods=['GET', 'POST'])
def triggerIncomingCall():
    nextAgent = request.form['agent']
    provider = request.form['provider']
    instance = request.form['instance']
    session['nextAgent'] = nextAgent
    session['provider'] = provider
    session['instance'] = instance
    # session['agents_list'].remove(agent_name)
    customerName = "Customer_Name"  # Replace this with actual customer name if available
    return render_template('incoming_call.html', nextAgent=nextAgent, customerName=customerName)

@app.route('/noResponse', methods=['GET', 'POST'])
def noResponseFromAgent():
    session['nextAgent'] = ""
    session['isAgentRepsonded'] = False
    if(session['isTransferCall']):
        return redirect(request.referrer)
    return redirect(url_for('index'))

@app.route('/handleIncomingCallActions', methods=['GET', 'POST'])
def handleIncomingCallActions():
    action = request.form['call-actions']
    if action == 'accept':
        prevAgent=session.get('currentAgent',"") ## in case of conference call, transfer call
        print("prev agent: ",prevAgent)
        print("next agent: ", session['nextAgent'])
        session['currentAgent'] = session['nextAgent']
        session['nextAgent'] = ""
        available_agents = json.loads(redis_client.get('availableAgents'))
        if session['currentAgent'] in available_agents:
            available_agents.remove(session['currentAgent'])
            redis_client.set('availableAgents', json.dumps(available_agents))
        print("available agents :", redis_client.get('availableAgents'))
        isTransferCall = session.get('isTransferCall', False)
        print("is transfer call : ", isTransferCall)
        if(isTransferCall):
            availableAgents = json.loads(redis_client.get('availableAgents'))
            availableAgents.append(prevAgent)
            redis_client.set('availableAgents', json.dumps(availableAgents))                        
            session['isTransferCall'] = False
        isConferenceCall = session.get('isConferenceCall', False) 
        if(isConferenceCall):
            print("yeahj, confere")
            try:
                if(session['currentAgent'] not in session['conferenceAgents']):
                    session['conferenceAgents'].append(session['currentAgent'])
                if(prevAgent != "" and prevAgent not in session['conferenceAgents']):
                    session['conferenceAgents'].append(prevAgent)
            except Exception:
                session['conferenceAgents'] = []
                session['conferenceAgents'].append(session['currentAgent'])
                if(prevAgent != ""):
                    session['conferenceAgents'].append(prevAgent)
            return render_template('ongoing_call.html', isConferenceCall = True, conferenceAgents = session['conferenceAgents'], availableAgents = json.loads(redis_client.get('availableAgents')))
        availableAgents = json.loads(redis_client.get('availableAgents'))
        print("available agents", availableAgents)
        print(session.get('conferenceAgents'," uu"))
        print(session['currentAgent'])
        return render_template('ongoing_call.html', isConferenceCall = False, currentAgent = session['currentAgent'], availableAgents = json.loads(redis_client.get('availableAgents')))
    else:
        if(session['isTransferCall']):
            return redirect(request.referrer)
        session['isAgentRejected'] = True
        return redirect(url_for('index'))
    
@app.route('/transferCall', methods=['GET', 'POST'])
def transferCallToAnotherAgent():
    session['isTransferCall'] = True
    session['nextAgent'] = request.form['agent']
    print("in transfer next agent: ", session['nextAgent'])
    customer_name = "Customer_Name"
    return render_template('incoming_call.html', isTransferCall=session['isTransferCall'], currentAgent=session['currentAgent'], nextAgent=session['nextAgent'], customerName=customer_name)


@app.route('/conferenceCall', methods=['GET', 'POST'])
def addAnotherAgentToCall():
    print("in conference")
    print("curr ahe: ", session['currentAgent'])
    session['isConferenceCall'] = True
    session['nextAgent'] = request.form['agent']
    print("in conference nextagent ", session['nextAgent'])
    customer_name = "Customer_Name"
    return render_template('incoming_call.html', isConferenceCall=session['isConferenceCall'], currentAgent=session['currentAgent'], nextAgent=session['nextAgent'], customerName=customer_name)

@app.route('/endCall', methods=['GET', 'POST'])
def endCall():
    try:
        callDuration = request.form['callDuration']
        return render_template('call_ended.html', callDuration=callDuration, isConferenceCall = session['isConferenceCall'], conferenceAgents = session['conferenceAgents'], currentAgent = session['currentAgent'])
    finally:
        if (session['isConferenceCall']):
            availableAgents = json.loads(redis_client.get('availableAgents'))
            availableAgents += session['conferenceAgents']
            redis_client.set('availableAgents', json.dumps(availableAgents))
        else:
            availableAgents = json.loads(redis_client.get('availableAgents'))
            availableAgents.append(session['currentAgent'])
            redis_client.set('availableAgents', json.dumps(availableAgents))
        session.clear()
        


if __name__ == '__main__':
    app.run(debug=True)