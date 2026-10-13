import streamlit as st

st.set_page_config(
    page_title="Tıbbi Biyokimya Çapraz Bulmaca",
    page_icon="🧩",
    layout="wide"
)

def normalize_text(text: str) -> str:
    if not text:
        return ""
    mapping = str.maketrans("iıüşöçİIÜŞÖÇ", "IIUSOCIIUSOC")
    return text.strip().upper().translate(mapping).replace(" ", "")

# 10 Soruluk Bulmaca Tanımları (5 Yatay, 5 Dikey - Tamamı Birbiriyle Kesişen Ağ)
CLUES = {
    # YATAY SORULAR
    "Y1": {
        "no": 1,
        "yon": "Yatay",
        "soru": "Anomerik karbonları glikozidik bağa katıldığı için Tollens, Fehling ve Benedict testlerinde negatif kalan (indirgeyici olmayan) disakkarit.",
        "cevap": "SUKROZ",
        "harf_sayisi": 6,
        "row": 0, "col": 14
    },
    "Y3": {
        "no": 3,
        "yon": "Yatay",
        "soru": "Bakır(II) iyonlarını tartarat (Rochelle tuzu) ile şelatlayarak alkali ortamda kiremit kırmızısı Cu2O çökeltisi oluşturan klasik ayıraç.",
        "cevap": "FEHLING",
        "harf_sayisi": 7,
        "row": 4, "col": 11
    },
    "Y5": {
        "no": 5,
        "yon": "Yatay",
        "soru": "Glukoz ile hemoglobin amino ucu arasındaki Schiff bazının ardından stabil ve kalıcı HbA1c oluşumunu sağlayan düzenlenme reaksiyonu.",
        "cevap": "AMADORI",
        "harf_sayisi": 7,
        "row": 6, "col": 6
    },
    "Y7": {
        "no": 7,
        "yon": "Yatay",
        "soru": "Diyabetik ketoasidozda nefeste karakteristik kokuya yol açan, solunum ve idrarla atılan gerçek keton yapısındaki keton cismi.",
        "cevap": "ASETON",
        "harf_sayisi": 6,
        "row": 8, "col": 5
    },
    "Y9": {
        "no": 9,
        "yon": "Yatay",
        "soru": "Primer alkollerin bir basamak yükseltgenmesiyle oluşan ve indirgeyici şeker testlerini doğrudan pozitif yapan fonksiyonel grup.",
        "cevap": "ALDEHIT",
        "harf_sayisi": 7,
        "row": 10, "col": 2
    },
    # DİKEY SORULAR
    "D2": {
        "no": 2,
        "yon": "Dikey",
        "soru": "Sekonder alkollerin yükseltgenmesiyle oluşan; tersiyer alkollerin ise yükseltgenmeye dirençli olması sebebiyle oluşturamadığı karbonil bileşiği.",
        "cevap": "KETON",
        "harf_sayisi": 5,
        "row": 0, "col": 16
    },
    "D4": {
        "no": 4,
        "yon": "Dikey",
        "soru": "Bakır(II) iyonlarını sodyum sitrat ile şelatlayıp sodyum karbonatla ılımlı alkali ortam sağlayan tek çözeltili glukoz tarama testi.",
        "cevap": "BENEDICT",
        "harf_sayisi": 8,
        "row": 1, "col": 12
    },
    "D6": {
        "no": 6,
        "yon": "Dikey",
        "soru": "Fruktozun (ketoz) alkali ortamda aldoza dönüşüp indirgeyici testleri pozitif vermesini sağlayan kararsız tautomer ara ürün.",
        "cevap": "ENEDIOL",
        "harf_sayisi": 7,
        "row": 3, "col": 9
    },
    "D8": {
        "no": 8,
        "yon": "Dikey",
        "soru": "Karbonil grubu (C=O) ile primer aminlerin (R-NH2) katılması sonucu oluşan azometin bağı (C=N) içeren baz.",
        "cevap": "SCHIFF",
        "harf_sayisi": 6,
        "row": 8, "col": 6
    },
    "D10": {
        "no": 10,
        "yon": "Dikey",
        "soru": "Diamingümüş kompleksi içeren ve aldehitlerin varlığında deney tüpü çeperinde parlak gümüş ayna oluşturan ayıraç/test.",
        "cevap": "TOLLENS",
        "harf_sayisi": 7,
        "row": 8, "col": 3
    }
}

GRID_ROWS = 15
GRID_COLS = 20

