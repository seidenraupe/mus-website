# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def page(rel, title, body, data_root, data_page, desc=None):
    css = f"{data_root}css/site.css"
    js = f"{data_root}js/site.js"
    fav = f"{data_root}images/favicon.png"
    canon = f"https://www.museumschaffen.ch/{rel.replace('index.html', '')}"
    html = f"""<!DOCTYPE html>
<html lang="de-CH" data-root="{data_root}" data-page="{data_page}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc or "Das moderne historische Museum in Winterthur."}" />
  <link rel="icon" href="{fav}" />
  <link rel="canonical" href="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc or "Das moderne historische Museum in Winterthur."}" />
  <link rel="stylesheet" href="{css}" />
  <script src="{js}" defer></script>
</head>
<body>
  <div id="page">
    <div id="ticker" class="ticker"></div>
    <main>
{body}
    </main>
  </div>
</body>
</html>
"""
    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print("wrote", rel)


page(
    "index.html",
    "Museum Schaffen in Winterthur",
    """      <p class="city-mark">WintertHur</p>
      <h2 class="section-label">aktuell</h2>
      <article class="exhibition-hero">
        <div class="exhibition-copy">
          <div class="wash"></div>
          <a class="titles" href="ausstellungen/erinnerungstank-haldengut.html">
            Erinnerungstank Haldengut<br>
            – Wir zapfen Geschichte!<br>
            <span class="dates">8.5.26 – 4.4.27</span>
          </a>
        </div>
        <a href="ausstellungen/erinnerungstank-haldengut.html">
          <img src="images/erinnerungstank.jpg" alt="Erinnerungstank Haldengut">
        </a>
      </article>
      <h2 class="section-label">programm</h2>
      <div class="split-50 grid-wrap">
        <div class="grid-lines" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
        <div id="home-featured"></div>
        <div>
          <div id="home-rest"></div>
          <a class="more-link" href="programm/">+ alle Veranstaltungen</a>
        </div>
      </div>
      <h2 class="section-label">Journal</h2>
      <div class="cols-2">
        <a class="row-link" href="journal/hesch-gwuesst.html">
          <div class="row-meta"><span class="date">02.08.25</span><span class="lineticker">HESCH GWÜSST?</span></div>
          <div class="row-image"><img src="images/journal-reality-check.jpg" alt=""></div>
          <p class="teaser">Facts aus «REALITY CHECK»</p>
        </a>
        <a class="row-link" href="journal/growing-green.html">
          <div class="row-meta"><span class="date">01.06.25</span><span class="lineticker">Growing Green</span></div>
          <div class="row-image"><img src="images/journal-growing-green.jpg" alt=""></div>
          <p class="teaser">Video anschauen</p>
        </a>
      </div>""",
    "",
    "home",
)

page(
    "ausstellungen/index.html",
    "Ausstellungen — Museum Schaffen",
    """      <h1 class="page-title">Ausstellungen</h1>
      <h2 class="section-label">Aktuell</h2>
      <article class="exhibition-hero">
        <div class="exhibition-copy">
          <div class="wash"></div>
          <a class="titles" href="erinnerungstank-haldengut.html">
            Erinnerungstank Haldengut<br>
            – Wir zapfen Geschichte!<br>
            <span class="dates">8.5.26 – 4.4.27</span>
          </a>
        </div>
        <a href="erinnerungstank-haldengut.html">
          <img src="../images/erinnerungstank.jpg" alt="Erinnerungstank Haldengut">
        </a>
      </article>
      <h2 class="section-label">Archiv</h2>
      <a class="archive-item" href="#"><span class="year">2026</span><span class="name">TruePicture Winterthur 2026</span></a>
      <a class="archive-item" href="#"><span class="year">2026</span><span><span class="name">«ObjektWerkStadt»</span><span class="sub">mit Objekt-Dating-App Wintidings!</span></span></a>
      <a class="archive-item" href="#"><span class="year">2025</span><span><span class="name">Tanztheater Heidi J.M. Roth zu Gast im Museum Schaffen!</span><span class="sub">Tanzformate, Performance</span></span></a>
      <a class="archive-item" href="#"><span class="year">2025</span><span class="name">Reality Check!</span></a>
      <a class="archive-item" href="#"><span class="year">2024</span><span><span class="name">Urban Production</span><span class="sub">Zwischennutzung</span></span></a>
      <a class="archive-item" href="#"><span class="year">2023</span><span class="name">STAHL UND RAUCH</span></a>
      <a class="archive-item" href="#"><span class="year">2023</span><span class="name">Auf der Suche nach der Wahrheit</span></a>
      <a class="archive-item" href="#"><span class="year">2022</span><span class="name">«Brixe» / Pedro Wirz</span></a>
      <a class="archive-item" href="#"><span class="year">2022</span><span class="name">EINS, ZWEI, DREI, 4.0</span></a>
      <a class="archive-item" href="#"><span class="year">2022</span><span><span class="name">SYSTEM RESET</span><span class="sub">Krise als Chance?</span></span></a>
      <a class="archive-item" href="#"><span class="year">2018</span><span class="name">ZEIT. ZEUGEN. ARBEIT.</span></a>""",
    "../",
    "ausstellungen",
)

