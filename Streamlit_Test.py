import streamlit as st
import time
import json

st.set_page_config(page_title="Visibility Test", layout="wide")

st.title("🔍 Streamlit Browser Visibility Test App")

# --- Session state initialization ---
defaults = {
    "raw_visible": True,
    "debounced_visible": True,
    "last_hidden": None,
    "log": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# --- JavaScript to detect events ---
js = """
<script>
function send(msg) {
    window.parent.postMessage({streamlitMessage: msg}, "*");
}

send({init: true, in_iframe: (window.top !== window.self)});

document.addEventListener("visibilitychange", () => {
    send({
        type: "visibilitychange",
        raw_visible: !document.hidden,
        timestamp: Date.now()
    });
});

window.addEventListener("blur", () => {
    send({
        type: "blur",
        raw_visible: !document.hidden,
        timestamp: Date.now()
    });
});

window.addEventListener("focus", () => {
    send({
        type: "focus",
        raw_visible: !document.hidden,
        timestamp: Date.now()
    });
});
</script>
"""

st.components.v1.html(js, height=0)

# --- Process received messages from JS ---
msg = st.session_state.get("streamlitMessage")
if msg and isinstance(msg, dict):

    # logging events
    if "type" in msg:
        st.session_state.log.append(msg)

    # raw visibility update
    if "raw_visible" in msg:
        st.session_state.raw_visible = msg["raw_visible"]

    # iframe detection
    if "in_iframe" in msg:
        st.session_state.in_iframe = msg["in_iframe"]


# --- Debounce logic ---
debounce_seconds = 3
raw = st.session_state.raw_visible

if raw:
    st.session_state.debounced_visible = True
    st.session_state.last_hidden = None
else:
    if st.session_state.last_hidden is None:
        st.session_state.last_hidden = time.time()
    if time.time() - st.session_state.last_hidden > debounce_seconds:
        st.session_state.debounced_visible = False


# --- Display status ---
st.subheader("📌 Current Status")

col1, col2, col3 = st.columns(3)

col1.metric("Raw JS Visibility", st.session_state.raw_visible)
col2.metric("Debounced (3s)", st.session_state.debounced_visible)
col3.metric("Running in iframe?", st.session_state.get("in_iframe"))

st.divider()

# Log of visibility events
st.subheader("📜 Event Log (visibilitychange / focus / blur)")
st.json(st.session_state.log[-20:])  # show last 20 events

st.divider()

st.write("⏱ Last hidden timestamp:", st.session_state.last_hidden)
