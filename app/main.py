from concurrent.futures import ThreadPoolExecutor
import sys
import os
import socket

ENDLINE = "\r\n"

def server_connection(con, file_path):
    print("Recieved Connection From", con)
    with con:
        data = con.recv(4096)
        if data.endswith((ENDLINE * 2).encode()):
            parsed_request = data.decode("utf-8")
            parsed_request_lines = parsed_request.split(ENDLINE)
            http_method, path, http_version = parsed_request_lines[0].split(" ")
            request_headers = parsed_request_lines[1:]
            match path:
                case "/":
                    con.sendall(b"HTTP/1.1 200 OK" + (ENDLINE * 2).encode())
                case s if s.startswith("/echo"):
                    random_string = path.replace("/echo/", "")
                    con.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + bytes(str(len(random_string)), "utf-8") + (ENDLINE * 2).encode() + random_string.encode()) 
                case s if s.startswith("/user-agent"):
                    for header in request_headers:
                        if header.startswith("User-Agent:"):
                            user_agent_body = header.replace("User-Agent: ", "")
                            con.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + bytes(str(len(user_agent_body)), "utf-8") + (ENDLINE * 2).encode() + user_agent_body.encode()) 
                case s if s.startswith("/files"):
                    file_name = path.replace("/files/", "")
                    if os.path.exists(os.path.join(file_path, file_name)):
                        with open(os.path.join(file_path, file_name), "rb") as file:
                            contents = file.read()
                            con.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + bytes(str(len(contents)), "utf-8") + (ENDLINE * 2).encode() + contents)
                    else:
                        con.sendall(b"HTTP/1.1 404 Not Found" + (ENDLINE * 2).encode())
                case _:
                    con.sendall(b"HTTP/1.1 404 Not Found" + (ENDLINE * 2).encode())



def main():
    arguments = sys.argv
    file_path = None
    if len(arguments) >= 3:
        if arguments[1] == "--directory":
            #file_path = arguments[2]
            pass
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server Started")
    while True:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for _ in range(10):
                con, addr = server_socket.accept() # wait for client
                executor.submit(server_connection, con, file_path)

if __name__ == "__main__":
    main()
