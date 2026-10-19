# JARVIS Android 2.0 – kehityksen tila

Tämä haara on JARVISin Android-kehitystä varten. `main`-haaran verkkoversiota ja Renderin äänipalvelua ei pidä muuttaa Androidin virhekorjausten yhteydessä.

## Todettu laitetestissä 18.10.2026
- APK käynnistyy Samsung-puhelimessa ja näyttää hologrammin.
- Puheentunnistus palauttaa virhekoodin 5 (Android `SpeechRecognizer.ERROR_CLIENT`).
- Puhelimen ilmoitus `Puheentunnistus: 5. Yritetään uudelleen.` oli vanhan `MainActivity.java`-lähdekoodin merkkijono. Tämä ei vielä todista, mistä APK:sta ilmoitus tulee.
- Androidin TTS:n onnistumista ei ole voitu vahvistaa, koska puheentunnistus epäonnistuu ennen vastauksen muodostamista.

## Ensimmäinen korjaus
- Poista virhekoodin 5 automaattinen uudelleenyrittäminen.
- Estä päällekkäiset `startListening`-kutsut.
- Vapauta vanha tunnistusinstanssi ennen uuden istunnon käynnistystä.
- Jatka kuuntelua vasta `UtteranceProgressListener.onDone`-palautteen jälkeen.
- Tarkista `RECORD_AUDIO`-lupa, Androidin oletusarvoinen puheentunnistuspalvelu sekä `AndroidManifest.xml`-määritykset.
- Lisää näkyvä versionumero sovellukseen, jotta puhelimen APK voidaan yhdistää varmasti lähdekoodiversioon.

## Julkaisuehto
Älä merkitse puheohjausta toimivaksi ennen kuin puhelimessa toimii testiketju: Aloita kuuntelu → `Jarvis, paljonko kello on?` → tunnistettu teksti → suomenkielinen ääneen lausuttu aika. Käännös ja puhelintestaus ovat eri tarkistuksia.

## Seuraava tekninen edellytys
Lisää koko Android Studio -projektin lähdekoodi (mm. `app/src/main/java`, `app/src/main/AndroidManifest.xml`, `app/build.gradle`, resurssit ja Gradle-asetukset) tähän haaraan. Pelkkä verkkoversio ei muodosta asennettavaa Android-sovellusta. Tämän jälkeen voidaan ottaa käyttöön automaattinen APK-käännös GitHub Actionsissa ilman käyttäjän paikallista Android Studiota.