page(
    "ausstellungen/erinnerungstank-haldengut.html",
    "Erinnerungstank Haldengut — Museum Schaffen",
    """      <p class="page-title">Erinnerungstank Haldengut</p>
      <p class="city-mark">8.5.26 – 4.4.27</p>
      <img src="../images/erinnerungstank.jpg" alt="Erinnerungstank Haldengut">
      <article class="prose">
        <p>Wir zapfen Geschichte! – Die Fabrikantenfamilie, der Braumeister, der Mälzer, der Wagenmeister und die Chefbuchhalterin: Menschen in über 80 verschiedenen Berufen haben die Geschichte der Brauerei Haldengut zwischen 1843 und 2002 geprägt.</p>
        <p>Der Gärtank von einst wird im Museum Schaffen zum Erinnerungstank. Die Geschichten, die in diesem Tank lagern, wirken bis heute nach. In der Ausstellung «Erinnerungstank Haldengut» entführen einzigartige Objekte und Fotografien in eine vergangene Arbeitswelt. Alte Werbeplakate, Werkzeuge, eine lebendige Hefezucht und das erste alkoholfreie Bier der Schweiz erzählen von Erfindergeist, Identität und unternehmerischem Risiko. Im Zentrum steht die Brauerei als Arbeitskosmos, in dem Menschen, Pferde und Maschinen Seite an Seite arbeiten.</p>
        <p>In der Ausstellung kommen ehemalige Mitarbeitende und Zeitzeug*innen zu Wort. Gemeinsam fragen wir danach, was bleibt, wenn ein Industriebetrieb verschwindet.</p>
        <p>Komm vorbei und zapf dir ein Stück Winterthurer Geschichte!</p>
        <h2>Impressum</h2>
        <p>Kuration: Nadia Pettannice. In Begleitung: Anna Schneider. Szenografie: Studio Speck, Grafik: Studio Malta. Lektorat: Andrea Woods. Ausstellungsprogramm: Christina Lolos, Anja Huber. Vermittlung: Christina Lolos, Nadia Pettannice.</p>
        <h2>Programm</h2>
        <h3>Veranstaltungen &amp; Workshops</h3>
        <p>Das Museum Schaffen wird während der Ausstellungszeit zu einem Gärtank mit einem Sud aus verschiedenen Begegnungsmöglichkeiten, Veranstaltungen und Workshops. Sei auch du mit dabei!</p>
        <h3>Führungen – Wir zapfen Geschichte!</h3>
        <p>Öffentlicher dialogischer Rundgang mit dem Ausstellungsteam. Die Führungen sind im Eintrittspreis inbegriffen und finden jeweils am Abend statt. Es ist keine Anmeldung erforderlich. Private Führungen jederzeit auf Anfrage möglich.</p>
        <p><a href="../programm/">Zum Programm</a></p>
      </article>""",
    "../",
    "exhibition",
    "Wir zapfen Geschichte! Ausstellung zur Brauerei Haldengut, 8.5.26 – 4.4.27.",
)

page(
    "programm/index.html",
    "Programm — Museum Schaffen",
    """      <h1 class="page-title">Programm</h1>
      <div id="event-filters" class="filters"></div>
      <div id="event-list"></div>""",
    "../",
    "programm",
)

page(
    "programm/event.html",
    "Veranstaltung — Museum Schaffen",
    """      <div id="event-detail"></div>""",
    "../",
    "event",
)

