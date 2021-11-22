#!usr/bin/activate
# license: 3-clause BSD license (see LICENSE.txt)
#
"""Astropy Digest notes, Vol. 181, Issue 8."""

# Topic: [Astropy] Some SIMBAD queries erroring?
# Author: Jim Singh
# Date: 2021-Oct-18, 13:12:27 CEST
# To: Astronomical Python mailing list

# Original query imports
from astroquery.jplhorizons import Horizons
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.time import Time
import astropy.coordinates as coord
from astropy.coordinates import Angle
# added imports
import astropy


def original():
    """Astropy Digest notes, Vol.181, Issue 8.

    Topic: Some SIMBAD queries erroring? (reproduced the original script by Issue_nr.8's author, only for reference purposes.)
    Original snipet/script from Jim Singh.
    """

    observing_time = Time.strptime('2021-Oct-18 09:30:00',
    '%Y-%b-%d %H:%M:%S')

    # obj = Horizons(id="ceres", location=None, epochs=observing_time.jd)
    # The Simbad query for "ceres", "pallas", "vesta" fails, but id=199 returns
    # a result.

    obj = Horizons(id='599', id_type='majorbody', location=None,
    epochs=observing_time.jd)
    # The Simbad query for '599' and '699' fails, but '799' and '899' return
    # a result.

    # ----Fetch RA and Dec of object from JPL Horizons----
    eph = obj.ephemerides()
    CentreRA = eph['RA'][0]
    CentreDec = eph['DEC'][0]
    a = Angle(CentreRA, u.deg)
    CentreRAhms = (a.to_string(unit=u.hour))
    b = Angle(CentreDec, u.deg)
    CentreDecdms = (b.to_string(unit=u.deg))
    CoordStr = (CentreRAhms + "" + CentreDecdms)
    print(CoordStr)

    # ----Query SIMBAD----
    result = Simbad.query_region(coord.SkyCoord(CoordStr,
    frame='icrs'), radius='1d0m0s')
    print(result)

def modified(observing_time: astropy.time.core.Time, obj_list: list) -> dict:
    """Astropy Digest notes, Vol.181, Issue 8, with additions.

    Calculate Coordinates of a list of objects from SIMBAD queries (modified query by AstroThings' author).

    **Example 1**: calculate coordinates of a list of objects.
    >>> observing_time = Time.strptime('2021-Oct-18 09:30:00', '%Y-%b-%d %H:%M:%S')

    >>> obj_dict = modified(observing_time, ['ceres', 'pallas', 'vesta', '199'])

    >>> for key, value in obj_dict.items():
    ...     print(key,': ', value, sep='')
    ceres: 4h43m28.3464s16d12m45.18s
    pallas: 22h47m11.4912s-8d06m02.7s
    vesta: 14h51m19.3944s-12d20m11.184s
    199: 22h47m40.224s-29d14m33.144s
    """
    try:
        obj_dict = {}
        for item in obj_list:
            obj =  Horizons(id=item, location=None, epochs=observing_time.jd)
            eph = obj.ephemerides()
            CentreRA = eph['RA'][0]
            CentreDec = eph['DEC'][0]
            a = Angle(CentreRA, u.deg)
            CentreRAhms = (a.to_string(unit=u.hour))
            b = Angle(CentreDec, u.deg)
            CentreDecdms = (b.to_string(unit=u.deg))
            CoordStr = (CentreRAhms + "" + CentreDecdms)
            obj_dict.update({item: CoordStr})
    except ValueError:
        print('No value found for object id: ', obj.id)
    return obj_dict


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
