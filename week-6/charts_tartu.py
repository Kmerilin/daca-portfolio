"""
UrbanStyle Tartu Dashboard — Diagrammide Loomine
=================================================
Tartu kaupluse loole keskenduvad diagrammid: müügitrend (annotatsioonide ja
viitejoonega), TOP 5 toodet ning kliendisegmentide jaotus.

DACA Programm, Nädal 6: Andmelugu (Roll B), Track B.

"""

import math
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Kohalik dashboard/ kaust importteele (theme.py jaoks), et moodul töötaks nii
# Streamlitis kui ka eraldi käivitatuna.
sys.path.insert(0, str(Path(__file__).resolve().parent / "dashboard"))
from theme import COLORS, COLORWAY, PLOTLY_TEMPLATE  # noqa: E402

# Brändivärvid teemast (üks tõeallikas — vt dashboard/theme.py)
BRAND_TEAL = COLORS["teal"]    # #009B8D
ALERT_RED = COLORS["pink"]     # #E91E63 — hoiatus / langus
CARD_GREEN = COLORS["green"]   # #4CAF50 — KPI / positiivne
FONT_FAMILY = PLOTLY_TEMPLATE["layout"]["font"]["family"]


def eur(value, prefix="€"):
    """Vorminda arv Euroopa stiilis: tühik tuhandete eraldajana, koma EI ole eraldaja.

    Nt eur(1234567) -> '€1 234 567'. Tagame, et ükski koma ei jää tuhandete
    eraldajaks üheski Pythonis renderdatud tekstis.
    """
    return f"{prefix}{value:,.0f}".replace(",", " ")


def tartu_kpi_cards(df_tartu, tallinn_monthly_avg, tartu_monthly_avg):
    """
    Eraldiseisev pilt 4 KPI-kaardist (roheline, valge tekst) — sama sisu ja stiil
    mis dashboard'i sektsioon 6, kuid allalaaditava PNG-na.

    Kaardid: Kogukäive · Tellimusi · Keskmine tellimus · Kuukeskmine vs Tallinn.
    """
    total_revenue = df_tartu["total_price"].sum()
    total_orders = len(df_tartu)
    avg_order = total_revenue / total_orders if total_orders else 0
    delta_vs_tln = tartu_monthly_avg - tallinn_monthly_avg

    cards = [
        # (väärtus,                              silt,                  delta-tekst)
        (eur(total_revenue),                     "Kogukäive (Tartu)",   None),
        (f"{total_orders:,}".replace(",", " "),  "Tellimusi",           None),
        (eur(avg_order),                         "Keskmine tellimus",   None),
        (eur(tartu_monthly_avg),                 "Kuukeskmine vs Tallinn",
         f"{eur(delta_vs_tln, prefix='')} € vs Tallinn"),
    ]

    fig = go.Figure()

    n = len(cards)
    OUTER = 0.01      # ääris paberi servast
    GAP = 0.02        # vahe kaartide vahel
    card_w = (1 - 2 * OUTER - (n - 1) * GAP) / n
    y0, y1 = 0.08, 0.92

    for i, (value_str, label_str, delta_str) in enumerate(cards):
        x0 = OUTER + i * (card_w + GAP)
        x1 = x0 + card_w
        cx = (x0 + x1) / 2

        fig.add_shape(                          # roheline kaart, ümarad nurgad
            type="rect", xref="paper", yref="paper",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=CARD_GREEN, line_width=0,
            layer="below",
        )
        fig.add_annotation(                     # silt (ülal)
            x=cx, y=y1 - 0.16,
            xref="paper", yref="paper",
            text=label_str,
            font=dict(size=15, color="white", family=FONT_FAMILY),
            showarrow=False, xanchor="center", yanchor="middle",
            opacity=0.9,
        )
        fig.add_annotation(                     # väärtus (keskel)
            x=cx, y=0.5,
            xref="paper", yref="paper",
            text=f"<b>{value_str}</b>",
            font=dict(size=30, color="white", family=FONT_FAMILY),
            showarrow=False, xanchor="center", yanchor="middle",
        )
        if delta_str:
            fig.add_annotation(                 # delta (all)
                x=cx, y=y0 + 0.13,
                xref="paper", yref="paper",
                text=delta_str,
                font=dict(size=13, color="white", family=FONT_FAMILY),
                showarrow=False, xanchor="center", yanchor="middle",
                opacity=0.95,
            )

    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    fig.update_layout(
        font_family=FONT_FAMILY,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        separators=", ",
    )
    return fig


