import streamlit as st
from openai import OpenAI
import random
import time
import json

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


def get_client():
    return OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com"
    )


def get_ai_response(friend_name, message, chat_history=None):
    try:
        friend = AI_FRIENDS[friend_name]
        if chat_history is None:
            chat_history = []
        formatted_history = []
        for msg in chat_history[-10:]:
            if msg['sender'] == 'user':
                formatted_history.append(f"Пользователь: {msg['text']}")
            else:
                formatted_history.append(f"{msg['sender']}: {msg['text']}")
        history_text = "\n".join(formatted_history)
        client = get_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": friend['system_prompt']},
                {"role": "user", "content": f"Контекст чата:\n{history_text}\n\nТекущее сообщение: {message}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"


def get_responders(message, chat_history):
    try:
        client = get_client()
        friends_desc = "\n".join([
            f"- {name}: {info['personality']}, {info['profession']}"
            for name, info in AI_FRIENDS.items()
        ])
        history_lines = []
        for msg in chat_history[-6:]:
            if msg['sender'] == 'user':
                history_lines.append(f"Пользователь: {msg['text']}")
            else:
                history_lines.append(f"{msg['sender']}: {msg['text']}")
        history_text = "\n".join(history_lines)
        prompt = f"""Ты модератор группового чата. В чате есть 6 друзей:
{friends_desc}

История чата:
{history_text}

Новое сообщение: "{message}"

Реши кто захочет ответить исходя из характеров. Обычно 2-4 человека, иногда 1.
Верни ТОЛЬКО JSON: {{"responders": ["Имя1", "Имя2"]}}"""
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        responders = [r for r in data.get("responders", []) if r in AI_FRIENDS]
        return responders if responders else ["Макс"]
    except Exception:
        return random.sample(list(AI_FRIENDS.keys()), random.randint(2, 3))


def get_auto_message(chat_history):
    try:
        client = get_client()
        initiator = random.choice(list(AI_FRIENDS.keys()))
        friend = AI_FRIENDS[initiator]
        history_lines = []
        for msg in chat_history[-6:]:
            if msg['sender'] == 'user':
                history_lines.append(f"Пользователь: {msg['text']}")
            else:
                history_lines.append(f"{msg['sender']}: {msg['text']}")
        history_text = "\n".join(history_lines)
        prompt = f"""Ты {initiator}, {friend['profession']}. Характер: {friend['personality']}.

История чата:
{history_text}

Напиши короткое спонтанное сообщение в групповой чат — поделись мыслью, задай вопрос группе или прокомментируй что-то из последних сообщений. Пиши в своём стиле. Не более 2 предложений."""
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": friend['system_prompt']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.9
        )
        return initiator, response.choices[0].message.content
    except Exception:
        return None, None


def render_messages(messages):
    for msg in messages:
        if msg['sender'] == 'user':
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
            if msg['sender'] not in AI_FRIENDS:
                continue
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


def main():
    st.set_page_config(
        page_title="AI Friend Circle",
        page_icon="👥",
        layout="wide"
    )

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
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    header {display: none;}
    </style>
    """, unsafe_allow_html=True)

    # Session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
    if 'selected_friend' not in st.session_state:
        st.session_state.selected_friend = None
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    if 'pending_responses' not in st.session_state:
        st.session_state.pending_responses = []
    if 'current_message' not in st.session_state:
        st.session_state.current_message = ''
    if 'live_mode' not in st.session_state:
        st.session_state.live_mode = False
    if 'last_auto_message_time' not in st.session_state:
        st.session_state.last_auto_message_time = 0.0
    if 'live_auto_message' not in st.session_state:
        st.session_state.live_auto_message = None

    # Header
    st.markdown("""
