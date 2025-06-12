from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    try:
        with open("server_public_key.pem", "rb") as f:
            server_public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
        parameters = server_public_key.parameters()
        private_key, public_key = generate_client_key_pair(parameters)
        shared_secret = derive_shared_secret(private_key, server_public_key)
        
        print("Shared Secret:", shared_secret.hex())
    
    except FileNotFoundError:
        print("Error: server_public_key.pem not found")
    except ValueError:
        print("Error: Invalid public key format")
    except Exception as e:
        print(f"Unknown error: {str(e)}")

if __name__ == "__main__":
    main()