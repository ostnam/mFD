# mFD
import krpc
import time

# Initializing global variables
RECORDING_INIT = False
wow_list = [None, None, None]
wow_sum = None
data = []
current_iteration = 0
INIT_TIME = 0.0
DATA_FILE = "flightdata.csv"

# Connecting to the kRPC instance
try:
        conn = krpc.connect(name = "mFBW")
except:
        print("There was an error connecting kRPC.")
        exit()

vessel = conn.space_center.active_vessel

# Functions definition
def initialize_record():
    global RECORDING_INIT
    global INIT_TIME
    global last_data_time
    print("Initializing...")
    INIT_TIME = time.time()
    last_data_time = 0.0
    RECORDING_INIT = True
    print("Initialized successfully")

def wow1(x):
        # This function updates the wow1 value
        # the x is necessary for functions that are called back by krpc streams
	global wow_list
	wow_list[0] = krpc.stream.Stream.__call__(wow_stream1)


def wow2(x):
        # This function updates the wow2 value
	global wow_list
	wow_list[1] = krpc.stream.Stream.__call__(wow_stream2)


def wow3(x):
        # This function updates the wow3 value
	global wow_list
	wow_list[2] = krpc.stream.Stream.__call__(wow_stream3)


def wow_summation(x):
        # This function updates the wow_sum variable
        global wow_list
        global wow_sum
        sum = 0
        for i in wow_list:
                if i == True:
                        sum = sum + 1
        if sum >=2:
                wow_sum = True
        else:
                wow_sum = False

eas_stream = conn.add_stream(getattr, vessel.flight(), "equivalent_air_speed")
alpha_stream = conn.add_stream(getattr, vessel.flight(), "angle_of_attack")
radaralt_stream = conn.add_stream(getattr, vessel.flight(), "surface_altitude")
verticalspeed_stream = conn.add_stream(getattr, vessel.flight(), "vertical_speed")
thrust_stream = conn.add_stream(getattr, vessel.control, "throttle")
pitch_command_stream = conn.add_stream(getattr, vessel.control, "pitch")

wheels = [i for i in vessel.parts.wheels]
for i in range(0, 3):
        # This loop creates the streams responsible for the wow and deployed data for each wheel
        current_wheel = wheels[i]
        if i == 0:
                wow_stream1 = conn.add_stream(getattr, current_wheel, "grounded")
                lg_pos_stream1 = conn.add_stream(getattr, current_wheel, "deployed")
        elif i == 1:
                wow_stream2 = conn.add_stream(getattr, current_wheel, "grounded")
                lg_pos_stream2 = conn.add_stream(getattr, current_wheel, "deployed")
        elif i == 2:
                wow_stream3 = conn.add_stream(getattr, current_wheel, "grounded")
                lg_pos_stream3 = conn.add_stream(getattr, current_wheel, "deployed")

wow_stream1.add_callback(wow1)
wow_stream1.add_callback(wow_summation)
wow_stream2.add_callback(wow2)
wow_stream2.add_callback(wow_summation)
wow_stream3.add_callback(wow3)
wow_stream3.add_callback(wow_summation)

wow_stream1.start()
wow_stream2.start()
wow_stream3.start()

while wow_sum == False:
    if RECORDING_INIT != True:
        initialize_record()
    current_time = time.time() - INIT_TIME
    if current_time - last_data_time < 0.01:
        continue
    else:
        current_alpha = float(krpc.stream.Stream.__call__(alpha_stream))
        current_eas = 1.94384 * float(krpc.stream.Stream.__call__(eas_stream))
        current_radaralt = float(krpc.stream.Stream.__call__(radaralt_stream)) 
        current_verticalspeed = float(krpc.stream.Stream.__call__(verticalspeed_stream)) 
        current_thrust = float(krpc.stream.Stream.__call__(thrust_stream)) 
        current_pitch_command = float(krpc.stream.Stream.__call__(pitch_command_stream))
        current_data = [current_time, current_alpha, current_eas, current_radaralt, current_verticalspeed, current_thrust, current_pitch_command]
        data.append(current_data)
        last_data_time = current_time

f = open(DATA_FILE, "rw") # open the data file 
f.truncate(0) # deletes its content
f.write("time, alpha, eas, radaralt, verticalspeed, power, pitch \n") # first lign of the data file, labelling the content of the columns
for i in data:
        current_line = i
        current_row = 0
        for j in current_line:
                f.write(str(j))
                if current_row != 6:
                        f.write(", ")
                        current_row = current_row + 1
        f.write("\n")
