import struct
import time
import random
import uuid


# Generate 8-byte account ID
def generate_account_id():
    return uuid.uuid4().bytes[:8]


# Create a fast, compact transaction
def create_transaction(sender_id, receiver_id, amount):
    if sender_id == receiver_id:
        raise ValueError("Sender and receiver must be different")
    if not (0.01 <= amount <= 10_000.0):
        raise ValueError("Amount must be between 0.01 and 10,000")
    amount_cents = int(amount * 100)  # Convert amount to integer cents
    timestamp = int(time.time()) & 0xFFFFFFFF  # Use 4 bytes for timestamp
    return struct.pack("8s8sII", sender_id, receiver_id, amount_cents, timestamp)


# Decode transaction
def decode_transaction(transaction):
    unpacked = struct.unpack("8s8sII", transaction)
    return {
        "sender_id": unpacked[0].hex(),
        "receiver_id": unpacked[1].hex(),
        "amount": unpacked[2] / 100.0,  # Convert back to dollars
        "timestamp": unpacked[3],
    }


# Simulate transactions
def simulate_transactions(account_ids, transaction_count=10):
    transactions = []
    for _ in range(transaction_count):
        sender_id = random.choice(account_ids)
        receiver_id = random.choice(account_ids)
        while sender_id == receiver_id:
            receiver_id = random.choice(account_ids)
        amount = random.uniform(0.01, 10_000.0)
        transaction = create_transaction(sender_id, receiver_id, round(amount, 2))
        transactions.append(transaction)
    return transactions


# Main execution
if __name__ == "__main__":
    # Generate account IDs
    account_ids = [generate_account_id() for _ in range(10)]

    # Start timer
    start_time = time.time()

    # Simulate transactions
    transactions = simulate_transactions(account_ids, transaction_count=300000)

    # End timer
    end_time = time.time()

    # Print results
    print(f"Generated {len(transactions)} transactions in {end_time - start_time:.6f} seconds")
    print("Sample decoded transactions:")
    for tx in transactions[:5]:  # Show first 5 transactions
        print(decode_transaction(tx))
