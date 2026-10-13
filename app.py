import streamlit as st
import unicodedata

# -----------------------------------------------------------------------------
# Sayfa Yapılandırması ve Başlık
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Biyokimya Bulmacası: Alkoller ve Karboniller",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Özel CSS Tasarımı
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #0f172a;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #475569;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    .crossword-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px 0 25px 0;
        overflow-x: auto;
    }
    .cw-table {
        border-collapse: separate;
        border-spacing: 2px;
        background: #0f172a;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .cw-cell {
        width: 36px;
        height: 36px;
        position: relative;
        text-align: center;
        vertical-align: middle;
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
        font-weight: 700;
        border-radius: 4px;
        user-select: none;
    }
    .cw-empty {
        background-color: #1e293b;
    }
    .cw-letter-cell {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #94a3b8;
    }
    .cw-letter-solved {
        background-color: #dcfce7;
        color: #166534;
        border: 1.5px solid #22c55e;
    }
    .cw-number {
        position: absolute;
        top: 1px;
        left: 2px;
        font-size: 9px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        color: #64748b;
        line-height: 1;
    }
    .clue-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 12px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
    }
    .clue-solved {
        border-left-color: #22c55e !important;
        background: #f0fdf4 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Metin Normalizasyonu (Türkçe Karakter Uyumlu)
# -----------------------------------------------------------------------------
def normalize_tr(text: str) -> str:
    if not text:
        return ""
    mapping = {
        'i': 'İ', 'ı': 'I', 'ğ': 'Ğ', 'ü': 'Ü', 'ş': 'Ş', 'ö': 'Ö', 'ç': 'Ç'
    }
    upper_chars = []
    for ch in text.strip():
        if ch in mapping:
            upper_chars.append(mapping[ch])
        else:
            upper_chars.append(ch.upper())
    res = "".join(upper_chars)
    # I-İ esnekliği (çapraz bulmaca standartlarında kolaylık)
    res = res.replace("İ", "I")
    return res

# -----------------------------------------------------------------------------
# Bulmaca Sözlüğü (10 Soru - 5 Yatay, 5 Dikey)
# Kesişimleri tam doğrulanmış 17x14 matris
# -----------------------------------------------------------------------------
WORDS = {
    # YATAY KELİMELER
    "A1": {
        "num": 2,
        "direction": "YATAY",
        "answer": "AMADORI",
        "clue": "Glukoz ile hemoglobinin amino ucu arasında oluşan Schiff bazının ardından kalıcı ve stabil HbA1c oluşumunu sağlayan düzenlenme (rearrangement) reaksiyonu.",
        "row": 1,
        "col": 2,
        "length": 7
    },
    "A2": {
        "num": 3,
        "direction": "YATAY",
        "answer": "ALDEHIT",
        "clue": "Primer alkollerin bir basamak kontrollü yükseltgenmesiyle oluşan; Tollens ve Fehling testlerine doğrudan pozitif yanıt veren karbonil sınıfı.",
        "row": 4,
        "col": 2,
        "length": 7
    },
    "A3": {
        "num": 7,
        "direction": "YATAY",
        "answer": "KETON",
        "clue": "Sekonder alkollerin yükseltgenmesiyle meydana gelen; asetoasetat ve asetonun kimyasal olarak dahil olduğu karbonil grubu.",
        "row": 7,
        "col": 0,
        "length": 5
    },
    "A4": {
        "num": 8,
        "direction": "YATAY",
        "answer": "ASETON",
        "clue": "Diyabetik ketoasidozda nefeste karakteristik tatlı/meyvemsi kokuya yol açan ve idrarla atılan en küçük keton cismi.",
        "row": 8,
        "col": 6,
        "length": 6
    },
    "A5": {
        "num": 9,
        "direction": "YATAY",
        "answer": "SCHIFF",
        "clue": "Karbonil grubu ile primer aminlerin nükleofilik katılma tepkimesi sonucu oluşan ve azometin bağı (C=N) içeren baz yapısı.",
        "row": 10,
        "col": 8,
        "length": 6
    },
    # DİKEY KELİMELER
    "D1": {
        "num": 1,
        "direction": "DİKEY",
        "answer": "YARIASETAL",
        "clue": "Bir aldehit ile alkolün katılma tepkimesiyle oluşan; glukoz ve galaktoz gibi monosakkaritlerin halkalı yapısının temelini kuran bağ/yapı.",
        "row": 0,
        "col": 2,
        "length": 10
    },
    "D2": {
        "num": 6,
        "direction": "DİKEY",
        "answer": "SUKROZ",
        "clue": "Anomerik karbonları glikozidik bağa katıldığı için serbest fonksiyonel grup açığa çıkaramayan, Fehling/Benedict testlerinde negatif kalan disakkarit.",
        "row": 5,
        "col": 0,
        "length": 6
    },
    "D3": {
        "num": 4,
        "direction": "DİKEY",
        "answer": "ENEDIOL",
        "clue": "Fruktozun alkali ortamda tautomerleşerek aldoza dönüşmesini ve böylece indirgeyici özellik kazanmasını sağlayan kararsız ara ürün formu.",
        "row": 4,
        "col": 5,
        "length": 7
    },
    "D4": {
        "num": 5,
        "direction": "DİKEY",
        "answer": "TOLLENS",
        "clue": "Diamingümüş reaktifi kullanarak aldehitlerin yükseltgenmesi esnasında deney tüpü çeperinde parlak bir gümüş ayna oluşturan ayıraç testi.",
        "row": 4,
        "col": 8,
        "length": 7
    },
    "D5": {
        "num": 10,
        "direction": "DİKEY",
        "answer": "FEHLING",
        "clue": "Bakır(II) iyonlarını tartarat (Rochelle tuzu) ile şelatlayarak tutan ve indirgeyici şeker varlığında kiremit kırmızısı Cu2O çökeltisi veren test.",
        "row": 10,
        "col": 12,
        "length": 7
    }
}

# -----------------------------------------------------------------------------
# Oturum Durumu (Session State) Başlatma
# -----------------------------------------------------------------------------
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {key: "" for key in WORDS.keys()}

if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# -----------------------------------------------------------------------------
# Yan Panel (Sidebar): Bilgi & GitHub Yayın Kılavuzu
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
    st.markdown("### 📌 Biyokimya Ders Notları")
    st.caption("**Konu:** Alkoller ve Karbonil Bileşikleri (Eve Götürülecek Mesajlar)")
    st.info("""
    **Önemli Hatırlatmalar:**
    - **Primer alkoller** $\\rightarrow$ Aldehit $\\rightarrow$ Karboksilik asit
    - **Sekonder alkoller** $\\rightarrow$ Keton
    - **Schiff bazı:** $C=N$ (Azometin bağı)
    - **HbA1c:** Schiff bazı + Amadori düzenlenmesi
    - **Fruktoz:** Enediol tautomerizasyonu ile aldoza döner, testleri pozitif yapar.
    - **$\\beta$-hidroksibütirat:** Keton değildir (sekonder alkoldür), nitroprusiyat testinde saptanamaz!
    """)

    st.markdown("---")
    st.markdown("### 🚀 GitHub & Yayınlama Rehberi")
    st.markdown("""
    Bu uygulamayı Streamlit Cloud'da yayınlamak için:
    1. GitHub'da yeni bir repo açın (Örn: `biyokimya-bulmaca`).
    2. Repoya bu dosyayı `app.py` olarak ekleyin.
    3. Yanına `requirements.txt` oluşturup içine sadece şunu yazın:
       ```
       streamlit
       ```
    4. [share.streamlit.io](https://share.streamlit.io) adresinden reponuzu seçip **Deploy** butonuna tıklayın!
    """)

# -----------------------------------------------------------------------------
# Başlık Alanı
# -----------------------------------------------------------------------------
st.markdown('<h1 class="main-header">🧪 Tıbbi Biyokimya Çapraz Bulmaca</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Alkoller, Aldehitler ve Ketonlar: <i>"Eve Götürülecek Mesajlar"</i> Egzersizi (10 Soru)</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Çözüm Durumunu Hesaplama
# -----------------------------------------------------------------------------
solved_status = {}
correct_count = 0

for key, data in WORDS.items():
    user_val = normalize_tr(st.session_state.user_inputs[key])
    target_val = normalize_tr(data["answer"])
    if user_val == target_val or st.session_state.show_answers:
        solved_status[key] = True
        correct_count += 1
    else:
        solved_status[key] = False

# İlerleme Çubuğu
col_prog, col_btn = st.columns([3, 1])
with col_prog:
    st.progress(correct_count / len(WORDS), text=f"Tamamlanan: {correct_count} / {len(WORDS)}")
with col_btn:
    if correct_count == len(WORDS) and not st.session_state.show_answers:
        st.success("Tebrikler! Bulmacayı Tamamladınız! 🎉")
        st.balloons()

# -----------------------------------------------------------------------------
# 17 Satır x 14 Sütunluk Bulmaca Tablosunun Hazırlanması
# -----------------------------------------------------------------------------
ROWS = 17
COLS = 14

# Izgara hücreleri: (harf, numara, çözüldü_mü)
grid_letters = [["" for _ in range(COLS)] for _ in range(ROWS)]
grid_numbers = [[None for _ in range(COLS)] for _ in range(ROWS)]
grid_solved = [[False for _ in range(COLS)] for _ in range(ROWS)]
grid_active = [[False for _ in range(COLS)] for _ in range(ROWS)]

for key, data in WORDS.items():
    r = data["row"]
    c = data["col"]
    ans = data["answer"]
    is_solved = solved_status[key]
    
    # Başlangıç numarası
    if grid_numbers[r][c] is None:
        grid_numbers[r][c] = data["num"]
        
    for i, ch in enumerate(ans):
        curr_r = r if data["direction"] == "YATAY" else r + i
        curr_c = c + i if data["direction"] == "YATAY" else c
        grid_active[curr_r][curr_c] = True
        
        if is_solved:
            grid_letters[curr_r][curr_c] = ch
            grid_solved[curr_r][curr_c] = True
        elif grid_letters[curr_r][curr_c] == "":
            grid_letters[curr_r][curr_c] = ""

# HTML Tablosunu Oluşturma
table_html = '<div class="crossword-container"><table class="cw-table">'
for r in range(ROWS):
    table_html += '<tr>'
    for c in range(COLS):
        if not grid_active[r][c]:
            table_html += '<td class="cw-cell cw-empty"></td>'
        else:
            cell_class = "cw-cell cw-letter-cell"
            if grid_solved[r][c]:
                cell_class += " cw-letter-solved"
                
            num_html = f'<span class="cw-number">{grid_numbers[r][c]}</span>' if grid_numbers[r][c] is not None else ''
            letter_char = grid_letters[r][c] if grid_letters[r][c] else '&nbsp;'
            table_html += f'<td class="{cell_class}">{num_html}{letter_char}</td>'
    table_html += '</tr>'
table_html += '</table></div>'

st.markdown(table_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Soru ve Cevap Giriş Alanı (İki Kolon: Yatay & Dikey)
# -----------------------------------------------------------------------------
col_yatay, col_dikey = st.columns(2)

with col_yatay:
    st.subheader("↔️ YATAY SORULAR")
    for key, data in WORDS.items():
        if data["direction"] == "YATAY":
            box_class = "clue-box clue-solved" if solved_status[key] else "clue-box"
            status_icon = "✅ " if solved_status[key] else ""
            st.markdown(f"""
            <div class="{box_class}">
                <b>{status_icon}{data['num']}. YATAY ({data['length']} Harf):</b><br>
                {data['clue']}
            </div>
            """, unsafe_allow_html=True)
            
            val = st.text_input(
                f"{data['num']}. Yatay Cevabınız:",
                value=data["answer"] if st.session_state.show_answers else st.session_state.user_inputs[key],
                key=f"input_{key}",
                placeholder=f"{data['length']} harfli cevap...",
                label_visibility="collapsed"
            )
            st.session_state.user_inputs[key] = val

with col_dikey:
    st.subheader("↕️ DİKEY SORULAR")
    for key, data in WORDS.items():
        if data["direction"] == "DİKEY":
            box_class = "clue-box clue-solved" if solved_status[key] else "clue-box"
            status_icon = "✅ " if solved_status[key] else ""
            st.markdown(f"""
            <div class="{box_class}">
                <b>{status_icon}{data['num']}. DİKEY ({data['length']} Harf):</b><br>
                {data['clue']}
            </div>
            """, unsafe_allow_html=True)
            
            val = st.text_input(
                f"{data['num']}. Dikey Cevabınız:",
                value=data["answer"] if st.session_state.show_answers else st.session_state.user_inputs[key],
                key=f"input_{key}",
                placeholder=f"{data['length']} harfli cevap...",
                label_visibility="collapsed"
            )
            st.session_state.user_inputs[key] = val

# -----------------------------------------------------------------------------
# Kontrol ve İşlem Düğmeleri
# -----------------------------------------------------------------------------
st.markdown("---")
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])

with btn_col1:
    if st.button("🔄 Sıfırla / Yeniden Başla", use_container_width=True):
        st.session_state.user_inputs = {key: "" for key in WORDS.keys()}
        st.session_state.show_answers = False
        st.rerun()

with btn_col2:
    label = "🙈 Cevapları Gizle" if st.session_state.show_answers else "💡 Tüm Cevapları Göster"
    if st.button(label, use_container_width=True):
        st.session_state.show_answers = not st.session_state.show_answers
        st.rerun()

with btn_col3:
    if st.button("🎯 Doğrulukları Kontrol Et", type="primary", use_container_width=True):
        if correct_count == len(WORDS):
            st.success("Mükemmel! 10 sorunun tamamı doğru cevaplandı!")
        else:
            st.info(f"{correct_count} / 10 doğru cevap bulundu. Eksik veya hatalı olanları gözden geçirebilirsiniz.")
        st.rerun()
