'''Created by Akhil Samarth'''

import socket, time

# set bulb address
bulb_addr = '192.168.1.7'


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))

def boundsCheck(var, min_val, max_val):
    '''makes sure var is between min and max value (inclusive). returns var if so, otherwise returns either min/max'''
    if var < min_val:
        return min_val
    elif var > max_val:
        return max_val
    return var

def setColor(r, g, b, w=0, c=0):
    '''sets the color of the bulb using rgb + (w)arm white + (c)ool white'''
    r = boundsCheck(r, 0, 255)
    g = boundsCheck(g, 0, 255)
    b = boundsCheck(b, 0, 255)
    w = boundsCheck(w, 0, 255)
    c = boundsCheck(c, 0, 255)
    
    payload='{"method":"setPilot","env":"pro","params":{"mac":"a8bb50d05544","rssi":-73,"src":"","state":true,"dimming":100,'
    payload += f'"r":{r},"g":{g},"b":{b},"c":{c},"w":{w}'
    payload += '}}'
    sock.sendto(payload.encode(), (bulb_addr, 38899))

def setTemp(temp, brightness=100):
    '''sets the temperature and brightness (good for normal use)'''
    temp = boundsCheck(temp, 2200, 6000)
    brightness = boundsCheck(brightness, 10, 100)
    
    payload='{"method":"setPilot","env":"pro","params":{"mac":"a8bb50d05544","rssi":-73,"src":"","state":true,'
    payload += f'"temp":{temp},"dimming":{brightness}'
    payload += '}}'
    sock.sendto(payload.encode(), (bulb_addr, 38899))

def changeState(state=None):
    '''toggles the bulb on (True) or off (False). None = toggle state'''
    if state is None:
        # toggle if state is none
        payload='{"method":"getPilot","params":{}}'
        sock.sendto(payload.encode(), (bulb_addr, 38899))
        data, addr = sock.recvfrom(2048)
        response = data.decode()
        state_char = response[response.index('"state":')+8:response.index('"state":')+9]
        new_state = "true" if state_char=='f' else "false"
    elif state:
        new_state = 'true'
    else:
        new_state = 'false'

    payload='{"method":"setPilot","env":"pro","params":{"mac":"a8bb50d05544","rssi":-73,"src":"",'
    payload += f'"state":{new_state}'
    payload += '}}'
    sock.sendto(payload.encode(), ('192.168.1.7', 38899))

def smoothTemp(start=4500, end=3000, duration=60):
    '''smoothly transitions between the given temps in the given duration (seconds). Default transitions between approx. daylight and warm white'''
    MAX_TRANS_PER_SEC = 4       # max number of transmissions to send per second
    TARGET_DEGS_PER_TRANS = 10  # how many degs per transmission to adjust by (provided max transmissions per second isn't exceeded)
    
    start = boundsCheck(start, 2200, 6000)
    end = boundsCheck(end, 2200, 6000)
    delta = end - start

    # figure out if target degs/transmission is possible, or if trans/sec is limiting factor
    avg_degs_per_second = delta / duration
    if avg_degs_per_second > MAX_TRANS_PER_SEC * TARGET_DEGS_PER_TRANS:
        # use MAX_TRANS transmissions/second, calculate required degs/transmission
        degs_per_trans = avg_degs_per_second / MAX_TRANS_PER_SEC
        time_interval = 1 / MAX_TRANS_PER_SEC
    else:
        # use TARGET_DEGS degrees per transmission, calculate time interval between trans
        degs_per_trans = TARGET_DEGS_PER_TRANS
        time_interval = TARGET_DEGS_PER_TRANS / avg_degs_per_second

    print(f'smoothTemp started from start: {start} to end: {end}, degs_per_trans: {degs_per_trans}, time_interval: {time_interval}')
    temp = start
    if start < end:
        while temp <= end:
            print(f'setting temp to {temp}')
            setTemp(temp)
            temp += degs_per_trans
            time.sleep(time_interval)
    else:
        while temp >= end:
            print(f'setting temp to {temp}')
            setTemp(temp)
            temp -= degs_per_trans
            time.sleep(time_interval)


if __name__ == '__main__':
    changeState(False)

    data, addr = sock.recvfrom(2048)
    print(f'Data received from {addr}:')
    print(data)
