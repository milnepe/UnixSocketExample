import asyncio
import os

# Configuration
UNIX_SOCKET_PATH = "/tmp/asyncio_unix_socket"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8888

async def connect_to_unix_socket(socket_path):
    try:
        # Attempt to connect to the Unix socket
        unix_reader, unix_writer = await asyncio.open_unix_connection(socket_path)
        # Success: Connection established
        print(f"Connected to {socket_path}")
        return unix_reader, unix_writer
    except Exception as e:
        raise Exception("Unix socket error")
        print(f"Connection error: {e}")
    except FileNotFoundError:
        print(f"Error: Socket file not found at {socket_path}")
    except ConnectionRefusedError:
        print(f"Error: Connection refused by the socket at {socket_path}")
    except OSError as e:
        print(f"OS error: {e}")
    return None, None


# Handle TCP client and forward data to UNIX socket
async def handle_tcp_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"TCP client connected: {addr}")

    try:
        # Connect to the UNIX socket
        # unix_reader, unix_writer = await asyncio.open_unix_connection(UNIX_SOCKET_PATH)
        reader, writer = await connect_to_unix_socket(UNIX_SOCKET_PATH)

        while True:
            # Read data from the TCP client
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()
            print(f"Received from TCP client: {message}")

            # Send data to the UNIX socket
            writer.write(data)
            await writer.drain()

            print(f"Written data to Unix socket: {message}")

            # # Read response from UNIX socket
            # unix_response = await unix_reader.read(1024)
            # if not unix_response:
                # break

            # # Send response back to TCP client
            # writer.write(unix_response)
            # await writer.drain()

    except Exception as e:
        print(f"Error handling TCP client: {e}")
    finally:
        print("Closing TCP client connection")
        writer.close()
        await writer.wait_closed()
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"Error closing Unix writer: {e}")


async def main():
    server = await asyncio.start_server(handle_tcp_client, TCP_HOST, TCP_PORT)
    print(f"TCP socket server started at {TCP_HOST}:{TCP_PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutting down...")
