import argparse

from app.domain.services import UserService
from app.repos.memory import UserRepositoryInMemory
from app.core.exceptions import UserAlreadyExists

def main():
    parser = argparse.ArgumentParser(description="User registration")
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    repository = UserRepositoryInMemory()
    service = UserService(repository)
    try:
        user = service.register_user(args.email)
        repository.save(user)
        print(f"User created: {user.email}")
    except UserAlreadyExists:
        print("User already exists.")

if __name__ == "__main__":
    main()