page(
    "besucherinfos/index.html",
    "Besuch — Museum Schaffen",
    """      <h1 class="page-title">Besuch</h1>
      <article class="prose">
        <h2>Herzlich willkommen</h2>
        <p>Das Team von Museum Schaffen freut sich auf Besuch in der Halle am Lagerplatz 9! Hier finden Sie alle aktuellen Informationen rund um den Besuch des Museums.</p>
      </article>
      <div class="info-grid">
        <div class="info-block">
          <h3>Anreise</h3>
          <p>Museum Schaffen<br>Lagerplatz 9<br>8400 Winterthur</p>
          <p><a href="tel:+41525505128">+41 (0)52 550 51 28</a><br><a href="mailto:mail@museumschaffen.ch">Mail</a></p>
          <p><strong>Vom Bahnhof</strong> ist der Lagerplatz in ca. 10 Minuten erreichbar – am besten via Unterführungsausgang «Einkaufszentrum Neuwiesen» (Rudolfstrasse), dem Weg an den Gleisen entlang bis zum Café/Restaurant Portier, von dort sind es nur noch 50 Meter.</p>
          <p><strong>Mit dem Auto:</strong> Vor dem Museum gibt es keine Besucher*innen-Parkplätze. Das nächstgelegene Parkhaus ist die Halle 53. Von dort aus ist das Museum nur 150 Meter entfernt.</p>
          <p><strong>Mit Bus:</strong> Die nächste Station ist «Wylandbrücke». Von dort geht es über eine kleine Brücke zum Lagerplatz.</p>
        </div>
        <div class="info-block">
          <h3>Öffnungszeiten &amp; Preise</h3>
          <p>MI–SO 10–17 UHR<br>Schulklassen auf Anfrage</p>
          <p>Eintritt CHF 12 / CHF 9*<br>Tickets an der Museumskasse</p>
          <p>* Vergünstigter Eintritt: Kinder und Jugendliche bis 16 Jahre, Schulklassen (ausserhalb Stadt Winterthur), Studierende, Berufslernende mit Legi, Erwachsenenbildung, AHV-/IV-Bezüger*innen, Gruppen ab 8 Personen. 50% Ermässigung: Kulturlegi.</p>
          <p>Kostenloser Eintritt: alle mit Aufenthaltsbewilligung N/F/S, Kinder bis 12 Jahre, öffentliche Schulen Stadt Winterthur, Mitglieder Historischer Verein Winterthur HVW, Winterthurer &amp; Schweizer Museumspass, Raiffeisen-Karte, VMS- und ICOM-Mitglieder.</p>
          <p>Für Veranstaltungen gelten die jeweiligen Preisangaben.</p>
        </div>
        <div class="info-block">
          <h3>Feiertage</h3>
          <p>Geöffnet 10.00–17.00 Uhr: 05.04.2026 (Ostern), 14.05.2026 (Auffahrt), 24.05.2026 (Pfingsten).</p>
          <p>Geschlossen: 03.04.2026 (Karfreitag), 01.05.2026 (Tag der Arbeit), 02.05.2026–07.05.2026 (Aufbau Ausstellung), 27.06.2026–28.06.2026 (Albanifest), 27.07.2026–11.08.2026 (Sommerferien), 21.12.2026–05.01.2027 (Weihnachtsferien).</p>
        </div>
        <div class="info-block">
          <h3>Führungen</h3>
          <p><strong>Käfele mit der Kuratorin</strong><br>28.8. / 25.9. / 30.10. / 27.11. / 18.12.<br>14–16 Uhr · Eintritt frei · ohne Anmeldung</p>
          <p><strong>Kuratorinnenführung</strong><br>3.9. / 10.10. / 25.11.<br>19–20 Uhr · CHF 12.– / 9.– (im Eintrittspreis inbegriffen) · ohne Anmeldung</p>
        </div>
        <div class="info-block">
          <h3>Schulen &amp; Privatpersonen</h3>
          <p>Privatpersonen: Führung 1h à CHF 160.– plus Eintritt 9.– pro Person; 2h à CHF 250.–. Zuschlag von 30.– ausserhalb der Öffnungszeiten.</p>
          <p>Schulen Stadt Winterthur: Führungen, Eintritt und Workshops kostenlos.</p>
          <p>Stadtexterne Schulen, Berufs- &amp; Kantonsschulen Winterthur: Führungen kostenlos, Eintritt 9.– pro Person.</p>
          <p>Anfrage via <a href="mailto:christina.lolos@museumschaffen.ch">Mail</a></p>
        </div>
        <div class="info-block">
          <h3>Schulvermittlung</h3>
          <p><strong>Zyklus 2 — Die Industrialisierung in Winterthur</strong><br>Workshop rund um den Katharina-Sulzer-Platz. Dauer 2 bis 2½ Stunden. Leitung: Franziska Dusek, Jasmina Hugi. Angebot der Museumspädagogik der Stadt Winterthur.</p>
          <p><strong>Zyklus 3 — Industrie- und Arbeitsstadt Winterthur im Wandel</strong><br>90 Min. (auch 60 Min. möglich). Leitung: Christina Lolos.</p>
        </div>
        <div class="info-block">
          <h3>Arbeitsmaterial</h3>
          <p>Hefte zur Ausstellung Eins, Zwei, Drei, 4.0 (2022), angelehnt an den Lehrplan 21, kostenfrei für Lehrpersonen.</p>
        </div>
        <div class="info-block">
          <h3>Barrierefreiheit</h3>
          <p>Das Museum Schaffen ist stufenlos zugänglich. Eine kleine Rampe überbrückt die Schwelle am Eingang. Die Ausstellungs- und Workshop-Ebene sind mit einem rollstuhlgerechten Lift erreichbar. Das externe WC befindet sich kurz nach der Lagerplatz-Einfahrt direkt hinter dem Portier im Gebäude 193.</p>
        </div>
      </div>""",
    "../",
    "besuch",
)

