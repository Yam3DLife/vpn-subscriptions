import json
import base64
import os
from datetime import datetime

# ===== ВАШИ КЛЮЧИ =====
# VIP — полный набор (скопируйте сюда ВЕСЬ Keys.txt)
VIP_KEYS = """#profile-title: HotVPN VIP 🔥
#support-url: https://t.me/Wd_Life
#profile-update-interval: 5
#announce: VIP доступ — все серверы

vless://81de8a98-9c3c-07d0-bdf4-91fba80fe7e9@cluster11.anti-vpn.ru:52006?security=tls...
(ВСЕ ваши ключи)
"""

# LITE — только часть ключей (создайте этот файл или вставьте сюда вручную)
LITE_KEYS = """#profile-title: HotVPN LITE ⚡
#support-url: https://t.me/Wd_Life
#profile-update-interval: 5
#announce: Облегчённая версия — основные серверы

vless://81de8a98-9c3c-07d0-bdf4-91fba80fe7e9@cluster11.anti-vpn.ru:52006?security=tls...
(только 5-10 лучших ключей)
"""
# =========================

def add_metadata(base_config, expire_timestamp, total_bytes, plan_name):
    """Добавляет метаданные о подписке в начало конфига"""
    user_info = f"upload=0; download=0; total={total_bytes}; expire={expire_timestamp}"
    
    final_config = (
        f"#profile-title: HotVPN {plan_name}\n"
        f"#profile-update-interval: 5\n"
        f"#support-url: https://t.me/Wd_Life\n"
        f"#subscription-userinfo: {user_info}\n"
        f"#sub-expire: true\n"
        f"\n{base_config}"
    )
    return base64.b64encode(final_config.encode()).decode()

def main():
    os.makedirs('subs', exist_ok=True)
    
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    for user_id, user_info in users.items():
        if user_info.get('status') != 'active':
            if os.path.exists(f'subs/{user_id}.txt'):
                os.remove(f'subs/{user_id}.txt')
                print(f"❌ Удалён (заблокирован): {user_id}")
            continue
        
        # ===== ВЫБОР ТАРИФА =====
        plan = user_info.get('plan', 'lite')  # по умолчанию lite
        
        if plan == 'vip':
            base_keys = VIP_KEYS
            plan_name = "VIP"
        else:
            base_keys = LITE_KEYS
            plan_name = "LITE"
        # ========================
        
        # Получаем срок подписки
        expire_date_str = user_info.get('expire_date')
        if expire_date_str:
            expire_timestamp = int(datetime.strptime(expire_date_str, "%Y-%m-%d").timestamp())
        else:
            expire_timestamp = 0
        
        # Получаем лимит трафика
        traffic_limit_gb = user_info.get('traffic_limit_gb', 50)
        total_bytes = traffic_limit_gb * 1073741824
        
        # Генерируем подписку
        final = add_metadata(base_keys, expire_timestamp, total_bytes, plan_name)
        
        with open(f'subs/{user_id}.txt', 'w', encoding='utf-8') as f:
            f.write(final)
        
        print(f"✅ {user_id}: {plan_name}, срок: {expire_date_str}, лимит: {traffic_limit_gb} GB")

if __name__ == "__main__":
    main()
