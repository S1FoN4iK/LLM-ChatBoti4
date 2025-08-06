import gradio as gr
from openrouter_api import ask_openrouter
from history_saver import save_dialogue

chat_history = []
SYSTEM_PROMPT = {...}

def chat(user_input, request: gr.Request):
    global chat_history

    if not user_input.strip():
        return chat_history

    # Получаем IP, при запуске в локалке всегда 127.0.0.1, однако при продакшене должно выдавать реальный IP пользователей
    forwarded_for = request.headers.get("X-Forwarded-For") or request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host or "unknown"

    # Генерируем ответ
    messages = [SYSTEM_PROMPT] + chat_history + [{"role": "user", "content": user_input}]
    bot_reply = ask_openrouter(user_input, chat_history)

    # Обновляем историю
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_reply})

    # Сохраняем
    save_dialogue(user_input, bot_reply, ip_address=ip)
    return chat_history

# Визуал и обработчики
with gr.Blocks() as demo:
    gr.Markdown("## 💬 Чат-боты4, спрашивайте 🫵")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Ваше сообщение")
    send_btn = gr.Button("Отправить")
    send_btn.click(fn=chat, inputs=[msg], outputs=chatbot)
    msg.submit(fn=chat, inputs=[msg], outputs=chatbot)
demo.launch()