page(
    "journal/index.html",
    "Journal — Museum Schaffen",
    """      <h1 class="page-title">Journal</h1>
      <div class="cols-2">
        <a class="row-link" href="hesch-gwuesst.html">
          <div class="row-meta"><span class="date">02.08.25</span><span class="lineticker">HESCH GWÜSST?</span></div>
          <div class="row-image"><img src="../images/journal-reality-check.jpg" alt=""></div>
          <p class="teaser">Facts aus «REALITY CHECK»</p>
        </a>
        <a class="row-link" href="growing-green.html">
          <div class="row-meta"><span class="date">01.06.25</span><span class="lineticker">Growing Green</span></div>
          <div class="row-image"><img src="../images/journal-growing-green.jpg" alt=""></div>
          <p class="teaser">Video anschauen</p>
        </a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">01.03.25</span><span class="lineticker">Bühnenprogramm «Mazzarella»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">01.03.25</span><span class="lineticker">«Geschichten für Aug &amp; Ohr»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">01.02.25</span><span class="lineticker">Tanz zu «Heimweh, Melancholie, weit weg»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">09.09.24</span><span class="lineticker">150 Jahre HVW!</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">05.06.24</span><span class="lineticker">Lesung «No Grazie, Non Fumo»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">26.05.24</span><span class="lineticker">Tanz zu «Heimweh, Melancholie, weit weg»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">15.03.24</span><span class="lineticker">Vernissage «Reality Check!»</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">Hörspiel «Sidi 1910»</span><span class="lineticker">News</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">Neueröffnung am Lagerplatz 9!</span><span class="lineticker">News / Videos</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">LIVE Referat Kommunismus</span><span class="lineticker">Videos</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">Die Arbeitswelt von morgen</span><span class="lineticker">Videos</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">Aktion für ein kluges Schaffen</span><span class="lineticker">Projekte</span></div></a>
        <a class="row-link" href="#"><div class="row-meta"><span class="date">Thomas Meyer im Interview</span><span class="lineticker">Interviews</span></div></a>
      </div>""",
    "../",
    "journal",
)

page(
    "journal/hesch-gwuesst.html",
    "HESCH GWÜSST? — Museum Schaffen",
    """      <h1 class="page-title">HESCH GWÜSST?</h1>
      <img src="../images/journal-reality-check.jpg" alt="">
      <article class="prose">
        <p>02.08.25 · Facts aus «REALITY CHECK»</p>
        <p>Wussten Sie das? In der Ausstellung «Reality Check!» Arbeit, Migration, Geschichte(n) kamen Fakten, Stimmen und Objekte zusammen, die zeigen, wie Arbeitsmigration Winterthur und die Schweiz geprägt hat.</p>
        <p><a href="./">Zurück zum Journal</a></p>
      </article>""",
    "../",
    "journal",
)

page(
    "journal/growing-green.html",
    "Growing Green — Museum Schaffen",
    """      <h1 class="page-title">Growing Green</h1>
      <img src="../images/journal-growing-green.jpg" alt="">
      <article class="prose">
        <p>01.06.25 · Video</p>
        <p>Growing Green begleitet das Museum Schaffen und seine Umgebung – ein Blick auf Wachstum, Arbeit und den Lagerplatz.</p>
        <p><a href="./">Zurück zum Journal</a></p>
      </article>""",
    "../",
    "journal",
)