def _monthly_revenue(df, min_revenue=5000):
    """
    Arvuta igakuine müügitulu ja eemalda hõredad sabakuud.

    Andmestiku lõpus on üksikud peaaegu tühjad kuud (nt €656), mis moonutaksid
    trendi. Jätame alles ainult kuud, kus tulu ületab min_revenue läve.
    """
    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))["total_price"]
        .sum()
        .reset_index()
    )
    monthly = monthly[monthly["total_price"] >= min_revenue].copy()
    monthly["sale_date"] = monthly["sale_date"].dt.to_timestamp()
    return monthly.sort_values("sale_date").reset_index(drop=True)


def tartu_monthly_trend(df_tartu, tallinn_monthly_avg):
    """
    Joondiagramm: Tartu igakuine müügitulu koos andmelooga.

    Lisab:
      - viitejoone Tartu enda kuukeskmisega (kontekst),
      - tippkuu annotatsiooni.

    Märkus: Tallinna punast benchmark-joont ja punast langus-annotatsiooni siin
    EI kuvata (puhas teal joon). Tallinna võrdlus elab KPI-kaartides ja narratiivis.
    `tallinn_monthly_avg` jääb signatuuri (kutsuja annab edasi), kuid on nüüd
    ainult informatiivne.
    """
    monthly = _monthly_revenue(df_tartu)

    fig = px.line(
        monthly,
        x="sale_date",
        y="total_price",
        title="Tartu kaupluse igakuine müügitulu",
        labels={"sale_date": "Kuu", "total_price": "Müügitulu (EUR)"},
        markers=True,
    )

    fig.update_traces(line_color=BRAND_TEAL, line_width=3,
                      marker=dict(size=7, color=BRAND_TEAL))

    fig.update_layout(
        template=PLOTLY_TEMPLATE,   # brändi teema (font, värvid, taust, ruudujooned)
        title_font_size=20,
        hovermode="x unified",
        yaxis_tickformat=",.0f",
        yaxis_tickprefix="€",
        showlegend=False,
        separators=", ",  # koma = koma(kümnend), tühik = tuhandete eraldaja
    )

    # Õrnad punktiirjooned (matchib näidist)
    fig.update_yaxes(griddash="dot")
    fig.update_xaxes(griddash="dot")

    # --- Viitejoon: Tartu enda kuukeskmine (kontekst) ---
    tartu_avg = monthly["total_price"].mean()
    fig.add_hline(
        y=tartu_avg,
        line_dash="dot",
        line_color="gray",
        annotation_text=f"Tartu keskmine: {eur(tartu_avg)}/kuu",
        annotation_position="bottom right",
    )

    if len(monthly) >= 2:
        # --- Annotatsioon 1: tippkuu (ANDME-koordinaadid: xref="x"/yref="y") ---
        # Positsioon sõltub andmetest — nool osutab tegelikule tippkuu punktile.
        idx_peak = monthly["total_price"].idxmax()
        peak = monthly.loc[idx_peak]
        fig.add_annotation(
            x=peak["sale_date"],     # andmeväärtus x-teljel (kuupäev)
            y=peak["total_price"],   # andmeväärtus y-teljel (euro summa)
            xref="x", yref="y",      # viitab telgedele = andme-koordinaadid
            text=(f"Müügitipp {eur(peak['total_price'])}<br>"
                  f"({peak['sale_date']:%b %Y})"),
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor=BRAND_TEAL,
            arrowwidth=2,
            ax=0,
            ay=-45,
            font=dict(size=12, color=BRAND_TEAL),
            bgcolor="white",
            bordercolor=BRAND_TEAL,
            borderwidth=1,
            borderpad=4,
        )

        # --- Annotatsioon 2: madalpunkt (ANDME-koordinaadid) ---
        idx_low = monthly["total_price"].idxmin()
        low = monthly.loc[idx_low]
        fig.add_annotation(
            x=low["sale_date"],
            y=low["total_price"],
            xref="x", yref="y",      # andme-koordinaadid
            text=(f"Madalseis {eur(low['total_price'])}<br>"
                  f"({low['sale_date']:%b %Y})"),
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor=ALERT_RED,
            arrowwidth=2,
            ax=0,
            ay=40,
            font=dict(size=11, color=ALERT_RED),
            bgcolor="white",
            bordercolor=ALERT_RED,
            borderwidth=1,
            borderpad=4,
        )

    # --- Annotatsioon 3: kontekstimärge (PABERI-koordinaadid) ---
    # Positsioon sõltub diagrammi mõõtmetest (0-1), MITTE andmetest. Jääb alati
    # samasse nurka, olenemata sellest, kuidas andmed muutuvad.
    fig.add_annotation(
        x=0.01,                  # 1% vasakult (diagrammi laiusest)
        y=0.02,                  # 2% alt (diagrammi kõrgusest)
        xref="paper",            # viitab diagrammi laiusele
        yref="paper",            # viitab diagrammi kõrgusele
        text="Allikas: UrbanStyle müügiandmed · ainult Tartu kauplus",
        showarrow=False,
        xanchor="left", yanchor="bottom",
        font=dict(size=10, color="gray"),
    )

    return fig


