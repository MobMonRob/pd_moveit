import cPickle
import requests
import json

# url definitions, currently only support simulation
sim_url = "http://10.211.55.4:8000/"
sim_enable = 0
base_url = "http://192.168.12.20:8000/"
mir_ip = "" # using this for anything?
REST_URI = "http://192.168.12.20:8080/v2.0.0/"
CREDENTIALS = "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="
REGISTERS_PATH = "registers"
STATUS_PATH = "status"

protocol = "json/"
if sim_enable == 1:
    register_url = sim_url+protocol+"register/"
    position_url = sim_url+protocol+"position/"
    mission_url = sim_url+protocol+"mission/"
    session_url = sim_url+protocol+"session/"
    status_url = sim_url+protocol+"status/"
    robot_url = sim_url+protocol+"robot/"
    map_url = sim_url+protocol+"map/"
    log_url = sim_url+protocol+"log/"
else:
    register_url = base_url+protocol+"register/"
    position_url = base_url+protocol+"position/"
    mission_url = base_url+protocol+"mission/"
    session_url = base_url+protocol+"session/"
    status_url = base_url+protocol+"status/"
    robot_url = base_url+protocol+"robot/"
    map_url = base_url+protocol+"map/"
    log_url = base_url+protocol+"log/"

# init and close
# 	start - all urls are set as global
# 	close - save url of robot

def start():
    # set url's as global variables
    global sim_url, base_url, mir_ip, register_url, position_url, position_ur
    global mission_url, session_url, status_url, robot_url, map_url
    if sim_enable == 0:
    	print "Connected to robot on address",base_url
    else:
        print "Simulation enabled, simulator url is used as base url",sim_url

def close():
    try:
        cPickle.dump(base_url, open("previous_ip.p", "wb"))
        print "Robot ip is saved"
    except:
        raise ValueError("Was not able to save ip of robot in close(),\ncheck your path")

# SET/GET/DELETE and PUT functions for the current version of the REST API 25/02/16
# 	Status, Robot, Mission, Session, Map, Position, Register, Log

#----------------------------------- Status ---------------------------------------#
def get_status(status_id = 'None'):
    gets_possible = ['battery','state','uptime','distance','job','map']
    if status_id == 'None':
        response = requests.get(status_url)
        return response.json()
    elif status_id in gets_possible:
        response = requests.get(status_url+str(status_id))
        return response.json()
    else:
        raise ValueError("The status: '%s' in get_status() is not valid" % status_id)
#----------------------------------- Robot ---------------------------------------#
def get_robot_state(robot_state = 'None'):
    gets_possible = ['position', 'state', 'distance_to_target', 'battery_time_left_seconds']
    if robot_state == 'None':
	response = requests.get(robot_url)
	return response.json()
    elif robot_state in gets_possible:
	response = requests.get(robot_url+str(robot_state))
	return response.json()
    else:
	raise ValueError("The robot state: '%s' in get_robot_state() is not valid" % robot_state)

# defualt state is pause!
def set_robot_state(robot_state):
    gets_possible = ["continue","pause"]
    if robot_state in gets_possible:
       data_robot_state = {"command" : robot_state}
       response = requests.post(robot_url, data = json.dumps(data_robot_state))
       if (response.json())['success'] == 'false':
	    print "robot is already in mode: ",robot_state
       else:
	    return response.json()
    else:
        raise ValueError("The robot command %s, is neither of these %d" % (gets_possible, robot_state))
#----------------------------------- Mission ---------------------------------------#
def delete_mission(mission_id):
    response = requests.delete(mission_url+"id/"+str(mission_id))
    if (response.json())['success'] == 'false':
    	raise ValueError("The mission id: %d was not found and therefore not deleted in delete_mission()" % mission_id)
    else:
        return response.json()

def clear_missions():
    response = requests.delete(mission_url)
    return response.json()

def get_mission_information(mission_info):
    get_possible = ['active', 'available', 'positions', 'queue']
    if mission_info in get_possible:
        response = requests.get(mission_url+mission_info)
        data_mission_info = response.json()
        return data_mission_info
    else:
        raise ValueError("The argument %s in get_mission_information() doesn't match either one of %s:" % (mission_info, get_possible))

def get_mission_status(mission_id = 'None'):
        #lists all missions if no mission_id = 'None'
        if mission_id == 'None':
            response = requests.get(mission_url)
            return response.json()
        else:
            # check if the mission is in our session queue
            response = requests.get(mission_url+"id/"+str(mission_id))
            if (response.json())['success'] == 'false':
		raise ValueError("The mission id: %d was not found in get_mission()" % mission_id)
            else:
                return response.json()

# setting mission payload type 1
def set_mission(type_, name):
    try:
        data_mission = {"type" : type_, "name" : name}
        response = requests.post(mission_url, data = json.dumps(data_mission))
        return response.json()
    except:
	raise ValueError("Unable to create mission with type: %d and name: %s in set_mission()" %(type_, name))