page(
    "ueber-uns/index.html",
    "Über uns — Museum Schaffen",
    """      <h1 class="page-title">Über uns</h1>
      <article class="prose">
        <h2>Das Moderne Historische Museum</h2>
        <p>Das Museum Schaffen rückt den Menschen als Schaffenden in den Mittelpunkt und widmet sich dem Thema Arbeit in Geschichte, Gegenwart und Zukunft. Es setzt auf die Teilhabe der Bevölkerung sowie auf unterschiedliche Kooperationen. Dank multifunktionaler Räumlichkeiten und niederschwelliger Vermittlungsangebote erlaubt es einen vielgestalteten Zugang zum Thema – sei es in Form von Wechselausstellungen oder Veranstaltungsangeboten. Zusätzlich bietet es Raum für Workshops und Arbeitsplätze.</p>
        <p>Von 2017 bis 2020 gastierte das Museum Schaffen in verschiedenen Zwischennutzungen in der Lokstadt (ehemaliges Sulzer-Areal). Mit der Halle auf dem Lagerplatz hat es im März 2021 seinen festen Standort gefunden.</p>
      </article>
      <h2 class="section-label">Team</h2>
      <div class="team-grid">
        <div class="person"><strong>Rita Borner</strong><span>Leitung Museum / Personal</span><span><a href="mailto:mail@museumschaffen.ch">Mail</a></span></div>
        <div class="person"><strong>Ursina Largiadèr</strong><span>Leitung Museum / Programm</span><span><a href="mailto:mail@museumschaffen.ch">Mail</a></span></div>
        <div class="person"><strong>Chris Huggenberg</strong><span>Leitung Museum / Finanzen / Kommunikation</span><span><a href="mailto:christian.huggenberg@hvwinterthur.ch">Mail</a></span></div>
        <div class="person"><strong>Christina Lolos</strong><span>Kulturvermittlung / Programm</span><span>077 464 37 64 / 052 550 51 29 / Di, Do, Fr</span><span><a href="mailto:christina.lolos@museumschaffen.ch">Mail</a></span></div>
        <div class="person"><strong>Nico Hollenstein</strong><span>Administration / Sekretariat</span><span>052 550 51 28 / Di–Do</span><span><a href="mailto:mail@museumschaffen.ch">Mail</a></span></div>
        <div class="person"><strong>Nadia Pettannice</strong><span>Gastkuration</span></div>
        <div class="person"><strong>Annina Eugster</strong><span>Cafébar / Museumsdienst / Vermietungen</span><span>052 550 51 45 / Sa–So</span><span><a href="mailto:annina.eugster@museumschaffen.ch">Mail</a></span></div>
      </div>
      <article class="prose" id="traegerschaft">
        <h2>Trägerschaft</h2>
        <p>Der Historische Verein Winterthur (HVW) wurde 1874 gegründet und ist Initiator sowie Träger vom Museum Schaffen. Mit dem Ziel, Geschichte abwechslungsreich und lebendig zu vermitteln, organisiert er Vorträge und Exkursionen und fördert Publikationen zur Geschichte Winterthurs. Zudem betreut der HVW die Villa Lindengut sowie die Mörsburg.</p>
        <p>HVW-Mitglieder profitieren von Einladungen zu allen HVW-Veranstaltungen, Gratis-Ausstellungen im Museum Schaffen, vergünstigten Event-Eintritten, kostenlosem Eintritt in Villa Lindengut und Mörsburg sowie dem Winterthurer Neujahrsblatt. Ab CHF 30 pro Jahr. Weitere Infos: <a href="https://www.historischer-verein-winterthur.ch/" target="_blank" rel="noopener">Historischer Verein Winterthur</a></p>
        <h2>Ausschuss &amp; Beirat</h2>
        <h3>Mitglieder des Ausschusses</h3>
        <ul>
          <li>Rita Borner, Vorstand Historischer Verein Winterthur</li>
          <li>Anja Huber, Vorstand Historischer Verein Winterthur</li>
          <li>Christian Huggenberg, Vorstand Historischer Verein Winterthur</li>
        </ul>
        <h3>Mitglieder des Beirates</h3>
        <ul>
          <li>Marlis Betschart, lic. Phil. I, Historikerin, Stadtarchivarin, Winterthur</li>
          <li>Christoph Dejung, Professor für Neueste Geschichte an der Universität Bern</li>
          <li>Lucius Dürr, Lic. Jur., Dipl. NPO-Manager VMI, Consultant</li>
          <li>Jacqueline Fehr, Regierungsrätin, Vorsteherin der Direktion der Justiz und des Innern des Kantons Zürich</li>
          <li>Hans Hollenstein, Dr. rer. pol., Alt-Regierungsrat, Winterthur</li>
          <li>Martin Künzli, Prof. em. Dipl. Ing. ETH, ehem. Direktor der School of Engineering der ZHAW</li>
          <li>Guido Lerch, Dozent Pädagogische Hochschule Thurgau</li>
          <li>Carol Nater Cartier, Dr. phil.</li>
        </ul>
        <h2>Partner*innen</h2>
        <p>Das Museum Schaffen wirkt auch dank und mit anderen. Einerseits finanziert es seine Aktivitäten aus Betriebsbeiträgen der Stadt Winterthur und des Lotteriefonds, andererseits aus Projektbeiträgen Dritter (öffentliche Hand, Stiftungen, Sponsoren). Ein grosses Augenmerk liegt auch auf verschiedenen Kooperationen, darunter die Internationalen Kurzfilmtage Winterthur, das Akzent Klubfestival und das 8. Schweizer Kinder- und Jugendchorfestival.</p>
        <h2 id="jobs">Offene Stellen</h2>
        <p>Aktuell haben wir keine offenen Positionen.</p>
      </article>""",
    "../",
    "ueber-uns",
)

