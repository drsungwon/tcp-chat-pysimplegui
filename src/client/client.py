import PySimpleGUI as sg
import socket
import threading
from datetime import datetime

def create_gui_layout(chat_info):

    # left plane : chatting messages

    title = 'Started: ' + datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    l_1_a = sg.Output(size=(50, 20))
    l_2_t = sg.Text(title, size=(40, 1))

    grp_l = sg.Frame(' Chatting Messages ', [[l_1_a], [l_2_t]])

    # right plane : menus

    r_1_t = sg.Text('Chatting ID', size=(10, 1))
    r_1_i = sg.In(size=(20,1), key='-CHATTINGID-')
    r_2_t = sg.Text('Server', size=(10, 1))
    r_2_s = sg.Text(chat_info.server_ip + ':' + str(chat_info.server_port), size=(20, 1), relief='sunken')
    r_3_t = sg.Text('Client (Me)', size=(10, 1))
    r_3_s = sg.Text('', size=(20,1), key='-CLIENTINFO-', relief='sunken')
    r_4_t = sg.Text('Session', size=(10, 1))
    r_4_s = sg.Text('DISCONNECTED', size=(20,1), key='-CONNSTATUS-', relief='sunken')   
    r_5_l = sg.Button('CONNECT', size=(14, 1), button_color=(sg.YELLOWS[0], sg.GREENS[0]))
    r_5_r = sg.Button('DISCONNECT', size=(14, 1), button_color=(sg.YELLOWS[0], sg.GREENS[0]))

    r_6_t = sg.Text('Type & enter to send', size=(30, 1))
    r_7_m = sg.Multiline(size=(30, 4), font=('Consolas', 13), enter_submits=True, key='-QUERY-', do_not_clear=False)
    r_8_b = sg.Button('SEND', size=(31, 1), button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True)
            
    r_9_b = sg.Button('EXIT', size=(31, 1), button_color=(sg.YELLOWS[0], sg.GREENS[0]))

    f_r_1 = sg.Frame(' Service Information ',[[r_1_t, r_1_i], [r_2_t, r_2_s], [r_3_t, r_3_s], [r_4_t, r_4_s], [r_5_l, r_5_r]])
    f_r_2 = sg.Frame(' Chatting ',[[r_6_t],[r_7_m],[r_8_b]])
    f_r_3 = sg.Frame(' Service Termination ', [[r_9_b]])

    grp_r = sg.Column([[f_r_1], [f_r_2], [f_r_3]])

    # complete layout

    final_layout = [ grp_l, grp_r ]
    final_layout = [ sg.vtop( final_layout ) ]

    return final_layout

class Chatting_Service_Info:
    def __init__(self, server_ip='127.0.0.1', server_port=65456):
        self.server_ip = server_ip
        self.server_port = server_port
        self.status = False # TCP connection status: True is connected, False is disconnected 
        self.socket = ''
        self.ip = ''
        self.port = ''
        self.id = ''
        self.net_addr = ''
        self.delimeter = '|'

def encode_chat(chat_info, msg):
    message = chat_info.net_addr + chat_info.delimeter + chat_info.id + chat_info.delimeter + msg
    return bytes(message, 'utf-8')

def get_msg_net_addr(msg):
    return msg[0]

def get_msg_id(msg):
    return msg[1]

def get_msg_body(msg):
    return msg[2]

def print_info(msg):
    print('[info] ', msg)

def recv_handler(chat_info):
    while True:
        recv_msg = chat_info.socket.recv(1024).decode('utf-8').split(chat_info.delimeter)
        if get_msg_net_addr(recv_msg) != chat_info.net_addr:
            print('(' + get_msg_id(recv_msg) + ') ' + get_msg_body(recv_msg), flush=True)
        elif get_msg_body(recv_msg) == "quit":
            chat_info.socket.close()
            break

def main():
    chat_info = Chatting_Service_Info()
    window = sg.Window('TCP Chatting Program Ver.1', create_gui_layout(chat_info), font=('Consolas', 13), use_default_focus=False)

    while True: # The Event Loop
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'EXIT'): # quit if exit button or X
            if chat_info.status == False:
                break
            else:
                print_info('DISCONNECT required')

        elif event == 'CONNECT':
            if chat_info.id == '':
                id = values['-CHATTINGID-']
                if len(id) != 0:
                    chat_info.id = id
                else:
                    print_info('Chatting ID required')

            if chat_info.status == False and chat_info.id != '':
                try:
                    chat_info.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if chat_info.socket.connect((chat_info.server_ip, chat_info.server_port)) == -1:
                        print_info('connect() failed, server may be down...')
                        chat_info.socket.close()
                    else:
                        chat_info.ip, chat_info.port = chat_info.socket.getsockname()
                        chat_info.net_addr = chat_info.ip + ':' + str(chat_info.port)

                        recv_handler_thread = threading.Thread(target=recv_handler, args=(chat_info,))
                        recv_handler_thread.daemon = True
                        recv_handler_thread.start()
            
                        window['-CLIENTINFO-'].update(chat_info.net_addr)
                        window['-CONNSTATUS-'].update('CONNECTED')
                        chat_info.status = True

                        print_info('chatting started...')
                except:
                    print_info('connect() failed, server may be down...')
                    
            elif chat_info.status != False:
                print_info('already CONNECTed')

        elif event == 'DISCONNECT':
            if chat_info.status == True:
                chat_info.socket.sendall(encode_chat(chat_info, 'quit'))
                window['-CONNSTATUS-'].update('DISCONNECTED')
                chat_info.status = False
                print_info('chatting closed...')
            else:
                print_info('already DISCONNECTed')

        elif event == 'SEND':
            if chat_info.status == True:
                send_text = values['-QUERY-'].rstrip()
                chat_info.socket.sendall(encode_chat(chat_info, send_text))
                print('(*) {}'.format(send_text), flush=True)
            else:
                print_info('CONNECT required')

    window.close()

if __name__ == "__main__":
    main()