# setting mission payload type 2
def set_taxa(type_, name):
    try:
        data_taxa = {"type" : type_, "name" : name}
        response = requests.post(mission_url, data = json.dumps(data_taxa))
        return response.json()
    except:
        raise ValueError("Unable to create mission with type: %d and name: %s in set_taxa()" %(type_, name))

def set_taxa_pose(type_, x=0, y=0, orientation=0):
    try:
        data_taxa_pose = {"type" : type_, "x" : x, "y" : y, "orientation" : orientation}
        response = requests.post(mission_url, data = json.dumps(data_taxa_pose))
        return response.json()
    except:
	raise ValueError("Unable to create taxi+pose in set_taxa_pose()")
#----------------------------------- Session ---------------------------------------#
def get_session_list():
    response = requests.get(session_url)
    return response.json()

def get_session(session_id):
    response = requests.get(session_url+str(session_id))
    if (response.json())['success'] == 'false':
	raise ValueError("The session with id: %d was not found in get_session()" % session_id)
    else:
        return response.json()

#----------------------------------- Map ---------------------------------------#
def get_map_list():
    response = requests.get(map_url)
    return response.json()

def get_map(map_id):
    response = requests.get(map_url+str(map_id))
    if (response.json())['success'] == 'false':
	raise ValueError("The map with id: %d was not found in get_map()" % map_id)
    else:
	return response.json()

#----------------------------------- Position ---------------------------------------#
def delete_position(position_id):
    response = requests.delete(position_url+str(position_id))
    if (response.json())['success'] == 'false':
    	raise ValueError("The position id: %d was not found and therefore not deleted in delete_position()" % position_id)
    else:
        return response.json()

def get_position_list():
    response = requests.get(position_url)
    return response.json()

def get_position(position_id):  
    response = requests.get(position_url+str(position_id))
    if (response.json())['success'] == 'false':
        raise ValueError("I couldn't find the position with the id:%d" % position_id)
    else:
        return response.json()

def get_position_relevant():
    #get all positions and extract size
    complete_list = get_position_list()
    size_ = complete_list['size']
    current_map = get_status("map")
    map_id = current_map['map']['id']
    relevant_maps = []
    for i in range(size_):
    # for every match to our map_id we want to save it to a list 
        if complete_list['items'][i]['map_id'] == map_id:
            relevant_maps.append(complete_list['items'][i])
    return relevant_maps

def put_position(position_id, name, pos_x=0, pos_y=0, orientation=0, type_=0, map_id = 1):
    data_position = {"id" : position_id,
        "name" : name,
            "pos_x" : pos_x,
                "pos_y" : pos_y,
                    "orientation" : orientation,
                    "type" : type_,
                    "map_id" : map_id}
    try:
        response = requests.put(position_url+str(position_id), data = json.dumps(data_position))
        if (response.json())['success'] == 'false':
            #raise ValueError("position with id: %d was not found" % position_id)
            #print "position with id:", position_id
            raise ValueError('position with id %d, was not found' % position_id)
        else:
            return response.json()
    except:
        raise ValueError("was not able to update position:\nid:%d\nname:%s\ntype_:%d\nmap_id:%d" % (position_id, name, type_, map_id))
#----------------------------------- Register ---------------------------------------#
def get_register_value(register_id):
    if register_id in range(1,201):
        response = requests.get(register_url+str(register_id))
        return (response.json())['value']
    else:
	raise ValueError("The registered id number:%d does not exist.\nValid inputs for get_register_value() are [1,200]" % register_id)

def get_register_list():
    response = requests.get(register_url)
    return response.json()

def get_register_range(interval1, interval2):
    if interval1 < interval2 and interval1 in range(1,201) and interval2 in range(1,201):
        response = requests.get(register_url+str(interval1)+"/"+str(interval2)+"/")
        return response.json()
    elif interval1 > interval2:
	raise ValueError("interval 1 should be less than interval 2 in get_register_range(interval 1, interval 2)")
    else:
	raise ValueError("interval 1 = %d, interval 2 = %d. One of the intervals is not in the range [1,200] in get_register_range()" % (interval1, interval2))

def set_register(register_id, register_value):
    if register_id in range(1,201):
        data_register = {'value': register_value}
        try:
            response = requests.post(register_url+str(register_id), data = json.dumps(data_register))
            print response.json()
        except:
            raise valueError("Error in set_register")
    else:
	raise valueError("The registered id number: %d does not exist.\nValid inputs are [1,200]." % register_id)

def clear_registers():
	data_register = {'value' : 0}
	for i in range(1,201):
	    requests.post(register_url+str(i), data = json.dumps(data_register))
#----------------------------------- Log ---------------------------------------#
def get_log_list():
    response = requests.get(log_url)
    return response.json()

def get_log(log_id):
    response = requests.get(log_url+str(log_id))
    if (response.json())['success'] == 'false':
	raise ValueError("The log with id: %d was not found in get_log()" % log_id)
    else:
	return response.json()
