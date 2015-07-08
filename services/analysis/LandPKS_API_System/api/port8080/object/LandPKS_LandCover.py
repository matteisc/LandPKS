# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"


BARE = "Bare"
TREES = "Trees"
SHRUBS = "Shrubs"
SUB_SHRUBS = "Sub-shrubs"
PER_GRASS = "Perennial grasses"
ANNUAL = "Annuals"
HERB_LITTER = "Herb litter"
WOOD_LITTER = "Wood litter"
ROCK = "Rock"


STICK_SEGMENT_SET = set([BARE.upper(),TREES.upper(),SHRUBS.upper(),SUB_SHRUBS.upper(),PER_GRASS.upper(),ANNUAL.upper(),HERB_LITTER.upper(),WOOD_LITTER.upper(),ROCK.upper(),''])

CANOPY_HEIGHT_SET = set(['<10cm'.upper(),'10-50cm'.upper(),'50cm-1m'.upper(),'1-2m'.upper(),'2-3m'.upper(),'>3m'.upper()])

LAND_COVER_DISPLAY_SET = set(['SUMMARY'])
