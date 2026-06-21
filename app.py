import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def _pl_sort_key(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    zamiany = {
        "ą": "a~", "ć": "c~", "ę": "e~", "ł": "l~", "ń": "n~", 
        "ó": "o~", "ś": "s~", "ź": "z~", "ż": "z~~"
    }
    for pol, ang in zamiany.items():
        text = text.replace(pol, ang)
    return text

st.set_page_config(page_title="Dashboard Filmowy", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("filmy.csv")
    df["średnia"] = (df["rating_1_votes"]*1 + df["rating_2_votes"]*2 + 
                     df["rating_3_votes"]*3 + df["rating_4_votes"]*4 + 
                     df["rating_5_votes"]*5 + df["rating_6_votes"]*6 + 
                     df["rating_7_votes"]*7 + df["rating_8_votes"]*8 + 
                     df["rating_9_votes"]*9 + df["rating_10_votes"]*10) / df["votes"]
    
    jezyki = {
        "en": "angielski", "es": "hiszpański", "fr": "francuski", "de": "niemiecki",
        "it": "włoski", "ja": "japoński", "ko": "koreański", "zh": "chiński",
        "ru": "rosyjski", "pl": "polski", "pt": "portugalski", "hi": "hindi",
        "sv": "szwedzki", "da": "duński", "no": "norweski", "fi": "fiński",
        "nl": "holenderski", "tr": "turecki", "ar": "arabski", "th": "tajski",
        "is": "islandzki", "cs": "czeski", "hu": "węgierski", "el": "grecki",
        "fa": "perski", "hy": "ormiański", "id": "indonezyjski", "vi": "wietnamski",
        "lv": "łotewski", "sh": "serbo-chorwacki", "sr": "serbski", "te": "telugu"
    }
    
    kraje = {
        "us": "Stany Zjednoczone", "gb": "Wielka Brytania", "au": "Australia",
        "fr": "Francja", "de": "Niemcy", "jp": "Japonia", "kr": "Korea Południowa",
        "ca": "Kanada", "it": "Włochy", "es": "Hiszpania", "pl": "Polska",
        "nz": "Nowa Zelandia", "in": "Indie", "cn": "Chiny", "mx": "Meksyk",
        "br": "Brazylia", "ru": "Rosja", "se": "Szwecja", "dk": "Dania",
        "ie": "Irlandia", "be": "Belgia", "ar": "Argentyna", "za": "RPA",
        "nl": "Holandia", "hk": "Hongkong", "tw": "Tajwan", "cz": "Czechy",
        "hu": "Węgry", "is": "Islandia", "ch": "Szwajcaria", "at": "Austria",
        "su": "Związek Radziecki", "xc": "Czechosłowacja", "yu": "Jugosławia",
        "ae": "Zjednoczone Emiraty Arabskie", "fi": "Finlandia", "bm": "Bermudy",
        "bw": "Botswana", "no": "Norwegia", "gr": "Grecja", "tr": "Turcja",
        "hr": "Chorwacja", "id": "Indonezja", "il": "Izrael", "ir": "Iran",
        "kw": "Kuwejt", "lv": "Łotwa", "th": "Tajlandia"
    }
    
    if "language" in df.columns:
        df["language"] = df["language"].str.lower().map(jezyki).fillna(df["language"])
        
    if "country" in df.columns:
        df["country"] = df["country"].str.lower().map(kraje).fillna(df["country"])

    return df

df = load_data()

st.sidebar.title("Nawigacja")
page = st.sidebar.radio("Wybierz podstronę:", 
                        ["Strona główna",
                         "Profil wybranego filmu",
                         "Przegląd bazy filmów", 
                         "Rozkład ocen widzów", 
                         "Wpływ czasu trwania na ocenę",
                         "Ewolucja kina w czasie",
                         "Ranking najwybitniejszych reżyserów",
                         "Analiza gatunków filmowych",
                         "Mapa drzewa kina"])

if page == "Strona główna":
    st.title("Analiza danych filmowych z Trakt.tv")
    st.markdown("### Autorzy")
    st.write("Stanisław Olek 275946, Maciej Kędzierski 275963")
    
    st.markdown("### Źródło danych")
    st.write("Dane zostały pozyskane z oficjalnego API serwisu Trakt.tv. Zbiór obejmuje najpopularniejsze filmy z lat 1960-2024 wraz ze szczegółowymi statystykami ich oglądalności i ocenami widzów.")
    
    st.markdown("### Cel analizy")
    st.info("Celem analizy w tym dashboardzie jest interaktywna eksploracja cech, które w największym stopniu kształtują oceny widzów. Weryfikujemy m.in. wpływ czasu trwania produkcji na jej końcową ocenę, analizujemy historyczne trendy w kinie na przestrzeni dekad oraz badamy dorobek reżyserów pod kątem regularnego dostarczania najwyżej ocenianych produkcji.")

elif page == "Profil wybranego filmu": 
    st.title("Szczegółowy profil filmu")
    st.write("Wybierz film z listy, aby zobaczyć jego statystyki oraz dokładny rozkład wszystkich oddanych głosów (od 1 do 10).")

    tytuly = sorted(df["title"].dropna().unique(), key=_pl_sort_key)
    wybrany_film = st.selectbox("Wyszukaj i wybierz film:", tytuly)

    dane_filmu = df[df["title"] == wybrany_film].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Średnia ocena", round(dane_filmu["średnia"], 2))
    
    votes_str = "{:,}".format(int(dane_filmu["votes"])).replace(",", " ")
    col2.metric("Liczba głosów", votes_str)
    
    col3.metric("Czas trwania (min)", int(dane_filmu["runtime"]))
    col4.metric("Kraj produkcji", str(dane_filmu["country"]))

    st.markdown("---")
    st.markdown("### Pozostałe informacje o filmie")
    
    detale1, detale2 = st.columns(2)
    
    rok = int(dane_filmu["year"])
    rezyser = dane_filmu.get("director", "Brak danych")
    aktorzy = dane_filmu.get("actors", "Brak danych")
    gatunki = dane_filmu.get("genres", "Brak danych")
    jezyk = dane_filmu.get("language", "Brak danych")
    
    kategoria = dane_filmu.get("certification", "Brak danych")
    watchers_str = "{:,}".format(int(dane_filmu.get("watchers", 0))).replace(",", " ")
    komentarze = int(dane_filmu.get("comment_count", 0))
    tlumaczenia = int(dane_filmu.get("translations_count", 0))

    with detale1:
        st.markdown(f"**Rok premiery:** {rok}")
        st.markdown(f"**Reżyser:** {rezyser}")
        st.markdown(f"**Aktorzy:** {aktorzy}")
        st.markdown(f"**Gatunki:** {gatunki}")
        st.markdown(f"**Język oryginalny:** {jezyk}")
        
    with detale2:
        st.markdown(f"**Kategoria wiekowa:** {kategoria}")
        st.markdown(f"**Obejrzano (watchers):** {watchers_str}")
        st.markdown(f"**Liczba komentarzy:** {komentarze}")
        st.markdown(f"**Dostępne tłumaczenia:** {tlumaczenia}")
        
    st.markdown("---")

    oceny_kolumny = [f"rating_{i}_votes" for i in range(1, 11)]
    oceny_wartosci = dane_filmu[oceny_kolumny].values

    df_oceny = pd.DataFrame({
        "Ocena": [str(i) for i in range(1, 11)],
        "Liczba głosów": oceny_wartosci
    })

    fig_oceny = px.bar(df_oceny, 
                    x="Ocena", 
                    y="Liczba głosów",
                    title=f"Rozkład oddanych głosów dla: {wybrany_film}",
                    color="Ocena",
                    color_discrete_sequence=px.colors.sequential.Plasma,
                    labels={"Ocena": "Gwiazdki (1-10)", "Liczba głosów": "Liczba oddanych głosów"})

    fig_oceny.update_layout(showlegend=False)
    fig_oceny.update_xaxes(showgrid=False)
    fig_oceny.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")

    st.plotly_chart(fig_oceny, use_container_width=True)

elif page == "Przegląd bazy filmów":
    st.title("Przegląd bazy filmów")
    st.write("Poniższa tabela prezentuje kluczowe cechy liczbowe i kategoryczne. Kliknij nagłówek, aby posortować według wybranej kolumny. Użyj opcji filtrowania, aby zawęzić wyniki do interesujących Cię filmów.")
    
    kolumny_do_wyswietlenia = [
        "title", "year", "director", "country", 
        "language", "runtime", "watchers", "votes", 
        "comment_count", "translations_count", "średnia"
    ]
    
    dostepne_kolumny = [col for col in kolumny_do_wyswietlenia if col in df.columns]
    
    df_filtered = df.copy()
    
    with st.expander("Opcje filtrowania tabeli"):
        f1_col1, f1_col2, f1_col3, f1_col4 = st.columns(4)
        
        with f1_col1:
            min_rok = int(df["year"].min())
            max_rok = int(df["year"].max())
            wybrany_rok = st.slider("Rok premiery", min_value=min_rok, max_value=max_rok, value=(min_rok, max_rok))
            
        with f1_col2:
            min_ocena = float(df["średnia"].min())
            max_ocena = float(df["średnia"].max())
            wybrana_ocena = st.slider("Średnia ocena", min_value=min_ocena, max_value=max_ocena, value=(min_ocena, max_ocena))
            
        with f1_col3:
            min_czas = int(df["runtime"].min())
            max_czas = int(df["runtime"].max())
            wybrany_czas = st.slider("Czas trwania (min)", min_value=min_czas, max_value=max_czas, value=(min_czas, max_czas))
            
        with f1_col4:
            dostepni_rezyserzy = sorted(df["director"].dropna().astype(str).unique(), key=_pl_sort_key)
            wybrani_rezyserzy = st.multiselect("Reżyser", options=dostepni_rezyserzy)

        f2_col1, f2_col2, f2_col3, f2_col4 = st.columns(4)

        with f2_col1:
            min_obejrzane = int(df["watchers"].min())
            max_obejrzane = int(df["watchers"].max())
            wybrane_obejrzane = st.slider("Liczba obejrzanych (watchers)", min_value=min_obejrzane, max_value=max_obejrzane, value=(min_obejrzane, max_obejrzane), step=1000)

        with f2_col2:
            min_glosy = int(df["votes"].min())
            max_glosy = int(df["votes"].max())
            wybrane_glosy = st.slider("Liczba głosów", min_value=min_glosy, max_value=max_glosy, value=(min_glosy, max_glosy), step=1000)
            
        with f2_col3:
            dostepne_kraje = sorted(df["country"].dropna().astype(str).unique(), key=_pl_sort_key)
            wybrane_kraje = st.multiselect("Kraj produkcji", options=dostepne_kraje)
            
        with f2_col4:
            dostepne_jezyki = sorted(df["language"].dropna().astype(str).unique(), key=_pl_sort_key)
            wybrane_jezyki = st.multiselect("Język", options=dostepne_jezyki)
            
    df_filtered = df_filtered[(df_filtered["year"] >= wybrany_rok[0]) & (df_filtered["year"] <= wybrany_rok[1])]
    df_filtered = df_filtered[(df_filtered["średnia"] >= wybrana_ocena[0]) & (df_filtered["średnia"] <= wybrana_ocena[1])]
    df_filtered = df_filtered[(df_filtered["runtime"] >= wybrany_czas[0]) & (df_filtered["runtime"] <= wybrany_czas[1])]
    df_filtered = df_filtered[(df_filtered["watchers"] >= wybrane_obejrzane[0]) & (df_filtered["watchers"] <= wybrane_obejrzane[1])]
    df_filtered = df_filtered[(df_filtered["votes"] >= wybrane_glosy[0]) & (df_filtered["votes"] <= wybrane_glosy[1])]
    
    if len(wybrani_rezyserzy) > 0:
        df_filtered = df_filtered[df_filtered["director"].isin(wybrani_rezyserzy)]
        
    if len(wybrane_kraje) > 0:
        df_filtered = df_filtered[df_filtered["country"].isin(wybrane_kraje)]
        
    if len(wybrane_jezyki) > 0:
        df_filtered = df_filtered[df_filtered["language"].isin(wybrane_jezyki)]
        
    st.write(f"Znaleziono rekordów: **{len(df_filtered)}**")
    st.dataframe(df_filtered[dostepne_kolumny], use_container_width=True)

elif page == "Rozkład ocen widzów":
    st.title("Rozkład średnich ocen filmów")
    st.write("Poniższy wykres to statyczny histogram wygenerowany za pomocą biblioteki Matplotlib, pokazujący jak rozkładają się wyliczone średnie oceny w naszym zbiorze 5000 filmów.")
    
    with plt.style.context("dark_background"):
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.hist(df["średnia"].dropna(), bins=30, color="#9b59b6", edgecolor="white", alpha=0.85)
        
        ax.set_title("Histogram średnich ocen")
        ax.set_xlabel("Średnia ocena")
        ax.set_ylabel("Liczba filmów")
        
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
    
    st.pyplot(fig, transparent=True)

elif page == "Wpływ czasu trwania na ocenę":
    st.title("Interaktywna analiza: Czas trwania vs Średnia ocena")
    st.write("Użyj suwaka poniżej, aby odfiltrować filmy według liczby oddanych głosów. Najechanie na kropkę pozwala wyświetlić tytuł filmu.")
    
    min_glosow = st.slider("Wybierz minimalną liczbę głosów (votes):", 
                           min_value=int(df["votes"].min()), 
                           max_value=100000, 
                           value=10000, 
                           step=5000)
    
    df_filtered = df[df["votes"] >= min_glosow]
    
    fig_plotly = px.scatter(df_filtered, 
                            x="runtime", 
                            y="średnia", 
                            hover_data=["title", "year"],
                            color="średnia",
                            color_continuous_scale="Viridis",
                            title=f"Filmy z co najmniej {min_glosow} głosami",
                            labels={"runtime": "Czas trwania (minuty)", "średnia": "Średnia ocena"})

    fig_plotly.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
    fig_plotly.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
    
    st.plotly_chart(fig_plotly, use_container_width=True)

elif page == "Ewolucja kina w czasie":
    st.title("Historyczne trendy filmowe")
    st.write("Jak zmieniało się kino na przestrzeni lat? Wybierz metrykę oraz zakres czasowy, aby przeanalizować średnie wartości w poszczególnych latach.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metryki = {
            "Średnia ocena filmów": "średnia",
            "Średnia liczba widzów (watchers)": "watchers",
            "Średnia liczba głosów (votes)": "votes",
            "Średnia liczba komentarzy": "comment_count"
        }
        wybrana_nazwa = st.selectbox("Co chcesz przeanalizować na osi Y?", list(metryki.keys()))
        wybrana_kolumna = metryki[wybrana_nazwa]
        
    with col2:
        min_rok = int(df["year"].min())
        max_rok = int(df["year"].max())
        zakres_lat = st.slider("Wybierz zakres lat:", 
                               min_value=min_rok, 
                               max_value=max_rok, 
                               value=(1990, 2024))
        
    df_lata = df[(df["year"] >= zakres_lat[0]) & (df["year"] <= zakres_lat[1])]
    
    df_agregacja = df_lata.groupby("year")[wybrana_kolumna].mean().reset_index()
    
    fig_trend = px.line(df_agregacja, 
                        x="year", 
                        y=wybrana_kolumna, 
                        markers=True,
                        title=f"Trend: {wybrana_nazwa} w latach {zakres_lat[0]} - {zakres_lat[1]}",
                        labels={"year": "Rok premiery", wybrana_kolumna: wybrana_nazwa})

    fig_trend.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)", dtick=5)
    fig_trend.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
    fig_trend.update_traces(line_color="#e74c3c", line_width=3, marker=dict(size=8, color="#c0392b"))
    
    st.plotly_chart(fig_trend, use_container_width=True)

elif page == "Ranking najwybitniejszych reżyserów":
    st.title("Kto tworzy arcydzieła? Analiza reżyserów")
    st.write("Sprawdźmy, którzy reżyserzy regularnie tworzą najlepsze filmy. Użyj suwaka, aby ustalić minimalną liczbę filmów wyreżyserowanych przez twórcę, aby znaleźć tych najbardziej wpływowych.")
    
    min_filmow = st.slider("Minimalna liczba filmów wyreżyserowanych przez twórcę:", 
                           min_value=1, max_value=20, value=5, step=1)
    
    df_rezyserzy = df.groupby("director").agg(
        liczba_filmow=("title", "count"),
        srednia_ocena=("średnia", "mean")
    ).reset_index()
    
    df_top_rezyserzy = df_rezyserzy[(df_rezyserzy["liczba_filmow"] >= min_filmow) & (df_rezyserzy["director"] != "Nieznany")]
    df_top_rezyserzy = df_top_rezyserzy.sort_values(by="srednia_ocena", ascending=False).head(15)
    
    fig_bar = px.bar(df_top_rezyserzy,
                     x="srednia_ocena",
                     y="director",
                     orientation="h",
                     color="srednia_ocena",
                     color_continuous_scale="Magma", 
                     title=f"Top 15 reżyserów (min. {min_filmow} filmów)",
                     labels={"director": "Reżyser", "srednia_ocena": "Średnia ocena dorobku"})
    
    fig_bar.update_layout(yaxis={"categoryorder":"total ascending"}) 
    fig_bar.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
    fig_bar.update_yaxes(showgrid=False)
    
    st.plotly_chart(fig_bar, use_container_width=True)

elif page == "Analiza gatunków filmowych":
    st.title("Wpływ gatunku na ocenę filmu")
    st.write("Sprawdźmy, czy niektóre gatunki filmowe są z reguły oceniane wyżej niż inne. Poniższe wykresy pudełkowe prezentują rozkład ocen dla najpopularniejszych gatunków. Użyj suwaka, aby wybrać, ile najczęstszych gatunków chcesz porównać.")
    
    col_genre = "genres" if "genres" in df.columns else ("genre" if "genre" in df.columns else None)
    
    if col_genre:
        df_genres = df.copy()
        
        df_genres["gatunek"] = df_genres[col_genre].astype(str).str.replace(r"[\[\]'\"]", "", regex=True).str.split(",")
        
        df_genres = df_genres.explode("gatunek")
        df_genres["gatunek"] = df_genres["gatunek"].str.strip()
        
        df_genres = df_genres[(df_genres["gatunek"] != "nan") & (df_genres["gatunek"] != "")]
        
        top_n = st.slider("Wybierz liczbę najpopularniejszych gatunków do porównania:", 
                          min_value=5, max_value=20, value=12, step=1)
        
        najczestsze_gatunki = df_genres["gatunek"].value_counts().nlargest(top_n).index
        
        df_top_genres = df_genres[df_genres["gatunek"].isin(najczestsze_gatunki)]
        
        fig_box = px.box(df_top_genres,
                         x="gatunek",
                         y="średnia",
                         color="gatunek",
                         title=f"Rozkład średnich ocen dla {top_n} najczęstszych gatunków",
                         labels={"gatunek": "Gatunek filmowy", "średnia": "Średnia ocena"},
                         points="outliers")
                         
        fig_box.update_layout(showlegend=False, xaxis={"categoryorder":"median descending"}) 
        fig_box.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
        fig_box.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="rgba(255, 255, 255, 0.15)")
        
        st.plotly_chart(fig_box, use_container_width=True)

