# Szkielet Projektu (Streamlit Mobile/Desktop Boilerplate)

Ten projekt stanowi profesjonalny szkielet startowy (boilerplate) dla nowych aplikacji budowanych w oparciu o Streamlit. Jest on zoptymalizowany pod kątem działania zarówno na komputerach (layout desktopowy), jak i na telefonach komórkowych (layout mobilny w stylu natywnej aplikacji iOS).

> [!NOTE]
> Szczegółowy opis wszystkich pól formularzy, zmiennych stanu sesji (`st.session_state`) oraz schematu bazy danych/arkusza Google Sheets znajdziesz w pliku [DOKUMENTACJA_POL.md](file:///c:/Projects/Szkielet%20Projektu/DOKUMENTACJA_POL.md).

---

## 📱 Architektura i Układ Graficzny (Mockup)

Poniższy diagram przedstawia rozkład elementów na ekranie w zależności od szerokości urządzenia.

### Układ Mobilny (`width <= 1000px`)
```text
┌────────────────────────────────────────────────────────┐
│ [≡] Hamburger  |  TYTUŁ APLIKACJI  |  [MS] Avatar/Ustaw│ <-- .ios-top-bar-wrapper (.ios-nav-bar)
├────────────────────────────────────────────────────────┤
│                                                        │
│                                                        │
│                  OBSZAR ROBOCZY                        │ <-- .block-container
│         (Dynamiczny widok wybranej strony)             │
│                                                        │
│                                                        │
├────────────────────────────────────────────────────────┤
│         [HOME] Strona Główna    |    [EDYTUJ] Tryb     │ <-- .ios-bottom-bar-wrapper
└────────────────────────────────────────────────────────┘
```

### Układ Desktopowy (`width > 1000px`)
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  PANEL BOCZNY (.mobile-sidebar-content)  │  OBSZAR ROBOCZY (.block-container)           │
│ ┌──────────────────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │ PANEL DOWODZENIA (Control Panel)     │ │ │ NAGŁÓWEK STRONY (.header-section)      │ │
│ │ Witaj, MS!                           │ │ │ 🏠 Strona Główna                        │ │
│ │ Status patchowania: OK               │ │ └─────────────────────────────────────────┘ │
│ └──────────────────────────────────────┘ │ ┌─────────────────────────────────────────┐ │
│ ┌──────────────────────────────────────┐ │ │ KARTA ZAWARTOŚCI (.content-card)         │ │
│ │ BENTO TILE 1 (Strona Główna)         │ │ │ Treść podstrony...                      │ │
│ └──────────────────────────────────────┘ │ │                                         │ │
│ ┌──────────────────────────────────────┐ │ │                                         │ │
│ │ BENTO TILE 2 (Profil)                │ │ │                                         │ │
│ └──────────────────────────────────────┘ │ │                                         │ │
│ ┌──────────────────────────────────────┐ │ │                                         │ │
│ │ BENTO TILE 3 (Ustawienia)            │ │ │                                         │ │
│ └──────────────────────────────────────┘ │ └─────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Słownik Pojęć i Klas CSS (Nomenklatura)

Aby ułatwić komunikację przy dalszym rozwoju aplikacji, poniżej znajduje się spis głównych elementów interfejsu i ich klas CSS:

| Nazwa widoku / Elementu | Klasa CSS | Opis |
| :--- | :--- | :--- |
| **Górny pasek iOS** | `.ios-top-bar-wrapper` | Stały pasek na górze ekranu na urządzeniach mobilnych. |
| **Pasek nawigacyjny** | `.ios-nav-bar` | Element wewnątrz górnego paska trzymający hamburgera, tytuł i avatar. |
| **Przycisk menu (Hamburger)** | `.ios-hamburger` | Trzy kreski wyzwalające rozwijane menu na telefonie. Dodaje klasę `.open` po otwarciu. |
| **Tytuł górnego paska** | `.ios-nav-title` | Główny tekst w nagłówku mobilnym (np. "Szkielet MS"). |
| **Podtytuł górnego paska** | `.ios-nav-subtitle` | Mniejszy tekst w nagłówku wyświetlający np. datę i tydzień. |
| **Awatar / Profil** | `.ios-avatar` | Okrągły przycisk po prawej stronie górnego paska (inicjały "MS"). |
| **Rozwijane Menu Mobilne** | `.mobile-nav-dropdown` | Menu wysuwające się z góry po naciśnięciu hamburgera na telefonie. |
| **Elementy menu** | `.mobile-nav-item` | Przyciski wewnątrz rozwijanego menu mobilnego. |
| **Dolny pasek iOS** | `.ios-bottom-bar-wrapper` | Stały dolny pasek z przyciskami funkcyjnymi na telefonie. |
| **Przycisk akcji dolnego paska**| `.ios-action-btn` | Pojedynczy przycisk na dolnym pasku (np. HOME, EDYTUJ). Dodaje klasę `.active` gdy aktywny. |
| **Panel Dowodzenia** | `.control-panel-card` | Karta u góry panelu bocznego na komputerze (Desktop-only). |
| **Kafelek Bento** | `.tile-link` | Pojedynczy kafelek menu bocznego na desktopie. |
| **Główny Layout** | `.main-layout` | Kontener flexbox dzielący ekran na panel boczny i obszar roboczy. |
| **Nagłówek sekcji** | `.header-section` | Karta z tytułem aktualnej strony. |
| **Karta zawartości** | `.content-card` | Kontener na główną treść strony. |

---

## 📱 Funkcja PWA i automatyczna generacja ikon

Szkielet posiada wbudowaną automatyczną obsługę instalacji aplikacji na telefonie (jako aplikacja PWA - Progressive Web App):

1. **Generowanie ikony**: Podczas pierwszego uruchomienia, biblioteka `Pillow` automatycznie generuje stylową ikonę 192x192 pikseli z inicjałami **MS** i zapisuje ją w pliku `zdjecia/icon.png`.
2. **Wstrzykiwanie nagłówków HTML**:
   - Skrypt `setup.py` podczas instalacji (build-time) wstrzykuje odpowiednie tagi do pliku `index.html` Streamlita.
   - Jeśli to się nie powiedzie, funkcja `patch_streamlit_index()` w pliku `app.py` wykonuje ten patch w czasie uruchomienia aplikacji (runtime).
   - Przesyłamy ikonę w formacie **Base64 Data-URI**, co zapewnia, że ikona ładuje się poprawnie bez problemów ze ścieżkami względnymi na różnych serwerach.

---

## ⚡ Mostek Komunikacyjny JS-Python (JS Bridge)

Wszystkie interakcje użytkownika w elementach HTML (takie jak kliknięcie kafelka bento czy przycisków dolnego paska) są obsługiwane przez dedykowany skrypt JavaScript umieszczony na dole pliku `app.py`.

- Każdy element HTML, który ma reagować na kliknięcie, posiada atrybut `data-action` (np. `data-action="action=nav&page=profile"`).
- Kliknięcie takiego elementu powoduje przekazanie tej akcji przez JavaScript bezpośrednio do ukrytego pola `st.text_input` w Pythonie (o etykiecie `js_data_exchange`).
- Python wykrywa zmianę wartości tego pola, przetwarza ją za pomocą biblioteki `urllib.parse` i wywołuje odpowiednie akcje (np. zmianę strony w `st.session_state` lub przełączenie trybu edycji) oraz odświeża interfejs za pomocą `st.rerun()`.

---

## 🚀 Jak uruchomić aplikację lokalnie

1. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Uruchom aplikację:
   ```bash
   streamlit run app.py
   ```
3. Otwórz przeglądarkę pod adresem `http://localhost:8501`. Aby przetestować wersję mobilną, otwórz Narzędzia Deweloperskie (F12) i włącz widok responsywny telefonu.
