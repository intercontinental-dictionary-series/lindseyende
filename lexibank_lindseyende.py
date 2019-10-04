import attr
from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Lexeme


@attr.s
class IDSLexeme(Lexeme):
    Transcription = attr.ib(default=None)
    AlternativeValue = attr.ib(default=None)
    AlternativeTranscription = attr.ib(default=None)

class IDSEntry:
    def __init__(self, ids_id, form, alt_form, comment):
        self.ids_id = ids_id
        self.form = form
        self.alt_form = alt_form
        self.comment = comment

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "lindseyende"

    lexeme_class = IDSLexeme

    def cmd_download(self, **kw):
        self.raw.xls2csv("ids_cl_ende_final.xlsx")

    def cmd_install(self, **kw):

        ccode = {
            x.attributes["ids_id"]:
                {
                    "concepticon_id": x.concepticon_id,
                    "concepticon_gloss": x.concepticon_gloss,
                    "name": x.english,
                }
                for x in self.conceptlist.concepts.values()
        }

        glottocode = "ende1235"
        lang_id = "endepapuanewguinea"

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())

            ds.add_language(
                ID=lang_id,
                Name="Ende (Papua New Guinea)",
                Glottocode=glottocode,
                # Latitude=-8.957653,
                # Longitude=142.239116,
            )

            for form in self.read_csv():
                ds.add_concept(
                    ID=form.ids_id,
                    Name=ccode[form.ids_id]["name"],
                    Concepticon_ID=ccode[form.ids_id]["concepticon_id"],
                    Concepticon_Gloss=ccode[form.ids_id]["concepticon_gloss"],
                )
                if form.form:
                    ds.add_lexemes(
                        Language_ID=lang_id,
                        Parameter_ID=form.ids_id,
                        Value=form.form,
                        Comment=form.comment,
                        Source="Lindsey2019",
                        Transcription="standardorth",
                        AlternativeValue=form.alt_form,
                        AlternativeTranscription="phonetic",
                    )

    def read_csv(self, fname="ids_cl_ende_final.idsclldorg.csv"):
        for i, row in enumerate(self.raw.read_csv(fname)):
            row = [c.strip() for c in row[0:10]]
            if i > 0:
                row[0:2] = [int(float(c)) for c in row[0:2]]
                entry = IDSEntry("%s-%s" % (row[0], row[1]), row[3], row[4], row[9])
                yield entry
