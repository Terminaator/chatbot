from langprocessing.wordTags import WordTag as wt


class ImportantUniWebsites:
    def canAnswer(self, layer):
        return wt.website in layer[wt.keywords] and len(layer[wt.websiteName]) != 0

    def answer(self, layer):
        """
        Returns commonly used university's webpage links
        :param siteName: webpage name, that was in the question
        :return: answer with link to asked site
        """
        siteName = layer[wt.websiteName]
        if siteName == "courses":
            return "Courses asub aadressil https://courses.cs.ut.ee/"
        elif siteName == "moodle":
            return "Moodle asub aadressil https://moodle.ut.ee/"
        elif siteName == "õis" or siteName == "õppeinfosüsteem":
            return "Tartu ülikooli ÕIS asub aadressil https://www.is.ut.ee/pls/ois_sso/tere.tulemast"
        elif siteName == "raamatukogu":
            return "Tartu ülikooli raamatukogu asub aadressil https://utlib.ut.ee/"
        elif siteName == "ester":
            return "Ester asub aadressil https://www.ester.ee/"
        elif siteName == "esileht":
            return "Tartu ülikooli esileht asub aadressil https://www.ut.ee/"
        return "Arendajad unustasid antud veebilehe lingi lisada või midagi läks valesti."

