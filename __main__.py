import os
from flask import Flask, render_template, request, url_for, redirect, session
import requests

app = Flask(__name__, template_folder="html_templates")
app.secret_key = os.urandom(24) 



@app.route('/')
def index():
    print("In index")
    session['agents_list'] = ['Jimmy', 'Ravi', 'Steve', 'Ajay']
    session['providers_list'] = ['provider1', 'provider2', 'provider3']
    session['instances_list'] = ['instance1', 'instance2', 'instance3']

    call_rejected = session.pop('call_rejected', False) 
    is_agent_repsonded = session.pop('is_agent_repsonded', True)
    agent_name = session.get('agent_name', "")     
    return render_template('agent-simulation.html',agents = session['agents_list'], providers = session['providers_list'], instances = session['instances_list'], call_rejected = call_rejected, agent_name = agent_name, is_agent_repsonded = is_agent_repsonded)

@app.route('/trigger_incoming_call', methods=['POST'])
def trigger_incoming_call():
    print("In trigger incoming call")
    is_call_transfered = session.get('is_call_transfered',False)
    if(is_call_transfered):
        print("in trigger incoming call - transfer case")
        session['is_call_transfered'] = False
        agent_name = session['agent_name']
    else:
        print("in trigger incoming call - normal case")
        agent_name = request.form['agent']
        provider = request.form['provider']
        instance = request.form['instance']
        session['agent_name'] = agent_name
        session['provider'] = provider
        session['instance'] = instance
    print(session['agents_list'])
    # session['agents_list'].remove(agent_name)
    customer_name = "Customer_Name"  # Replace this with actual customer name if available
    return render_template('incoming_call.html', agent_name=agent_name, customer_name=customer_name)

@app.route('/no-response', methods=['POST'])
def no_response_from_agent():
    # message = request.form['message']
    session['is_agent_repsonded'] = False
    # session['agents_list'].append(session['agent_name'])
    # Handle the no response scenario here, for example, log it or update the UI
    return redirect(url_for('index'))

@app.route('/handle_incoming_call_actions', methods=['POST'])
def handle_incoming_call_actions():
    print("in handle incoming")

    action = request.form['call-actions']
    if action == 'accept':
        if session['agent_name'] in session['agents_list']:
            print("not in list")
            print(session['agent_name'])
            session['agents_list'].remove(session['agent_name'])
        # url = 'https://api-call-preprocessing-mapping-lokesh.us.cloud.uniphoredev.com/'
        # try:
        #     response = requests.get(url)
        #     if response.status_code == 200:
        #         print('Request to URL successful!')
        #     else:
        #         print(f'Request to URL failed with status code: {response.status_code}')
        # except requests.exceptions.RequestException as e:
        #     print(f'Request to URL failed: {e}')
        return render_template('ongoing_call.html', agent_name = session['agent_name'], agents = session['agents_list'])
    else:
        session['call_rejected'] = True
        return redirect(url_for('index'))
    
@app.route('/transfer_call', methods=['POST'])
def transfer_call_to_another_agent():
    print("inntransfer call")
    session['is_call_transfered'] = True
    if session['agent_name'] in session['agents_list']:
        session['agents_list'].remove(session['agent_name'])
    new_agent_name = request.form['agent']
    session['agents_list'].remove(new_agent_name)
    session['agent_name'] = new_agent_name
    # print(f"call transfered to {new_agent_name}")
    customer_name = "Customer_Name"
    return render_template('incoming_call.html', agent_name=new_agent_name, customer_name=customer_name)
    # return redirect(url_for('trigger_incoming_call'))
    # # return redirect(url_for('incoming_call'))
    # if request.method == 'POST':
    #     session['is_call_transfered'] = True
    #     new_agent_name = request.form['agent']
    #     session['agent_name'] = new_agent_name
    #     return redirect(url_for('incoming_call'))
    # else:
    #     # Handle other HTTP methods gracefully, if necessary
    #     return "Method Not Allowed", 405
    
@app.route('/end-call', methods=['POST'])
def end_call():
    call_duration = request.form['call_duration']
    return render_template('call_ended.html', call_duration=call_duration, agent_name = session['agent_name'])

if __name__ == '__main__':
    app.run(debug=True)