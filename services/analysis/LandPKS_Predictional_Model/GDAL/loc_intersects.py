"""
name: loc_intersects.py
author: J.W. Karl
Modifier : Thanh Nguyen
date: 5/3/13
Update : 6/22/14
purpose: accepts input csv from location_parser.py, intersects the points with the JournalMap search/similarity layers to get the values at each point, and structures the locations.csv table to be uploaded into JournalMap
arguments: none, but paths and file inputs need to be modified below
"""
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy
from __builtin__ import str

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
    
def getRasterValue(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    try:
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_UInt16)  # Assumes 16 bit int aka 'short'
        intval = struct.unpack('h' , structval)  # use the 'short' format code (2 bytes) not int (4 bytes)
        return(intval[0])
    except Exception,err:
        return -1
def getRasterValue_ThanhNH(srcfile, mx, my):  
    try:# # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception,err:
        return -1
def getRasterValue_ThanhNH_Float(srcfile, mx, my):
    try:  # # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
        return structval[0][0]
    except Exception,err:
        return -1
def lookupState(statecode):
    states = {1:'Hawaii', 2:'Washington', 3:'Montana', 4:'Maine', 5:'North Dakota', 6:'South Dakota', 7:'Wyoming', 8:'Wisconsin', 9:'Idaho', 10:'Vermont', 11:'Minnesota', 12:'Oregon', 13:'New Hampshire', 14:'Iowa', 15:'Massachusetts', 16:'Nebraska', 17:'New York', 18:'Pennsylvania', 19:'Connecticut', 20:'Rhode Island', 21:'New Jersey', 22:'Indiana', 23:'Nevada', 24:'Utah', 25:'California', 26:'Ohio', 27:'Illinois', 28:'District of Columbia', 29:'Delaware', 30:'West Virginia', 31:'Maryland', 32:'Colorado', 33:'Kentucky', 34:'Kansas', 35:'Virginia', 36:'Missouri', 37:'Arizona', 38:'Oklahoma', 39:'North Carolina', 40:'Tennessee', 41:'Texas', 42:'New Mexico', 43:'Alabama', 44:'Mississippi', 45:'Georgia', 46:'South Carolina', 47:'Arkansas', 48:'Louisiana', 49:'Florida', 50:'Michigan', 51:'Alaska'}
    try:
        state = states[statecode]
    except:
        state = ''
    return state

def lookupCountry(isocode):
    countries = {0:'', 4:'Afghanistan', 8:'Albania', 10:'Antarctica', 12:'Algeria', 16:'American Samoa', 20:'Andorra', 24:'Angola', 28:'Antigua & Barbuda', 31:'Azerbaijan', 32:'Argentina', 36:'Australia', 40:'Austria', 44:'The Bahamas', 48:'Bahrain', 50:'Bangladesh', 51:'Armenia', 52:'Barbados', 56:'Belgium', 60:'Bermuda', 64:'Bhutan', 68:'Bolivia', 70:'Bosnia & Herzegovina', 72:'Botswana', 74:'Bouvet I.', 76:'Brazil', 84:'Belize', 86:'British Indian Ocean Territory', 90:'Solomon Is.', 92:'British Virgin Is.', 96:'Brunei', 100:'Bulgaria', 104:'Myanmar', 108:'Burundi', 112:'Belarus', 116:'Cambodia', 120:'Cameroon', 124:'Canada', 132:'Cape Verde', 136:'Cayman Is.', 140:'Central African Republic', 144:'Sri Lanka', 148:'Chad', 152:'Chile', 156:'China', 162:'Christmas I.', 166:'Cocos Is.', 170:'Colombia', 174:'Comoros', 175:'Mayotte', 178:'Congo', 180:'Congo, DRC', 184:'Cook Is.', 188:'Costa Rica', 191:'Croatia', 192:'Cuba', 196:'Cyprus', 203:'Czech Republic', 204:'Benin', 208:'Denmark', 212:'Dominica', 214:'Dominican Republic', 218:'Ecuador', 222:'El Salvador', 226:'Equatorial Guinea', 231:'Ethiopia', 232:'Eritrea', 233:'Estonia', 234:'Faroe Is.', 238:'Falkland Is.', 239:'South Georgia & the South Sandwich Is.', 242:'Fiji', 246:'Finland', 250:'France', 254:'French Guiana', 258:'French Polynesia', 260:'French Southern & Antarctic Lands', 262:'Djibouti', 266:'Gabon', 268:'Georgia', 270:'The Gambia', 276:'Germany', 288:'Ghana', 292:'Gibraltar', 296:'Kiribati', 300:'Greece', 304:'Greenland', 308:'Grenada', 312:'Guadeloupe', 316:'Guam', 320:'Guatemala', 324:'Guinea', 328:'Guyana', 332:'Haiti', 334:'Heard I. & McDonald Is.', 336:'Vatican City', 340:'Honduras', 348:'Hungary', 352:'Iceland', 356:'India', 360:'Indonesia', 364:'Iran', 368:'Iraq', 372:'Ireland', 376:'Israel', 380:'Italy', 384:'Cote dIvoire', 388:'Jamaica', 392:'Japan', 398:'Kazakhstan', 400:'Jordan', 404:'Kenya', 408:'North Korea', 410:'South Korea', 414:'Kuwait', 417:'Kyrgyzstan', 418:'Laos', 422:'Lebanon', 426:'Lesotho', 428:'Latvia', 430:'Liberia', 434:'Libya', 438:'Liechtenstein', 440:'Lithuania', 442:'Luxembourg', 450:'Madagascar', 454:'Malawi', 458:'Malaysia', 462:'Maldives', 466:'Mali', 470:'Malta', 474:'Martinique', 478:'Mauritania', 480:'Mauritius', 484:'Mexico', 492:'Monaco', 496:'Mongolia', 498:'Moldova', 500:'Montserrat', 504:'Morocco', 508:'Mozambique', 512:'Oman', 516:'Namibia', 520:'Nauru', 524:'Nepal', 528:'Netherlands', 530:'Netherlands Antilles', 533:'Aruba', 540:'New Caledonia', 548:'Vanuatu', 554:'New Zealand', 558:'Nicaragua', 562:'Niger', 566:'Nigeria', 570:'Niue', 574:'Norfolk I.', 578:'Norway', 580:'Northern Mariana Is.', 581:'Baker I.', 581:'Howland I.', 581:'Jarvis I.', 581:'Johnston Atoll', 581:'Midway Is.', 581:'Wake I.', 583:'Micronesia', 584:'Marshall Is.', 585:'Palau', 586:'Pakistan', 591:'Panama', 598:'Papua New Guinea', 600:'Paraguay', 604:'Peru', 608:'Philippines', 612:'Pitcairn Is.', 616:'Poland', 620:'Portugal', 624:'Guinea-Bissau', 626:'Timor Leste', 630:'Puerto Rico', 634:'Qatar', 638:'Reunion', 642:'Romania', 643:'Russia', 646:'Rwanda', 654:'St. Helena', 659:'St. Kitts & Nevis', 660:'Anguilla', 662:'St. Lucia', 666:'St. Pierre & Miquelon', 670:'St. Vincent & the Grenadines', 674:'San Marino', 678:'Sao Tome & Principe', 682:'Saudi Arabia', 686:'Senegal', 690:'Seychelles', 694:'Sierra Leone', 702:'Singapore', 703:'Slovakia', 704:'Vietnam', 705:'Slovenia', 706:'Somalia', 710:'South Africa', 716:'Zimbabwe', 724:'Spain', 732:'Western Sahara', 736:'Sudan', 740:'Suriname', 744:'Jan Mayen', 744:'Svalbard', 748:'Swaziland', 752:'Sweden', 756:'Switzerland', 760:'Syria', 762:'Tajikistan', 764:'Thailand', 768:'Togo', 772:'Tokelau', 776:'Tonga', 780:'Trinidad & Tobago', 784:'United Arab Emirates', 788:'Tunisia', 792:'Turkey', 795:'Turkmenistan', 796:'Turks & Caicos Is.', 798:'Tuvalu', 800:'Uganda', 804:'Ukraine', 807:'Macedonia', 818:'Egypt', 826:'United Kingdom', 833:'Isle of Man', 834:'Tanzania', 840:'United States', 850:'Virgin Is.', 854:'Burkina Faso', 858:'Uruguay', 860:'Uzbekistan', 862:'Venezuela', 876:'Wallis & Futuna', 882:'Samoa', 887:'Yemen', 891:'Serbia & Montenegro', 894:'Zambia'}
    try:
        country = countries[isocode]
    except:
        country = ''
    return country

