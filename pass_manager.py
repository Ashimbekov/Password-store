import json
import base64

def create_password_store():
    store = {}
    with open('passwords.json', 'w') as file:
        json.dump(store, file)

def load_password_store():
    try:
        with open('passwords.json', 'r') as file:
            store = json.load(file)
    except FileNotFoundError:
        create_password_store()
        store = {}
    return store

def save_password_store(store):
    with open('passwords.json', 'w') as file:
        json.dump(store, file)

def encrypt_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    encrypted_password = encoded_bytes.decode('utf-8')
    return encrypted_password

def decrypt_password(encrypted_password):
    decoded_bytes = base64.b64decode(encrypted_password.encode('utf-8'))
    decrypted_password = decoded_bytes.decode('utf-8')
    return decrypted_password

def add_password(store):
    service = input("Введите название сервиса или сайта: ")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    category = "Custom"
    subcategory = "Custom"
    
    if category not in store:
        store[category] = {}
    
    if subcategory not in store[category]:
        store[category][subcategory] = {}
    
    encrypted_password = encrypt_password(password)
    store[category][subcategory][service] = {"login": login, "password": encrypted_password}
    save_password_store(store)
    print("Пароль сохранен.")

def get_password(store, command):
    parts = command.split('/')
    if len(parts) != 2:
        print("Некорректный формат команды.")
        return
    
    service = parts[0]
    login = parts[1]
    
    for category in store:
        for subcategory in store[category]:
            for stored_service, credentials in store[category][subcategory].items():
                if stored_service.lower() == service.lower() and credentials["login"].lower() == login.lower():
                    decrypted_password = decrypt_password(credentials['password'])
                    print(f"Сервис: {stored_service}")
                    print(f"Логин: {credentials['login']}")
                    print(f"Пароль: {decrypted_password}")
                    return
    
    print("Пароль не найден.")

def delete_password(store):
    service = input("Введите название сервиса или сайта: ")

    found = False
    for category in store:
        for subcategory in store[category]:
            if service in store[category][subcategory]:
                del store[category][subcategory][service]
                found = True

                if not store[category][subcategory]:
                    del store[category][subcategory]

                if not store[category]:
                    del store[category]

    if found:
        save_password_store(store)
        print("Пароль удален.")
    else:
        print("Пароль не найден.")

def main():
    store = load_password_store()
    while True:
        command = input("Введите команду: ")

        if command.startswith("pass "):
            get_password(store, command[5:])
        elif command == "add":
            add_password(store)
        elif command == "delete":
            delete_password(store)
        elif command == "exit":
            break
        else:
            print("Некорректная команда. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
