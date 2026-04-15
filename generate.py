import json
import base64
import os
from datetime import datetime

# ⚠️ ВСТАВЬТЕ СЮДА ВАШУ ОСНОВНУЮ ССЫЛКУ (конфиг, который работает)
# Это та самая ссылка, которую вы сейчас выдаёте пользователям
BASE_CONFIG = "https://raw.githubusercontent.com/Yam3DLife/HotVPN/refs/heads/main/Keys.txt"

def generate_subscription(user_id, user_info):
    """
    Генерирует персональную подписку для пользователя.
    Здесь можно модифицировать ссылку под каждого пользователя,
    если нужно добавить уникальные параметры.
    """
    # Если статус не active — не генерируем
    if user_info.get('status') != 'active':
        return None
    
    # Проверяем срок действия
    expire_date = user_info.get('expire_date')
    if expire_date:
        expire_dt = datetime.fromisoformat(expire_date)
        if datetime.now() > expire_dt:
            return None
    
    # Базовая конфигурация (пока одинаковая для всех)
    # В будущем можно добавить user_id в конфиг для отслеживания
    config = BASE_CONFIG
    
    # Кодируем в base64 (как требует Happ)
    encoded = base64.b64encode(config.encode()).decode()
    return encoded

def main():
    # Читаем список пользователей
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # Создаём папку для подписок, если её нет
    os.makedirs('subs', exist_ok=True)
    
    generated_count = 0
    for user_id, user_info in users.items():
        subscription = generate_subscription(user_id, user_info)
        
        if subscription:
            # Сохраняем подписку в файл subs/[user_id].txt
            with open(f'subs/{user_id}.txt', 'w', encoding='utf-8') as f:
                f.write(subscription)
            print(f"✅ Сгенерировано: {user_id}")
            generated_count += 1
        else:
            # Если пользователь неактивен — удаляем его файл, если он существует
            if os.path.exists(f'subs/{user_id}.txt'):
                os.remove(f'subs/{user_id}.txt')
                print(f"❌ Удалён (неактивен): {user_id}")
    
    print(f"\n📊 Итого: {generated_count} активных подписок")

if __name__ == "__main__":
    main()
