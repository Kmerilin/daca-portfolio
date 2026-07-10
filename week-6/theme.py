"""
UrbanStyle brändivärvid ja Plotly kujundusmall — kasutab charts_tartu.py.
Teal on sama brändivärv, mida Nädal 5 CEO dashboard kasutas (#009B8D).
"""

COLORS = {
    "white": "#FFFFFF",
    "teal": "#009B8D",
    "navy": "#1B2A4A",
    "pink": "#E91E63",
    "green": "#4CAF50",
}

# Kategooriline värvipalett graafikutele (segmendid, kategooriad jne).
# Piisavalt värve, et katta kuni 6 kategooriat ilma kordumiseta.
COLORWAY = [
    "#009B8D",  # teal (brändivärv)
    "#1B2A4A",  # navy
    "#4FC3B0",  # helereal
    "#C0392B",  # coral/red (kontrast, nt "At Risk"/"Lost" segmendid)
    "#F0B429",  # amber
    "#7F8C8D",  # neutraalne hall
]

# Plotly template-dict — antakse otse `template=` argumendina.
# Plotly aktsepteerib dict-vormingus template'i samamoodi kui go.layout.Template'i.
PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Arial", "color": COLORS["navy"], "size": 13},
        "paper_bgcolor": COLORS["white"],
        "plot_bgcolor": COLORS["white"],
        "colorway": COLORWAY,
        "title": {"font": {"size": 20, "color": COLORS["navy"]}},
        "xaxis": {"gridcolor": "#E5E5E5", "linecolor": "#CCCCCC"},
        "yaxis": {"gridcolor": "#E5E5E5", "linecolor": "#CCCCCC"},
    }
}
