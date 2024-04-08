from concurrent.futures import ThreadPoolExecutor
import socket

ENDLINE = "\r\n"

def server_connection(con):
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
                case _:
                    con.sendall(b"HTTP/1.1 404 Not Found" + (ENDLINE * 2).encode())



def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server Started")
    while True:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for _ in range(10):
                con, addr = server_socket.accept() # wait for client
                executor.submit(server_connection, con)

if __name__ == "__main__":
    main()
