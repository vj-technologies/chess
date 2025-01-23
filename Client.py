import socket
import tkinter as tk
from tkinter import messagebox
import json

def send_move(move):
    """Send the move to the server."""
    try:
        client_socket.sendall(move.encode())
        response = client_socket.recv(1024).decode()
        messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send move: {e}")

def on_square_click(row, col):
    """Handle the square click event."""
    square = f"{col} {row}"  # Convert to chess notation
    send_move(square)

def send_board_state():
    """Send the entire board state to the server."""
    board_state = []
    for row in range(8):
        for col in range(8):
            widget = board.grid_slaves(row=row, column=col)[0]
            if widget.winfo_children():  # If there's a piece on the square
                label = widget.winfo_children()[0]
                piece_type = label.cget("text")
                piece_color = "white" if label.cget("fg") == "white" else "black"
                board_state.append({"x": col, "y": row, "type": piece_type, "color": piece_color})
    try:
        client_socket.sendall(json.dumps({"board": board_state}).encode())
        response = client_socket.recv(1024).decode()
        messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send board state: {e}")

def create_chessboard(board_data=None):
    """Create a simple chessboard GUI with optional piece data."""
    for widget in board.winfo_children():
        widget.destroy()  # Clear previous board

    for row in range(8):
        for col in range(8):
            color = "white" if (row + col) % 2 == 0 else "black"
            frame = tk.Frame(master=board, width=60, height=60, bg=color)
            frame.grid(row=row, column=col)
            frame.bind("<Button-1>", lambda e, r=row, c=col: on_square_click(r, c))

            # Add piece if board data exists
            if board_data:
                piece = next((p for p in board_data if p["x"] == col and p["y"] == row), None)
                if piece:
                    label = tk.Label(frame, text=piece["type"].upper(), fg="white" if piece["color"] == "white" else "black")
                    label.pack()

def update_board_from_json(json_data):
    """Update the chessboard based on JSON data."""
    try:
        data = json.loads(json_data)
        board_data = data.get("board", [])
        create_chessboard(board_data)
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid JSON data: {e}")

# Networking setup
# HOST = "127.0.0.1"  # Change to your server's IP
# PORT = 65432          # Change to your server's port

# try:
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((HOST, PORT))
# except Exception as e:
#     print(f"Failed to connect to server: {e}")
#     exit(1)

# GUI setup
root = tk.Tk()
root.title("Chess Client")

board = tk.Frame(root)
board.pack()

send_board_button = tk.Button(root, text="Send Board State", command=send_board_state)
send_board_button.pack()

create_chessboard()

# Example usage: Receive JSON from server and update board
try:
    json_data = client_socket.recv(4096).decode()  # Simulating receiving JSON from server
    update_board_from_json(json_data)
except Exception as e:
    print(f"Error receiving data: {e}")

root.mainloop()

# Close the socket on exit
client_socket.close()