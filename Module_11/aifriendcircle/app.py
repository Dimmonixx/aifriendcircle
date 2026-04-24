import streamlit as st
from openai import OpenAI
import random

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

def get_ai_response(api_key, friend_name, user_message, detailed=False):
    """Get AI response from DeepSeek API"""
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        friend = AI_FRIENDS[friend_name]
        
        if detailed:
            prompt = f"Дай развёрнутый ответ (5-7 предложений) на сообщение пользователя: '{user_message}'. {friend['system_prompt']}"
        else:
            prompt = f"Дай короткую реакцию (1-2 предложения) на сообщение пользователя: '{user_message}'. {friend['system_prompt']}"
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": friend['system_prompt']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200 if detailed else 100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Ошибка: {str(e)}"

def main():
    st.set_page_config(
        page_title="AI Friend Circle",
        page_icon="👥",
        layout="wide"
    )
    
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
    
    # Title
    st.title("👥 AI Friend Circle")
    st.markdown("*Общайся с друзьями с разными характерами!*")
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
    
    # Main chat interface with sidebar
    col1, col2 = st.columns([1, 3])
    
    # Soft lavender sidebar styling and white header
    st.markdown("""
    <style>
    .stColumn:first-child {
        background-color: #F0EEF8;
        padding: 20px;
        border-radius: 10px;
        margin-right: 10px;
    }
    .stApp > div {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E0DCF5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Friend cards sidebar
    with col1:
        st.markdown("### 👥 Друзья")
        
        # Initialize selected_friend if not exists
        if 'selected_friend' not in st.session_state:
            st.session_state.selected_friend = None
        
        # Group chat button
        group_active = st.session_state.selected_friend is None
        if st.button(
            "&#128515; Все друзья\nГрупповой чат", 
            key="group_chat_btn",
            type="primary" if group_active else "secondary",
            use_container_width=True
        ):
            st.session_state.selected_friend = None
            st.rerun()
        
        # Individual friend cards
        for friend_name, friend_info in AI_FRIENDS.items():
            is_active = st.session_state.selected_friend == friend_name
            
            if st.button(
                f"{friend_info['avatar']} {friend_name}\n{friend_info['profession']}", 
                key=f"chat_{friend_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state.selected_friend = friend_name
                st.rerun()
    
    # Chat area - unified chat
    with col2:
        st.markdown("### 💬 Чат с друзьями")
        
        # Message history
        chat_container = st.container()
        with chat_container:
            # Get messages based on selected friend
            if st.session_state.selected_friend is None:
                # Show group messages
                messages = st.session_state.chat_history.get('group', [])
                
                if not messages:
                    st.markdown("""
                    <div style="text-align: center; padding: 40px; color: #666;">
                        <div style="font-size: 24px; margin-bottom: 10px;">👥</div>
                        <div>Начни разговор с друзьями!</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
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
            else:
                # Show personal messages for selected friend
                friend_name = st.session_state.selected_friend
                messages = st.session_state.chat_history.get(friend_name, [])
                
                if not messages:
                    friend = AI_FRIENDS[friend_name]
                    st.markdown(f"""
                    <div style="text-align: center; padding: 40px; color: #666;">
                        <div style="font-size: 24px; margin-bottom: 10px;">{friend['avatar']}</div>
                        <div>Начни разговор с {friend_name}!</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    for msg in messages:
                        if msg['sender'] == 'user':
                            # User message - right side
                            st.markdown(f"""
                            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                                <div style="background-color: #E3F2FD; border-radius: 15px; padding: 10px 15px; max-width: 70%; border-top-right-radius: 5px;">
                                    <div style="color: #1976D2; font-weight: bold; font-size: 12px;">Вы</div>
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
                                    <div style="color: #666; font-weight: bold; font-size: 12px;">{friend_name}</div>
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
        
        st.markdown(f"**{recipient_text}**")
        
        # Initialize input counter
        if 'input_counter' not in st.session_state:
            st.session_state.input_counter = 0
        if 'should_send' not in st.session_state:
            st.session_state.should_send = False
        
        # Message input with Enter support
        def handle_input_change():
            if st.session_state.get(f"msg_input_{st.session_state.input_counter}", "").strip():
                st.session_state.should_send = True
        
        user_message = st.text_input(
            "Сообщение:",
            placeholder=placeholder_text,
            key=f"msg_input_{st.session_state.input_counter}",
            on_change=handle_input_change
        )
        
        if st.button("📤 Отправить", type="primary", use_container_width=True):
            st.session_state.should_send = True
        
        # Process message if should_send is True
        if st.session_state.should_send and user_message.strip():
                if st.session_state.selected_friend is None:
                    # Group message
                    if 'group' not in st.session_state.chat_history:
                        st.session_state.chat_history['group'] = []
                    
                    st.session_state.chat_history['group'].append({
                        'sender': 'user',
                        'text': user_message.strip(),
                        'recipient': 'Всем',
                        'timestamp': 'now'
                    })
                    
                    # All friends respond
                    with st.spinner("Друзья думают над ответами..."):
                        for friend_name in AI_FRIENDS.keys():
                            response = get_ai_response(
                                st.session_state.api_key,
                                friend_name,
                                user_message.strip(),
                                detailed=False
                            )
                            
                            st.session_state.chat_history['group'].append({
                                'sender': friend_name,
                                'text': response,
                                'timestamp': 'now'
                            })
                else:
                    # Personal message
                    friend_name = st.session_state.selected_friend
                    if friend_name not in st.session_state.chat_history:
                        st.session_state.chat_history[friend_name] = []
                    
                    st.session_state.chat_history[friend_name].append({
                        'sender': 'user',
                        'text': user_message.strip(),
                        'timestamp': 'now'
                    })
                    
                    # Only selected friend responds
                    with st.spinner(f"{friend_name} думает над ответом..."):
                        response = get_ai_response(
                            st.session_state.api_key,
                            friend_name,
                            user_message.strip(),
                            detailed=False
                        )
                        
                        st.session_state.chat_history[friend_name].append({
                            'sender': friend_name,
                            'text': response,
                            'timestamp': 'now'
                        })
                
                # Clear input field and increment counter
                st.session_state[f"msg_input_{st.session_state.input_counter}"] = ""
                st.session_state.input_counter += 1
                st.session_state.should_send = False
                st.rerun()

if __name__ == "__main__":
    main()