def lookupBiome(ecoid):  # # I mistakenly ran the biome intersections on ecoregion. Easier to correct for it here than to rerun. This also preserves ability to get ecoregions down the road if we want/need.
    biomes = {-9999:'rock and ice', -9998:'lake', 10101:'Tropical and subtropical moist broadleaf forests', 10102:'Tropical and subtropical moist broadleaf forests', 10103:'Tropical and subtropical moist broadleaf forests', 10104:'Tropical and subtropical moist broadleaf forests', 10105:'Tropical and subtropical moist broadleaf forests', 10106:'Tropical and subtropical moist broadleaf forests', 10107:'Tropical and subtropical moist broadleaf forests', 10108:'Tropical and subtropical moist broadleaf forests', 10109:'Tropical and subtropical moist broadleaf forests', 10110:'Tropical and subtropical moist broadleaf forests', 10111:'Tropical and subtropical moist broadleaf forests', 10112:'Tropical and subtropical moist broadleaf forests', 10113:'Tropical and subtropical moist broadleaf forests', 10114:'Tropical and subtropical moist broadleaf forests', 10115:'Tropical and subtropical moist broadleaf forests', 10116:'Tropical and subtropical moist broadleaf forests', 10117:'Tropical and subtropical moist broadleaf forests', 10118:'Tropical and subtropical moist broadleaf forests', 10119:'Tropical and subtropical moist broadleaf forests', 10120:'Tropical and subtropical moist broadleaf forests', 10121:'Tropical and subtropical moist broadleaf forests', 10122:'Tropical and subtropical moist broadleaf forests', 10123:'Tropical and subtropical moist broadleaf forests', 10124:'Tropical and subtropical moist broadleaf forests', 10125:'Tropical and subtropical moist broadleaf forests', 10126:'Tropical and subtropical moist broadleaf forests', 10127:'Tropical and subtropical moist broadleaf forests', 10128:'Tropical and subtropical moist broadleaf forests', 10201:'Tropical and subtropical dry broadleaf forests', 10202:'Tropical and subtropical dry broadleaf forests', 10203:'Tropical and subtropical dry broadleaf forests', 10204:'Tropical and subtropical dry broadleaf forests', 10401:'temperate broadleaf and mixed forests', 10402:'temperate broadleaf and mixed forests', 10403:'temperate broadleaf and mixed forests', 10404:'temperate broadleaf and mixed forests', 10405:'temperate broadleaf and mixed forests', 10406:'temperate broadleaf and mixed forests', 10407:'temperate broadleaf and mixed forests', 10408:'temperate broadleaf and mixed forests', 10409:'temperate broadleaf and mixed forests', 10410:'temperate broadleaf and mixed forests', 10411:'temperate broadleaf and mixed forests', 10412:'temperate broadleaf and mixed forests', 10413:'temperate broadleaf and mixed forests', 10414:'temperate broadleaf and mixed forests', 10701:'tropical and subtropical grasslands, savannas, sh*', 10702:'tropical and subtropical grasslands, savannas, sh*', 10703:'tropical and subtropical grasslands, savannas, sh*', 10704:'tropical and subtropical grasslands, savannas, sh*', 10705:'tropical and subtropical grasslands, savannas, sh*', 10706:'tropical and subtropical grasslands, savannas, sh*', 10707:'tropical and subtropical grasslands, savannas, sh*', 10708:'tropical and subtropical grasslands, savannas, sh*', 10709:'tropical and subtropical grasslands, savannas, sh*', 10801:'temperate grasslands, savannas, and shrublands', 10802:'temperate grasslands, savannas, and shrublands', 10803:'temperate grasslands, savannas, and shrublands', 11001:'montane grasslands and shrublands', 11002:'montane grasslands and shrublands', 11003:'montane grasslands and shrublands', 11101:'tundra', 11201:'Mediterranean forests, woodlands, and scrub', 11202:'Mediterranean forests, woodlands, and scrub', 11203:'Mediterranean forests, woodlands, and scrub', 11204:'Mediterranean forests, woodlands, and scrub', 11205:'Mediterranean forests, woodlands, and scrub', 11206:'Mediterranean forests, woodlands, and scrub', 11207:'Mediterranean forests, woodlands, and scrub', 11208:'Mediterranean forests, woodlands, and scrub', 11209:'Mediterranean forests, woodlands, and scrub', 11210:'Mediterranean forests, woodlands, and scrub', 11301:'deserts and xeric shrublands', 11302:'deserts and xeric shrublands', 11303:'deserts and xeric shrublands', 11304:'deserts and xeric shrublands', 11305:'deserts and xeric shrublands', 11306:'deserts and xeric shrublands', 11307:'deserts and xeric shrublands', 11308:'deserts and xeric shrublands', 11309:'deserts and xeric shrublands', 11310:'deserts and xeric shrublands', 11401:'mangroves', 21101:'tundra', 21102:'tundra', 21103:'tundra', 21104:'tundra', 30101:'Tropical and subtropical moist broadleaf forests', 30102:'Tropical and subtropical moist broadleaf forests', 30103:'Tropical and subtropical moist broadleaf forests', 30104:'Tropical and subtropical moist broadleaf forests', 30105:'Tropical and subtropical moist broadleaf forests', 30106:'Tropical and subtropical moist broadleaf forests', 30107:'Tropical and subtropical moist broadleaf forests', 30108:'Tropical and subtropical moist broadleaf forests', 30109:'Tropical and subtropical moist broadleaf forests', 30110:'Tropical and subtropical moist broadleaf forests', 30111:'Tropical and subtropical moist broadleaf forests', 30112:'Tropical and subtropical moist broadleaf forests', 30113:'Tropical and subtropical moist broadleaf forests', 30114:'Tropical and subtropical moist broadleaf forests', 30115:'Tropical and subtropical moist broadleaf forests', 30116:'Tropical and subtropical moist broadleaf forests', 30117:'Tropical and subtropical moist broadleaf forests', 30118:'Tropical and subtropical moist broadleaf forests', 30119:'Tropical and subtropical moist broadleaf forests', 30120:'Tropical and subtropical moist broadleaf forests', 30121:'Tropical and subtropical moist broadleaf forests', 30122:'Tropical and subtropical moist broadleaf forests', 30123:'Tropical and subtropical moist broadleaf forests', 30124:'Tropical and subtropical moist broadleaf forests', 30125:'Tropical and subtropical moist broadleaf forests', 30126:'Tropical and subtropical moist broadleaf forests', 30127:'Tropical and subtropical moist broadleaf forests', 30128:'Tropical and subtropical moist broadleaf forests', 30129:'Tropical and subtropical moist broadleaf forests', 30130:'Tropical and subtropical moist broadleaf forests', 30201:'Tropical and subtropical dry broadleaf forests', 30202:'Tropical and subtropical dry broadleaf forests', 30203:'Tropical and subtropical dry broadleaf forests', 30701:'tropical and subtropical grasslands, savannas, sh*', 30702:'tropical and subtropical grasslands, savannas, sh*', 30703:'tropical and subtropical grasslands, savannas, sh*', 30704:'tropical and subtropical grasslands, savannas, sh*', 30705:'tropical and subtropical grasslands, savannas, sh*', 30706:'tropical and subtropical grasslands, savannas, sh*', 30707:'tropical and subtropical grasslands, savannas, sh*', 30708:'tropical and subtropical grasslands, savannas, sh*', 30709:'tropical and subtropical grasslands, savannas, sh*', 30710:'tropical and subtropical grasslands, savannas, sh*', 30711:'tropical and subtropical grasslands, savannas, sh*', 30712:'tropical and subtropical grasslands, savannas, sh*', 30713:'tropical and subtropical grasslands, savannas, sh*', 30714:'tropical and subtropical grasslands, savannas, sh*', 30715:'tropical and subtropical grasslands, savannas, sh*', 30716:'tropical and subtropical grasslands, savannas, sh*', 30717:'tropical and subtropical grasslands, savannas, sh*', 30718:'tropical and subtropical grasslands, savannas, sh*', 30719:'tropical and subtropical grasslands, savannas, sh*', 30720:'tropical and subtropical grasslands, savannas, sh*', 30721:'tropical and subtropical grasslands, savannas, sh*', 30722:'tropical and subtropical grasslands, savannas, sh*', 30723:'tropical and subtropical grasslands, savannas, sh*', 30724:'tropical and subtropical grasslands, savannas, sh*', 30725:'tropical and subtropical grasslands, savannas, sh*', 30726:'tropical and subtropical grasslands, savannas, sh*', 30801:'temperate grasslands, savannas, and shrublands', 30802:'temperate grasslands, savannas, and shrublands', 30803:'temperate grasslands, savannas, and shrublands', 30901:'flooded grasslands and savannas', 30902:'flooded grasslands and savannas', 30903:'flooded grasslands and savannas', 30904:'flooded grasslands and savannas', 30905:'flooded grasslands and savannas', 30906:'flooded grasslands and savannas', 30907:'flooded grasslands and savannas', 30908:'flooded grasslands and savannas', 31001:'montane grasslands and shrublands', 31002:'montane grasslands and shrublands', 31003:'montane grasslands and shrublands', 31004:'montane grasslands and shrublands', 31005:'montane grasslands and shrublands', 31006:'montane grasslands and shrublands', 31007:'montane grasslands and shrublands', 31008:'montane grasslands and shrublands', 31009:'montane grasslands and shrublands', 31010:'montane grasslands and shrublands', 31011:'montane grasslands and shrublands', 31012:'montane grasslands and shrublands', 31013:'montane grasslands and shrublands', 31014:'montane grasslands and shrublands', 31015:'montane grasslands and shrublands', 31201:'Mediterranean forests, woodlands, and scrub', 31202:'Mediterranean forests, woodlands, and scrub', 31203:'Mediterranean forests, woodlands, and scrub', 31301:'deserts and xeric shrublands', 31302:'deserts and xeric shrublands', 31303:'deserts and xeric shrublands', 31304:'deserts and xeric shrublands', 31305:'deserts and xeric shrublands', 31306:'deserts and xeric shrublands', 31307:'deserts and xeric shrublands', 31308:'deserts and xeric shrublands', 31309:'deserts and xeric shrublands', 31310:'deserts and xeric shrublands', 31311:'deserts and xeric shrublands', 31312:'deserts and xeric shrublands', 31313:'deserts and xeric shrublands', 31314:'deserts and xeric shrublands', 31315:'deserts and xeric shrublands', 31316:'deserts and xeric shrublands', 31318:'deserts and xeric shrublands', 31319:'deserts and xeric shrublands', 31320:'deserts and xeric shrublands', 31321:'deserts and xeric shrublands', 31322:'deserts and xeric shrublands', 31401:'mangroves', 31402:'mangroves', 31403:'mangroves', 31404:'mangroves', 31405:'mangroves', 40101:'Tropical and subtropical moist broadleaf forests', 40102:'Tropical and subtropical moist broadleaf forests', 40103:'Tropical and subtropical moist broadleaf forests', 40104:'Tropical and subtropical moist broadleaf forests', 40105:'Tropical and subtropical moist broadleaf forests', 40106:'Tropical and subtropical moist broadleaf forests', 40107:'Tropical and subtropical moist broadleaf forests', 40108:'Tropical and subtropical moist broadleaf forests', 40109:'Tropical and subtropical moist broadleaf forests', 40110:'Tropical and subtropical moist broadleaf forests', 40111:'Tropical and subtropical moist broadleaf forests', 40112:'Tropical and subtropical moist broadleaf forests', 40113:'Tropical and subtropical moist broadleaf forests', 40114:'Tropical and subtropical moist broadleaf forests', 40115:'Tropical and subtropical moist broadleaf forests', 40116:'Tropical and subtropical moist broadleaf forests', 40117:'Tropical and subtropical moist broadleaf forests', 40118:'Tropical and subtropical moist broadleaf forests', 40119:'Tropical and subtropical moist broadleaf forests', 40120:'Tropical and subtropical moist broadleaf forests', 40121:'Tropical and subtropical moist broadleaf forests', 40122:'Tropical and subtropical moist broadleaf forests', 40123:'Tropical and subtropical moist broadleaf forests', 40124:'Tropical and subtropical moist broadleaf forests', 40125:'Tropical and subtropical moist broadleaf forests', 40126:'Tropical and subtropical moist broadleaf forests', 40127:'Tropical and subtropical moist broadleaf forests', 40128:'Tropical and subtropical moist broadleaf forests', 40129:'Tropical and subtropical moist broadleaf forests', 40130:'Tropical and subtropical moist broadleaf forests', 40131:'Tropical and subtropical moist broadleaf forests', 40132:'Tropical and subtropical moist broadleaf forests', 40133:'Tropical and subtropical moist broadleaf forests', 40134:'Tropical and subtropical moist broadleaf forests', 40135:'Tropical and subtropical moist broadleaf forests', 40136:'Tropical and subtropical moist broadleaf forests', 40137:'Tropical and subtropical moist broadleaf forests', 40138:'Tropical and subtropical moist broadleaf forests', 40139:'Tropical and subtropical moist broadleaf forests', 40140:'Tropical and subtropical moist broadleaf forests', 40141:'Tropical and subtropical moist broadleaf forests', 40142:'Tropical and subtropical moist broadleaf forests', 40143:'Tropical and subtropical moist broadleaf forests', 40144:'Tropical and subtropical moist broadleaf forests', 40145:'Tropical and subtropical moist broadleaf forests', 40146:'Tropical and subtropical moist broadleaf forests', 40147:'Tropical and subtropical moist broadleaf forests', 40148:'Tropical and subtropical moist broadleaf forests', 40149:'Tropical and subtropical moist broadleaf forests', 40150:'Tropical and subtropical moist broadleaf forests', 40151:'Tropical and subtropical moist broadleaf forests', 40152:'Tropical and subtropical moist broadleaf forests', 40153:'Tropical and subtropical moist broadleaf forests', 40154:'Tropical and subtropical moist broadleaf forests', 40155:'Tropical and subtropical moist broadleaf forests', 40156:'Tropical and subtropical moist broadleaf forests', 40157:'Tropical and subtropical moist broadleaf forests', 40158:'Tropical and subtropical moist broadleaf forests', 40159:'Tropical and subtropical moist broadleaf forests', 40160:'Tropical and subtropical moist broadleaf forests', 40161:'Tropical and subtropical moist broadleaf forests', 40162:'Tropical and subtropical moist broadleaf forests', 40163:'Tropical and subtropical moist broadleaf forests', 40164:'Tropical and subtropical moist broadleaf forests', 40165:'Tropical and subtropical moist broadleaf forests', 40166:'Tropical and subtropical moist broadleaf forests', 40167:'Tropical and subtropical moist broadleaf forests', 40168:'Tropical and subtropical moist broadleaf forests', 40169:'Tropical and subtropical moist broadleaf forests', 40170:'Tropical and subtropical moist broadleaf forests', 40171:'Tropical and subtropical moist broadleaf forests', 40172:'Tropical and subtropical moist broadleaf forests', 40201:'Tropical and subtropical dry broadleaf forests', 40202:'Tropical and subtropical dry broadleaf forests', 40203:'Tropical and subtropical dry broadleaf forests', 40204:'Tropical and subtropical dry broadleaf forests', 40205:'Tropical and subtropical dry broadleaf forests', 40206:'Tropical and subtropical dry broadleaf forests', 40207:'Tropical and subtropical dry broadleaf forests', 40208:'Tropical and subtropical dry broadleaf forests', 40209:'Tropical and subtropical dry broadleaf forests', 40210:'Tropical and subtropical dry broadleaf forests', 40211:'Tropical and subtropical dry broadleaf forests', 40212:'Tropical and subtropical dry broadleaf forests', 40301:'tropical and subtropical coniferous forests', 40302:'tropical and subtropical coniferous forests', 40303:'tropical and subtropical coniferous forests', 40304:'tropical and subtropical coniferous forests', 40401:'temperate broadleaf and mixed forests', 40402:'temperate broadleaf and mixed forests', 40403:'temperate broadleaf and mixed forests', 40501:'temperate coniferous forests', 40502:'temperate coniferous forests', 40701:'tropical and subtropical grasslands, savannas, sh*', 40901:'flooded grasslands and savannas', 41001:'montane grasslands and shrublands', 41301:'deserts and xeric shrublands', 41302:'deserts and xeric shrublands', 41303:'deserts and xeric shrublands', 41304:'deserts and xeric shrublands', 41401:'mangroves', 41402:'mangroves', 41403:'mangroves', 41404:'mangroves', 41405:'mangroves', 41406:'mangroves', 50201:'Tropical and subtropical dry broadleaf forests', 50301:'tropical and subtropical coniferous forests', 50302:'tropical and subtropical coniferous forests', 50303:'tropical and subtropical coniferous forests', 50401:'temperate broadleaf and mixed forests', 50402:'temperate broadleaf and mixed forests', 50403:'temperate broadleaf and mixed forests', 50404:'temperate broadleaf and mixed forests', 50405:'temperate broadleaf and mixed forests', 50406:'temperate broadleaf and mixed forests', 50407:'temperate broadleaf and mixed forests', 50408:'temperate broadleaf and mixed forests', 50409:'temperate broadleaf and mixed forests', 50410:'temperate broadleaf and mixed forests', 50411:'temperate broadleaf and mixed forests', 50412:'temperate broadleaf and mixed forests', 50413:'temperate broadleaf and mixed forests', 50414:'temperate broadleaf and mixed forests', 50415:'temperate broadleaf and mixed forests', 50416:'temperate broadleaf and mixed forests', 50417:'temperate broadleaf and mixed forests', 50501:'temperate coniferous forests', 50502:'temperate coniferous forests', 50503:'temperate coniferous forests', 50504:'temperate coniferous forests', 50505:'temperate coniferous forests', 50506:'temperate coniferous forests', 50507:'temperate coniferous forests', 50508:'temperate coniferous forests', 50509:'temperate coniferous forests', 50510:'temperate coniferous forests', 50511:'temperate coniferous forests', 50512:'temperate coniferous forests', 50513:'temperate coniferous forests', 50514:'temperate coniferous forests', 50515:'temperate coniferous forests', 50516:'temperate coniferous forests', 50517:'temperate coniferous forests', 50518:'temperate coniferous forests', 50519:'temperate coniferous forests', 50520:'temperate coniferous forests', 50521:'temperate coniferous forests', 50522:'temperate coniferous forests', 50523:'temperate coniferous forests', 50524:'temperate coniferous forests', 50525:'temperate coniferous forests', 50526:'temperate coniferous forests', 50527:'temperate coniferous forests', 50528:'temperate coniferous forests', 50529:'temperate coniferous forests', 50530:'temperate coniferous forests', 50601:'Boreal forests/taiga', 50602:'Boreal forests/taiga', 50603:'Boreal forests/taiga', 50604:'Boreal forests/taiga', 50605:'Boreal forests/taiga', 50606:'Boreal forests/taiga', 50607:'Boreal forests/taiga', 50608:'Boreal forests/taiga', 50609:'Boreal forests/taiga', 50610:'Boreal forests/taiga', 50611:'Boreal forests/taiga', 50612:'Boreal forests/taiga', 50613:'Boreal forests/taiga', 50614:'Boreal forests/taiga', 50615:'Boreal forests/taiga', 50616:'Boreal forests/taiga', 50617:'Boreal forests/taiga', 50701:'tropical and subtropical grasslands, savannas, sh*', 50801:'temperate grasslands, savannas, and shrublands', 50802:'temperate grasslands, savannas, and shrublands', 50803:'temperate grasslands, savannas, and shrublands', 50804:'temperate grasslands, savannas, and shrublands', 50805:'temperate grasslands, savannas, and shrublands', 50806:'temperate grasslands, savannas, and shrublands', 50807:'temperate grasslands, savannas, and shrublands', 50808:'temperate grasslands, savannas, and shrublands', 50809:'temperate grasslands, savannas, and shrublands', 50810:'temperate grasslands, savannas, and shrublands', 50811:'temperate grasslands, savannas, and shrublands', 50812:'temperate grasslands, savannas, and shrublands', 50813:'temperate grasslands, savannas, and shrublands', 50814:'temperate grasslands, savannas, and shrublands', 50815:'temperate grasslands, savannas, and shrublands', 51101:'tundra', 51102:'tundra', 51103:'tundra', 51104:'tundra', 51105:'tundra', 51106:'tundra', 51107:'tundra', 51108:'tundra', 51109:'tundra', 51110:'tundra', 51111:'tundra', 51112:'tundra', 51113:'tundra', 51114:'tundra', 51115:'tundra', 51116:'tundra', 51117:'tundra', 51118:'tundra', 51201:'Mediterranean forests, woodlands, and scrub', 51202:'Mediterranean forests, woodlands, and scrub', 51203:'Mediterranean forests, woodlands, and scrub', 51301:'deserts and xeric shrublands', 51302:'deserts and xeric shrublands', 51303:'deserts and xeric shrublands', 51304:'deserts and xeric shrublands', 51305:'deserts and xeric shrublands', 51306:'deserts and xeric shrublands', 51307:'deserts and xeric shrublands', 51308:'deserts and xeric shrublands', 51309:'deserts and xeric shrublands', 51310:'deserts and xeric shrublands', 51311:'deserts and xeric shrublands', 51312:'deserts and xeric shrublands', 51313:'deserts and xeric shrublands', 60101:'Tropical and subtropical moist broadleaf forests', 60102:'Tropical and subtropical moist broadleaf forests', 60103:'Tropical and subtropical moist broadleaf forests', 60104:'Tropical and subtropical moist broadleaf forests', 60105:'Tropical and subtropical moist broadleaf forests', 60106:'Tropical and subtropical moist broadleaf forests', 60107:'Tropical and subtropical moist broadleaf forests', 60108:'Tropical and subtropical moist broadleaf forests', 60109:'Tropical and subtropical moist broadleaf forests', 60110:'Tropical and subtropical moist broadleaf forests', 60111:'Tropical and subtropical moist broadleaf forests', 60112:'Tropical and subtropical moist broadleaf forests', 60113:'Tropical and subtropical moist broadleaf forests', 60114:'Tropical and subtropical moist broadleaf forests', 60115:'Tropical and subtropical moist broadleaf forests', 60116:'Tropical and subtropical moist broadleaf forests', 60117:'Tropical and subtropical moist broadleaf forests', 60118:'Tropical and subtropical moist broadleaf forests', 60119:'Tropical and subtropical moist broadleaf forests', 60120:'Tropical and subtropical moist broadleaf forests', 60121:'Tropical and subtropical moist broadleaf forests', 60122:'Tropical and subtropical moist broadleaf forests', 60123:'Tropical and subtropical moist broadleaf forests', 60124:'Tropical and subtropical moist broadleaf forests', 60125:'Tropical and subtropical moist broadleaf forests', 60126:'Tropical and subtropical moist broadleaf forests', 60127:'Tropical and subtropical moist broadleaf forests', 60128:'Tropical and subtropical moist broadleaf forests', 60129:'Tropical and subtropical moist broadleaf forests', 60130:'Tropical and subtropical moist broadleaf forests', 60131:'Tropical and subtropical moist broadleaf forests', 60132:'Tropical and subtropical moist broadleaf forests', 60133:'Tropical and subtropical moist broadleaf forests', 60134:'Tropical and subtropical moist broadleaf forests', 60135:'Tropical and subtropical moist broadleaf forests', 60136:'Tropical and subtropical moist broadleaf forests', 60137:'Tropical and subtropical moist broadleaf forests', 60138:'Tropical and subtropical moist broadleaf forests', 60139:'Tropical and subtropical moist broadleaf forests', 60140:'Tropical and subtropical moist broadleaf forests', 60141:'Tropical and subtropical moist broadleaf forests', 60142:'Tropical and subtropical moist broadleaf forests', 60143:'Tropical and subtropical moist broadleaf forests', 60144:'Tropical and subtropical moist broadleaf forests', 60145:'Tropical and subtropical moist broadleaf forests', 60146:'Tropical and subtropical moist broadleaf forests', 60147:'Tropical and subtropical moist broadleaf forests', 60148:'Tropical and subtropical moist broadleaf forests', 60149:'Tropical and subtropical moist broadleaf forests', 60150:'Tropical and subtropical moist broadleaf forests', 60151:'Tropical and subtropical moist broadleaf forests', 60152:'Tropical and subtropical moist broadleaf forests', 60153:'Tropical and subtropical moist broadleaf forests', 60154:'Tropical and subtropical moist broadleaf forests', 60155:'Tropical and subtropical moist broadleaf forests', 60156:'Tropical and subtropical moist broadleaf forests', 60157:'Tropical and subtropical moist broadleaf forests', 60158:'Tropical and subtropical moist broadleaf forests', 60159:'Tropical and subtropical moist broadleaf forests', 60160:'Tropical and subtropical moist broadleaf forests', 60161:'Tropical and subtropical moist broadleaf forests', 60162:'Tropical and subtropical moist broadleaf forests', 60163:'Tropical and subtropical moist broadleaf forests', 60164:'Tropical and subtropical moist broadleaf forests', 60165:'Tropical and subtropical moist broadleaf forests', 60166:'Tropical and subtropical moist broadleaf forests', 60167:'Tropical and subtropical moist broadleaf forests', 60168:'Tropical and subtropical moist broadleaf forests', 60169:'Tropical and subtropical moist broadleaf forests', 60170:'Tropical and subtropical moist broadleaf forests', 60171:'Tropical and subtropical moist broadleaf forests', 60172:'Tropical and subtropical moist broadleaf forests', 60173:'Tropical and subtropical moist broadleaf forests', 60174:'Tropical and subtropical moist broadleaf forests', 60175:'Tropical and subtropical moist broadleaf forests', 60176:'Tropical and subtropical moist broadleaf forests', 60177:'Tropical and subtropical moist broadleaf forests', 60178:'Tropical and subtropical moist broadleaf forests', 60179:'Tropical and subtropical moist broadleaf forests', 60180:'Tropical and subtropical moist broadleaf forests', 60181:'Tropical and subtropical moist broadleaf forests', 60182:'Tropical and subtropical moist broadleaf forests', 60201:'Tropical and subtropical dry broadleaf forests', 60202:'Tropical and subtropical dry broadleaf forests', 60204:'Tropical and subtropical dry broadleaf forests', 60205:'Tropical and subtropical dry broadleaf forests', 60206:'Tropical and subtropical dry broadleaf forests', 60207:'Tropical and subtropical dry broadleaf forests', 60209:'Tropical and subtropical dry broadleaf forests', 60210:'tropical and subtropical grasslands, savannas, sh*', 60211:'Tropical and subtropical dry broadleaf forests', 60212:'Tropical and subtropical dry broadleaf forests', 60213:'Tropical and subtropical dry broadleaf forests', 60214:'Tropical and subtropical dry broadleaf forests', 60215:'Tropical and subtropical dry broadleaf forests', 60216:'Tropical and subtropical dry broadleaf forests', 60217:'Tropical and subtropical dry broadleaf forests', 60218:'Tropical and subtropical dry broadleaf forests', 60219:'Tropical and subtropical dry broadleaf forests', 60220:'Tropical and subtropical dry broadleaf forests', 60221:'Tropical and subtropical dry broadleaf forests', 60222:'Tropical and subtropical dry broadleaf forests', 60223:'Tropical and subtropical dry broadleaf forests', 60224:'Tropical and subtropical dry broadleaf forests', 60225:'Tropical and subtropical dry broadleaf forests', 60226:'Tropical and subtropical dry broadleaf forests', 60227:'Tropical and subtropical dry broadleaf forests', 60228:'Tropical and subtropical dry broadleaf forests', 60229:'Tropical and subtropical dry broadleaf forests', 60230:'Tropical and subtropical dry broadleaf forests', 60232:'Tropical and subtropical dry broadleaf forests', 60233:'Tropical and subtropical dry broadleaf forests', 60235:'Tropical and subtropical dry broadleaf forests', 60301:'tropical and subtropical coniferous forests', 60302:'tropical and subtropical coniferous forests', 60303:'tropical and subtropical coniferous forests', 60304:'tropical and subtropical coniferous forests', 60305:'tropical and subtropical coniferous forests', 60306:'tropical and subtropical coniferous forests', 60307:'tropical and subtropical coniferous forests', 60308:'tropical and subtropical coniferous forests', 60309:'tropical and subtropical coniferous forests', 60310:'tropical and subtropical coniferous forests', 60401:'temperate broadleaf and mixed forests', 60402:'temperate broadleaf and mixed forests', 60403:'temperate broadleaf and mixed forests', 60404:'temperate broadleaf and mixed forests', 60702:'tropical and subtropical grasslands, savannas, sh*', 60703:'tropical and subtropical grasslands, savannas, sh*', 60704:'tropical and subtropical grasslands, savannas, sh*', 60705:'tropical and subtropical grasslands, savannas, sh*', 60707:'tropical and subtropical grasslands, savannas, sh*', 60708:'tropical and subtropical grasslands, savannas, sh*', 60709:'tropical and subtropical grasslands, savannas, sh*', 60710:'tropical and subtropical grasslands, savannas, sh*', 60801:'temperate grasslands, savannas, and shrublands', 60802:'temperate grasslands, savannas, and shrublands', 60803:'temperate grasslands, savannas, and shrublands', 60805:'temperate grasslands, savannas, and shrublands', 60902:'flooded grasslands and savannas', 60903:'flooded grasslands and savannas', 60904:'flooded grasslands and savannas', 60905:'flooded grasslands and savannas', 60906:'flooded grasslands and savannas', 60907:'flooded grasslands and savannas', 60908:'flooded grasslands and savannas', 60909:'flooded grasslands and savannas', 61001:'montane grasslands and shrublands', 61002:'montane grasslands and shrublands', 61003:'montane grasslands and shrublands', 61004:'montane grasslands and shrublands', 61005:'montane grasslands and shrublands', 61006:'montane grasslands and shrublands', 61007:'montane grasslands and shrublands', 61008:'montane grasslands and shrublands', 61010:'montane grasslands and shrublands', 61201:'Mediterranean forests, woodlands, and scrub', 61301:'deserts and xeric shrublands', 61303:'deserts and xeric shrublands', 61304:'deserts and xeric shrublands', 61305:'deserts and xeric shrublands', 61306:'deserts and xeric shrublands', 61307:'deserts and xeric shrublands', 61308:'deserts and xeric shrublands', 61309:'deserts and xeric shrublands', 61311:'deserts and xeric shrublands', 61312:'deserts and xeric shrublands', 61313:'deserts and xeric shrublands', 61314:'deserts and xeric shrublands', 61315:'deserts and xeric shrublands', 61316:'deserts and xeric shrublands', 61318:'deserts and xeric shrublands', 61401:'mangroves', 61402:'mangroves', 61403:'mangroves', 61404:'mangroves', 61405:'mangroves', 61406:'mangroves', 61407:'mangroves', 70101:'Tropical and subtropical moist broadleaf forests', 70102:'Tropical and subtropical moist broadleaf forests', 70103:'Tropical and subtropical moist broadleaf forests', 70104:'Tropical and subtropical moist broadleaf forests', 70105:'Tropical and subtropical moist broadleaf forests', 70106:'Tropical and subtropical moist broadleaf forests', 70107:'Tropical and subtropical moist broadleaf forests', 70108:'Tropical and subtropical moist broadleaf forests', 70109:'Tropical and subtropical moist broadleaf forests', 70110:'Tropical and subtropical moist broadleaf forests', 70111:'Tropical and subtropical moist broadleaf forests', 70112:'Tropical and subtropical moist broadleaf forests', 70113:'Tropical and subtropical moist broadleaf forests', 70114:'Tropical and subtropical moist broadleaf forests', 70115:'Tropical and subtropical moist broadleaf forests', 70116:'Tropical and subtropical moist broadleaf forests', 70117:'Tropical and subtropical moist broadleaf forests', 70201:'Tropical and subtropical dry broadleaf forests', 70202:'Tropical and subtropical dry broadleaf forests', 70203:'Tropical and subtropical dry broadleaf forests', 70204:'Tropical and subtropical dry broadleaf forests', 70701:'tropical and subtropical grasslands, savannas, sh*', 70702:'tropical and subtropical grasslands, savannas, sh*', 70703:'tropical and subtropical grasslands, savannas, sh*', 80101:'Tropical and subtropical moist broadleaf forests', 80102:'Tropical and subtropical moist broadleaf forests', 80401:'temperate broadleaf and mixed forests', 80402:'temperate broadleaf and mixed forests', 80403:'temperate broadleaf and mixed forests', 80404:'temperate broadleaf and mixed forests', 80405:'temperate broadleaf and mixed forests', 80406:'temperate broadleaf and mixed forests', 80407:'temperate broadleaf and mixed forests', 80408:'temperate broadleaf and mixed forests', 80409:'temperate broadleaf and mixed forests', 80410:'temperate broadleaf and mixed forests', 80411:'temperate broadleaf and mixed forests', 80412:'temperate broadleaf and mixed forests', 80413:'temperate broadleaf and mixed forests', 80414:'temperate broadleaf and mixed forests', 80415:'temperate broadleaf and mixed forests', 80416:'temperate broadleaf and mixed forests', 80417:'temperate broadleaf and mixed forests', 80418:'temperate broadleaf and mixed forests', 80419:'temperate broadleaf and mixed forests', 80420:'temperate broadleaf and mixed forests', 80421:'temperate broadleaf and mixed forests', 80422:'temperate broadleaf and mixed forests', 80423:'temperate broadleaf and mixed forests', 80424:'temperate broadleaf and mixed forests', 80425:'temperate broadleaf and mixed forests', 80426:'temperate broadleaf and mixed forests', 80427:'temperate broadleaf and mixed forests', 80428:'temperate broadleaf and mixed forests', 80429:'temperate broadleaf and mixed forests', 80430:'temperate broadleaf and mixed forests', 80431:'temperate broadleaf and mixed forests', 80432:'temperate broadleaf and mixed forests', 80433:'temperate broadleaf and mixed forests', 80434:'temperate broadleaf and mixed forests', 80435:'temperate broadleaf and mixed forests', 80436:'temperate broadleaf and mixed forests', 80437:'temperate broadleaf and mixed forests', 80438:'temperate broadleaf and mixed forests', 80439:'temperate broadleaf and mixed forests', 80440:'temperate broadleaf and mixed forests', 80441:'temperate broadleaf and mixed forests', 80442:'temperate broadleaf and mixed forests', 80443:'temperate broadleaf and mixed forests', 80444:'temperate broadleaf and mixed forests', 80445:'temperate broadleaf and mixed forests', 80446:'temperate broadleaf and mixed forests', 80501:'temperate coniferous forests', 80502:'temperate coniferous forests', 80503:'temperate coniferous forests', 80504:'temperate coniferous forests', 80505:'temperate coniferous forests', 80506:'temperate coniferous forests', 80507:'temperate coniferous forests', 80508:'temperate coniferous forests', 80509:'temperate coniferous forests', 80510:'temperate coniferous forests', 80511:'temperate coniferous forests', 80512:'temperate coniferous forests', 80513:'temperate coniferous forests', 80514:'temperate coniferous forests', 80515:'temperate coniferous forests', 80516:'temperate coniferous forests', 80517:'temperate coniferous forests', 80518:'temperate coniferous forests', 80519:'temperate coniferous forests', 80520:'temperate coniferous forests', 80521:'temperate coniferous forests', 80601:'Boreal forests/taiga', 80602:'Boreal forests/taiga', 80603:'Boreal forests/taiga', 80604:'Boreal forests/taiga', 80605:'Boreal forests/taiga', 80606:'Boreal forests/taiga', 80607:'Boreal forests/taiga', 80608:'Boreal forests/taiga', 80609:'Boreal forests/taiga', 80610:'Boreal forests/taiga', 80611:'Boreal forests/taiga', 80801:'temperate grasslands, savannas, and shrublands', 80802:'temperate grasslands, savannas, and shrublands', 80803:'temperate grasslands, savannas, and shrublands', 80804:'temperate grasslands, savannas, and shrublands', 80805:'temperate grasslands, savannas, and shrublands', 80806:'temperate grasslands, savannas, and shrublands', 80807:'temperate grasslands, savannas, and shrublands', 80808:'temperate grasslands, savannas, and shrublands', 80809:'temperate grasslands, savannas, and shrublands', 80810:'temperate grasslands, savannas, and shrublands', 80811:'temperate grasslands, savannas, and shrublands', 80812:'temperate grasslands, savannas, and shrublands', 80813:'temperate grasslands, savannas, and shrublands', 80814:'temperate grasslands, savannas, and shrublands', 80815:'temperate grasslands, savannas, and shrublands', 80816:'temperate grasslands, savannas, and shrublands', 80817:'temperate grasslands, savannas, and shrublands', 80818:'temperate grasslands, savannas, and shrublands', 80901:'flooded grasslands and savannas', 80902:'flooded grasslands and savannas', 80903:'flooded grasslands and savannas', 80904:'flooded grasslands and savannas', 80905:'flooded grasslands and savannas', 80906:'flooded grasslands and savannas', 80907:'flooded grasslands and savannas', 80908:'flooded grasslands and savannas', 81001:'montane grasslands and shrublands', 81002:'montane grasslands and shrublands', 81003:'montane grasslands and shrublands', 81004:'montane grasslands and shrublands', 81005:'montane grasslands and shrublands', 81006:'montane grasslands and shrublands', 81007:'montane grasslands and shrublands', 81008:'montane grasslands and shrublands', 81009:'montane grasslands and shrublands', 81010:'montane grasslands and shrublands', 81011:'montane grasslands and shrublands', 81012:'montane grasslands and shrublands', 81013:'montane grasslands and shrublands', 81014:'montane grasslands and shrublands', 81015:'montane grasslands and shrublands', 81016:'montane grasslands and shrublands', 81017:'montane grasslands and shrublands', 81018:'montane grasslands and shrublands', 81019:'montane grasslands and shrublands', 81020:'montane grasslands and shrublands', 81021:'montane grasslands and shrublands', 81022:'montane grasslands and shrublands', 81101:'tundra', 81102:'tundra', 81103:'tundra', 81104:'tundra', 81105:'tundra', 81106:'tundra', 81107:'tundra', 81108:'tundra', 81109:'tundra', 81110:'tundra', 81111:'tundra', 81112:'tundra', 81113:'tundra', 81114:'tundra', 81201:'Mediterranean forests, woodlands, and scrub', 81202:'Mediterranean forests, woodlands, and scrub', 81203:'Mediterranean forests, woodlands, and scrub', 81204:'Mediterranean forests, woodlands, and scrub', 81205:'Mediterranean forests, woodlands, and scrub', 81206:'Mediterranean forests, woodlands, and scrub', 81207:'Mediterranean forests, woodlands, and scrub', 81208:'Mediterranean forests, woodlands, and scrub', 81209:'Mediterranean forests, woodlands, and scrub', 81210:'Mediterranean forests, woodlands, and scrub', 81211:'Mediterranean forests, woodlands, and scrub', 81212:'Mediterranean forests, woodlands, and scrub', 81213:'Mediterranean forests, woodlands, and scrub', 81214:'Mediterranean forests, woodlands, and scrub', 81215:'Mediterranean forests, woodlands, and scrub', 81216:'Mediterranean forests, woodlands, and scrub', 81217:'Mediterranean forests, woodlands, and scrub', 81218:'Mediterranean forests, woodlands, and scrub', 81219:'Mediterranean forests, woodlands, and scrub', 81220:'Mediterranean forests, woodlands, and scrub', 81221:'Mediterranean forests, woodlands, and scrub', 81222:'Mediterranean forests, woodlands, and scrub', 81301:'deserts and xeric shrublands', 81302:'deserts and xeric shrublands', 81303:'deserts and xeric shrublands', 81304:'deserts and xeric shrublands', 81305:'deserts and xeric shrublands', 81306:'deserts and xeric shrublands', 81307:'deserts and xeric shrublands', 81308:'deserts and xeric shrublands', 81309:'deserts and xeric shrublands', 81310:'deserts and xeric shrublands', 81311:'deserts and xeric shrublands', 81312:'deserts and xeric shrublands', 81313:'deserts and xeric shrublands', 81314:'deserts and xeric shrublands', 81315:'deserts and xeric shrublands', 81316:'deserts and xeric shrublands', 81317:'deserts and xeric shrublands', 81318:'deserts and xeric shrublands', 81319:'deserts and xeric shrublands', 81320:'deserts and xeric shrublands', 81321:'deserts and xeric shrublands', 81322:'deserts and xeric shrublands', 81323:'deserts and xeric shrublands', 81324:'deserts and xeric shrublands', 81325:'deserts and xeric shrublands', 81326:'deserts and xeric shrublands', 81327:'deserts and xeric shrublands', 81328:'deserts and xeric shrublands', 81329:'deserts and xeric shrublands', 81330:'deserts and xeric shrublands', 81331:'deserts and xeric shrublands', 81332:'deserts and xeric shrublands', 81333:'deserts and xeric shrublands'}
    try:
        biome = biomes[ecoid]
    except:
        biome = ''
    return biome