def tartu_top_products(df_tartu, top_n=5):
    """Horisontaalne tulpdiagramm: Tartu TOP N toodet müügitulu järgi."""
    product_revenue = (
        df_tartu.groupby("product_name")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
        .head(top_n)
        .sort_values("total_price", ascending=True)  # visuaaliks kasvavalt
    )

    fig = px.bar(
        product_revenue,
        x="total_price",
        y="product_name",
        orientation="h",
        title=f"Tartu TOP {top_n} toodet müügitulu järgi",
        labels={"total_price": "Müügitulu (EUR)", "product_name": "Toode"},
        color="total_price",
        color_continuous_scale="Teal",
        text="total_price",
    )

    fig.update_traces(texttemplate="€%{text:,.0f}", textposition="inside",
                      insidetextanchor="end")

    fig.update_layout(
        template=PLOTLY_TEMPLATE,   # brändi teema
        title_font_size=20,
        showlegend=False,
        xaxis_tickformat=",.0f",
        xaxis_tickprefix="€",
        coloraxis_showscale=False,
        separators=", ",  # tühik tuhandete eraldajana
    )

    return fig


def tartu_segments(df_tartu):
    """Sektordiagramm: Tartu müügitulu jaotus kliendisegmentide (loyalty_tier) kaupa."""
    seg = df_tartu.copy()
    seg["loyalty_tier"] = (
        seg["loyalty_tier"].fillna("Registreerimata").str.capitalize()
    )

    seg_revenue = (
        seg.groupby("loyalty_tier")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
    )

    fig = px.pie(
        seg_revenue,
        values="total_price",
        names="loyalty_tier",
        title="Tartu müügitulu kliendisegmentide kaupa",
        color_discrete_sequence=COLORWAY,   # brändi värvijada
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>"
                      "Tulu: €%{value:,.0f}<br>"
                      "Osakaal: %{percent}<extra></extra>",
    )

    fig.update_layout(template=PLOTLY_TEMPLATE, title_font_size=20, separators=", ")

    return fig