page(
    "kontakt/index.html",
    "Kontakt — Museum Schaffen",
    """      <h1 class="page-title">Kontakt</h1>
      <div class="info-grid">
        <div class="info-block">
          <h3>Museum, Veranstaltungen, Work Lab</h3>
          <p>Lagerplatz 9, 8400 Winterthur</p>
          <p><a href="mailto:mail@museumschaffen.ch">Mail</a> · <a href="tel:+41525505145">+41 (0)52 550 51 45</a> (Mi–So)</p>
        </div>
        <div class="info-block">
          <h3>Betriebsbüro</h3>
          <p>Römerstrasse 8, 8404 Winterthur</p>
          <p><a href="mailto:mail@museumschaffen.ch">Mail</a> · <a href="tel:+41525505128">+41 (0)52 550 51 28</a> (Di–Do)</p>
        </div>
      </div>
      <h2 class="section-label">Team</h2>
      <div class="team-grid">
        <div class="person"><strong>Rita Borner</strong><span>Leitung / Personal</span></div>
        <div class="person"><strong>Anja Huber</strong><span>Leitung / Programm</span><span><a href="mailto:anja.huber@hvwinterthur.ch">Mail</a></span></div>
        <div class="person"><strong>Chris Huggenberg</strong><span>Leitung / Finanzen &amp; Kommunikation</span></div>
        <div class="person"><strong>Nico Hollenstein</strong><span>Administration / Sekretariat</span><span>+41 (0)52 550 51 28</span></div>
        <div class="person"><strong>Christina Lolos</strong><span>Kulturvermittlung / Veranstaltungen</span><span>+41 (0)52 550 51 29</span></div>
        <div class="person"><strong>Annina Eugster</strong><span>Cafébar / Museumsdienst / Vermietungen</span><span>+41 (0)52 550 51 45 (Mi–So)</span></div>
      </div>
      <form class="simple" action="mailto:mail@museumschaffen.ch" method="post" enctype="text/plain">
        <h2>Kontaktformular</h2>
        <label>Name <input name="name" required></label>
        <label>E-Mail <input type="email" name="email" required></label>
        <label>Nachricht <textarea name="nachricht" rows="6" required></textarea></label>
        <button type="submit">Senden</button>
      </form>""",
    "../",
    "kontakt",
)

page(
    "raummiete/index.html",
    "Raummiete — Museum Schaffen",
    """      <h1 class="page-title">Raummiete</h1>
      <article class="prose">
        <h2>Platz da!</h2>
        <p>Beim Umdenken, Neudenken und Weiterkommen helfen kraftvolle Schauplätze. Das Museum Schaffen ist ein solcher Ort. In der ehemaligen Sulzer-Halle am Lagerplatz im Herzen der ehemaligen Arbeiter*innenstadt Winterthur treffen Industriecharme auf Geschichte und Innovation. Und es ist Platz da: für Workshops, Meet-Ups, Weiterbildungen, Tagungen, Events wie Mitarbeitenden- oder Kund*innenanlässe und vieles mehr.</p>
      </article>
      <div class="info-grid">
        <div class="info-block">
          <h3>WorkLab</h3>
          <p>1 bis 14 Plätze</p>
        </div>
        <div class="info-block">
          <h3>Ganze Halle</h3>
          <p>Bis 70 Plätze</p>
        </div>
      </div>
      <article class="prose">
        <p>Anfragen: <a href="mailto:annina.eugster@museumschaffen.ch">annina.eugster@museumschaffen.ch</a> · 052 550 51 45</p>
      </article>""",
    "../",
    "raummiete",
)

