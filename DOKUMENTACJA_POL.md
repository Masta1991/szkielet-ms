# 📝 Dokumentacja Pól i Integracji Bazy Danych (Szkielet Projektu)

Niniejsza dokumentacja opisuje konkretne pola formularza rejestracji treningu w aplikacji (zarówno po stronie interfejsu Streamlit, jak i stanu sesji `st.session_state`) oraz definiuje ich mapowanie do struktur danych i arkusza Google Sheets z **Projektu Darka**. 

Dzięki tym informacjom możesz natychmiastowo podpiąć szkielet pod logikę zapisywania i odczytywania danych, tak aby aplikacja była w pełni funkcjonalna ("żeby to już działało").

---

## 🗂️ Słownik Pól Formularza i Stanu Sesji (`st.session_state`)

Podstrona **Rejestracja Treningu** (`page == "add_data"`) posiada następujące pola wejściowe. Każdemu elementowi interfejsu odpowiada konkretny klucz w stanie sesji Streamlit:

| Nazwa w Interfejsie | Typ Elementu | Klucz w `st.session_state` | Typ Danych | Wartość Domyślna | Opis / Pochodzenie Listy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Podopieczny** | `st.selectbox` | `register_client` | `str` | `CLIENTS_LIST[0]` (Jan Kowalski) | Lista pobierana z tabeli klientów. Definiowana w kodzie jako `CLIENTS_LIST`. |
| **Data** | `st.date_input` | `register_date` | `datetime.date` | `datetime.date.today()` | Bieżąca data wybrana w kalendarzu. |
| **Godzina** | `st.selectbox` | `register_hour` | `int` | `12` | Zakres godzin (od 6 do 21). |
| **Rodzaj treningu** | `st.selectbox` | `register_workout_type` | `str` | `WORKOUT_TYPES[0]` (Push) | Rodzaje jednostek treningowych. Definiowane jako `WORKOUT_TYPES`. |
| **Główna Partia** | `st.selectbox` | `register_main_part` | `str` | `list(EXERCISES_DATA.keys())[0]` | Aktualna partia mięśniowa (np. Plecy, Klatka) filtrująca listę ćwiczeń. |
| **Wiersz ćwiczenia** | Niestandardowy (HTML/JS) | `exercise_weights` | `dict` (klucz: `str`, wartość: `float`) | `{}` | Słownik przechowujący aktualne obciążenie dla ćwiczeń, np. `{"Przysiad ze sztangą": 62.5}`. |

---

## ⚙️ Lokalne Listy Konfiguracyjne (Dane Testowe w `app.py`)

W pliku `app.py` w sekcji `4. DATA INITIALIZATION & FIELD LISTS` znajdziesz gotowe struktury, które należy zastąpić połączeniem z bazą (Google Sheets) podczas pełnego wdrożenia:

```python
# Lista podopiecznych (powiązana z st.selectbox "Podopieczny")
CLIENTS_LIST = ["Jan Kowalski", "Anna Nowak", "Piotr Zieliński", "Marek Murator", "Ania"]

# Lista rodzajów treningu (powiązana z st.selectbox "Rodzaj treningu")
WORKOUT_TYPES = ["Push", "Pull", "Legs", "Cardio", "FBW"]

# Słownik partii i przypisanych do nich ćwiczeń (filtrowane przez st.selectbox "Główna Partia")
EXERCISES_DATA = {
    "Klatka piersiowa": ["Wyciskanie sztangi na ławce poziomej", "Wyciskanie hantli na ławce skośnej", "Rozpiętki"],
    "Plecy": ["Podciąganie na drążku", "Wiosłowanie sztangą", "Ściąganie drążka wyciągu"],
    "Nogi": ["Przysiad ze sztangą", "Wykroki z hantlami", "Prostownie nóg na maszynie"],
    "Barki": ["Wyciskanie żołnierskie", "Wznosy hantli bokiem"],
    "Ramiona": ["Uginanie przedramion z hantlami", "Prostownie przedramion na wyciągu"]
}
```

---

## 📊 Mapowanie i Schemat Arkusza Google Sheets

W **Projekcie Darka** dane są zapisywane w dwóch głównych arkuszach. Oto ich schematy kolumn (od lewej do prawej) oraz odpowiadające im zmienne z formularza:

### 1. Arkusz `"Kalendarz"` (Zapis rezerwacji terminu)
Używany do dodawania wpisów w grafiku tygodniowym.

| Indeks Kolumny | Nazwa Kolumny w Arkuszu | Powiązana Zmienna w `app.py` | Przykład Wartości |
| :--- | :--- | :--- | :--- |
| **A** (1) | `Dzień` | `str(st.session_state.register_date)` | `"2026-05-25"` |
| **B** (2) | `Godzina` | `st.session_state.register_hour` | `10` |
| **C** (3) | `Klient` | `st.session_state.register_client` | `"Jan Kowalski"` |
| **D** (4) | `Trening` / `Rodzaj treningu` | `st.session_state.register_workout_type` | `"Push"` |
| **E** (5) | `Status` | Stała (domyślnie `"active"`) | `"active"` |

