import streamlit as st
from openai import OpenAI
import random
import time

# AI Friends personalities
AI_FRIENDS = {
    "Макс": {
        "age": 25,
        "profession": "стартапер",
        "personality": "энергичный и рискованный",
        "avatar": "🚀",
        "color": "#FF6B6B",
        "system_prompt": "Ты Макс, 25-летний стартапер. Ты энергичный, всегда ищешь новые возможности, любишь рисковать и говорить о бизнесе. Отвечай кратко, по-деловому, но с энтузиазмом. Используй сленг стартаперов. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    },
    "Елена": {
        "age": 45,
        "profession": "психолог",
        "personality": "мудрая и внимательная",
        "avatar": "🧠",
        "color": "#4ECDC4",
        "system_prompt": "Ты Елена, 45-летний психолог. Ты мудрая, эмпатичная, всегда внимательно слушаешь и даешь дельные советы. Говоришь спокойно, поддерживающе. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    },
    "Дед Иван": {
        "age": 72,
        "profession": "пенсионер",
        "personality": "житейская мудрость и юмор",
        "avatar": "👴",
        "color": "#95E77E",
        "system_prompt": "Ты Дед Иван, 72-летний пенсионер. У тебя огромная житейская мудрость, ты любишь рассказывать истории из прошлого, добавляешь юмор и говоришь простым языком. Иногда используешь пословицы. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    },
    "Саша": {
        "age": 19,
        "profession": "студент",
        "personality": "дерзкий и говорит мемами",
        "avatar": "😎",
        "color": "#FFE66D",
        "system_prompt": "Ты Саша, 19-летний студент. Ты дерзкий, говоришь на языке мемов и сленга молодежи, часто отшучиваешься. Используй современные выражения, иногда добавляешь эмодзи. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    },
    "Карим": {
        "age": 35,
        "profession": "бизнесмен",
        "personality": "практичный и любит цифры",
        "avatar": "💼",
        "color": "#A8DADC",
        "system_prompt": "Ты Карим, 35-летний бизнесмен. Ты очень практичный, все измеряешь цифрами, говоришь по делу, ценишь эффективность. Часто приводишь примеры из бизнеса и финансов. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    },
    "Лиза": {
        "age": 28,
        "profession": "художница",
        "personality": "творческая и эмоциональная",
        "avatar": "🎨",
        "color": "#E8B4F3",
        "system_prompt": "Ты Лиза, 28-летняя художница. Ты творческая, эмоциональная, всё видишь в цветах и образах. Говоришь поэтично, часто используешь метафоры и художественные сравнения. Всегда отвечай на вопрос пользователя. Не задавай встречных вопросов. Давай короткий живой ответ в своём стиле. Если тебя спрашивают о реальных ценах, курсах валют, акциях, криптовалюте и других данных которые меняются — честно говори что не знаешь актуальную цену и предлагай проверить на сайте типа coinmarketcap.com или google. Не выдумывай цифры."
    }
}

def generate_daily_topic():
    """Generate daily topic for live chat mode"""
    # Check if user has selected a custom topic
    if 'user_selected_topic' in st.session_state and st.session_state.user_selected_topic:
        return st.session_state.user_selected_topic
    
    topics = [
        "Новые гаджеты 2024: что уже вышло и чего ждать",
        "Искусственный интеллект в повседневной жизни: польза или вред?",
        "Криптовалюты: стоит ли инвестировать в 2024 году",
        "Здоровый образ жизни: мифы и реальность",
        "Путешествия: лучшие направления для отпуска",
        "Кино и сериалы: что посмотреть в этом месяце",
        "Технологии: последние тренды и инновации",
        "Еда и кулинария: новые рецепты и тренды",
        "Погода и климат: что происходит с планетой",
        "Работа и карьера: как найти призвание",
        "Отношения: психология современности",
        "Спорт и фитнес: мотивация и результаты"
    ]
    
    import random
    return random.choice(topics)

def generate_initial_conversation(topic):
    """Generate initial conversation between friends about topic"""
    try:
        # Select 3 random friends for initial conversation
        import random
        selected_friends = random.sample(list(AI_FRIENDS.keys()), 3)
        
        # Shuffle the order of responding friends
        random.shuffle(selected_friends)
        
        conversation_prompt = f"""
Сгенерируй начальный диалог между {selected_friends[0]}, {selected_friends[1]} и {selected_friends[2]} на тему "{topic}".

Правила:
1. Каждый друг говорит согласно своему характеру из AI_FRIENDS
2. Диалог должен быть живым и естественным
3. 3-4 сообщения всего
4. Каждый должен реагировать на предыдущего
5. Используй их аватары и манеру речи
6. Порядок ответов: {selected_friends[0]} → {selected_friends[1]} → {selected_friends[2]}

Верни ответ в формате JSON:
[
    {{"sender": "{selected_friends[0]}", "text": "..."}},
    {{"sender": "{selected_friends[1]}", "text": "..."}},
    {{"sender": "{selected_friends[2]}", "text": "..."}}
]
"""
        
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты - создатель живых диалогов между друзьями-персонажами. Создавай естественные и интересные разговоры."},
                {"role": "user", "content": conversation_prompt}
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        import json
        messages = json.loads(response.choices[0].message.content)
        return messages, selected_friends
    except Exception as e:
        return [], []

def get_ai_response(friend_name, message, chat_history=None):
    try:
        friend = AI_FRIENDS[friend_name]
        system_prompt = friend['system_prompt']
        
        # Format chat history for context (handle both list and None)
        if chat_history is None:
            chat_history = []
        
        formatted_history = []
        for msg in chat_history[-10:]:  # Last 10 messages for context
            if msg['sender'] == 'user':
                formatted_history.append(f"Пользователь: {msg['text']}")
            else:
                formatted_history.append(f"{msg['sender']}: {msg['text']}")
        
        history_text = "\n".join(formatted_history)
        
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Контекст чата:\n{history_text}\n\nТекущее сообщение: {message}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

def main():
    # Page config
    st.set_page_config(
        page_title="AI Friend Circle",
        page_icon="👥",
        layout="wide"
    )
    
    # CSS background gradient
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        border: none;
        color: white;
    }
    [data-testid="stSidebar"] ~ div .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        border: none;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    header {display: none;}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_responses' not in st.session_state:
        st.session_state.current_responses = {}
    if 'reply_to_friend' not in st.session_state:
        st.session_state.reply_to_friend = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
    if 'selected_recipient' not in st.session_state:
        st.session_state.selected_recipient = 'Всем'
    if 'active_chat' not in st.session_state:
        st.session_state.active_chat = None
    if 'live_mode' not in st.session_state:
        st.session_state.live_mode = False
    if 'daily_topic' not in st.session_state:
        st.session_state.daily_topic = None
    if 'last_auto_message_time' not in st.session_state:
        st.session_state.last_auto_message_time = None
    
    # Title with live mode toggle
    col_title, col_toggle = st.columns([4, 1])
    
    with col_title:
        st.markdown("""
<div style="padding: 24px 0 16px 0;">
    <span style="font-size: 28px; font-weight: 700; 
    color: #4c1d95;">👥 AI Friend Circle</span>
    <span style="font-size: 14px; color: #6b7280; 
    margin-left: 12px;">Общайся с друзьями с разными характерами!</span>
</div>
""", unsafe_allow_html=True)
    
    with col_toggle:
        st.markdown("<div style='padding: 24px 0 0 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        # Check if username exists in query_params (page refresh scenario)
        query_params = st.query_params
        if "user" in query_params and query_params["user"]:
            # Auto-login if username exists in query params
            st.session_state.logged_in = True
            st.session_state.user_name = query_params["user"]
            st.session_state.api_key = st.secrets["DEEPSEEK_API_KEY"]
        else:
            # Login form
            st.subheader("🔐 Вход в Friend Circle")
            
            user_name = st.text_input(
                "Ваше имя:",
                placeholder="Как тебя будут называть друзья...",
                help="Введите имя, которое будут использовать друзья при обращении"
            )
            
            password = st.text_input(
                "Пароль:",
                type="password",
                help="Введите пароль для доступа к приложению"
            )
            
            if st.button("Войти в Friend Circle", type="primary", use_container_width=True):
                if not user_name.strip():
                    st.error("Введите ваше имя!")
                elif not password.strip():
                    st.error("Введите пароль!")
                elif password.strip() != st.secrets["APP_PASSWORD"]:
                    st.error("Неверный пароль!")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_name.strip()
                    st.session_state.api_key = st.secrets["DEEPSEEK_API_KEY"]
                    # Set query params to preserve login
                    st.query_params["user"] = user_name.strip()
                    st.success(f"Добро пожаловать в Friend Circle, {user_name.strip()}!")
                    st.rerun()
            return
    
    # Update query params if logged in but not in params
    if "user" not in st.query_params or st.query_params["user"] != st.session_state.user_name:
        st.query_params["user"] = st.session_state.user_name
    
    # User is logged in - show greeting and profile menu
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👋 Привет, {st.session_state.user_name}!")
    with col2:
        # Profile menu in top right corner
        with st.popover("👤", use_container_width=True):
            st.markdown(f"**Пользователь:** {st.session_state.user_name}")
            st.markdown("---")
            if st.button("🚪 Выйти", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_name = ''
                st.session_state.api_key = ''
                st.session_state.current_responses = {}
                st.session_state.reply_to_friend = None
                st.session_state.chat_history = {}
                st.session_state.selected_recipient = 'Всем'
                st.session_state.active_chat = None
                st.rerun()
    
    # Friend cards in sidebar - only buttons
    with st.sidebar:
        # Initialize selected_friend if not exists
        if 'selected_friend' not in st.session_state:
            st.session_state.selected_friend = None
        
        # Group chat button
        group_active = st.session_state.selected_friend is None
        if st.button(
            "&#128515; Все друзья 🟢\nГрупповой чат", 
            key="group_chat_btn",
            type="primary" if group_active else "secondary",
            use_container_width=True
        ):
            st.session_state.selected_friend = None
            st.rerun()
        
        # Live mode toggle in sidebar
        if 'live_mode' not in st.session_state:
            st.session_state.live_mode = False
        
        live_mode_text = "🔥 Живая тусовка: ВКЛ" if st.session_state.live_mode else "🔥 Живая тусовка: ВЫКЛ"
        if st.button(live_mode_text, key="sidebar_live_mode_toggle", use_container_width=True):
            st.session_state.live_mode = not st.session_state.live_mode
            st.rerun()
        
        st.markdown("---")
        
        # Friends list in sidebar
        st.markdown("### 👥 Друзья")
        
        # Individual friend cards
        for friend_name, friend_info in AI_FRIENDS.items():
            is_active = st.session_state.selected_friend == friend_name
            
            if st.button(
                f"{friend_info['avatar']} {friend_name} 🟢\n{friend_info['profession']}", 
                key=f"chat_{friend_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state.selected_friend = friend_name
                st.rerun()
    
    # Chat area - full width in main area
    st.markdown("### 💬 Чат с друзьями")
    
    # Topic selection area (only in live mode)
    if st.session_state.live_mode:
        st.markdown("### 📰 Тема дня")
        
        # Initialize user_selected_topic if not exists
        if 'user_selected_topic' not in st.session_state:
            st.session_state.user_selected_topic = None
        
        # Custom topic input
        st.markdown("**Введи свою тему:**")
        custom_topic = st.text_area(
            "Твоя тема:",
            placeholder="Например: Новые гаджеты Apple 2024: инновации и тренды...",
            key="custom_topic_input",
            height=100
        )
        
        if st.button("🚀 Применить тему", key="apply_custom_topic", use_container_width=True):
            if custom_topic.strip():
                st.session_state.user_selected_topic = custom_topic.strip()
                st.rerun()
        
        st.markdown("---")
    
    # Live mode logic
    if st.session_state.live_mode:
        # Generate daily topic only if user has selected one or custom topic
        if not st.session_state.daily_topic and st.session_state.user_selected_topic:
            with st.spinner("Создаю тему дня..."):
                topic = generate_daily_topic()
                st.session_state.daily_topic = topic
                
                # Generate initial conversation about the topic
                initial_messages, selected_friends = generate_initial_conversation(topic)
                
                # Add initial messages to chat one by one with delays
                if 'group' not in st.session_state.chat_history:
                    st.session_state.chat_history['group'] = []
                
                # Store pending messages for sequential display
                st.session_state.pending_messages = initial_messages
                st.session_state.current_message_index = 0
                st.session_state.last_auto_message_time = time.time()
                
                # Add first message immediately
                if st.session_state.pending_messages and st.session_state.current_message_index < len(st.session_state.pending_messages):
                    msg = st.session_state.pending_messages[st.session_state.current_message_index]
                    st.session_state.chat_history['group'].append(msg)
                    st.session_state.current_message_index += 1
                    st.rerun()
        
        # Check if we need to add more pending messages
        if hasattr(st.session_state, 'pending_messages') and st.session_state.pending_messages:
            if st.session_state.current_message_index < len(st.session_state.pending_messages):
                # Check if enough time has passed since last message
                time_since_last = time.time() - st.session_state.last_auto_message_time
                if time_since_last >= random.uniform(0.5, 2.5):
                    # Add next message
                    msg = st.session_state.pending_messages[st.session_state.current_message_index]
                    st.session_state.chat_history['group'].append(msg)
                    st.session_state.current_message_index += 1
                    st.session_state.last_auto_message_time = time.time()
                    
                    # Clear pending messages if all are added
                    if st.session_state.current_message_index >= len(st.session_state.pending_messages):
                        st.session_state.pending_messages = []
                    
                    st.rerun()
        
        # Display daily topic
        if st.session_state.daily_topic:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 12px; border-radius: 8px; margin-bottom: 16px; text-align: center;">
                <div style="font-size: 16px; font-weight: bold;">📰 Тема дня</div>
                <div style="font-size: 14px; margin-top: 8px;">{st.session_state.daily_topic}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Auto-messages from friends every 2-3 minutes (only if no pending messages)
        current_time = time.time()
        if (st.session_state.last_auto_message_time and 
            current_time - st.session_state.last_auto_message_time > 120 and  # 2 minutes
            not hasattr(st.session_state, 'pending_messages')):  # No pending messages
            with st.spinner("Друзья общаются..."):
                import random
                friend_name = random.choice(list(AI_FRIENDS.keys()))
                
                # Create context-aware message
                context_messages = [msg for msg in st.session_state.chat_history.get('group', [])[-5:]]
                context_text = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in context_messages])
                
                auto_prompt = f"""
Ты - {friend_name}. Продолжай обсуждение темы дня "{st.session_state.daily_topic}". 
Учитывай всю историю разговора:
{context_text}

Отвечай естественно, согласно своему характеру. Не упоминай что ты ИИ.
"""
                
                response = get_ai_response(friend_name, auto_prompt, [])
                if response and not response.startswith("Ошибка:"):
                    st.session_state.chat_history['group'].append({
                        'sender': friend_name,
                        'text': response,
                        'recipient': 'Всем',
                        'timestamp': 'now'
                    })
                    st.session_state.last_auto_message_time = current_time
                    st.rerun()
    
    # Always show group messages
    messages = st.session_state.chat_history.get('group', [])
    
    if not messages:
        # Show empty state without white background
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #666;">
            <div style="font-size: 24px; margin-bottom: 10px;">👥</div>
            <div>Начни разговор с друзьями!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show messages without container wrapper
        for msg in messages:
            if msg['sender'] == 'user':
                # User message - right side
                recipient_text = f" → {msg['recipient']} (лично)" if msg.get('recipient') and msg['recipient'] != 'Всем' else ""
                
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                    <div style="background-color: #E3F2FD; border-radius: 15px; padding: 10px 15px; max-width: 70%; border-top-right-radius: 5px;">
                        <div style="color: #1976D2; font-weight: bold; font-size: 12px;">Вы{recipient_text}</div>
                        <div style="color: #333;">{msg['text']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Friend message - left side with avatar
                friend = AI_FRIENDS[msg['sender']]
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                    <div style="font-size: 24px; margin-right: 10px; margin-top: 5px;">{friend['avatar']}</div>
                    <div style="background-color: #f5f5f5; border-radius: 15px; padding: 10px 15px; max-width: 70%; border-top-left-radius: 5px; border: 1px solid #e0e0e0;">
                        <div style="color: #666; font-weight: bold; font-size: 12px;">{msg['sender']}</div>
                        <div style="color: #333;">{msg['text']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Recipient indicator above input
    if st.session_state.selected_friend is None:
        recipient_text = "Пишешь: Всем"
        placeholder_text = "Расскажи что-то интересное, задай вопрос или поделись новостями..."
    else:
        friend = AI_FRIENDS[st.session_state.selected_friend]
        recipient_text = f"Пишешь: {st.session_state.selected_friend} {friend['avatar']}"
        placeholder_text = f"Напишите {st.session_state.selected_friend}..."
    
    st.markdown(f"""
<div style="
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    margin-bottom: 8px;
">✍️ {recipient_text}</div>
""", unsafe_allow_html=True)
    
    # Initialize input key for Enter support
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    user_message = st.text_input(
        "Сообщение:",
        placeholder=placeholder_text,
        key=f"msg_{st.session_state.input_key}",
        label_visibility="collapsed"
    )
    
    if st.button("📤 Отправить", type="primary", use_container_width=True) or user_message.strip():
        # Initialize message_sent flag
        if 'message_sent' not in st.session_state:
            st.session_state.message_sent = False
        
        # Prevent message duplication
        if not st.session_state.message_sent:
            # All messages go to group chat with recipient field
            if 'group' not in st.session_state.chat_history:
                st.session_state.chat_history['group'] = []
            
            # Determine recipient
            if st.session_state.selected_friend is None:
                recipient = 'Всем'
            else:
                recipient = st.session_state.selected_friend
            
            # Add user message
            st.session_state.chat_history['group'].append({
                'sender': 'user',
                'text': user_message.strip(),
                'recipient': recipient,
                'timestamp': 'now'
            })
            
            # Set flag to prevent duplication
            st.session_state.message_sent = True
        
        # Generate responses
        if st.session_state.selected_friend is None:
            # All friends respond (considering full conversation history in live mode)
            with st.spinner("Друзья думают над ответами..."):
                for friend_name in AI_FRIENDS.keys():
                    # Get full conversation history for context
                    full_history = st.session_state.chat_history.get('group', [])
                    response = get_ai_response(
                        friend_name,
                        user_message.strip(),
                        full_history
                    )
                    
                    if response and not response.startswith("Ошибка:"):
                        st.session_state.chat_history['group'].append({
                            'sender': friend_name,
                            'text': response,
                            'recipient': 'Всем',
                            'timestamp': 'now'
                        })
        else:
            # Only selected friend responds
            friend_name = st.session_state.selected_friend
            with st.spinner(f"{friend_name} думает над ответом..."):
                # Get full conversation history for context
                full_history = st.session_state.chat_history.get('group', [])
                response = get_ai_response(
                    friend_name,
                    user_message.strip(),
                    full_history
                )
                
                st.session_state.chat_history['group'].append({
                    'sender': friend_name,
                    'text': response,
                    'timestamp': 'now'
                })
        
        # Clear input field
        st.session_state.input_key += 1
        st.session_state.message_sent = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
