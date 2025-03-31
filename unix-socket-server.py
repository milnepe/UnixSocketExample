import asyncio
import os

# Configuration
UNIX_SOCKET_PATH = "/tmp/asyncio_unix_socket"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8888


# Handle incoming UNIX socket client messages
async def handle_unix_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"UNIX client connected: {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()
            print(f"Received from UNIX client: {message}")

            # Send acknowledgment back to the UNIX client
            response = f"Server received: {message}"
            writer.write(response.encode())
            await writer.drain()

    except Exception as e:
        print(f"Error with UNIX client: {e}")
    finally:
        print("Closing UNIX client connection")
        writer.close()
        await writer.wait_closed()


# Start the UNIX socket server
async def start_unix_server():
    # Remove existing socket file if it exists
    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)

    # Create and start UNIX socket server
    server = await asyncio.start_unix_server(handle_unix_client, UNIX_SOCKET_PATH)
    print(f"UNIX socket server started at {UNIX_SOCKET_PATH}")

    async with server:
        await server.serve_forever()


# Run both TCP and UNIX servers concurrently
async def main():
    await asyncio.gather(start_unix_server())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutting down...")
