import streamlit as st
import json
import os
from openai import OpenAI
import random

# Конфигурация страницы
st.set_page_config(
    page_title="QuoteGenerator - Генератор цитат",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Стили CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f0f4f8;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .quote-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .quote-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .saved-quote {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #333333;
        border: 2px solid #e1e8ed;
    }
    .stSelectbox > div > div > select {
        background-color: #ffffff;
        color: #333333;
        border: 2px solid #e1e8ed;
    }
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #5a6fd8;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Темы для цитат
THEMES = {
    "Успех": "Придумай вдохновляющую цитату об успехе, достижении целей и преодолении трудностей. Цитата должна быть мотивирующей и энергичной.",
    "Любовь": "Создай красивую цитату о любви, отношениях и чувствах. Цитата должна быть романтичной и трогательной.",
    "Спорт": "Придумай мотивирующую цитату о спорте, дисциплине и командной работе. Цитата должна быть энергичной и решительной.",
    "Бизнес": "Создай деловую цитату о бизнесе, лидерстве и инновациях. Цитата должна быть профессиональной и вдохновляющей.",
    "Мудрость": "Придумай глубокую цитату о мудрости, жизненном опыте и самопознании. Цитата должна быть философской и заставляющей задуматься."
}

# Вымышленные авторы
FICTIONAL_AUTHORS = [
    "Александр Ветров", "Мария Светлова", "Виктор Думин", "Елена Радуга",
    "Игорь Мечтатель", "Ольга Мудрая", "Дмитрий Путь", "София Сердце",
    "Антон Творец", "Наталья Искра", "Павел Рассвет", "Юлия Гармония"
]

def load_quotes():
    """Загрузка сохраненных цитат"""
    try:
        if os.path.exists('quotes.json'):
            with open('quotes.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Ошибка загрузки цитат: {e}")
        return []

def save_quotes(quotes):
    """Сохранение цитат в файл"""
    try:
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения цитат: {e}")
        return False

def generate_quote(api_key, theme):
    """Генерация цитаты через DeepSeek API"""
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        prompt = f"{THEMES[theme]} Придумай короткую цитату (1-2 предложения) и вымышленное имя автора в формате: 'Цитата' - Имя Фамилия."
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты талантливый автор цитат. Создавай оригинальные и вдохновляющие цитаты на заданную тему."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Ошибка генерации: {str(e)}"

def main():
    # Заголовок
    st.markdown('<h1 style="color: #2c3e50; text-align: center;">📝 QuoteGenerator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; text-align: center;">Генератор вдохновляющих цитат</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Инициализация session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'current_quote' not in st.session_state:
        st.session_state.current_quote = ''
    if 'saved_quotes' not in st.session_state:
        st.session_state.saved_quotes = load_quotes()
    
    # Поле для API ключа
    api_key = st.text_input(
        "🔑 API ключ DeepSeek:",
        type="password",
        value=st.session_state.api_key,
        help="Введите ваш API ключ от DeepSeek для генерации цитат"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("🔐 API ключ сохранен!")
    else:
        st.warning("⚠️ Введите API ключ для генерации цитат")
        st.info("💡 Нужен API ключ? Получите его на [deepseek.com](https://platform.deepseek.com)")
    
    st.markdown("---")
    
    # Выбор темы
    st.subheader("🎨 Выберите тему")
    selected_theme = st.selectbox(
        "Тема цитаты:",
        options=list(THEMES.keys()),
        help="Выберите тему для генерации цитаты"
    )
    
    # Кнопка генерации
    if st.button("✨ Сгенерировать цитату", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Сначала введите API ключ!")
        else:
            with st.spinner("🧠 Генерирую цитату..."):
                generated_quote = generate_quote(api_key, selected_theme)
                st.session_state.current_quote = generated_quote
                st.rerun()
    
    # Отображение сгенерированной цитаты
    if st.session_state.current_quote:
        st.markdown("---")
        st.subheader("💎 Сгенерированная цитата")
        
        st.markdown(f"""
        <div class="quote-card fade-in">
            <div style="font-size: 18px; line-height: 1.6; margin-bottom: 15px;">
                {st.session_state.current_quote}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Кнопка сохранения
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Сохранить", type="secondary", use_container_width=True):
                if st.session_state.current_quote not in st.session_state.saved_quotes:
                    st.session_state.saved_quotes.append(st.session_state.current_quote)
                    save_quotes(st.session_state.saved_quotes)
                    st.success("✅ Цитата сохранена!")
                else:
                    st.warning("⚠️ Такая цитата уже есть в сохраненных")
        
        with col2:
            if st.button("🔄 Новая цитата", use_container_width=True):
                st.session_state.current_quote = ''
                st.rerun()
    
    # Отображение сохраненных цитат
    if st.session_state.saved_quotes:
        st.markdown("---")
        st.subheader("💖 Мои любимые цитаты")
        
        for i, quote in enumerate(reversed(st.session_state.saved_quotes[-10:]), 1):  # Последние 10 цитат
            st.markdown(f"""
            <div class="saved-quote fade-in">
                <div style="font-size: 14px; line-height: 1.5;">
                    {quote}
                </div>
                <div style="font-size: 12px; opacity: 0.8; margin-top: 8px;">
                    #{len(st.session_state.saved_quotes) - i + 1}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Информация
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 20px;">
        <p>QuoteGenerator v1.0 | Создавайте и коллекционируйте вдохновляющие цитаты</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
