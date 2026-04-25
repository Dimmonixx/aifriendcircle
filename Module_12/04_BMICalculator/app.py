import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Конфигурация страницы
st.set_page_config(
    page_title="BMICalculator - Калькулятор ИМТ",
    page_icon="⚖️",
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
    .bmi-result {
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .bmi-underweight {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    }
    .bmi-normal {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
    }
    .bmi-overweight {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    }
    .bmi-obese {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    }
    .recommendations {
        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2980b9;
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

def calculate_bmi(weight, height, system):
    """Расчёт ИМТ"""
    if system == "metric":
        # Метрическая система: вес в кг, рост в см
        height_m = height / 100  # переводим рост в метры
        bmi = weight / (height_m ** 2)
    else:
        # Imperial система: вес в фунтах, рост в дюймах
        bmi = (weight / (height ** 2)) * 703
    
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Определение категории ИМТ"""
    if bmi < 18.5:
        return "Недовес", "underweight", "#3498db"
    elif bmi < 25:
        return "Норма", "normal", "#27ae60"
    elif bmi < 30:
        return "Избыток веса", "overweight", "#f39c12"
    else:
        return "Ожирение", "obese", "#e74c3c"

def get_recommendations(category):
    """Получение рекомендаций"""
    recommendations = {
        "underweight": [
            "🍽️ Увеличьте калорийность питания",
            "💪 Добавьте силовые тренировки для набора мышечной массы",
            "🥛 Употребляйте больше белка",
            "😴 Обеспечьте достаточный сон (7-8 часов)"
        ],
        "normal": [
            "✅ Продолжайте поддерживать здоровый образ жизни",
            "🏃 Регулярно занимайтесь физической активностью",
            "🥗 Соблюдайте сбалансированное питание",
            "💧 Пейте достаточно воды"
        ],
        "overweight": [
            "🥗 Уменьшите калорийность питания",
            "🏃 Увеличьте физическую активность",
            "🚯 Ограничьте быстрые углеводы",
            "📊 Контролируйте порции"
        ],
        "obese": [
            "🏥 Проконсультируйтесь с врачом",
            "🎯 Поставьте реалистичные цели по снижению веса",
            "🚶 Начните с ежедневных прогулок",
            "🥦 Перейдите на дробное питание"
        ]
    }
    return recommendations.get(category, [])

def create_bmi_chart(bmi_value):
    """Создание графика шкалы ИМТ"""
    categories = [
        {"name": "Недовес", "range": [0, 18.5], "color": "#3498db"},
        {"name": "Норма", "range": [18.5, 25], "color": "#27ae60"},
        {"name": "Избыток веса", "range": [25, 30], "color": "#f39c12"},
        {"name": "Ожирение", "range": [30, 40], "color": "#e74c3c"}
    ]
    
    fig = go.Figure()
    
    # Добавляем цветные зоны
    for cat in categories:
        fig.add_shape(
            type="rect",
            x0=cat["range"][0], x1=cat["range"][1],
            y0=0, y1=1,
            fillcolor=cat["color"],
            opacity=0.3,
            layer="below",
            line_width=0,
        )
        
        # Добавляем текстовые метки
        fig.add_annotation(
            x=sum(cat["range"]) / 2,
            y=0.5,
            text=cat["name"],
            showarrow=False,
            font=dict(size=12, color="black")
        )
    
    # Добавляем линию пользователя
    fig.add_vline(
        x=bmi_value,
        line_width=3,
        line_color="red",
        annotation_text=f"Ваш ИМТ: {bmi_value}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="📊 Шкала Индекса Массы Тела",
        xaxis_title="ИМТ",
        yaxis_title="",
        yaxis=dict(showticklabels=False, range=[0, 1]),
        template="plotly_white",
        height=200,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def main():
    # Заголовок
    st.markdown('<h1 style="color: #2c3e50; text-align: center;">⚖️ BMICalculator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; text-align: center;">Калькулятор Индекса Массы Тела</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Инициализация session state
    if 'bmi_calculated' not in st.session_state:
        st.session_state.bmi_calculated = False
    if 'bmi_value' not in st.session_state:
        st.session_state.bmi_value = 0
    if 'bmi_category' not in st.session_state:
        st.session_state.bmi_category = ""
    
    # Выбор системы измерений
    st.subheader("🔧 Выберите систему измерений")
    system = st.radio(
        "Система:",
        options=["metric", "imperial"],
        format_func=lambda x: "📏 Метрическая (кг/см)" if x == "metric" else "🇺🇸 Imperial (фунты/дюймы)",
        horizontal=True
    )
    
    # Поля ввода
    st.subheader("📏 Введите ваши данные")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if system == "metric":
            weight = st.number_input(
                "Вес (кг):",
                min_value=20.0,
                max_value=300.0,
                value=70.0,
                step=0.1,
                help="Введите ваш вес в килограммах"
            )
            height = st.number_input(
                "Рост (см):",
                min_value=100.0,
                max_value=250.0,
                value=170.0,
                step=1.0,
                help="Введите ваш рост в сантиметрах"
            )
        else:
            weight = st.number_input(
                "Вес (фунты):",
                min_value=44.0,
                max_value=660.0,
                value=154.0,
                step=0.1,
                help="Введите ваш вес в фунтах"
            )
            height = st.number_input(
                "Рост (дюймы):",
                min_value=39.0,
                max_value=98.0,
                value=67.0,
                step=1.0,
                help="Введите ваш рост в дюймах"
            )
    
    # Кнопка расчёта
    if st.button("🧮 Рассчитать ИМТ", type="primary", use_container_width=True):
        if weight <= 0 or height <= 0:
            st.error("❌ Введите корректные значения веса и роста!")
        else:
            # Расчёт ИМТ
            bmi = calculate_bmi(weight, height, system)
            category, category_class, color = get_bmi_category(bmi)
            
            st.session_state.bmi_calculated = True
            st.session_state.bmi_value = bmi
            st.session_state.bmi_category = category
            st.session_state.bmi_class = category_class
            st.session_state.bmi_color = color
            st.rerun()
    
    # Отображение результатов
    if st.session_state.bmi_calculated:
        st.markdown("---")
        st.subheader("📊 Результаты")
        
        # Карточка с результатом
        st.markdown(f"""
        <div class="bmi-result bmi-{st.session_state.bmi_class} fade-in">
            <h2 style="margin: 0; font-size: 48px;">{st.session_state.bmi_value}</h2>
            <p style="margin: 10px 0; font-size: 24px;">{st.session_state.bmi_category}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # График шкалы ИМТ
        chart = create_bmi_chart(st.session_state.bmi_value)
        st.plotly_chart(chart, use_container_width=True)
        
        # Рекомендации
        st.markdown("---")
        st.subheader("💡 Рекомендации")
        
        recommendations = get_recommendations(st.session_state.bmi_class)
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="recommendations fade-in">
                {rec}
            </div>
            """, unsafe_allow_html=True)
        
        # Кнопка пересчёта
        if st.button("🔄 Пересчитать", use_container_width=True):
            st.session_state.bmi_calculated = False
            st.session_state.bmi_value = 0
            st.session_state.bmi_category = ""
            st.rerun()
    
    # Информация об ИМТ
    st.markdown("---")
    st.subheader("ℹ️ Что такое ИМТ?")
    
    st.markdown("""
    **Индекс Массы Тела (ИМТ)** — это показатель, который используется для оценки массы тела человека в соотношении с его ростом.
    
    **Формула расчёта:**
    - Метрическая система: ИМТ = вес (кг) / (рост (м))²
    - Imperial система: ИМТ = вес (фунты) / (рост (дюймы))² × 703
    
    **Категории ИМТ:**
    - **< 18.5** - Недовес
    - **18.5 - 24.9** - Норма
    - **25.0 - 29.9** - Избыток веса
    - **≥ 30.0** - Ожирение
    
    ⚠️ **Важно:** ИМТ является ориентировочным показателем и не учитывает состав тела (мышцы vs жир).
    """)
    
    # Информация
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 20px;">
        <p>BMICalculator v1.0 | Контролируйте свой вес для здоровой жизни</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
