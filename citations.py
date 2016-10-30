"""Used for citing all third party images.

An image could have several derivatives.
In that case each derivative has its own citation.
"""
ACCEPTABLE_LICENSES = {'cc0', 'public domain', 'cc by'}

IMAGES_CITED = set()    # File names
FIRST_IMAGE_TO_CITATION_MAP = {}


class ImageCitation(object):
    """
    Used for citing each individual work.
    Citation includes all related data along with extra requirements by the copyright owner.

    NOTE: Assumes the returned text will be displayed with markup enabled.
    """

    def __init__(self,
                 work_name,
                 creation_date,
                 licence,
                 adaptation,
                 file_names,
                 creator_name=None, creator_pseudonym=None,
                 url='',
                 extra_text='',
                 ignore=False):
        """
        Takes all needed data for the citation.
        Creator can be identified by either name or pseudonym.

        In case of a pseudonym, pseudonym related origin should be present.

        WARNING: In case of multiple files, start with original file
            since only the first image is displayed.

        :param work_name: (str)
        :param creator_name: (str)
        :param creator_pseudonym: (str) Pseudonym with pseudonym origin, e.g. "TallPony (wikipedia user)"
        :param creation_date: (str) Work creation date. e.g. 10-May-2015 (avoid displaying month as a number)
        :param url: (str)
        :param licence: (str) "cc0", "public domain" etc
        :param adaptation: (bool) Adapted (modified) or original work (refers to first file in file_names)
        :param file_names: (list) Names of all image files derived from the work.
        :param extra_text: (str) Extra text required by the copyright owner.
        :param ignore: (bool) Used if citation has been created but image is not included.
            Useful in case image is used again, in order to avoid creating citation again.
        """
        if not (creator_name or creator_pseudonym):
            raise ValueError('At least one of `creator_name` and `creator_pseudonym` should be provided.')
        if creator_name and creator_pseudonym:
            raise ValueError('Only one of `creator_name` and `creator_pseudonym` should be provided.')
        if licence not in ACCEPTABLE_LICENSES:
            raise ValueError('Licence not acceptable')

        self.file_names = file_names
        self.adaptation = adaptation
        self.licence = licence
        self.url = url
        self.creation_date = creation_date
        self.creator_name = creator_name
        self.creator_pseudonym = creator_pseudonym
        self._creator = creator_name or creator_pseudonym
        self.work_name = work_name
        self.extra_text = extra_text

        if not ignore:
            IMAGES_CITED.update(file_names)
            FIRST_IMAGE_TO_CITATION_MAP.update({file_names[0]: self})

    def full_text(self):
        """
        Final citation text.

        NOTE: Assumes markup is done by "[b]", "[size=8]", etc.
        """
        final_text = ("[b]{work_name}[/b] image by {creator} ({creation_date}). "
                      "\n[size=10]{url}[/size]").format(work_name=self.work_name,
                                                        creator=self._creator,
                                                        creation_date=self.creation_date,
                                                        url=self.url)

        if self.adaptation:
            final_text = 'My adaptation of ' + final_text

        if self.extra_text:
            final_text += '\n' + self.extra_text

        return '[size=12]{}[/size]'.format(final_text)


# (To be used for copy-pasting when creating new ImageCitation
# in order to avoid accidentally forgetting to change an arg value.)
"""
 = ImageCitation(
    work_name=,
    creation_date=,
    licence=,
    adaptation=,
    file_names=,
    creator_name=,
    creator_pseudonym=,
    url=,
    extra_text=)
"""


KICK = ImageCitation(
    work_name='kickboxing-kick-karate-muay-thai-150330',
    creation_date='Oct 12, 2013',
    licence='cc0',
    adaptation=False,
    file_names=['kick.png'],
    creator_name=None,
    creator_pseudonym='OpenClipart-Vectors (pixabay user)',
    url='https://pixabay.com/en/kickboxing-kick-karate-muay-thai-150330/',
    extra_text='')

HEALTH = ImageCitation(
    work_name='medicine-37101',
    creation_date='April 18, 2012',
    licence='cc0',
    adaptation=False,
    file_names=['medicine.png'],
    creator_name=None,
    creator_pseudonym='Clker-Free-Vector-Images (pixabay user)',
    url='https://pixabay.com/en/medicine-pharmacy-doctor-medic-37101/',
    extra_text='')

SUN = ImageCitation(
    work_name='M7.9-Class Solar Flare',
    creation_date='June 25, 2015',
    licence='public domain',
    adaptation=False,
    file_names=['nasa_sun.png'],
    creator_name='NASA/SDO',
    creator_pseudonym=None,
    url='http://www.nasa.gov/image-feature/solar-dynamics-observatory-sees-m79-class-solar-flare',
    extra_text='')

