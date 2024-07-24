import socketserver
import threading

# Create a DB (client's socket information) and flag 
group_queue = []
quit_help_flag = False

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Import a client DB & flag into Request Handler
        global group_queue
        global quit_help_flag

        # Show a client connection information
        if len(group_queue) == 0 and quit_help_flag == True:
            print('')
            quit_help_flag = False
        print('> client connected by IP address {0} with Port number {1}'.format(self.client_address[0], self.client_address[1]), flush=True)
        
        # Register a new client connection information into a client DB
        group_queue.append(self.request)

        while True:
            recv_data = self.request.recv(1024)
            recv_msg = recv_data.decode('utf-8').split('|')
            
            if recv_msg[2] == 'quit':
                print('> client {} disconnected.'.format(recv_msg[1]), flush=True)

                if len(group_queue) == 1:
                    print('> if you want, type "quit" to stop server: ', end='', flush=True)
                    quit_help_flag = True

                # Deregister a disconnected client from a client DB
                self.request.sendall(recv_data)
                group_queue.remove(self.request)
                break
            else:
                # Forward a client message to whole clients (currently a broadcast)
                print('> received (', recv_data.decode('utf-8'), ') and echoed to ', len(group_queue), 'clients', flush=True)
                for conn in group_queue:
                    conn.sendall(recv_data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 65456
    print('> TCP chatting server is activated')
    print('> type \'quit\' to stop server')

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)

        # Set to exit the server thread when the main thread terminates, then execute the main thread
        server_thread.daemon = True
        server_thread.start()
        print("> server loop running in thread (main thread):", server_thread.name)
        
        # Server termination by input "quit" when all client connections are disconnected
        base_thread_number = threading.active_count()
        while True:
            msg = input('')
            if msg == 'quit':
                if base_thread_number == threading.active_count():
                    print("> stop procedure started")
                    break
                else:
                    print("> active threads are remained :", threading.active_count() - base_thread_number, "threads")

        print('> TCP chatting server is de-activated')
        server.shutdown()
        