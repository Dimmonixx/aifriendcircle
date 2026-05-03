import streamlit as st
from PIL import Image

def show_page():
    st.title("📷 Фото-инженер")

    st.info(
        "Модуль анализирует фото и корректирует цвет для точного "
        "подбора оттенка. Поддерживает два режима: калибровка по "
        "серой карте (профессиональный) и по расцветке Vita (быстрый)."
    )

    mode = st.radio(
        "Выбери режим калибровки",
        options=["⬜ Серая карта (Grey Card)", "🦷 Расцветка Vita"],
        horizontal=True
    )

    st.divider()

    if mode == "⬜ Серая карта (Grey Card)":
        st.subheader("Инструкция")
        st.markdown(
            """1. Сфотографируй коронку вместе с серой картой в одном кадре
2. Одинаковое освещение для карты и коронки
3. Загрузи фото ниже — система найдёт карту автоматически"""
        )
        st.divider()

        col1, col2 = st.columns(2)
        grey_file = None
        crown_file = None

        with col1:
            st.markdown("### 📸 Фото с серой картой")
            grey_file = st.file_uploader(
                "Загрузи фото",
                type=["jpg", "jpeg", "png"],
                key="grey_card"
            )

        with col2:
            st.markdown("### 🦷 Фото коронки")
            crown_file = st.file_uploader(
                "Загрузи фото",
                type=["jpg", "jpeg", "png"],
                key="crown_grey"
            )

        # Show previews if both files uploaded
        if grey_file is not None and crown_file is not None:
            st.divider()
            preview_col1, preview_col2 = st.columns(2)

            with preview_col1:
                grey_image = Image.open(grey_file)
                st.image(grey_image, caption="Серая карта", use_container_width=True)

            with preview_col2:
                crown_image = Image.open(crown_file)
                st.image(crown_image, caption="Коронка", use_container_width=True)

            st.divider()
            if st.button("🔍 Анализировать баланс белого", type="primary", use_container_width=True):
                st.info("Алгоритм WB подключим на следующем шаге")

    elif mode == "🦷 Расцветка Vita":
        st.subheader("Инструкция")
        st.markdown(
            """1. Сфотографируй коронку рядом с расцветкой Vita в одном кадре
2. Расцветка должна занимать минимум 20% кадра
3. Избегай теней и бликов на расцветке"""
        )
        st.divider()

        st.markdown("### 📸 Фото коронки с расцветкой Vita")
        vita_file = st.file_uploader(
            "Загрузи фото",
            type=["jpg", "jpeg", "png"],
            key="vita"
        )

        selected_shade = st.selectbox(
            "Предполагаемый оттенок (для сравнения)",
            options=["A1", "A2", "A3", "A3.5", "A4", "B1", "B2", "B3", "B4",
                     "C1", "C2", "C3", "C4", "D2", "D3", "D4"]
        )

        # Show preview if file uploaded
        if vita_file is not None:
            st.divider()
            vita_image = Image.open(vita_file)
            st.image(vita_image, caption="Фото с расцветкой Vita", use_container_width=True)

            st.divider()
            if st.button("🔍 Сравнить с расцветкой", type="primary", use_container_width=True):
                st.info("Алгоритм сравнения подключим на следующем шаге")
