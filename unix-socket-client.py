import asyncio

# TCP server configuration
TCP_HOST = "127.0.0.1"
TCP_PORT = 8888


# TCP client to send and receive data
async def tcp_client():
    reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT)

    try:
        # Send a message to the TCP server
        message = "Hello from TCP client!"
        print(f"Sending: {message}")
        writer.write(message.encode())
        await writer.drain()

        # # Receive response from the server
        # data = await reader.read(1024)
        # print(f"Received: {data.decode()}")

    except Exception as e:
        print(f"TCP client error: {e}")
    finally:
        print("Closing TCP client connection...")
        writer.close()
        await writer.wait_closed()


# Run the TCP client
if __name__ == "__main__":
    asyncio.run(tcp_client())
