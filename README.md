# Sawtpedia
This is a joint development project of [Wikimedia Tunisia](https://meta.wikimedia.org/wiki/Wikimedia_Tunisie) and [Data Engineering and Semantics Research Unit](http://www.fss.rnu.tn/eng/s3465/pages/819/DES-UNIT) within the framework of [Hack4OpenGLAM](https://hack4openglam.okf.fi/). Based on inspiration from the logic of [QRpedia](https://qrpedia.org), Yamen Bousrih has first presented the [idea](https://hack4openglam.okf.fi/tools/audioqrpedia/) at the Hack4OpenGLAM Showcase at the 2021 Creative Commons Global Summit. Then, he has disseminated it in Wikimedia Conferences such as [WikidataCon 2021](https://pretalx.com/wdcon21/talk/BPE3VZ/). Deployed at https://sawtpedia.toolforge.org, Sawtpedia generates a [QRCode](https://en.wikipedia.org/wiki/QR_code) related to a monument that once scanned will fetch the [Wikidata](https://www.wikidata.org) item for that monument and then open the audio file for the [Wikipedia](https://en.wikipedia.org) article about the monument in the mobile device's language if available in [Wikimedia Commons](https://commons.wikimedia.org).
## Principles
The tool uses the same principle as QRpedia. However, we have updated the project approach by considering the latest advances in Web Development and in Wikimedia Projects. In fact, the tool is implemented in [Python](https://www.python.org) with [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) instead of [PHP](https://en.wikipedia.org/wiki/PHP) and benefits from the large-scale multilingual [structured data](https://en.wikipedia.org/wiki/Linked_data) available in [Wikidata](https://www.wikidata.org) to work.



 using the statement spoken text audio and the property P407

Following the same logic as QRPedia codes (qrpedia.org), Sawtpedia .
## Team
* **[Yamen Bousrih](https://meta.wikimedia.org/wiki/User:Yamen)**, *Original idea*
* **[Houcemeddine Turki](https://meta.wikimedia.org/wiki/User:Csisc)**, *Tool Development*
## Acknowledgements
* Capacity Building about Web Development with Flask has been provided by Data Engineering and Semantics Research Unit, University of Sfax, Tunisia as a part of the Federated Research Project PRF-COV19-D1-P1.
* We thank Terence Eden and Roger Bamkin for providing the [source](https://code.google.com/archive/p/qrwp/) codes of QRpedia. We were inspired by the QRpedia Principles and we have even reused several excerpts as well as the QRpedia web service for the generation of the QRCode from URL in our source codes. As we built Sawtpedia based on QRpedia, we use the MIT License for our source code and we adopt the [Website Privacy Policy](https://wikimedia.org.uk/wiki/Website_Privacy_Policy) of [Wikimedia UK](https://wikimedia.org.uk) for our tool.
* We thank [Legoktm](https://www.mediawiki.org/wiki/User:Legoktm), [Mutante](https://www.mediawiki.org/wiki/User:Mutante), [AntiComposite](https://en.wikipedia.org/wiki/User:AntiCompositeNumber), [Reedy](https://www.mediawiki.org/wiki/User:Reedy), [RhinosF1](https://www.mediawiki.org/wiki/User:RhinosF1), and [Bryan Davis](https://www.mediawiki.org/wiki/User:BDavis_(WMF)) for supporting the deployment of the tool on Toolforge using SSH Server.
* We thank [Habib M'henni](https://commons.wikimedia.org/wiki/User:Dyolf77) from Wikimedia Tunisia for his contribution to our testing of the tool.