def build_grid_map():
    cells = {}
    for key, item in CLUES.items():
        r, c = item["row"], item["col"]
        direction = item["yon"]
        word = item["cevap"]
        num = item["no"]
        
        for idx, ch in enumerate(word):
            curr_r = r + idx if direction == "Dikey" else r
            curr_c = c if direction == "Dikey" else c + idx
            
            if (curr_r, curr_c) not in cells:
                cells[(curr_r, curr_c)] = {
                    "char": ch,
                    "num": num if idx == 0 else None,
                    "keys": [key]
                }
            else:
                if idx == 0 and cells[(curr_r, curr_c)]["num"] is None:
                    cells[(curr_r, curr_c)]["num"] = num
                cells[(curr_r, curr_c)]["keys"].append(key)
    return cells

grid_map = build_grid_map()

st.title("🧩 Tıbbi Biyokimya Çapraz Bulmaca")
st.caption("Alkoller ve Karbonil Bileşikleri — İnteraktif Pekiştirme Bulmacası")
st.write("")

with st.form("crossword_form"):
    col_left, col_right = st.columns(2)
    user_inputs = {}

    with col_left:
        st.subheader("➡️ YATAY SORULAR")
        for key in ["Y1", "Y3", "Y5", "Y7", "Y9"]:
            item = CLUES[key]
            st.markdown(f"**{item['no']}.** {item['soru']} *({item['harf_sayisi']} Harf)*")
            user_inputs[key] = st.text_input(
                f"Cevabınız ({item['no']}. Yatay):",
                key=f"ans_{key}",
                placeholder=f"{item['harf_sayisi']} harf"
            )
            st.write("")

    with col_right:
        st.subheader("⬇️ DİKEY SORULAR")
        for key in ["D2", "D4", "D6", "D8", "D10"]:
            item = CLUES[key]
            st.markdown(f"**{item['no']}.** {item['soru']} *({item['harf_sayisi']} Harf)*")
            user_inputs[key] = st.text_input(
                f"Cevabınız ({item['no']}. Dikey):",
                key=f"ans_{key}",
                placeholder=f"{item['harf_sayisi']} harf"
            )
            st.write("")

    submitted = st.form_submit_button("Cevapları Kontrol Et", use_container_width=True, type="primary")

results = {}
correct_count = 0

for key, item in CLUES.items():
    ans_cleaned = normalize_text(user_inputs.get(key, ""))
    target = normalize_text(item["cevap"])
    is_ok = (ans_cleaned == target)
    results[key] = is_ok
    if is_ok:
        correct_count += 1

if submitted:
    st.write("---")
    if correct_count == 10:
        st.success(f"Tebrikler! Bulmacayı eksiksiz tamamladınız ({correct_count}/10).")
        st.balloons()
    else:
        st.info(f"Sonuç: 10 sorudan {correct_count} tanesini doğru bildiniz. Yanıtlarınızı gözden geçirebilirsiniz.")

show_all = st.checkbox("Çözümleri Izgarada Göster", value=(correct_count == 10))

st.write("---")
st.subheader("📐 Bulmaca Izgarası")

table_rows = []
for r in range(GRID_ROWS):
    tds = []
    for c in range(GRID_COLS):
        if (r, c) in grid_map:
            cdata = grid_map[(r, c)]
            num_span = f"<span class='cell-num'>{cdata['num']}</span>" if cdata['num'] else ""
            is_solved = any(results.get(k, False) for k in cdata["keys"])
            
            letter_char = ""
            if show_all or is_solved:
                letter_char = f"<span class='cell-char'>{cdata['char']}</span>"
            
            css_class = "solved" if is_solved else "active"
            tds.append(f"<td class='cell {css_class}'>{num_span}{letter_char}</td>")
        else:
            tds.append("<td class='cell black'></td>")
    table_rows.append(f"<tr>{''.join(tds)}</tr>")

grid_html = f"""
<style>
.crossword-table {{
    border-collapse: collapse;
    margin: 15px auto;
    background-color: transparent;
}}
.cell {{
    width: 38px;
    height: 38px;
    border: 1px solid #4A5568;
    text-align: center;
    vertical-align: middle;
    position: relative;
    padding: 0;
}}
.cell.black {{
    background-color: #1A202C;
    border-color: #2D3748;
}}
.cell.active {{
    background-color: #FFFFFF;
    color: #1A202C;
}}
.cell.solved {{
    background-color: #C6F6D5;
    color: #22543D;
    font-weight: bold;
}}
.cell-num {{
    position: absolute;
    top: 2px;
    left: 3px;
    font-size: 9px;
    font-weight: bold;
    color: #2D3748;
    line-height: 1;
}}
.cell-char {{
    font-size: 16px;
    font-family: monospace;
    font-weight: 700;
}}
</style>
<div style="overflow-x: auto;">
<table class="crossword-table">
{''.join(table_rows)}
</table>
</div>
"""

st.markdown(grid_html, unsafe_allow_html=True)