def create_combined_figure(df_tartu, tallinn_monthly_avg):
    """
    Üks kombineeritud pilt kõigi diagrammide ja KPI-kaartidega (PowerPointi slaid).
    Mõõdud: 1920×1080 px (16:9, standard PowerPointi slaid).

    Layout (3 rida × 2 veerg):
      Rida 1: 4 KPI kaarti (täislaiuses riba ÜLASERVAS, valged kaardid)
      Rida 2: Müügitrend (täislaiuses, colspan 2)
      Rida 3: TOP 5 toodet (vas) | Sektordiagramm (par)

    KPI-kaardid joonistatakse paber-koordinaatides Rida 1 y-vööndis, üle peidetud
    dummy-subploti. Stiil järgib näidisslaidi: hall slaiditaust, valged paneelid,
    tsentreeritud teal pealkirjad, esimene KPI väärtus punane.
    """
    # ── Andmete ettevalmistus ──────────────────────────────────
    monthly = _monthly_revenue(df_tartu)
    # Kaleido ei suuda pandas Timestamp objekte serialiseerida
    monthly["sale_date"] = monthly["sale_date"].dt.strftime("%Y-%m")
    tartu_avg = monthly["total_price"].mean()

    product_revenue = (
        df_tartu.groupby("product_name")["total_price"]
        .sum().reset_index()
        .sort_values("total_price", ascending=False)
        .head(5)
        .sort_values("total_price", ascending=True)
    )

    seg = df_tartu.copy()
    seg["loyalty_tier"] = seg["loyalty_tier"].fillna("Registreerimata").str.capitalize()
    seg_revenue = (
        seg.groupby("loyalty_tier")["total_price"]
        .sum().reset_index()
        .sort_values("total_price", ascending=False)
    )

    total_rev  = df_tartu["total_price"].sum()
    n_orders   = len(df_tartu)
    avg_order  = total_rev / n_orders if n_orders else 0

    peak_idx  = monthly["total_price"].idxmax()
    peak_val  = monthly.loc[peak_idx, "total_price"]
    peak_date = monthly.loc[peak_idx, "sale_date"]
    last_val  = monthly.iloc[-1]["total_price"]
    last_date = monthly.iloc[-1]["sale_date"]
    prev_val  = monthly.iloc[-2]["total_price"]
    prev_date = monthly.iloc[-2]["sale_date"]
    mo_drop   = (last_val - prev_val) / prev_val * 100
    peak_drop = (last_val - peak_val) / peak_val * 100
    vs_tln    = tartu_avg / tallinn_monthly_avg * 100

    # ── Subplots ───────────────────────────────────────────────
    # Rida 1 = KPI-riba (peidetud dummy), Rida 2 = trend,
    # Rida 3 = bar | pie | juhtide kokkuvõte (tekst)
    #
    # Rida 3 on nüüd 3 veergu: TOP 5 (vas) | sektordiagramm (kesk) |
    # juhtide kokkuvõte (par, all paremas). Diagrammid kitsenevad, et tekstile ruumi teha.
    # Rida 3 algab tühja vahekolonniga (~10%), et bar | pie | kokkuvõte
    # nihkuks paremale. Ülemised read katavad endiselt täislaiuse (colspan 4).
    fig = make_subplots(
        rows=3, cols=4,
        specs=[
            [{"colspan": 4, "type": "xy"}, None, None, None],   # KPI-riba (dummy)
            [{"colspan": 4, "type": "xy"}, None, None, None],   # trend
            [{"type": "xy"}, {"type": "xy"}, {"type": "domain"}, {"type": "xy"}],  # vahe | bar | pie | kokkuvõte
        ],
        subplot_titles=[
            "",                              # KPI riba — pealkiri peidetud
            "Tartu igakuine müügitulu",
            "",                              # vahekolonn — pealkiri puudub
            "TOP 5 toodet müügitulu järgi",
            "Kliendisegmendid (loyalty)",
            "Juhtide kokkuvõte",
        ],
        column_widths=[0.10, 0.34, 0.24, 0.32],
        row_heights=[0.16, 0.46, 0.38],
        vertical_spacing=0.07,
        horizontal_spacing=0.04,
    )

    # Peida vahekolonni teljed (Rida 3, col 1 → x3/y3)
    fig.update_xaxes(visible=False, range=[0, 1], row=3, col=1)
    fig.update_yaxes(visible=False, range=[0, 1], row=3, col=1)

    # ── Rida 1: peidetud dummy subplot — taustaks KPI-kaartidele ──
    fig.add_trace(go.Scatter(
        x=[0], y=[0.5], mode="markers",
        marker=dict(opacity=0, size=1),
        showlegend=False, hoverinfo="none",
    ), row=1, col=1)
    fig.update_xaxes(visible=False, range=[0, 1], row=1, col=1)
    fig.update_yaxes(visible=False, range=[0, 1], row=1, col=1)

    # ── Rida 2: müügitrend ────────────────────────────────────
    # Trend on subplot 2 → teljed x2 / y2
    fig.add_trace(go.Scatter(
        x=monthly["sale_date"],
        y=monthly["total_price"],
        mode="lines+markers",
        line=dict(color=BRAND_TEAL, width=3),
        marker=dict(size=7, color=BRAND_TEAL),
        showlegend=False,
        hovertemplate="%{x}: €%{y:,.0f}<extra></extra>",
    ), row=2, col=1)

    # Hall Tartu-keskmine joon (kontekst).
    fig.add_hline(
        y=tartu_avg, line_dash="dot", line_color="gray",
        annotation_text=f"Tartu keskmine: {eur(tartu_avg)}/kuu",
        annotation_position="bottom right",
        row=2, col=1,
    )

    # Tallinna benchmark-joon — neutraalne teal (mitte punane).
    fig.add_hline(
        y=tallinn_monthly_avg, line_dash="dash", line_color=BRAND_TEAL,
        annotation_text=f"Tallinna keskmine: {eur(tallinn_monthly_avg)}/kuu",
        annotation_position="top right",
        annotation_font_color=BRAND_TEAL,
        row=2, col=1,
    )

    if len(monthly) >= 2:
        # Annotatsioon 1: tippkuu
        fig.add_annotation(
            x=peak_date, y=peak_val, xref="x2", yref="y2",
            text=f"Tippkuu {eur(peak_val)}<br>({peak_date})",
            showarrow=True, arrowhead=2, arrowcolor=BRAND_TEAL, arrowwidth=2,
            ax=0, ay=-38,
            font=dict(size=9, color=BRAND_TEAL),
            bgcolor="white", bordercolor=BRAND_TEAL, borderwidth=1,
        )
        # Annotatsioon 2: viimaste kuude langus (kuust kuusse)
        fig.add_annotation(
            x=last_date, y=last_val, xref="x2", yref="y2",
            text=f"Langus {mo_drop:+.0f}%<br>({prev_date}→{last_date})",
            showarrow=True, arrowhead=2, arrowcolor="#555555", arrowwidth=2,
            ax=-30, ay=-42,
            font=dict(size=9, color="#333333"),
            bgcolor="white", bordercolor="#999999", borderwidth=1,
        )

    fig.update_yaxes(tickformat=",.0f", tickprefix="€",
                     gridcolor="#e6e6e6", griddash="dot", row=2, col=1)
    fig.update_xaxes(gridcolor="#e6e6e6", griddash="dot", row=2, col=1)

    # ── Rida 3 col 2: TOP 5 toodet ────────────────────────────
    fig.add_trace(go.Bar(
        x=product_revenue["total_price"],
        y=product_revenue["product_name"],
        orientation="h",
        marker_color=BRAND_TEAL,
        text=product_revenue["total_price"].map(eur),
        textposition="inside",
        insidetextanchor="end",
        showlegend=False,
        hovertemplate="%{y}<br>€%{x:,.0f}<extra></extra>",
    ), row=3, col=2)

    fig.update_xaxes(tickformat=",.0f", tickprefix="€", showgrid=False, row=3, col=2)
    fig.update_yaxes(showgrid=False, row=3, col=2)

    # Annotatsioon tulpdiagrammile: enimmüüdud toode (product_revenue on
    # kasvavalt sorteeritud → viimane rida = tippmüüja). Tekst paremal,
    # nool osutab tippmüüja tulba otsale. Bar on nüüd x4/y4.
    if len(product_revenue) >= 1:
        top_prod = product_revenue.iloc[-1]
        bar_total = product_revenue["total_price"].sum()
        top_share = top_prod["total_price"] / bar_total * 100 if bar_total else 0
        fig.add_annotation(
            x=top_prod["total_price"], y=top_prod["product_name"],
            xref="x4", yref="y4",
            text=f"Tippmüüja<br>{top_share:.0f}% TOP 5 tulust",
            showarrow=True, arrowhead=2, arrowcolor=BRAND_TEAL, arrowwidth=2,
            ax=60, ay=-6,         # tekstikast paremal, nool vasakule tulba otsa
            font=dict(size=9, color=BRAND_TEAL),
            bgcolor="white", bordercolor=BRAND_TEAL, borderwidth=1,
            xanchor="left", align="left",
        )

    # ── Rida 3 col 3: sektordiagramm ──────────────────────────
    fig.add_trace(go.Pie(
        values=seg_revenue["total_price"],
        labels=seg_revenue["loyalty_tier"],
        textinfo="percent+label",
        textposition="inside",
        marker=dict(colors=COLORWAY[:len(seg_revenue)]),
        hovertemplate="<b>%{label}</b><br>€%{value:,.0f}<br>%{percent}<extra></extra>",
        showlegend=False,
    ), row=3, col=3)

    # Annotatsioon sektordiagrammile: suurim segment (seg_revenue on
    # kahanevalt sorteeritud → esimene rida = suurim). Tekst paremal,
    # nool osutab suurima segmendi sektorile.
    #
    # Sektordiagramm algab kell 12 ja liigub PÄRIPÄEVA. Suurim segment hõivab
    # nurga 0 → frac·360°; selle keskpunkt on poolel teel. Arvutame sektori
    # keskpunktile vastava punkti paber-koordinaatides ja suuname noole sinna.
    if len(seg_revenue) >= 1:
        top_seg = seg_revenue.iloc[0]
        seg_total = seg_revenue["total_price"].sum()
        seg_frac = top_seg["total_price"] / seg_total if seg_total else 0
        seg_share = seg_frac * 100

        # Pie domeen paber-koordinaatides (4-veeruline layout, vahekolonniga)
        pie_x0, pie_x1 = 0.467, 0.678
        pie_y0, pie_y1 = 0.0, 0.327
        pie_cx = (pie_x0 + pie_x1) / 2
        pie_cy = (pie_y0 + pie_y1) / 2
        # Raadius: poole sektori sügavusele (0.5·R), et nool jõuaks tüki sisse.
        # Paber-koordinaadid pole ruudukujulised (kuvasuhe 1920×1080), seega
        # teisendame x ja y eraldi.
        rx = (pie_x1 - pie_x0) / 2 * 0.55
        ry = (pie_y1 - pie_y0) / 2 * 1.5   # suurem → nooleots kõrgemale, sildist eemale
        # Nurk kell-12-st päripäeva = 90° − (sweep/2) tavakoordinaadistikus
        mid_deg = (seg_frac / 2) * 360.0
        theta = math.radians(90.0 - mid_deg)
        point_x = pie_cx + rx * math.cos(theta)
        point_y = pie_cy + ry * math.sin(theta)

        # Tekstikast sektordiagrammi üleval-paremal (väldib vasakpoolseid
        # sektori-silte ja juhtide kokkuvõtet). Nool osutab suurima segmendi
        # sektorisse.
        fig.add_annotation(
            x=point_x, y=point_y, xref="paper", yref="paper",
            text=(f"Suurim segment:<br><b>{top_seg['loyalty_tier']}</b> "
                  f"({seg_share:.0f}% tulust)"),
            showarrow=True, arrowhead=2, arrowcolor="#333333", arrowwidth=2,
            ax=-5, ay=-80,        # tekstikast üleval-paremal, nool alla-vasakule
            font=dict(size=10, color="#333333", family=FONT_FAMILY),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#999999", borderwidth=1, borderpad=4,
            xanchor="left", align="left",
        )

    # ── Rida 3 col 4: juhtide kokkuvõte (tekst, all paremas) ──
    # Peidetud dummy subplot taustaks; tekst paigutatakse selle domeeni (x5/y5).
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers",
        marker=dict(opacity=0, size=1),
        showlegend=False, hoverinfo="none",
    ), row=3, col=4)
    fig.update_xaxes(visible=False, range=[0, 1], row=3, col=4)
    fig.update_yaxes(visible=False, range=[0, 1], row=3, col=4)

    # Sisu järgib rakenduse st.error juhtide kokkuvõtet.
    summary_text = (
        f"<b>Tartu on langustrendis ja jääb selgelt Tallinnale alla.</b><br><br>"
        f"• Kuukeskmine vaid <b>{eur(tartu_avg)}</b> — ~{vs_tln:.0f}%<br>"
        f"&nbsp;&nbsp;Tallinna keskmisest ({eur(tallinn_monthly_avg)}/kuu).<br>"
        f"&nbsp;&nbsp;Tartu teenib umbes poole vähem.<br><br>"
        f"• Järsk kukkumine tipust:<br>"
        f"&nbsp;&nbsp;{eur(peak_val)} ({peak_date}) → {eur(last_val)} "
        f"({last_date}), <b>{peak_drop:+.0f}%</b>.<br><br>"
        f"• Põhjused: konkurent Tartu kesklinnas +<br>"
        f"&nbsp;&nbsp;online kannibaliseerib.<br><br>"
        f"• Tegevus: audit, kohalik turundus,<br>"
        f"&nbsp;&nbsp;tootevaliku kohandamine."
    )
    fig.add_annotation(
        x=0.0, y=0.97, xref="x5 domain", yref="y5 domain",
        text=summary_text,
        showarrow=False,
        font=dict(size=11, family=FONT_FAMILY, color="#333333"),
        align="left", xanchor="left", yanchor="top",
        bgcolor="rgba(248, 240, 240, 0.95)",
        bordercolor=ALERT_RED, borderwidth=1, borderpad=10,
    )

    # ── KPI kaardid — 4 kõrvuti ülaservas (paper-koordinaadid) ─
    #
    # Riba ulatub täislaiuses x ∈ [0.04, 0.99]. Stiil näidisslaidi järgi:
    # valge kaart, õhuke hall ääris, ilma teal accent-ribata. Esimene väärtus
    # (Kogukäive) on PUNANE pilgupüüdjaks, ülejäänud tumehallid.
    #   value font 26, label font 12.
    #
    # Rida 1 y-vöönd ≈ [0.792, 0.918] (vt make_subplots kommentaari ülal).
    KPI_CARDS = [
        # (väärtus,                              silt,                väärtuse värv)
        (eur(total_rev),                          "Kogukäive",         "#333333"),
        (f"{n_orders:,}".replace(",", " "),       "Tellimusi",         "#333333"),
        (eur(avg_order),                          "Keskmine tellimus", "#333333"),
        (eur(tartu_avg),                          "Kuukeskmine",       "#333333"),
    ]

    # Kaardid koondatud kokku (kitsam riba, väiksem vahe) ja tõstetud kõrgemale.
    STRIP_X0, STRIP_X1 = 0.18, 0.82   # kitsam, tsentreeritud riba
    OUTER_PAD = 0.0
    INNER_GAP = 0.004                  # kaardid tihedalt koos
    n_cards = len(KPI_CARDS)
    avail_w = (STRIP_X1 - STRIP_X0) - 2 * OUTER_PAD - (n_cards - 1) * INNER_GAP
    CARD_W = avail_w / n_cards

    CARD_Y0, CARD_Y1 = 0.880, 0.952   # tõstetud ülespoole (jääb tiitli alla)
    cy_value = CARD_Y0 + (CARD_Y1 - CARD_Y0) * 0.62   # väärtus ülemises osas
    cy_label = CARD_Y0 + (CARD_Y1 - CARD_Y0) * 0.26   # silt alumises osas

    for i, (value_str, label_str, value_color) in enumerate(KPI_CARDS):
        x0 = STRIP_X0 + OUTER_PAD + i * (CARD_W + INNER_GAP)
        x1 = x0 + CARD_W
        cx = (x0 + x1) / 2

        fig.add_shape(                          # valge kaart, õhuke hall ääris
            type="rect", xref="paper", yref="paper",
            x0=x0, y0=CARD_Y0, x1=x1, y1=CARD_Y1,
            fillcolor="white", line_color="#dddddd", line_width=1,
            layer="above",
        )
        fig.add_annotation(                     # väärtus (esimene punane)
            x=cx, y=cy_value,
            xref="paper", yref="paper",
            text=f"<b>{value_str}</b>",
            font=dict(size=26, color=value_color, family=FONT_FAMILY),
            showarrow=False, xanchor="center", yanchor="middle",
        )
        fig.add_annotation(                     # silt
            x=cx, y=cy_label,
            xref="paper", yref="paper",
            text=label_str,
            font=dict(size=12, color="#555555", family=FONT_FAMILY),
            showarrow=False, xanchor="center", yanchor="middle",
        )

    # ── Subplot-pealkirjad: tsentreeritud + teal (näidise stiil) ──
    for ann in fig.layout.annotations:
        # subplot_titles on lisatud annotatsioonidena; KPI/väärtuse annotatsioonid
        # on juba xref="paper" + custom font, neid me ei puuduta.
        if ann.text in ("Tartu igakuine müügitulu",
                        "TOP 5 toodet müügitulu järgi",
                        "Kliendisegmendid (loyalty)",
                        "Juhtide kokkuvõte"):
            ann.font = dict(color=BRAND_TEAL, size=15, family=FONT_FAMILY)

    # ── Üldine layout — 1920×1080 (16:9) ──────────────────────
    # Rakendame brändi teema (font, värvid), kuid SLAID kasutab teadlikult valgeid
    # paneele ja tsentreeritud tiitlit — kirjutame need teema peale tagasi.
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title=dict(
            text="UrbanStyle — Tartu Kaupluse Ülevaade",
            font=dict(size=18, family=FONT_FAMILY),
            x=0.5, xanchor="center",
        ),
        height=1080,
        width=1920,
        paper_bgcolor="white",     # slaidi valge taust
        plot_bgcolor="white",      # valged paneelid (mitte teema hall)
        # Suurem vasak veeris, et tulpdiagrammi toodete nimed ei jääks lõikesse.
        margin=dict(t=60, b=28, l=170, r=50),
        showlegend=False,
        separators=", ",           # tühik tuhandete eraldajana
    )

    return fig