<div style="padding: 24px 0 16px 0;">
    <span style="font-size: 28px; font-weight: 700; color: #4c1d95;">&#128101; AI Friend Circle</span>
    <span style="font-size: 14px; color: #6b7280; margin-left: 12px;">Общайся с друзьями с разными характерами!</span>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    # Auth
    if not st.session_state.logged_in:
        query_params = st.query_params
        if "user" in query_params and query_params["user"]:
            st.session_state.logged_in = True
            st.session_state.user_name = query_params["user"]
        else:
            st.subheader("🔐 Вход в Friend Circle")
            user_name = st.text_input("Ваше имя:", placeholder="Как тебя будут называть друзья...")
            password = st.text_input("Пароль:", type="password")
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
                    st.query_params["user"] = user_name.strip()
                    st.rerun()
            return

    if "user" not in st.query_params or st.query_params["user"] != st.session_state.user_name:
        st.query_params["user"] = st.session_state.user_name

    # Top bar
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👋 Привет, {st.session_state.user_name}!")
    with col2:
        with st.popover("👤", use_container_width=True):
            st.markdown(f"**Пользователь:** {st.session_state.user_name}")
            st.markdown("---")
            if st.button("🚪 Выйти", use_container_width=True):
                for key in ['logged_in', 'user_name', 'chat_history', 'selected_friend',
                            'pending_responses', 'current_message', 'live_mode',
                            'last_auto_message_time', 'live_auto_message']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    # Sidebar
    with st.sidebar:
        group_active = st.session_state.selected_friend is None
        if st.button(
            "&#128515; Все друзья &#128994;\nГрупповой чат",
            key="group_chat_btn",
            type="primary" if group_active else "secondary",
            use_container_width=True
        ):
            st.session_state.selected_friend = None
            st.session_state.pending_responses = []
            st.rerun()

        st.markdown("---")
        live_label = "&#128293; Живая тусовка: ВКЛ" if st.session_state.live_mode else "&#128293; Живая тусовка: ВЫКЛ"
        if st.button(live_label, key="live_mode_btn", use_container_width=True):
            st.session_state.live_mode = not st.session_state.live_mode
            if st.session_state.live_mode:
                st.session_state.last_auto_message_time = time.time()
            st.rerun()
        st.markdown("---")

        for friend_name, friend_info in AI_FRIENDS.items():
            is_active = st.session_state.selected_friend == friend_name
            if st.button(
                f"{friend_info['avatar']} {friend_name} &#128994;\n{friend_info['profession']}",
                key=f"chat_{friend_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state.selected_friend = friend_name
                st.session_state.pending_responses = []
                st.rerun()

    # Chat area
    st.markdown("### &#128172; Чат с друзьями")

    messages = st.session_state.chat_history.get('group', [])
    if not messages and not st.session_state.pending_responses:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #666;">
            <div style="font-size: 24px; margin-bottom: 10px;">&#128101;</div>
            <div>Начни разговор с друзьями!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_messages(messages)

    # TYPING INDICATOR + QUEUE
    if st.session_state.pending_responses:
        friend_name = st.session_state.pending_responses[0]
        friend = AI_FRIENDS[friend_name]

        typing_placeholder = st.empty()
        typing_placeholder.markdown(f"""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="font-size: 24px; margin-right: 10px;">{friend['avatar']}</div>
            <div style="background-color: #f0f0f0; border-radius: 15px; padding: 8px 14px; color: #888; font-style: italic;">
                {friend_name} печатает...
            </div>
        </div>
        """, unsafe_allow_html=True)

        live_msg = st.session_state.live_auto_message
        if live_msg:
            response = live_msg
            st.session_state.live_auto_message = None
        else:
            full_history = st.session_state.chat_history.get('group', [])
            response = get_ai_response(
                friend_name,
                st.session_state.current_message,
                full_history
            )

        typing_placeholder.empty()

        if response and not response.startswith("Ошибка:"):
            if 'group' not in st.session_state.chat_history:
                st.session_state.chat_history['group'] = []
            st.session_state.chat_history['group'].append({
                'sender': friend_name,
                'text': response,
                'recipient': 'Всем',
                'timestamp': 'now'
            })

        st.session_state.pending_responses.pop(0)
        st.rerun()

    # LIVE MODE TIMER
    elif st.session_state.live_mode and st.session_state.selected_friend is None:
        now = time.time()
        interval = random.randint(30, 60)
        time_passed = now - st.session_state.last_auto_message_time

        if time_passed >= interval:
            full_history = st.session_state.chat_history.get('group', [])
            initiator, auto_msg = get_auto_message(full_history)
            if initiator and auto_msg:
                st.session_state.live_auto_message = auto_msg
                st.session_state.pending_responses = [initiator]
                st.session_state.current_message = ''
            st.session_state.last_auto_message_time = now
            st.rerun()
        else:
            remaining = int(interval - time_passed)
            st.markdown(f"""
            <div style="text-align: center; color: #a855f7; font-size: 12px; padding: 4px;">
                &#128293; Живая тусовка активна — следующее сообщение через ~{remaining} сек
            </div>
            """, unsafe_allow_html=True)
            time.sleep(5)
            st.rerun()

    # Input
    if st.session_state.selected_friend is None:
        recipient_text = "Пишешь: Всем"
        placeholder_text = "Расскажи что-то интересное, задай вопрос или поделись новостями..."
    else:
        friend = AI_FRIENDS[st.session_state.selected_friend]
        recipient_text = f"Пишешь: {st.session_state.selected_friend} {friend['avatar']}"
        placeholder_text = f"Напишите {st.session_state.selected_friend}..."

    st.markdown(f"""
<div style="display: inline-block; background: linear-gradient(135deg, #7c3aed, #a855f7);
color: white; padding: 4px 12px; border-radius: 20px; font-size: 13px; margin-bottom: 8px;">
&#9997;&#65039; {recipient_text}</div>
""", unsafe_allow_html=True)

    user_message = st.text_input(
        "Сообщение:",
        placeholder=placeholder_text,
        key=f"msg_{st.session_state.input_key}",
        label_visibility="collapsed"
    )

    if st.button("&#128228; Отправить", type="primary", use_container_width=True):
        if user_message.strip():
            if 'group' not in st.session_state.chat_history:
                st.session_state.chat_history['group'] = []
            recipient = st.session_state.selected_friend or 'Всем'
            st.session_state.chat_history['group'].append({
                'sender': 'user',
                'text': user_message.strip(),
                'recipient': recipient,
                'timestamp': 'now'
            })
            st.session_state.current_message = user_message.strip()
            if st.session_state.selected_friend is None:
                full_history = st.session_state.chat_history.get('group', [])
                responders = get_responders(user_message.strip(), full_history)
                st.session_state.pending_responses = responders
            else:
                st.session_state.pending_responses = [st.session_state.selected_friend]
            st.session_state.last_auto_message_time = time.time()
            st.session_state.input_key += 1
            st.rerun()


if __name__ == "__main__":
    main()
