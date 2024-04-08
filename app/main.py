# Uncomment this to pass the first stage
import socket

ENDLINE = "\r\n"

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    con, addr = server_socket.accept() # wait for client
    with con:
        data = con.recv(4096)
        if data.endswith((ENDLINE * 2).encode()):
            parsed_request = data.decode("utf-8")
            parsed_request_lines = parsed_request.split(ENDLINE)
            http_method, path, http_version = parsed_request_lines[0].split(" ")
            request_headers = parsed_request_lines[1:]
            if path == "/":
                con.sendall(b"HTTP/1.1 200 OK" + (ENDLINE * 2).encode())
            elif path.startswith("/echo"):
                random_string = path.replace("/echo/", "")
                con.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + bytes(str(len(random_string)), "utf-8") + (ENDLINE * 2).encode() + random_string.encode()) 
            elif path.startswith("/user-agent"):
                for header in request_headers:
                    if header.startswith("User-Agent:"):
                        user_agent_body = header.replace("User-Agent: ", "")
                        con.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + bytes(str(len(user_agent_body)), "utf-8") + (ENDLINE * 2).encode() + user_agent_body.encode()) 
            else:
                con.sendall(b"HTTP/1.1 404 Not Found" + (ENDLINE * 2).encode())



if __name__ == "__main__":
    main()
