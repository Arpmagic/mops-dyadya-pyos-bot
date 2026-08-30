#!/bin/bash
# ====================================================================
# Скрипт автоматичного розгортання Telegram-бота «Щурман» на Oracle Cloud VM
# ====================================================================

set -e

echo "🚀 Початок встановлення та запуску бота «Щурман» 24/7..."

# 1. Оновлення пакетів та встановлення Docker, якщо його немає
if ! command -v docker &> /dev/null; then
    echo "📦 Встановлення Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker успішно встановлено!"
fi

# 2. Перевірка docker compose
if ! docker compose version &> /dev/null; then
    echo "📦 Встановлення Docker Compose..."
    sudo apt-get update && sudo apt-get install -y docker-compose-plugin || sudo yum install -y docker-compose-plugin
fi

# 3. Перевірка наявності .env файлу
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "⚠️ Файл .env не знайдено, копіюю з .env.example..."
        cp .env.example .env
        echo "❗ Будь ласка, перевірте та відредагуйте .env файл за допомогою: nano .env"
    else
        echo "❌ Помилка: файл .env відсутній!"
        exit 1
    fi
fi

# 4. Створення папки для даних
mkdir -p data

# 5. Збірка та запуск контейнера у фоні (24/7)
echo "🔨 Збірка та запуск контейнера..."
sudo docker compose down 2>/dev/null || true
sudo docker compose up -d --build

echo "======================================================"
echo "🎉 БОТ «ЩУРМАН» УСПІШНО ЗАПУЩЕНИЙ ТА ПРАЦЮЄ 24/7!"
echo "======================================================"
echo "📋 Корисні команди для керування на сервері:"
echo " • Переглянути логи в реальному часі: sudo docker compose logs -f"
echo " • Зупинити бота:                     sudo docker compose down"
echo " • Перезапустити бота:                sudo docker compose restart"
echo " • Оновити після змін:                sudo docker compose up -d --build"
echo "======================================================"