page(
    "medien/index.html",
    "Medien — Museum Schaffen",
    """      <h1 class="page-title">Medien</h1>
      <article class="prose">
        <h2>Anfragen</h2>
        <p>Medienanfragen können Sie direkt an Christian Huggenberg richten: <a href="mailto:christian.huggenberg@hvwinterthur.ch">Mail</a> / 076 384 73 75 oder an die Leitung Programm Museum Schaffen, Anja Huber: <a href="mailto:anja.huber@hvwinterthur.ch">Mail</a>.</p>
        <h2>Pressemitteilungen</h2>
        <ul>
          <li>Reality-Check! Arbeit, Migration, Geschichte(n)</li>
          <li>Auf der Suche nach der Wahrheit</li>
          <li>STAHL UND RAUCH – verlängert</li>
          <li>Stahl und Rauch</li>
          <li>Neueröffnung und Installation System Reset</li>
          <li>Aktion für ein kluges Schaffen</li>
          <li>Eins, zwei, drei, 4.0</li>
        </ul>
        <h2>Pressebilder</h2>
        <ul>
          <li>Erinnerungstank Haldengut. Wir zapfen Geschichte!</li>
          <li>Reality Check! Arbeit, Migration, Geschichte(n)</li>
          <li>Auf der Suche nach der Wahrheit</li>
          <li>STAHL UND RAUCH</li>
          <li>Museum Schaffen Aussenansicht</li>
          <li>System Reset</li>
          <li>Gruppenbild Trägerschaft (Historischer Verein Winterthur)</li>
          <li>Eins zwei drei 4.0</li>
        </ul>
        <h2>Medienecho</h2>
        <ul>
          <li>«Reality Check!» Das Erschaffen einer gemeinsamen Realität — Coucou Magazin</li>
          <li>«Reality Check!» Ohne Migranten sähe die Schweiz anders aus. — Der Landbote</li>
          <li>«Reality Check!» Wie hat Arbeitsmigration die Schweiz geprägt? — arttv</li>
          <li>Im Museum ausgestellt: Der Journalismus und wir — SRF</li>
          <li>Museum Schaffen | Stahl und Rauch — arttv.ch</li>
        </ul>
      </article>""",
    "../",
    "medien",
)

page(
    "unterstuetzen/index.html",
    "Unterstützen — Museum Schaffen",
    """      <h1 class="page-title">Unterstützen</h1>
      <article class="prose">
        <p>Das Museum Schaffen ist die grundlegende Neuausrichtung des Winterthurer Stadtmuseums (Villa Lindengut) und als solche seit 2017 im Aufbau. Unsere Vision ist es, das moderne historische Museum zu einem Kompetenzzentrum zur Geschichte der Arbeit zu entwickeln. Das schaffen wir nur mit Unterstützung von Stiftungen, Unternehmen und vielen Menschen, die unser Interesse am Thema Arbeit teilen.</p>
        <h2>Spenden</h2>
        <p>Online mittels E-Banking: IBAN <strong>CH92 0900 0000 8978 9780 8</strong><br>
        Mit einem Einzahlungsschein – bestellen via <a href="mailto:mail@museumschaffen.ch">Mail</a>. Spenden an das Museum Schaffen sind steuerlich abzugsfähig.</p>
        <h2>Mitwirken</h2>
        <p>Als partizipatives Museum bietet das Museum Schaffen einen Ort zum Mitwirken – im Bereich Café-Bar und Besucher*innenservice oder im Rahmen von Veranstaltungen.</p>
        <h2>Freund*in / Gönner*in</h2>
        <ul>
          <li>Jugend-Mitgliedschaft 30.– pro Jahr</li>
          <li>Einzel-Mitgliedschaft 60.– pro Jahr</li>
          <li>Paar-Mitgliedschaft 80.– pro Jahr</li>
          <li>Freund*in ab 150.– pro Jahr</li>
        </ul>
        <p>Vorteile: Einladungen zu Veranstaltungen, gratis Ausstellungen, Winterthurer Neujahrsblatt.</p>
      </article>
      <form class="simple" action="mailto:mail@museumschaffen.ch" method="post" enctype="text/plain">
        <h2>Anmeldeformular</h2>
        <label>Ich möchte
          <select name="typ">
            <option>Jugend-Mitglied werden</option>
            <option>Einzel-Mitglied werden</option>
            <option>Paar-Mitglied werden</option>
            <option>Freund*in werden</option>
            <option>Mithelfen beim Betrieb</option>
            <option>Inhaltlich mitwirken</option>
          </select>
        </label>
        <label>Name, Vorname <input name="name" required></label>
        <label>Strasse, Hausnummer <input name="strasse"></label>
        <label>PLZ, Ort <input name="ort"></label>
        <label>Telefon <input name="telefon"></label>
        <label>E-Mail <input type="email" name="email" required></label>
        <label class="hp">Bitte nicht ausfüllen <input name="website" tabindex="-1" autocomplete="off"></label>
        <label>Mitteilung <textarea name="mitteilung" rows="4"></textarea></label>
        <label><input type="checkbox" required> Ich habe die Datenschutzerklärung gelesen und akzeptiere sie.</label>
        <button type="submit">Senden</button>
      </form>""",
    "../",
    "unterstuetzen",
)