### 2. Arkusz `"Treningi"` (Zapis wyników obciążeń)
Używany do archiwizacji wykonanych serii i kilogramów dla poszczególnych ćwiczeń.

| Indeks Kolumny | Nazwa Kolumny w Arkuszu | Powiązana Zmienna w `app.py` | Przykład Wartości |
| :--- | :--- | :--- | :--- |
| **A** (1) | `Timestamp` | Generowany automatycznie w Pythonie | `"2026-05-25 10:15:30"` |
| **B** (2) | `Klient` | `st.session_state.register_client` | `"Jan Kowalski"` |
| **C** (3) | `Ćwiczenie` | Nazwa ćwiczenia (klucz ze słownika `exercise_weights`) | `"Przysiad ze sztangą"` |
| **D** (4) | `Obciążenie` | Wartość obciążenia z `exercise_weights` (z zamianą kropki na przecinek) | `"62,5"` |
| **E** (5) | `Tydzień` | Obliczany numer tygodnia roku | `22` |

---

## 🛠️ Instrukcja Wdrożenia Integracji (Kod "Połączeniowy")

Aby formularz w `app.py` faktycznie zapisywał dane do arkusza Google Sheets (zgodnie z funkcjami klasy gsheets w Projekcie Darka), zmodyfikuj obsługę przycisku **"ZAPISZ TRENING"** (okolice linii 871 w `app.py`) w następujący sposób:

### Przykład kodu integracji przycisku zapisu:

```python
# Zaimportuj klasę obsługującą gsheets z Twojego projektu (np. z gsheets.py lub skopiuj definicję)
# from gsheets import GoogleSheets
# client_db = GoogleSheets(secrets_path="secrets.json")

# ... (wewnątrz bloku strony add_data) ...
if st.button("ZAPISZ TRENING", key="btn_save", type="primary", use_container_width=True):
    # 1. Oblicz numer tygodnia
    week_num = train_date.isocalendar()[1]
    date_str = train_date.strftime("%Y-%m-%d")
    
    success = True
    
    # 2. Zapisz wpis w Kalendarzu/Grafiku
    try:
        # Wywołanie funkcji z klasy GoogleSheets
        cal_ok = client_db.update_calendar_event(
            date_str=date_str,
            hour=train_hour,
            client=klient,
            training_type=workout_type,
            status='active'
        )
        if not cal_ok:
            success = False
    except Exception as e:
        st.error(f"Błąd zapisu do Kalendarza: {e}")
        success = False
        
    # 3. Zapisz wyniki ćwiczeń (tylko te, które mają ustawioną wagę)
    for ex_name, weight in st.session_state.exercise_weights.items():
        if weight > 0:  # Zapisujemy tylko ćwiczenia wykonane z jakimś obciążeniem
            try:
                res_ok = client_db.save_workout_result(
                    client=klient,
                    exercise=ex_name,
                    weight=weight,
                    week=week_num,
                    date_str=date_str
                )
                if not res_ok:
                    success = False
            except Exception as e:
                st.error(f"Błąd zapisu ćwiczenia {ex_name}: {e}")
                success = False
                
    # 4. Poinformuj użytkownika o rezultacie
    if success:
        st.success(f"Pomyślnie zapisano trening '{workout_type}' dla {klient}!")
        # Wyczyść stan ćwiczeń i wróć na stronę główną
        st.session_state.exercise_weights = {}
        st.session_state.page = "home"
        st.rerun()
    else:
        st.warning("Trening został zapisany częściowo. Sprawdź logi błędów powyżej.")
```

---

## ⚡ Mostek Komunikacyjny JS-Python dla Wierszy Ćwiczeń

Wiersze ćwiczeń posiadają interaktywne przyciski `+` i `-` zdefiniowane bezpośrednio w HTML. Kiedy użytkownik klika przycisk:
1. JavaScript wywołuje funkcję `sendActionToStreamlit('action=update_weight&ex=Nazwa+Ćwiczenia&delta=2.5')`.
2. Akcja ta jest przekazywana do ukrytego pola `js_data_exchange` (klucz widgetu `js_data_input`).
3. Python odbiera tę akcję i wykonuje poniższą operację aktualizacji stanu (znajdziesz to w sekcji `5. ACTION PROCESSOR` w `app.py`):

```python
elif action == "update_weight":
    ex = parts.get("ex")
    delta = float(parts.get("delta", 0))
    current = st.session_state.exercise_weights.get(ex, 20.0)
    # Zapisuje wagę w słowniku sesyjnym
    st.session_state.exercise_weights[ex] = max(0.0, current + delta)
    st.rerun()
```
Dzięki temu każde kliknięcie `+` lub `-` na telefonie natychmiastowo zmienia wartość w `st.session_state.exercise_weights` i odświeża widok bez przeładowania całej strony.