# # Input filenames
src_dir = sys.argv[3]  # '/Users/jasokarl/Documents/JournalMap/JournalMap_geodata/'
tif_aridity = 'aridity/ai_yr.tif' #OK
tif_elevation_old = 'elevation/elevation.tif'
tif_elevation = 'GLOBAL_GIS_DATA/AFRICA_DEM/SRTM_MOSAIC1.tif'
tif_africa_sis_sca = 'GLOBAL_GIS_DATA/AFRICA_SIS_SCA_MOSAIC/AFSIS_SCA.tif'
tif_africa_sis_twi = 'GLOBAL_GIS_DATA/AFRICA_SIS_TWI/Afsis.tif'
tif_gdd = 'growing_degree_days/gdd.tif' #OK
tif_states = 'countries/states.tif'
#tif_countries = 'countries2/countries_8bit.tif'
tif_countries = 'countryrastermap/Countries_Raster.tif'
tif_annual_precip = 'annual_precip/annual_precip.tif'
tif_landcover = 'landcover/landcover_GLCC2.tif'
tif_slope = 'slope/int_slope.tif'
tif_depth = 'soil_depth/depth.tif'
tif_texture = 'soil_texture/soil_texture.tif'
tif_biomes = 'wwf_biomes/wwf.tif'
tif_hwsd = 'soil_texture/hwsd_soil.tif'
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
tif_aspect = 'aspect/ASPECT.tif'
tif_world_k_geiger = 'GLOBAL_LAYER/WorldKGeiger/WorldKGeiger.tif'
tif_fao_lgp = 'GLOBAL_LAYER/FAO_LGP/LGP.tif'
tif_suitability_index_low_input = 'GLOBAL_LAYER/CEREAL_SUITABILITY_INDEX/LOWINPUT_RC/LowInput_rainfedC.tif'
tif_suitability_index_hight_input = 'GLOBAL_LAYER/CEREAL_SUITABILITY_INDEX/HIGHINPUT_C/HighInput_cer.tif'
#COUNTRY TIF File Checking
tif_kenya_slope_percentage = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_slope/Kenya_slope.tif'
tif_kenya_slope_reclassified = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_reclassified_slope/KenyaslopeRe.tif'
tif_kenya_dem = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_dem/kenyademwgs1.tif'
tif_kenya_plane_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_plancurv/kenyaplancurv.tif'
tif_kenya_profile_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_profilecurv/kenyaprofcurv.tif'
tif_kenya_aspect = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_aspect/kenyaAspect.tif'
tif_kenya_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_curvature/kenyacurv.tif'