elif page == "Mapa drzewa kina":
    st.title("Mapa drzewa kina")
    st.write("Kliknij w dowolny wygenerowany prostokąt (np. konkretny kraj), aby wejść w niego głębiej i zobaczyć szczegółowy podział na podkategorie.")

    df_tree = df.copy()

    col_genre = "genres" if "genres" in df.columns else None
    if col_genre:
        df_tree["gatunek"] = df_tree[col_genre].astype(str).str.replace(r"[\[\]'\"]", "", regex=True).str.split(",")
        df_tree = df_tree.explode("gatunek")
        df_tree["gatunek"] = df_tree["gatunek"].str.strip()
        df_tree = df_tree[(df_tree["gatunek"] != "nan") & (df_tree["gatunek"] != "")]

    df_tree["country"] = df_tree["country"].fillna("Nieznany kraj")
    df_tree["language"] = df_tree["language"].fillna("Nieznany język")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        dostepne_kategorie = {
            "Kraj produkcji": "country", 
            "Gatunek": "gatunek", 
            "Język oryginalny": "language", 
            "Kategoria wiekowa": "certification"
        }
        wybrane_kategorie_etykiety = st.multiselect(
            "Hierarchia podziału (kolejność ma znaczenie):",
            list(dostepne_kategorie.keys()),
            default=["Kraj produkcji", "Gatunek"]
        )
        sciezka = [dostepne_kategorie[k] for k in wybrane_kategorie_etykiety]

    with col2:
        miary_wielkosci = {
            "Liczba głosów (votes)": "votes", 
            "Obejrzano (watchers)": "watchers", 
            "Liczba komentarzy": "comment_count"
        }
        wybrana_wielkosc_etykieta = st.selectbox("Rozmiar prostokątów wyznacza:", list(miary_wielkosci.keys()))
        wybrana_wielkosc = miary_wielkosci[wybrana_wielkosc_etykieta]

    with col3:
        miary_koloru = {
            "Średnia ocena": "średnia", 
            "Rok premiery": "year", 
            "Czas trwania (minuty)": "runtime"
        }
        wybrany_kolor_etykieta = st.selectbox("Kolor prostokątów wyznacza:", list(miary_koloru.keys()))
        wybrany_kolor = miary_koloru[wybrany_kolor_etykieta]

    if len(sciezka) == 0:
        st.warning("Wybierz co najmniej jedną kategorię z listy hierarchii, aby wygenerować wykres.")
    else:
        pierwsza_kategoria = sciezka[0]
        top_kategorie = df_tree[pierwsza_kategoria].value_counts().nlargest(12).index
        df_tree_filtered = df_tree[df_tree[pierwsza_kategoria].isin(top_kategorie)]

        fig_tree = px.treemap(
            df_tree_filtered,
            path=[px.Constant("Wszystkie filmy")] + sciezka,
            values=wybrana_wielkosc,
            color=wybrany_kolor,
            color_continuous_scale="Magma",
            title=f"Mapa struktury wg: {' -> '.join(wybrane_kategorie_etykiety)}"
        )
        
        fig_tree.update_traces(root_color="rgba(255, 255, 255, 0.05)")
        fig_tree.update_layout(margin=dict(t=50, l=10, r=10, b=10))

        st.plotly_chart(fig_tree, use_container_width=True)