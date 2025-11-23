---
title: Adafruit LED Display für Solar Manager
---

# Übersicht

Diese Seite beschreibt den Bau einer einfachen und langlebigen optischen Anzeige für den Solar Manager. Die benötigte Firmware für das Adafruit Matrix Display ist im GitHub Repository des Projekts in englischer Sprache dokumentiert. Die Webseite dient als begleitende Erklärung, weshalb das Projekt entstanden ist, welche Anforderungen erfüllt werden sollten und wie die Hardware aufgebaut ist.

![Solar Manager Display](./assets/img/matrix-display-screen-segmentation.jpg)

# Ausgangslage

Im Jahr 2025 installierte ich auf einem kleinen Einfamilienhaus in der Schweiz eine Solaranlage. Zur Optimierung des Eigenverbrauchs wird die Anlage mit dem Solar Manager der Solar Manager AG betrieben. Das System ist stabil, zuverlässig und erfordert wenig Pflege. Zudem erlaubt es den Anschluss einer grossen Vielfalt an Geräten. In meinem Fall werden eine Wärmepumpe von Hoval, eine Ladestation von Zaptec, eine Batterie von Huawei, eine Boilerheizung sowie eine Entfeuchtungsanlage über Shelly Geräte gesteuert. Diese Offenheit macht das Produkt sowohl für Anwender, die eine unkomplizierte Lösung wünschen, als auch für technisch Interessierte attraktiv.

Die Solar Manager App und das Webportal bieten alle relevanten Informationen. Dennoch wollte ich zusätzlich eine Anzeige im Wohnbereich, die ohne Interaktion jederzeit sichtbar ist. Vergleiche mit Tablet basierten Lösungen existieren, jedoch suchte ich eine bewusst einfache und unaufdringliche Darstellung, die fest installiert ist und nur die wichtigsten Werte zeigt.

# Zielsetzung

Für das Projekt wurden folgende Anforderungen definiert:

* Die Gesamtkosten sollten ungefähr hundert Schweizer Franken nicht überschreiten.
* Alle wichtigen Werte sollten gleichzeitig sichtbar sein.
* Die Darstellung sollte nur einmal pro Minute aktualisiert werden, um eine ruhige Anzeige zu gewährleisten.
* Die Programmierung sollte einfach sein und langfristig ohne Wartungsaufwand funktionieren.
* Die Anzeige sollte vollständig lokal und ohne Internetverbindung betrieben werden.

# Hardwarewahl

Nach einer Recherche entschied ich mich für ein LED Matrix Display von Adafruit.  
Zum Einsatz kommt folgendes Set:

Adafruit RGB Matrix Bonnet und 64 mal 32 Pixel LED Display  
https://www.adafruit.com/product/4812  

Es handelt sich dabei nicht um Affiliate Links. Das Set habe ich selbst über DigiKey gekauft:  
https://www.digikey.ch/de/products/detail/adafruit-industries-llc/4812/15189153  
Der Preis lag mit Versand bei ungefähr sechzig Franken.

Das Set besteht aus einem 32 mal 64 Pixel LED Panel und einem Controllerboard mit einem SAMD51 und einem ESP32. Es lässt sich in CircuitPython programmieren. Das Display erscheint nach Anschluss per USB C als Laufwerk und der Code kann mit einem normalen Texteditor bearbeitet werden. Es ist keine zusätzliche Software nötig.

Der vollständige Code befindet sich im Repository des Projektes.

# Funktionsweise des Displays

Das Display zeigt vier Werte gleichzeitig an:

* Verbrauch des Hauses  
* Solarleistung  
* Ladezustand der Batterie  
* Wassertemperatur des Boilers  

Die Daten werden einmal pro Minute über die lokale REST API des Solar Managers abgefragt. Da die Abfrage vollständig lokal erfolgt, wird keine Authentifizierung benötigt und das Gerät ist nicht mit dem Internet verbunden. Eine Websocket Lösung wäre ebenfalls möglich, wurde jedoch bewusst nicht umgesetzt, um eine ruhige Darstellung ohne dauernde Wechsel zu erhalten.

# Gehäuse und Montage

Für das Display war ein passender Halter notwendig. Dieser wurde von ibex3d konstruiert und gefertigt. Das Modell kann im folgenden eingebetteten Viewer betrachtet werden. Es eignet sich für den 3D Druck und kann bei Bedarf direkt bei ibex3d bezogen werden.

<div class="iframe-container">
  <iframe 
    src="https://philippbruhin.autodesk360.com/shares/public/SH90d2dQT28d5b602811b9992e377d0221f6?mode=embed"
    allowfullscreen
    frameborder="0">
  </iframe>
</div>

# Fazit

Dieses Projekt soll als Vorlage für Anwender dienen, die eine einfache und zuverlässige optische Anzeige für ihren Solar Manager realisieren möchten. Die Lösung ist kostengünstig, arbeitet vollständig lokal und erfordert nach der Inbetriebnahme keinen weiteren Wartungsaufwand. Durch die Programmierung mit CircuitPython bleibt der Aufbau verständlich und gut nachvollziehbar.
