import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Конфигурация страницы с тёмной темой
st.set_page_config(
    page_title="MoodTracker - Трекер настроения",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Применение светлой темы через CSS
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
    .mood-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .mood-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #5a6fd8;
    }
</style>
""", unsafe_allow_html=True)

# Настройки настроений
MOODS = {
    "😊 Отлично": 5,
    "🙂 Хорошо": 4,
    "😐 Нормально": 3,
    "🙁 Плохо": 2,
    "😢 Ужасно": 1
}

def load_moods():
    """Загрузка данных о настроениях из JSON файла"""
    try:
        if os.path.exists('data/moods.json'):
            with open('data/moods.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        return []

def save_moods(moods):
    """Сохранение данных о настроениях в JSON файл"""
    try:
        # Проверяем существование папки data
        if not os.path.exists('data'):
            os.makedirs('data')
        
        with open('data/moods.json', 'w', encoding='utf-8') as f:
            json.dump(moods, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения данных: {e}")
        return False

def get_today_mood():
    """Получение записи за сегодня"""
    today = date.today().strftime("%Y-%m-%d")
    moods = load_moods()
    for mood in moods:
        if mood['date'] == today:
            return mood
    return None

def get_last_7_days():
    """Получение записей за последние 7 дней"""
    moods = load_moods()
    today = date.today()
    last_7_days = []
    
    for i in range(7):
        check_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for mood in moods:
            if mood['date'] == check_date:
                last_7_days.append(mood)
                break
    
    return last_7_days[::-1]  # В обратном порядке (от старого к новому)

def export_to_csv():
    """Экспорт данных в CSV"""
    try:
        moods = load_moods()
        if not moods:
            st.warning("Нет данных для экспорта")
            return
        
        df = pd.DataFrame(moods)
        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Скачать CSV",
            data=csv,
            file_name=f"mood_tracker_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Ошибка экспорта: {e}")

def create_mood_chart():
    """Создание графика изменения настроения"""
    moods = get_last_7_days()
    if not moods:
        return None
    
    dates = [mood['date'] for mood in moods]
    values = [MOODS.get(mood['mood'], 3) for mood in moods]
    mood_labels = [mood['mood'].split()[1] for mood in moods]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        text=mood_labels,
        textposition='top center',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#667eea')
    ))
    
    fig.update_layout(
        title="📈 Изменение настроения за неделю",
        xaxis_title="Дата",
        yaxis_title="Настроение",
        yaxis=dict(tickmode='array', tickvals=[1,2,3,4,5], ticktext=['Ужасно','Плохо','Нормально','Хорошо','Отлично']),
        template='plotly_dark',
        height=400
    )
    
    return fig

def create_pie_chart():
    """Создание круговой диаграммы распределения настроений"""
    moods = load_moods()
    if not moods:
        return None
    
    mood_counts = {}
    for mood in moods:
        mood_name = mood['mood'].split()[1]  # Берем только текст без эмодзи
        mood_counts[mood_name] = mood_counts.get(mood_name, 0) + 1
    
    if not mood_counts:
        return None
    
    fig = px.pie(
        values=list(mood_counts.values()),
        names=list(mood_counts.keys()),
        title="🎯 Распределение настроений",
        color_discrete_map={
            'Отлично': '#4CAF50',
            'Хорошо': '#2196F3',
            'Нормально': '#FF9800',
            'Плохо': '#FF5722',
            'Ужасно': '#9C27B0'
        },
        template='plotly_dark'
    )
    
    return fig

def main():
    # Заголовок
    st.markdown('<h1 style="color: white; text-align: center;">😊 MoodTracker</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ccc; text-align: center;">Отслеживай своё настроение каждый день</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Проверка на запись за сегодня
    today_mood = get_today_mood()
    
    if today_mood:
        st.warning(f"⚠️ Сегодня ({today_mood['date']}) уже есть запись!")
        st.info(f"Текущее настроение: {today_mood['mood']}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✏️ Редактировать", type="primary"):
                st.session_state.edit_mode = True
        with col2:
            if st.button("➡️ Пропустить", type="secondary"):
                st.session_state.edit_mode = False
        
        if st.session_state.get('edit_mode', False):
            # Режим редактирования
            st.subheader("✏️ Редактирование настроения")
            
            new_mood = st.selectbox(
                "Новое настроение:",
                options=list(MOODS.keys()),
                index=list(MOODS.keys()).index(today_mood['mood'])
            )
            
            new_note = st.text_area(
                "Новая заметка:",
                value=today_mood['note'],
                height=100
            )
            
            if st.button("💾 Сохранить изменения", type="primary"):
                moods = load_moods()
                for i, mood in enumerate(moods):
                    if mood['date'] == today_mood['date']:
                        moods[i] = {
                            'date': today_mood['date'],
                            'mood': new_mood,
                            'note': new_note
                        }
                        break
                
                if save_moods(moods):
                    st.success("✅ Запись обновлена!")
                    st.session_state.edit_mode = False
                    st.rerun()
                else:
                    st.error("❌ Ошибка при сохранении")
        
        st.markdown("---")
    
    elif not st.session_state.get('edit_mode', False):
        # Основная форма ввода
        st.subheader("📝 Как ты себя чувствуешь сегодня?")
        
        selected_mood = st.selectbox(
            "Выберите настроение:",
            options=list(MOODS.keys()),
            help="Выберите наиболее подходящее настроение"
        )
        
        note = st.text_area(
            "Заметка на день:",
            placeholder="Расскажи, что произошло сегодня...",
            height=100
        )
        
        if st.button("💾 Сохранить настроение", type="primary", use_container_width=True):
            if selected_mood and note.strip():
                new_entry = {
                    'date': date.today().strftime("%Y-%m-%d"),
                    'mood': selected_mood,
                    'note': note.strip()
                }
                
                moods = load_moods()
                moods.append(new_entry)
                
                if save_moods(moods):
                    st.success("✅ Настроение сохранено!")
                    st.balloons()  # Анимация при сохранении
                    st.rerun()
                else:
                    st.error("❌ Ошибка при сохранении")
            else:
                st.warning("⚠️ Заполните все поля")
        
        st.markdown("---")
    
    # История настроений
    st.subheader("📚 История настроений")
    last_7_days = get_last_7_days()
    
    if last_7_days:
        for mood in last_7_days:
            # Обрезаем заметку до 50 символов
            note_preview = mood['note'][:50] + "..." if len(mood['note']) > 50 else mood['note']
            
            st.markdown(f"""
            <div class="mood-card fade-in">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; font-size: 18px;">{mood['mood']}</h4>
                        <p style="margin: 5px 0; opacity: 0.9;">📅 {mood['date']}</p>
                        <p style="margin: 0; opacity: 0.8;">{note_preview}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 Пока нет записей. Начни отслеживать настроение сегодня!")
    
    st.markdown("---")
    
    # Статистика
    st.subheader("📊 Статистика")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        mood_chart = create_mood_chart()
        if mood_chart:
            st.plotly_chart(mood_chart, use_container_width=True)
        else:
            st.info("📈 Недостаточно данных для графика")
    
    with col2:
        pie_chart = create_pie_chart()
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
        else:
            st.info("🎯 Недостаточно данных для диаграммы")
    
    st.markdown("---")
    
    # Экспорт данных
    st.subheader("💾 Экспорт данных")
    export_to_csv()
    
    # Информация
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 20px;">
        <p>MoodTracker v1.0 | Отслеживай своё настроение для лучшего самопознания</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