tif_namibia_slope_percentage = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope/NamSlopewgs.tif'
tif_namibia_slope_reclassified = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope_Reclassified/NamSlopeReclass.tif'
tif_namibia_dem = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_DEM/NamDEMwgs.tif'
tif_namibia_plane_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Plan_Curvature/NAM_curvPLANWGS.tif'
tif_namibia_profile_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Profile_Curvature/NamProfCurvaturewgs.tif'
tif_namibia_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Curvature/NAM_curvWGS.tif'

#WORLD GRID TIF FILE DATA
####DEM-DERIVED
tif_world_grid_dem_derived_dem_sre_3a_p1 = 'WORLD_GRID/DEM_Derived/demsre3a_p1.tif/DEMSRE3a_P1.tif'
tif_world_grid_dem_derived_dem_sre_3a_p2 = 'WORLD_GRID/DEM_Derived/demsre3a_p2.tif/DEMSRE3a_P2.tif'
tif_world_grid_dem_derived_dem_sre_3a_p3 = 'WORLD_GRID/DEM_Derived/demsre3a_p3.tif/DEMSRE3a_P3.tif'
tif_world_grid_dem_derived_dem_sre_3a_p4 = 'WORLD_GRID/DEM_Derived/demsre3a_p4.tif/DEMSRE3a_P4.tif'
tif_world_grid_dem_derived_dem_sre_3a_p5 = 'WORLD_GRID/DEM_Derived/demsre3a_p5.tif/DEMSRE3a_P5.tif'
tif_world_grid_dem_derived_dem_sre_3a_p6 = 'WORLD_GRID/DEM_Derived/demsre3a_p6.tif/DEMSRE3a_P6.tif'
tif_world_grid_dem_derived_dem_sre_3a_p7 = 'WORLD_GRID/DEM_Derived/demsre3a_p7.tif/DEMSRE3a_P7.tif'
tif_world_grid_dem_derived_dem_sre_3a_p8 = 'WORLD_GRID/DEM_Derived/demsre3a_p8.tif/DEMSRE3a_P8.tif'
tif_world_grid_dem_derived_dem_sre_3a_p9 = 'WORLD_GRID/DEM_Derived/demsre3a_p9.tif/DEMSRE3a_P9.tif'
tif_world_grid_dem_derived_dem_sre_3a_p10 = 'WORLD_GRID/DEM_Derived/demsre3a_p10.tif/DEMSRE3a_P10.tif'
tif_world_grid_dem_derived_dem_sre_3a_p11 = 'WORLD_GRID/DEM_Derived/demsre3a_p11.tif/DEMSRE3a_P11.tif'
tif_world_grid_dem_derived_dem_sre_3a_p12 = 'WORLD_GRID/DEM_Derived/demsre3a_p12.tif/DEMSRE3a_P12.tif'
tif_world_grid_dem_derived_dem_sre_3a_p13 = 'WORLD_GRID/DEM_Derived/demsre3a_p13.tif/DEMSRE3a_P13.tif'
tif_world_grid_dem_derived_dem_sre_3a_p14 = 'WORLD_GRID/DEM_Derived/demsre3a_p14.tif/DEMSRE3a_P14.tif'
tif_world_grid_dem_derived_dem_sre_3a_p15 = 'WORLD_GRID/DEM_Derived/demsre3a_p15.tif/DEMSRE3a_P15.tif'
tif_world_grid_dem_derived_dem_sre_3a_p16 = 'WORLD_GRID/DEM_Derived/demsre3a_p16.tif/DEMSRE3a_P16.tif'
tif_world_grid_dem_derived_dem_sre_3a_p17 = 'WORLD_GRID/DEM_Derived/demsre3a_p17.tif/DEMSRE3a_P17.tif'
tif_world_grid_dem_derived_dem_sre_3a_p18 = 'WORLD_GRID/DEM_Derived/demsre3a_p18.tif/DEMSRE3a_P18.tif'
tif_world_grid_dem_derived_dem_sre_3a_p19 = 'WORLD_GRID/DEM_Derived/demsre3a_p13.tif/DEMSRE3a_P19.tif'
tif_world_grid_dem_derived_dem_sre_3a_p20 = 'WORLD_GRID/DEM_Derived/demsre3a_p14.tif/DEMSRE3a_P20.tif'
tif_world_grid_dem_derived_dem_sre_3a_p21 = 'WORLD_GRID/DEM_Derived/demsre3a_p15.tif/DEMSRE3a_P21.tif'
tif_world_grid_dem_derived_dem_sre_3a_p22 = 'WORLD_GRID/DEM_Derived/demsre3a_p16.tif/DEMSRE3a_P22.tif'
tif_world_grid_dem_derived_dem_sre_3a_p23 = 'WORLD_GRID/DEM_Derived/demsre3a_p17.tif/DEMSRE3a_P23.tif'
tif_world_grid_dem_derived_dem_sre_3a_p24 = 'WORLD_GRID/DEM_Derived/demsre3a_p18.tif/DEMSRE3a_P24.tif'
tif_world_grid_dem_derived_inmsre_3 = 'WORLD_GRID/DEM_Derived/inmsre3a.tif/INMSRE3a.tif'
tif_world_grid_dem_derived_inssre_3 = 'WORLD_GRID/DEM_Derived/inssre3a.tif/INSSRE3a.tif'
tif_world_grid_dem_derived_l3pobi_3b = 'WORLD_GRID/DEM_Derived/l3pobi3b.tif/L3POBI3b.tif'
tif_world_grid_dem_derived_opisre_3a = 'WORLD_GRID/DEM_Derived/opisre3a.tif/OPISRE3a.tif'
tif_world_grid_dem_derived_SLPSRT_3a = 'WORLD_GRID/DEM_Derived/SLPSRT3a.tif/SLPSRT3a.tif'
tif_world_grid_dem_derived_twisre_3a = 'WORLD_GRID/DEM_Derived/twisre3a.tif/TWISRE3a.tif'
####Climatic Meteorological 
tif_world_grid_climatic_px1wcl_3a = 'WORLD_GRID/Climatic_Meteorological_Data/px1wcl3a.tif/PX1WCL3a.tif'
tif_world_grid_climatic_px2wcl_3a = 'WORLD_GRID/Climatic_Meteorological_Data/px2wcl3a.tif/PX2WCL3a.tif'
tif_world_grid_climatic_px3wcl_3a = 'WORLD_GRID/Climatic_Meteorological_Data/px3wcl3a.tif/PX3WCL3a.tif'
tif_world_grid_climatic_px4wcl_3a = 'WORLD_GRID/Climatic_Meteorological_Data/px4wcl3a.tif/PX4WCL3a.tif'


