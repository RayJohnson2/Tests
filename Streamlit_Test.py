
# streamlit run Streamlit_Test.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Matplotlib Demo", layout="wide")

st.title("📊 Streamlit + Matplotlib Demo")
st.write("Test of deze app goed werkt op je smartphone!")

# Sidebar met opties
st.sidebar.header("Instellingen")
grafiek_type = st.sidebar.selectbox(
    "Kies een grafiek type:",
    ["Lijngrafiek", "Staafdiagram", "Scatter plot", "Cirkeldiagram"]
)

aantal_punten = st.sidebar.slider("Aantal datapunten:", 5, 50, 20)

# Genereer random data
x = np.linspace(0, 10, aantal_punten)
y = np.sin(x) + np.random.normal(0, 0.1, aantal_punten)

# Maak de grafiek
fig, ax = plt.subplots(figsize=(10, 6))

if grafiek_type == "Lijngrafiek":
    ax.plot(x, y, marker='o', linestyle='-', color='blue', linewidth=2)
    ax.set_xlabel('X-as')
    ax.set_ylabel('Y-as')
    ax.set_title('Sinus Lijngrafiek met Ruis')
    ax.grid(True, alpha=0.3)

elif grafiek_type == "Staafdiagram":
    colors = plt.cm.viridis(np.linspace(0, 1, aantal_punten))
    ax.bar(range(aantal_punten), y, color=colors)
    ax.set_xlabel('Index')
    ax.set_ylabel('Waarde')
    ax.set_title('Staafdiagram')
    ax.grid(True, alpha=0.3, axis='y')

elif grafiek_type == "Scatter plot":
    sizes = np.random.randint(20, 200, aantal_punten)
    colors = np.random.rand(aantal_punten)
    ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='coolwarm')
    ax.set_xlabel('X-as')
    ax.set_ylabel('Y-as')
    ax.set_title('Scatter Plot met Random Groottes')
    ax.grid(True, alpha=0.3)

else:  # Cirkeldiagram
    labels = [f'Segment {i+1}' for i in range(min(6, aantal_punten))]
    sizes = np.random.randint(10, 100, min(6, aantal_punten))
    colors = plt.cm.Pastel1(range(len(sizes)))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title('Cirkeldiagram')

plt.tight_layout()

# Toon de grafiek
st.pyplot(fig)

# Extra informatie
st.info("✅ Als je deze grafiek kunt zien en kunt interacteren met de sidebar, werkt Streamlit goed op je smartphone!")

# Toon wat statistieken
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Min waarde", f"{y.min():.2f}")
with col2:
    st.metric("Max waarde", f"{y.max():.2f}")
with col3:
    st.metric("Gemiddelde", f"{y.mean():.2f}")

# Test van responsive design
st.write("---")
st.subheader("📱 Smartphone Test")
st.write("Kun je:")
st.write("- ✓ De sidebar openen/sluiten?")
st.write("- ✓ De slider gebruiken?")
st.write("- ✓ Het grafiek type veranderen?")
st.write("- ✓ De grafieken duidelijk zien?")