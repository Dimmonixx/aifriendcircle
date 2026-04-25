import streamlit as st
import requests
import json
from datetime import datetime, timezone
import time

# Конфигурация страницы
st.set_page_config(
    page_title="CurrencyConverter - Конвертер валют",
    page_icon="💱",
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
    .conversion-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .conversion-result:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .history-item {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .rate-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        text-align: center;
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

# Валюты и их флаги
CURRENCIES = {
    "USD": {"name": "Доллар США", "flag": "🇺🇸"},
    "EUR": {"name": "Евро", "flag": "🇪🇺"},
    "UAH": {"name": "Украинская гривна", "flag": "🇺🇦"},
    "RUB": {"name": "Российский рубль", "flag": "🇷🇺"},
    "GBP": {"name": "Британский фунт", "flag": "🇬🇧"},
    "JPY": {"name": "Японская йена", "flag": "🇯🇵"},
    "CNY": {"name": "Китайский юань", "flag": "🇨🇳"}
}

def get_exchange_rates():
    """Получение курсов валют из API"""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data["rates"], data["date"]
        else:
            return None, None
    except Exception as e:
        st.error(f"Ошибка получения курсов валют: {e}")
        return None, None

def convert_currency(amount, from_currency, to_currency, rates):
    """Конвертация валюты"""
    if from_currency == "USD":
        usd_amount = amount
    else:
        usd_amount = amount / rates[from_currency]
    
    if to_currency == "USD":
        return usd_amount
    else:
        return usd_amount * rates[to_currency]

def save_conversion_history(from_currency, to_currency, amount, result, rate):
    """Сохранение истории конвертаций"""
    if 'conversion_history' not in st.session_state:
        st.session_state.conversion_history = []
    
    conversion = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": result,
        "rate": rate,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    st.session_state.conversion_history.append(conversion)
    
    # Сохраняем только последние 5 конвертаций
    if len(st.session_state.conversion_history) > 5:
        st.session_state.conversion_history = st.session_state.conversion_history[-5:]

def main():
    # Заголовок
    st.markdown('<h1 style="color: #2c3e50; text-align: center;">💱 CurrencyConverter</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; text-align: center;">Конвертер валют в реальном времени</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Инициализация session state
    if 'rates' not in st.session_state:
        st.session_state.rates = None
    if 'rates_date' not in st.session_state:
        st.session_state.rates_date = None
    if 'conversion_history' not in st.session_state:
        st.session_state.conversion_history = []
    
    # Получение курсов валют
    if st.session_state.rates is None:
        with st.spinner("🔄 Загрузка курсов валют..."):
            rates, rates_date = get_exchange_rates()
            if rates:
                st.session_state.rates = rates
                st.session_state.rates_date = rates_date
                st.success("✅ Курсы валют успешно загружены!")
            else:
                st.error("❌ Не удалось загрузить курсы валют")
                st.stop()
    
    # Информация о курсах
    if st.session_state.rates_date:
        st.markdown(f"""
        <div class="rate-info fade-in">
            📊 Курсы валют от {st.session_state.rates_date}
        </div>
        """, unsafe_allow_html=True)
    
    # Основная форма конвертации
    st.subheader("💰 Конвертер валют")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Валюта ИЗ
        from_currency = st.selectbox(
            "Из валюты:",
            options=list(CURRENCIES.keys()),
            format_func=lambda x: f"{CURRENCIES[x]['flag']} {CURRENCIES[x]['name']}",
            key="from_currency"
        )
        
        amount = st.number_input(
            "Сумма:",
            min_value=0.0,
            value=100.0,
            step=0.01,
            help="Введите сумму для конвертации"
        )
    
    with col2:
        # Валюта В
        to_currency = st.selectbox(
            "В валюту:",
            options=list(CURRENCIES.keys()),
            format_func=lambda x: f"{CURRENCIES[x]['flag']} {CURRENCIES[x]['name']}",
            index=1,
            key="to_currency"
        )
        
        # Кнопка конвертации
        if st.button("🔄 Конвертировать", type="primary", use_container_width=True):
            if amount <= 0:
                st.error("❌ Введите сумму больше 0")
            elif from_currency == to_currency:
                st.error("❌ Выберите разные валюты")
            else:
                # Конвертация
                result = convert_currency(amount, from_currency, to_currency, st.session_state.rates)
                
                # Расчёт курса
                if from_currency == "USD":
                    rate = st.session_state.rates[to_currency]
                elif to_currency == "USD":
                    rate = 1 / st.session_state.rates[from_currency]
                else:
                    rate = st.session_state.rates[to_currency] / st.session_state.rates[from_currency]
                
                # Сохранение в историю
                save_conversion_history(from_currency, to_currency, amount, result, rate)
                
                # Отображение результата
                st.session_state.last_conversion = {
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount,
                    "result": result,
                    "rate": rate
                }
                
                st.rerun()
    
    with col3:
        # Информация о курсе
        if st.session_state.rates:
            st.subheader("📈 Текущие курсы")
            
            # Показываем несколько популярных курсов
            popular_rates = ["EUR", "RUB", "UAH", "GBP"]
            
            for currency in popular_rates:
                if currency != "USD" and currency in st.session_state.rates:
                    rate = st.session_state.rates[currency]
                    st.markdown(f"""
                    <div style="text-align: center; margin: 5px 0;">
                        <strong>{CURRENCIES[currency]['flag']} 1 USD = {rate:.4f} {currency}</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Отображение результата конвертации
    if 'last_conversion' in st.session_state:
        conv = st.session_state.last_conversion
        
        st.markdown("---")
        st.subheader("💎 Результат конвертации")
        
        st.markdown(f"""
        <div class="conversion-result fade-in">
            <div style="font-size: 24px; margin-bottom: 10px;">
                {CURRENCIES[conv['from']]['flag']} {conv['amount']:.2f} {conv['from']} 
                → 
                {CURRENCIES[conv['to']]['flag']} {conv['result']:.2f} {conv['to']}
            </div>
            <div style="font-size: 16px; opacity: 0.9;">
                Курс: 1 {conv['from']} = {conv['rate']:.4f} {conv['to']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # История конвертаций
    if st.session_state.conversion_history:
        st.markdown("---")
        st.subheader("📚 История конвертаций")
        
        for i, conv in enumerate(reversed(st.session_state.conversion_history), 1):
            st.markdown(f"""
            <div class="history-item fade-in">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 16px; font-weight: bold;">
                            {CURRENCIES[conv['from']]['flag']} {conv['amount']:.2f} {conv['from']} 
                            → 
                            {CURRENCIES[conv['to']]['flag']} {conv['result']:.2f} {conv['to']}
                        </div>
                        <div style="font-size: 12px; opacity: 0.8;">
                            Курс: 1 {conv['from']} = {conv['rate']:.4f} {conv['to']}
                        </div>
                    </div>
                    <div style="font-size: 11px; opacity: 0.7;">
                        {conv['timestamp']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Кнопка обновления курсов
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔄 Обновить курсы", use_container_width=True):
            st.session_state.rates = None
            st.rerun()
    
    with col2:
        if st.button("🗑️ Очистить историю", use_container_width=True):
            st.session_state.conversion_history = []
            if 'last_conversion' in st.session_state:
                del st.session_state.last_conversion
            st.rerun()
    
    # Информация
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 20px;">
        <p>CurrencyConverter v1.0 | Конвертируйте валюты по актуальным курсам</p>
        <p style="font-size: 12px;">Данные предоставлены API exchangerate-api.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