####Geological Parent Material
tif_world_grid_geological_material = 'WORLD_GRID/Geological_Parent_Material/geaisg3a.tif/GEAISG3a.tif'
tif_world_grid_population_density_from_5_km = '/WORLD_GRID/Population_Density_from_5.6_km/pdmgpw1a.tif/PDMGPW1a.tif'

####GAEZ
tif_gaez_act2000cer2000CerealProdValPerHA = 'GAEZ_NEW_LAYERS/act2000cer2000CerealProdValPerHA/act2000cer2000CerealProdValPerHA.tif'
tif_gaez_annualprecip1960_1990mm = 'GAEZ_NEW_LAYERS/annualprecip1960-1990mm/annualprecip1960-1990mm.tif'
tif_gaez_Cultivated_Land = 'GAEZ_NEW_LAYERS/Cultivated_Land/Cultivated_Land.tif'
tif_gaez_GAEZThermalzones1961to1990 = 'GAEZ_NEW_LAYERS/GAEZThermalzones1961to1990/GAEZThermalzones1961to1990.tif'
tif_gaez_GlobalSoilFertilityMap = 'GAEZ_NEW_LAYERS/GlobalSoilFertilityMap/GlobalSoilFertilityMap.tif'
tif_gaez_Grassland_woodland = 'GAEZ_NEW_LAYERS/Grassland_woodland/Grassland_woodland.tif'
tif_gaez_irrigatedcultivatedland = 'GAEZ_NEW_LAYERS/irrigatedcultivatedland/irrigatedcultivatedland.tif'
tif_gaez_protected_area_types = 'GAEZ_NEW_LAYERS/protected_area_types/protected_area_types.tif'
tif_gaez_protectedAreasAgriculture = 'GAEZ_NEW_LAYERS/protectedAreasAgriculture/protectedAreasAgriculture.tif'
tif_gaez_RuminantLivestock = 'GAEZ_NEW_LAYERS/RuminantLivestock/RuminantLivestock.tif'
tif_gaez_SoilToxicities = 'GAEZ_NEW_LAYERS/SoilToxicities/SoilToxicities.tif'
tif_gaez_SOILWorkability = 'GAEZ_NEW_LAYERS/SOILWorkability/SOILWorkability.tif'
tif_gaez_TotCropProdValPerHA = 'GAEZ_NEW_LAYERS/TotCropProdValPerHA/TotCropProdValPerHA.tif'


