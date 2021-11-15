# Sawtpedia
This is a joint development project of [Wikimedia Tunisia](https://meta.wikimedia.org/wiki/Wikimedia_Tunisie) and [Data Engineering and Semantics Research Unit](http://www.fss.rnu.tn/eng/s3465/pages/819/DES-UNIT) within the framework of [Hack4OpenGLAM](https://hack4openglam.okf.fi/). Based on inspiration from the logic of [QRpedia](https://qrpedia.org), Yamen Bousrih has first presented the [idea](https://hack4openglam.okf.fi/tools/audioqrpedia/) at the Hack4OpenGLAM Showcase at the 2021 Creative Commons Global Summit. Then, he has disseminated it in Wikimedia Conferences such as [WikidataCon 2021](https://pretalx.com/wdcon21/talk/BPE3VZ/). Deployed at https://sawtpedia.toolforge.org, Sawtpedia generates a [QRCode](https://en.wikipedia.org/wiki/QR_code) related to a monument that once scanned will fetch the [Wikidata](https://www.wikidata.org) item for that monument and then open the audio file for the [Wikipedia](https://en.wikipedia.org) article about the monument in the mobile device's language if available in [Wikimedia Commons](https://commons.wikimedia.org).
## Principles
The tool uses the same principle as QRpedia. However, we have updated the project approach by considering the latest advances in [Web Development](https://en.wikipedia.org/wiki/Web_development) and in [Wikimedia Projects](https://en.wikipedia.org/wiki/Wikimedia_Foundation#Wikimedia_projects). In fact, the tool is implemented in [Python](https://www.python.org) with [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) instead of [PHP](https://en.wikipedia.org/wiki/PHP) and benefits from the large-scale multilingual [structured data](https://en.wikipedia.org/wiki/Linked_data) available in [Wikidata](https://www.wikidata.org) to work. The tool has two components:
* A [HTML](https://en.wikipedia.org/wiki/HTML) Page with advanced [JavaScript](https://en.wikipedia.org/wiki/JavaScript) and [CSS](https://en.wikipedia.org/wiki/CSS) codes to generate a QRCode for a given monument. The input is the Wikipedia Page of the monument in any language. The Wikidata item of the monument is retrieved from the Wikipedia Page using JavaScript and [mw.config](https://www.mediawiki.org/wiki/Manual:Interface/JavaScript). Then, a QRCode will be generated using the QRpedia web interface leading to a web service leading to the audio recording of the Wikipedia article about the monument in the language of the web browser of the mobile device.
* A [Web Service](https://en.wikipedia.org/wiki/Web_service) implemented in [Python](https://www.python.org) with [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) to redirect the user to the audio recording of the Wikipedia article about the monument in the language of the web browser of the mobile device. The input here is the Wikidata ID of the monument. The Web Service will retrieve the language of the web browser of the user. Then, it will find the URL of the audio recording in the considered language using a SPARQL query on [spoken text audio](https://www.wikidata.org/wiki/Property:P407) statements of Wikidata. Here, [Wikidata hub](https://hub.toolforge.org/) is used to return the Wikidata ID of the user language based on its [IETF Language Tag](https://en.wikipedia.org/wiki/IETF_language_tag). If the file exists, the user will be redirected to the audio. If it does not exist, the tool can:
  * convert the lead of the Wikipedia article about the Wikidata item in the user language to an audio using [gTTS](https://gtts.readthedocs.io/en/latest/).
  * generate an error message if gTTS does not support the user language.
## Requirements
* [Flask](https://pypi.org/project/Flask/) 2.0.2
* [Requests](https://pypi.org/project/requests/) 2.26.0
* [SPARQLWrapper](https://pypi.org/project/SPARQLWrapper/) 1.8.5
* [gTTS](https://pypi.org/project/gTTS/) 2.2.3
## Team
* **[Yamen Bousrih](https://meta.wikimedia.org/wiki/User:Yamen)**, *Original idea*
* **[Houcemeddine Turki](https://meta.wikimedia.org/wiki/User:Csisc)**, *Tool Development*
## Acknowledgements
* Capacity Building about Web Development with Flask has been provided by Data Engineering and Semantics Research Unit, University of Sfax, Tunisia as a part of the Federated Research Project PRF-COV19-D1-P1.
* We thank Terence Eden and Roger Bamkin for providing the [source](https://code.google.com/archive/p/qrwp/) codes of QRpedia. We were inspired by the QRpedia Principles and we have even reused several excerpts as well as the QRpedia web service for the generation of the QRCode from URL in our source codes. As we built Sawtpedia based on QRpedia, we use the MIT License for our source code and we adopt the [Website Privacy Policy](https://wikimedia.org.uk/wiki/Website_Privacy_Policy) of [Wikimedia UK](https://wikimedia.org.uk) for our tool.
* We thank [Legoktm](https://www.mediawiki.org/wiki/User:Legoktm), [Mutante](https://www.mediawiki.org/wiki/User:Mutante), [AntiComposite](https://en.wikipedia.org/wiki/User:AntiCompositeNumber), [Reedy](https://www.mediawiki.org/wiki/User:Reedy), [RhinosF1](https://www.mediawiki.org/wiki/User:RhinosF1), and [Bryan Davis](https://www.mediawiki.org/wiki/User:BDavis_(WMF)) for supporting the deployment of the tool on Toolforge using SSH Server.
* We thank [Habib M'henni](https://commons.wikimedia.org/wiki/User:Dyolf77) from Wikimedia Tunisia for his contribution to our testing of the tool.
