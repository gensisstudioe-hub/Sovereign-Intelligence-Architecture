import streamlit as st
import os
from openai import OpenAI
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import base64

# --- 1. إعدادات الهوية البصرية السيادية ---
st.set_page_config(page_title="Sovereign OS | Protocol 07", layout="wide")
st.markdown("<style>.main { background-color: #121212; color: #FFFFFF; }</style>", unsafe_allow_html=True)

# --- 2. تفعيل محرك الاستدلال (HF_TOKEN) ---
# يجب إضافة HF_TOKEN في Streamlit Secrets ليعمل هذا الجزء
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=st.secrets.get("HF_TOKEN"),
)

# --- 3. عرض شعار النظام ---
try:
    st.image("sovereign_logo.png", width=200)
except Exception:
    st.warning("Please upload 'sovereign_logo.png' to your GitHub repository.")

st.title("Sovereign OS | Protocol 07")
st.subheader("Structural Risk Architecture & Decision Engine")

# --- 4. مدخلات القائد (Context & Sliders) ---
st.markdown("### 1. Strategic Context")
context = st.text_area("Provide the challenge or the invisible asset you want to decrypt:", placeholder="Example: Tapping into human capital for market expansion...")

st.markdown("### 2. Equation Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    ia = st.slider("Invisible Assets (IA)", 0.1, 10.0, 5.0, help="Human capital, latent capabilities.")
with col2:
    srf = st.slider("Reflection Factor (SRF)", 0.1, 2.0, 1.0, help="Efficiency of institutional intelligence.")
with col3:
    re = st.slider("Risk Exposure (RE)", 0.1, 10.0, 3.0, help="External threats and structural blind spots.")

# --- 5. حساب المعادلة (SR Formula) ---
sr_score = (ia * srf) / re

# --- 6. توليد التقرير والذكاء الاصطناعي ---
if st.button("Generate Sovereign Report"):
    if context:
        with st.spinner("Sovereign Intelligence is analyzing..."):
            # (أ) تحليل الذكاء الاصطناعي
            try:
                completion = client.chat.completions.create(
                    model="moonshotai/Kimi-K2-Instruct-0905",
                    messages=[
                        {"role": "system", "content": "You are the Sovereign OS Intelligence. Use Decisive Simplicity English based on Protocol 07. Convert context and score into a risk management protocol and a clear strategic decision."},
                        {"role": "user", "content": f"Context: {context}\nSR Score: {sr_score:.2f} (IA={ia}, SRF={srf}, RE={re})"}
                    ]
                )
                ai_advice = completion.choices[0].message.content
                st.markdown("### 3. The Sovereign Decision")
                st.info(ai_advice)

                # (ب) إنشاء الرسم البياني
                fig, ax = plt.subplots()
                ax.bar(["SR Score"], [sr_score], color='#D4AF37') # ذهبي سيادي
                ax.axhline(5, color='#FFFFFF', linestyle='--') # خط مرجعي أبيض
                ax.set_ylim(0, 10)
                plt.savefig("plot.png", transparent=True)

                # (ج) توليد التقرير PDF مع العلامة المائية
                def generate_pdf(context, score, advice):
                    c = canvas.Canvas("sovereign_report.pdf", pagesize=A4)
                    width, height = A4

                    # إضافة العلامة المائية
                    try:
                        watermark = ImageReader("watermark.png")
                        c.saveState()
                        c.setFillAlpha(0.1) # شفافية 10%
                        c.drawImage(watermark, width/4, height/4, width=width/2, height=height/2, mask='auto')
                        c.restoreState()
                    except Exception:
                        pass # إذا لم توجد صورة العلامة المائية، لا تتوقف العملية

                    # كتابة محتوى التقرير
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(100, height-80, "Sovereign OS - Protocol 07 Report")
                    c.setFont("Helvetica", 12)
                    c.drawString(100, height-100, "Structural Readiness Architecture")
                    
                    c.drawString(100, height-140, "Strategic Context:")
                    c.setFont("Helvetica-Oblique", 11)
                    c.drawString(120, height-160, f"{context[:80]}...") # اقتطاع النص الطويل

                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(100, height-200, f"Sovereign Readiness Score (SR): {score:.2f}")

                    c.drawString(100, height-240, "Decision & Advice:")
                    c.setFont("Helvetica", 11)
                    # معالجة النص النصي الطويل (بشكل مبسط)
                    textobject = c.beginText(120, height-260)
                    textobject.setFont("Helvetica", 11)
                    for line in advice.split('\n'):
                        textobject.textLine(line)
                    c.drawText(textobject)

                    c.save()

                generate_pdf(context, sr_score, ai_advice)
                
                # (د) رابط تحميل التقرير
                with open("sovereign_report.pdf", "rb") as f:
                    bytes_data = f.read()
                b64 = base64.b64encode(bytes_data).decode('utf-8')
                link_text = '📥 Download Sovereign PDF Report'
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="sovereign_report.pdf">{link_text}</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error("Please add your 'HF_TOKEN' in the Streamlit Secrets.")

    else:
        st.warning("Please provide a Strategic Context to generate a report.")

st.markdown("---")
st.markdown("Eman El Shafie | Eudaimonics Theory Founder")