in_locs = sys.argv[1]  # '/Users/jasokarl/Dropbox/JournalMap/TF_XML/loc_parsing.csv'  # In our case, we don't have a shapefile, we have a list of coordinates in a .csv file (even easier...)

outfile = sys.argv[2]  # 'locations.csv'
def run(srcfile,mx,my):
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
    print structval
def main():
    f = open(in_locs, "rb")
    l = UnicodeReader(f)
    l.next()
    
    csvfile = open(outfile, 'wb')
    out = UnicodeWriter(csvfile)
    out.writerow(['doi', 'lat', 'lng', 'HWSD_soil', 'slate_weather', 'topsoil_texture', 'landcover', 'growing_degree_days', 'soil_depth', 'old_elevation', 'new_elevation', 'africa_sis_sca', 'africa_sis_twi' ,'slope', 'precipitation', 'aridity_index', 'country', 'state', 'biome', 'aspect', 'worldkgeiger', 'fao_lgp', 'cereals_suitability_low_input' , 'cereals_suitability_hight_input', 'kenya_slope (%)','kenya_slope_reclassified','kenya_aspect','kenya_plane_curvature','kenya_profile_curvature', 'kenya_dem' , 'kenya_curvature' ,'namibia_slope (%)',
                  'namibia_slope_reclassofied','namibia_plane_curvature','namibia_profile_curvature','namibia_dem','namibia_curvature',
                  'world_grid_dem_derived_3a_p1','world_grid_dem_derived_3a_p2','world_grid_dem_derived_3a_p3','world_grid_dem_derived_3a_p4','world_grid_dem_derived_3a_p5',
                  'world_grid_dem_derived_3a_p6','world_grid_dem_derived_3a_p7','world_grid_dem_derived_3a_p8','world_grid_dem_derived_3a_p9','world_grid_dem_derived_3a_p10',
                  'world_grid_dem_derived_3a_p11','world_grid_dem_derived_3a_p12','world_grid_dem_derived_3a_p13','world_grid_dem_derived_3a_p14','world_grid_dem_derived_3a_p15',
                  'world_grid_dem_derived_3a_p16','world_grid_dem_derived_3a_p17','world_grid_dem_derived_3a_p18','world_grid_dem_derived_3a_p19','world_grid_dem_derived_3a_p20',
                  'world_grid_dem_derived_3a_p21','world_grid_dem_derived_3a_p22','world_grid_dem_derived_3a_p23','world_grid_dem_derived_3a_p24', 'world_grid_dem_derived_inmsre_3', 
                  'world_grid_dem_derived_inssre_3','world_grid_dem_derived_l3pobi_3', 'world_grid_dem_derived_opisre_3', 'world_grid_dem_derived_SLPSRT_3', 'world_grid_dem_derived_twisre_3',  
                  'world_grid_geological_material','world_grid_population_density','world_grid_climatic_px1wcl','world_grid_climatic_px2wcl','world_grid_climatic_px3wcl','world_grid_climatic_px4wcl',
                  'gaez_act2000cer2000CerealProdValPerHA','gaez_annualprecip1960_1990mm','gaez_Cultivated_Land','gaez_GAEZThermalzones1961to1990','gaez_GlobalSoilFertilityMap','gaez_Grassland_woodland',
                  'gaez_irrigatedcultivatedland','gaez_protected_area_types','gaez_protectedAreasAgriculture','gaez_RuminantLivestock','gaez_SoilToxicities','gaez_SOILWorkability','gaez_TotCropProdValPerHA'])
    try:
       for row in l:
           doi = row[0]
           mx, my = float(row[2]), float(row[1])  # coord in map units
           print "================================================="
           print "DOI : %s | X = %s | Y = %s" % (doi,str(mx),str(my))

           aridity = getRasterValue(src_dir + tif_aridity, mx, my)    
           print "aridity=" + str(aridity)
           
           old_ele = getRasterValue(src_dir+tif_elevation_old,mx, my)
           print "old_elevation="+str(old_ele)
           
           new_ele = getRasterValue(src_dir + tif_elevation, mx, my)
           print "new_elevation=" + str(new_ele)
           
           africa_sis_sca = getRasterValue_ThanhNH_Float(src_dir + tif_africa_sis_sca, mx, my)
           print "Africa Sis SCA =" + str(africa_sis_sca)
           
           africa_sis_twi = getRasterValue_ThanhNH_Float(src_dir + tif_africa_sis_twi, mx, my)
           print "Africa Sis TWI =" + str(africa_sis_twi)
           #new_ele = "123"
           
           # states = getRasterValue(src_dir+tif_states, mx, my)
           # state = lookupState(states)
           # print "state="+state
           state = "Hawaii"
    
           country = getRasterValue_ThanhNH(src_dir+tif_countries, mx, my)
           #countries = lookupCountry(countries)
           print "countries = "+ str(country)
           #countries = "USA"
    
           gdd = getRasterValue(src_dir + tif_gdd, mx, my)
           print "gdd=" + str(gdd)
    
           annual_precip = getRasterValue(src_dir + tif_annual_precip, mx, my)
           print "annual precip=" + str(annual_precip)
    
           landcover = getRasterValue(src_dir+tif_landcover, mx, my)
           print "landcover="+str(landcover)
    
           slope = getRasterValue(src_dir+tif_slope, mx, my)
           print "slope="+str(slope)

           depth = getRasterValue(src_dir+tif_depth, mx, my)
           print "depth="+str(depth)
    
           texture = getRasterValue(src_dir+tif_texture, mx, my)
           print "texture="+str(texture)
           
           slate_weather = getRasterValue_ThanhNH(src_dir + tif_slate_weather, mx,my)
           print "Slate_Weather = " + str(slate_weather)
    
           hwsd_soil = getRasterValue(src_dir + tif_hwsd, mx, my)
           print "HWSD Soil ="+str(hwsd_soil)
           #biomes = getRasterValue(src_dir+tif_biomes, mx, my)
           #biome = lookupBiome(biomes)
           #print "biome="+str(biomes)+", "+biome
           biome = "rock and ice"
           
           aspect = getRasterValue(src_dir + tif_aspect, mx, my)
           print "Aspect = " + str(aspect)
           print "------------------------------------------------------------------------------"
           world_k_geiger = getRasterValue_ThanhNH(src_dir + tif_world_k_geiger, mx, my)
           print "GLOBAL LAYER - Koppen-Geiger Climate zones = " + str(world_k_geiger)
           
           fao_lgp = getRasterValue_ThanhNH(src_dir + tif_fao_lgp, mx, my)
           print "GLOBAL LAYER - FAO LGP - Length of Growing Period = " + str(fao_lgp)
           
           cereals_suitability_index_low_input = getRasterValue_ThanhNH(src_dir + tif_suitability_index_low_input, mx, my)
           print "GLOBAL LAYER - Cereals suitability for LOW input = " + str(cereals_suitability_index_low_input)
           
           cereals_suitability_index_hight_input = getRasterValue_ThanhNH(src_dir + tif_suitability_index_hight_input, mx, my)
           print "GLOBAL LAYER - Cereals suitability for HIGHT input = " + str(cereals_suitability_index_hight_input)
           
           print "------------------------------------------------------------------------------"
            
           kenya_slope_percent = getRasterValue_ThanhNH_Float(src_dir + tif_kenya_slope_percentage,mx,my)
           print "COUNTRY LAYER - Kenya - Slope (%) = " + str(kenya_slope_percent)
           
           kenya_slope_reclassified = getRasterValue_ThanhNH_Float(src_dir + tif_kenya_slope_reclassified,mx,my)
           print "COUNTRY LAYER - Kenya - Reclassified = " + str(kenya_slope_reclassified)
           
           kenya_aspect = getRasterValue_ThanhNH_Float(src_dir + tif_kenya_aspect,mx,my)
           print "COUNTRY LAYER - Kenya - Aspect = " + str(kenya_aspect)
           
           kenya_plane_curvature =  getRasterValue_ThanhNH_Float(src_dir + tif_kenya_plane_curvature,mx,my)
           print "COUNTRY LAYER - Kenya - Plan Curvature = " + str(kenya_plane_curvature)

           kenya_profile_curvature =  getRasterValue_ThanhNH_Float(src_dir + tif_kenya_profile_curvature,mx,my)
           print "COUNTRY LAYER - Kenya - Profile Curvature = " + str(kenya_profile_curvature)
           
           kenya_dem =  getRasterValue_ThanhNH(src_dir + tif_kenya_dem,mx,my)
           print "COUNTRY LAYER - Kenya - Kenya Dem = " + str(kenya_dem)
           
           kenya_curvature =  getRasterValue_ThanhNH_Float(src_dir + tif_kenya_curvature,mx,my)
           print "COUNTRY LAYER - Kenya - Kenya Curvature = " + str(kenya_curvature)
           
           print "------------------------------------------------------------------------------"
           
           namibia_slope_percent = getRasterValue_ThanhNH_Float(src_dir + tif_namibia_slope_percentage,mx,my)
           print "COUNTRY LAYER - Namibia - Slope (%) = " + str(namibia_slope_percent)
           #namibia_slope_percent = -1
           
           namibia_slope_class = getRasterValue_ThanhNH_Float(src_dir + tif_namibia_slope_reclassified,mx,my)
           print "COUNTRY LAYER - Namibia - Slope class = " + str(namibia_slope_class)
           #namibia_slope_class = -1
           
           namibia_dem = getRasterValue_ThanhNH_Float(src_dir + tif_namibia_dem,mx,my)
           print "COUNTRY LAYER - Namibia - DEM = " + str(namibia_dem)
           
           
           namibia_curvature = getRasterValue_ThanhNH_Float(src_dir + tif_namibia_curvature,mx,my)
           print "COUNTRY LAYER - Namibia - DEM = " + str(namibia_curvature)
           
           namibia_plane_curvature =  getRasterValue_ThanhNH_Float(src_dir + tif_namibia_plane_curvature,mx,my)
           #namibia_plane_curvature= -1
           print "COUNTRY LAYER - Namibia - Plan Curvature = " + str(namibia_plane_curvature)
           

           namibia_profile_curvature =  getRasterValue_ThanhNH_Float(src_dir + tif_namibia_profile_curvature,mx,my)
           #namibia_profile_curvature = -1
           print "COUNTRY LAYER - Namibia - Profile Curvature = " + str(namibia_profile_curvature)
           
           print "------------------------------------------------------------------------------"
           world_grid_dem_derived_3a_p1 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p1, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P1 : " + str(world_grid_dem_derived_3a_p1)
           world_grid_dem_derived_3a_p2 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p2, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P2 : " + str(world_grid_dem_derived_3a_p2)
           world_grid_dem_derived_3a_p3 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p3, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P3 : " + str(world_grid_dem_derived_3a_p3)
           world_grid_dem_derived_3a_p4 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p4, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P4 : " + str(world_grid_dem_derived_3a_p4)
           world_grid_dem_derived_3a_p5 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p5, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P5 : " + str(world_grid_dem_derived_3a_p5)
           world_grid_dem_derived_3a_p6 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p6, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P6 : " + str(world_grid_dem_derived_3a_p6)
           world_grid_dem_derived_3a_p7 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p7, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P7 : " + str(world_grid_dem_derived_3a_p7)
           world_grid_dem_derived_3a_p8 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p8, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P8 : " + str(world_grid_dem_derived_3a_p8)
           world_grid_dem_derived_3a_p9 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p9, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P9 : " + str(world_grid_dem_derived_3a_p9)
           world_grid_dem_derived_3a_p10 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p10, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P10 : " + str(world_grid_dem_derived_3a_p10)
           world_grid_dem_derived_3a_p11 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p11, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P11 : " + str(world_grid_dem_derived_3a_p11)
           world_grid_dem_derived_3a_p12 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p12, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P12 : " + str(world_grid_dem_derived_3a_p12)
           world_grid_dem_derived_3a_p13 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p13, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P13 : " + str(world_grid_dem_derived_3a_p13)
           world_grid_dem_derived_3a_p14 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p14, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P14 : " + str(world_grid_dem_derived_3a_p14)
           world_grid_dem_derived_3a_p15 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p15, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P15 : " + str(world_grid_dem_derived_3a_p15)
           world_grid_dem_derived_3a_p16 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p16, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P16 : " + str(world_grid_dem_derived_3a_p16)
           world_grid_dem_derived_3a_p17 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p17, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P17 : " + str(world_grid_dem_derived_3a_p17)
           world_grid_dem_derived_3a_p18 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p18, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P18 : " + str(world_grid_dem_derived_3a_p18)
           world_grid_dem_derived_3a_p19 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p19, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P19 : " + str(world_grid_dem_derived_3a_p19)
           world_grid_dem_derived_3a_p20 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p20, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P20 : " + str(world_grid_dem_derived_3a_p20)
           world_grid_dem_derived_3a_p21 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p21, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P21 : " + str(world_grid_dem_derived_3a_p21)
           world_grid_dem_derived_3a_p22 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p22, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P22 : " + str(world_grid_dem_derived_3a_p22)
           world_grid_dem_derived_3a_p23 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p23, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P23 : " + str(world_grid_dem_derived_3a_p23)
           world_grid_dem_derived_3a_p24 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_dem_sre_3a_p24, mx, my) 
           print "WORLD-GRID-Dem Derived-3a-P24 : " + str(world_grid_dem_derived_3a_p24)
           world_grid_dem_derived_inmsre_3 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_inmsre_3, mx, my) 
           print "WORLD-GRID-Dem Derived-INMSRE-3a : " + str(world_grid_dem_derived_inmsre_3)
           world_grid_dem_derived_inssre_3 = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_inssre_3, mx, my) 
           print "WORLD-GRID-Dem Derived-INSSRE-3a : " + str(world_grid_dem_derived_inssre_3)
           world_grid_dem_derived_l3pobi_3b = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_l3pobi_3b, mx, my) 
           print "WORLD-GRID-Dem Derived-L3POPI-3b : " + str(world_grid_dem_derived_l3pobi_3b)
           world_grid_dem_derived_opisre_3a = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_opisre_3a, mx, my) 
           print "WORLD-GRID-Dem Derived-OPISRE-3a : " + str(world_grid_dem_derived_opisre_3a)
           world_grid_dem_derived_slpsrt_3a = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_SLPSRT_3a, mx, my) 
           print "WORLD-GRID-Dem Derived-SLPSRT-3a : " + str(world_grid_dem_derived_slpsrt_3a)
           world_grid_dem_derived_twisre_3a = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_dem_derived_twisre_3a, mx, my) 
           print "WORLD-GRID-Dem Derived-TWISRE-3a : " + str(world_grid_dem_derived_twisre_3a)
           print "------------------------------------------------------------------------------"
           world_grid_geological_material = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_geological_material, mx, my)
           print "WORLD-GRID-Geological-Material : " + str(world_grid_geological_material)
           
           world_grid_population_density = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_population_density_from_5_km, mx, my)
           print "WORLD-GRID-Population-Density-from 5.6 km : " + str(world_grid_population_density)
           print "------------------------------------------------------------------------------"
           world_grid_climatic_px1wcl = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_climatic_px1wcl_3a, mx, my)
           print "WORLD-GRID-Climatic-PX1WCL : " + str(world_grid_climatic_px1wcl)
           world_grid_climatic_px2wcl = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_climatic_px2wcl_3a, mx, my)
           print "WORLD-GRID-Climatic-PX2WCL : " + str(world_grid_climatic_px2wcl)
           world_grid_climatic_px3wcl = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_climatic_px3wcl_3a, mx, my)
           print "WORLD-GRID-Climatic-PX3WCL : " + str(world_grid_climatic_px3wcl)
           world_grid_climatic_px4wcl = getRasterValue_ThanhNH_Float(src_dir + tif_world_grid_climatic_px4wcl_3a, mx, my)
           print "WORLD-GRID-Climatic-PX4WCL : " + str(world_grid_climatic_px4wcl)
           print "------------------------------------------------------------------------------"
           #GAEZ
           gaez_act2000cer2000CerealProdValPerHA = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_act2000cer2000CerealProdValPerHA,mx,my)
           print "gaez_act2000cer2000CerealProdValPerHA : " + str(gaez_act2000cer2000CerealProdValPerHA)
           gaez_annualprecip1960_1990mm = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_annualprecip1960_1990mm,mx,my)
           print "gaez_annualprecip1960_1990mm : " + str(gaez_annualprecip1960_1990mm)
           gaez_Cultivated_Land = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_Cultivated_Land,mx,my)
           print "gaez_Cultivated_Land : " + str(gaez_Cultivated_Land)
           gaez_GAEZThermalzones1961to1990 = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_GAEZThermalzones1961to1990,mx,my)
           print "gaez_GAEZThermalzones1961to1990 : " + str(gaez_GAEZThermalzones1961to1990)
           gaez_GlobalSoilFertilityMap = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_GlobalSoilFertilityMap,mx,my)
           print "gaez_GlobalSoilFertilityMap : " + str(gaez_GlobalSoilFertilityMap)
           gaez_Grassland_woodland = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_Grassland_woodland,mx,my)
           print "gaez_Grassland_woodland : " + str(gaez_Grassland_woodland)
           gaez_irrigatedcultivatedland = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_irrigatedcultivatedland,mx,my)
           print "gaez_irrigatedcultivatedland : " + str(gaez_irrigatedcultivatedland)
           gaez_protected_area_types = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_protected_area_types,mx,my)
           print "gaez_protected_area_types : " + str(gaez_protected_area_types)
           gaez_protectedAreasAgriculture = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_protectedAreasAgriculture,mx,my)
           print "gaez_protectedAreasAgriculture : " + str(gaez_protectedAreasAgriculture)
           gaez_RuminantLivestock = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_RuminantLivestock,mx,my)
           print "gaez_RuminantLivestock : " + str(gaez_RuminantLivestock)
           gaez_SoilToxicities = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_SoilToxicities,mx,my)
           print "gaez_SoilToxicities : " + str(gaez_SoilToxicities)
           gaez_SOILWorkability = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_SOILWorkability,mx,my)
           print "gaez_SOILWorkability : " + str(gaez_SOILWorkability)
           gaez_TotCropProdValPerHA = getRasterValue_ThanhNH_Float(src_dir + tif_gaez_TotCropProdValPerHA,mx,my)
           print "gaez_TotCropProdValPerHA : " + str(gaez_TotCropProdValPerHA)
           
           out.writerow([doi, str(my), str(mx), str(hwsd_soil), str(slate_weather), str(texture), str(landcover), str(gdd), str(depth), str(old_ele), str(new_ele), str(africa_sis_sca), 
                         str(africa_sis_twi) , str(slope), str(annual_precip), str(aridity), str(country), state, biome, str(aspect), str(world_k_geiger), str(fao_lgp), 
                         str(cereals_suitability_index_low_input), str(cereals_suitability_index_hight_input),str(kenya_slope_percent), str(kenya_slope_reclassified) ,
                         str(kenya_aspect),str(kenya_plane_curvature),str(kenya_profile_curvature),str(kenya_dem),str(kenya_curvature),
                         str(namibia_slope_percent),str(namibia_slope_class),str(namibia_plane_curvature),str(namibia_profile_curvature),str(namibia_dem),
                         str(namibia_curvature), str(world_grid_dem_derived_3a_p1), str(world_grid_dem_derived_3a_p2), str(world_grid_dem_derived_3a_p3), str(world_grid_dem_derived_3a_p4), 
                         str(world_grid_dem_derived_3a_p5),str(world_grid_dem_derived_3a_p6),str(world_grid_dem_derived_3a_p7),str(world_grid_dem_derived_3a_p8),
                         str(world_grid_dem_derived_3a_p9),str(world_grid_dem_derived_3a_p10),str(world_grid_dem_derived_3a_p11),str(world_grid_dem_derived_3a_p12),str(world_grid_dem_derived_3a_p13),
                         str(world_grid_dem_derived_3a_p14),str(world_grid_dem_derived_3a_p15),str(world_grid_dem_derived_3a_p16),str(world_grid_dem_derived_3a_p17),str(world_grid_dem_derived_3a_p18),
                         str(world_grid_dem_derived_3a_p19),str(world_grid_dem_derived_3a_p20),str(world_grid_dem_derived_3a_p21),str(world_grid_dem_derived_3a_p22),str(world_grid_dem_derived_3a_p23),
                         str(world_grid_dem_derived_3a_p24),str(world_grid_dem_derived_inmsre_3),str(world_grid_dem_derived_inssre_3),str(world_grid_dem_derived_l3pobi_3b),str(world_grid_dem_derived_opisre_3a), 
                         str(world_grid_dem_derived_slpsrt_3a),str(world_grid_dem_derived_twisre_3a),
                         str(world_grid_geological_material), str(world_grid_population_density),str(world_grid_climatic_px1wcl),str(world_grid_climatic_px2wcl),str(world_grid_climatic_px3wcl),str(world_grid_climatic_px4wcl),
                         str(gaez_act2000cer2000CerealProdValPerHA),str(gaez_annualprecip1960_1990mm),str(gaez_Cultivated_Land),str(gaez_GAEZThermalzones1961to1990),str(gaez_GlobalSoilFertilityMap),
                         str(gaez_Grassland_woodland),str(gaez_irrigatedcultivatedland),str(gaez_protected_area_types),str(gaez_protectedAreasAgriculture),str(gaez_RuminantLivestock),
                         str(gaez_SoilToxicities),str(gaez_SOILWorkability),str(gaez_TotCropProdValPerHA)])
    except Exception, err:
           print err
           print 1
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
