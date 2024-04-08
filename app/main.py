# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    con, addr = server_socket.accept() # wait for client
    with con:
        data = con.recv(4096)
        if data.endswith(b"\r\n\r\n"):
            parsed_request = data.decode("utf-8")
            parsed_request_lines = parsed_request.split("\r\n")
            http_method, path, http_version = parsed_request_lines[0].split(" ")
            print(http_method, path, http_version)
            if path == "/":
                con.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                con.sendall(b"HTTP/1.1 404 Not Found")
        print(data, data.endswith(b"\r\n\r\n"))



if __name__ == "__main__":
    main()
