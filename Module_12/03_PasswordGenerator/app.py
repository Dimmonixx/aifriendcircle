import streamlit as st
import random
import string

# Конфигурация страницы
st.set_page_config(
    page_title="PasswordGenerator - Генератор паролей",
    page_icon="🔐",
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
    .password-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        word-break: break-all;
    }
    .strength-weak {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .strength-medium {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .strength-strong {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .stSlider > div > div > div {
        background-color: #667eea;
    }
    .stCheckbox > div > div > label > div {
        background-color: #667eea;
    }
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #5a6fd8;
        transform: translateY(-1px);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# Наборы символов
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    """Генерация пароля с указанными параметрами"""
    char_pool = ""
    
    if use_uppercase:
        char_pool += UPPERCASE
    if use_lowercase:
        char_pool += LOWERCASE
    if use_digits:
        char_pool += DIGITS
    if use_symbols:
        char_pool += SYMBOLS
    
    if not char_pool:
        return "Ошибка: выберите хотя бы один тип символов"
    
    # Генерация пароля
    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password

def calculate_strength(password, length, use_uppercase, use_lowercase, use_digits, use_symbols):
    """Расчёт надёжности пароля"""
    score = 0
    
    # Длина пароля
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    
    # Разнообразие символов
    if use_uppercase:
        score += 1
    if use_lowercase:
        score += 1
    if use_digits:
        score += 1
    if use_symbols:
        score += 1
    
    # Определение уровня надёжности
    if score <= 3:
        return "Слабый", "weak"
    elif score <= 5:
        return "Средний", "medium"
    else:
        return "Сильный", "strong"

def copy_to_clipboard(text):
    """Копирование текста в буфер обмена через JavaScript"""
    st.markdown(f"""
    <script>
    navigator.clipboard.writeText("{text}").then(function() {{
        console.log('Текст скопирован в буфер обмена');
    }}, function(err) {{
        console.error('Ошибка копирования: ', err);
    }});
    </script>
    """, unsafe_allow_html=True)
    return True

def main():
    # Заголовок
    st.markdown('<h1 style="color: #2c3e50; text-align: center;">🔐 PasswordGenerator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; text-align: center;">Создайте надёжный пароль для защиты данных</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Инициализация session state
    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = ""
    if 'password_generated' not in st.session_state:
        st.session_state.password_generated = False
    
    # Настройки пароля
    st.subheader("⚙️ Настройки пароля")
    
    # Длина пароля
    password_length = st.slider(
        "Длина пароля:",
        min_value=8,
        max_value=32,
        value=16,
        step=1,
        help="Рекомендуемая длина: 12-16 символов"
    )
    
    # Типы символов
    col1, col2 = st.columns(2)
    
    with col1:
        use_uppercase = st.checkbox("🔠 Заглавные буквы (A-Z)", value=True)
        use_lowercase = st.checkbox("🔡 Строчные буквы (a-z)", value=True)
    
    with col2:
        use_digits = st.checkbox("🔢 Цифры (0-9)", value=True)
        use_symbols = st.checkbox("🔣 Симвols (!@#$%)", value=True)
    
    # Кнопка генерации
    if st.button("🎲 Сгенерировать пароль", type="primary", use_container_width=True):
        # Проверка выбранных опций
        if not any([use_uppercase, use_lowercase, use_digits, use_symbols]):
            st.error("❌ Выберите хотя бы один тип символов!")
        else:
            # Генерация пароля
            password = generate_password(
                password_length,
                use_uppercase,
                use_lowercase,
                use_digits,
                use_symbols
            )
            
            st.session_state.generated_password = password
            st.session_state.password_generated = True
            st.rerun()
    
    # Отображение сгенерированного пароля
    if st.session_state.password_generated and st.session_state.generated_password:
        st.markdown("---")
        st.subheader("🔑 Ваш пароль")
        
        # Расчёт надёжности
        strength_text, strength_class = calculate_strength(
            st.session_state.generated_password,
            password_length,
            use_uppercase,
            use_lowercase,
            use_digits,
            use_symbols
        )
        
        # Индикатор надёжности
        if strength_class == "weak":
            st.markdown(f'<div class="strength-weak fade-in">⚠️ {strength_text}</div>', unsafe_allow_html=True)
        elif strength_class == "medium":
            st.markdown(f'<div class="strength-medium fade-in">🔒 {strength_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="strength-strong fade-in">🛡️ {strength_text}</div>', unsafe_allow_html=True)
        
        # Отображение пароля
        st.markdown(f"""
        <div class="password-display fade-in">
            {st.session_state.generated_password}
        </div>
        """, unsafe_allow_html=True)
        
        # Кнопки действий
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📋 Скопировать", use_container_width=True):
                if copy_to_clipboard(st.session_state.generated_password):
                    st.success("✅ Пароль скопирован в буфер обмена!")
                else:
                    st.warning("⚠️ Не удалось скопировать пароль")
        
        with col2:
            if st.button("🔄 Новый пароль", use_container_width=True):
                # Генерация нового пароля с теми же настройками
                new_password = generate_password(
                    password_length,
                    use_uppercase,
                    use_lowercase,
                    use_digits,
                    use_symbols
                )
                st.session_state.generated_password = new_password
                st.rerun()
        
        with col3:
            if st.button("🗑️ Очистить", use_container_width=True):
                st.session_state.generated_password = ""
                st.session_state.password_generated = False
                st.rerun()
    
    # Советы по безопасности
    st.markdown("---")
    st.subheader("💡 Советы по безопасности")
    
    tips = [
        "🔒 Используйте уникальные пароли для каждого аккаунта",
        "📝 Не используйте личную информацию (имя, дата рождения)",
        "🔄 Регулярно меняйте пароли (каждые 3-6 месяцев)",
        "🔐 Используйте менеджер паролей для хранения",
        "⚠️ Не делитесь паролями с другими людьми"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")
    
    # Информация
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 20px;">
        <p>PasswordGenerator v1.0 | Создавайте надёжные пароли для защиты данных</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
