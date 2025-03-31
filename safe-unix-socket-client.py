import asyncio
import os


async def connect_to_unix_socket(socket_path, timeout=5):
    """
    Attempts to connect to a Unix socket with a timeout.
    Returns (reader, writer) if successful, otherwise (None, None).
    """
    try:
        # Check if the socket file exists
        if not os.path.exists(socket_path):
            raise FileNotFoundError(f"Socket not found at {socket_path}")

        # Attempt to connect to the Unix socket with a timeout
        reader, writer = await asyncio.wait_for(
            asyncio.open_unix_connection(socket_path), timeout=timeout
        )

        print(f"✅ Successfully connected to {socket_path}")
        return reader, writer

    except asyncio.TimeoutError:
        print(f"⏰ Error: Connection timed out after {timeout} seconds")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except ConnectionRefusedError:
        print(f"❌ Error: Connection refused by the socket at {socket_path}")
    except OSError as e:
        print(f"⚡ OS error: {e}")

    return None, None


async def send_to_unix_socket(socket_path, message):
    """
    Opens a connection and sends a message to the Unix socket.
    Checks if the connection was successful before writing.
    """
    reader, writer = await connect_to_unix_socket(socket_path)

    # Check if the connection was successful
    if writer and not writer.is_closing():
        try:
            # Send the message
            writer.write(message.encode())
            await writer.drain()
            print(f"📨 Sent message: {message}")

            # Read response (optional)
            response = await reader.read(100)
            print(f"📩 Received response: {response.decode()}")

        finally:
            # Close the connection
            writer.close()
            await writer.wait_closed()
            print("🔒 Connection closed")
    else:
        print("❌ Failed to connect, no data sent.")


# Main entry point
async def main():
    socket_path = "/tmp/asyncio_unix_socket"  # Update with your Unix socket path
    message = "Hello, Unix socket!"

    # Send a message to the socket
    await send_to_unix_socket(socket_path, message)


if __name__ == "__main__":
    asyncio.run(main())