page(
    "newsletter/index.html",
    "Newsletter — Museum Schaffen",
    """      <h1 class="page-title">Newsletter Abo</h1>
      <article class="prose">
        <p>Wer über unsere Ausstellungen und Veranstaltungen auf dem Laufenden sein möchte, ist herzlich eingeladen, hier unseren Newsletter zu abonnieren.</p>
      </article>
      <form class="simple" action="mailto:mail@museumschaffen.ch" method="post" enctype="text/plain">
        <label>Vorname <input name="vorname"></label>
        <label>Nachname <input name="nachname"></label>
        <label>E-Mail* <input type="email" name="email" required></label>
        <label class="hp">Bitte nicht ausfüllen* <input name="website" tabindex="-1" autocomplete="off"></label>
        <label><input type="checkbox" required> Ich habe die Datenschutzerklärung gelesen und akzeptiere sie.</label>
        <button type="submit">Abonnieren</button>
        <p>Hinweis: Sollten Sie keine E-Mail in Ihrem Posteingang vorfinden, schauen Sie bitte in Ihren Spam-Ordner.</p>
      </form>""",
    "../",
    "newsletter",
)

page(
    "impressum/index.html",
    "Impressum — Museum Schaffen",
    """      <h1 class="page-title">Impressum</h1>
      <article class="prose">
        <p>Getragen wird Museum Schaffen vom Historischen Verein Winterthur. Die Realisierung wird ermöglicht durch die Stadt Winterthur und den Lotteriefonds des Kantons Zürich sowie durch private Geldgeber. Alle Rechte bleiben vorbehalten.</p>
        <p>Copyright Museum Schaffen<br>Lagerplatz 9<br>CH-8400 Winterthur</p>
        <h2>Konzept und Gestaltung (Original)</h2>
        <p>Studio Malta, Haldenstrasse 63, 8045 Zürich</p>
        <h2>Diese Neuimplementierung</h2>
        <p>Statische Website auf Basis von museumschaffen.ch. Veranstaltungen über den Eventfrog-JSON-Export (OrgID 5116588 / mus_export.json) aus dem Repo prototype-hvw-website.</p>
        <h2>Bildrechte</h2>
        <p>Museumsansichten: Lea Reutimann. Soweit es nicht anders angegeben ist, liegt das Copyright für alle Bilder beim Museum Schaffen. Eventbilder: Eventfrog / jeweilige Veranstalter.</p>
        <p>Die im Webauftritt veröffentlichten Informationen, Texte und Bilder dienen ausschliesslich der Information über das Museum Schaffen. Kommerzielle Verwendungszwecke sind nur nach schriftlicher Genehmigung des Museum Schaffen gestattet.</p>
      </article>""",
    "../",
    "impressum",
)

page(
    "datenschutz/index.html",
    "Datenschutz — Museum Schaffen",
    """      <h1 class="page-title">Datenschutz</h1>
      <article class="prose">
        <h2>Datenerfassung</h2>
        <p>Die Internetseiten verwenden teilweise so genannte Cookies. Cookies richten auf Ihrem Rechner keinen Schaden an und enthalten keine Viren. Die meisten der von uns verwendeten Cookies sind Session-Cookies und werden nach Ende Ihres Besuchs automatisch gelöscht.</p>
        <p>Der Provider erhebt Server-Log-Dateien (Browsertyp und -version, Betriebssystem, Referrer-URL, Hostname, Uhrzeit, IP-Adresse). Eine Zusammenführung mit anderen Datenquellen wird nicht vorgenommen.</p>
        <h2>Kontaktformular</h2>
        <p>Angaben aus Formularen werden zwecks Bearbeitung der Anfrage gespeichert und nicht ohne Einwilligung weitergegeben. Sie können die Einwilligung jederzeit per E-Mail widerrufen.</p>
        <h2>Instagram</h2>
        <p>Die Website verlinkt auf den Instagram-Kanal @museum_schaffen. Beim Aufruf von Instagram gelten die Datenschutzbestimmungen von Meta.</p>
        <h2>Eventfrog</h2>
        <p>Veranstaltungsdaten werden aus dem JSON-Export der Eventfrog-Organisation Museum Schaffen (OrgID 5116588) geladen. Ticket- und Detailseiten liegen bei Eventfrog.</p>
      </article>""",
    "../",
    "datenschutz",
)

print("done")
