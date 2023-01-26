import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from io import StringIO
from lxml import etree
import unicodedata

from utils import sanitize_xml

def sanitize_xml(xml):
    svg_string = unicodedata.normalize('NFKD', xml.getvalue()).encode('utf-8', 'ignore')
    doc = etree.fromstring(svg_string)
    
    for element in doc.iter("{http://www.w3.org/2000/svg}metadata"):
        doc.remove(element)
    
    svg_string = etree.tostring(doc, encoding='unicode')
        
    return svg_string

def save_svg(svg_string, filename):
    svg_string = sanitize_xml(svg_string)

    # If saving to file
    # with open(filename, "w") as f:
    #     f.write(svg_string)

    return svg_string
    
def plot(leads):

    leads = np.array(leads)
    
    lead_labels = ["I", 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    
    rows = 12
    sample_rate = 500
    step = 1.0/sample_rate

    cm = 1/2.54
    height = (3*cm)* rows
    width = 27.5*cm
    fig, ax = plt.subplots(figsize=(width,height))
    studies = 5500
    duration = studies*step

    x_max = 11
    x_min = 0
    y_max = 1.5
    y_min = y_max - (y_max*(rows*2))

    ax.set_xticks(np.arange(x_min,x_max,0.2))
    ax.set_yticks(np.arange(y_min,y_max,0.5))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.tick_params(axis=u'both', which=u'both',length=0)

    ax.minorticks_on()
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))

    ax.grid(which='major', linestyle='-', linewidth='0.5', color="#FF2B2B", alpha=1)
    ax.grid(which='minor', linestyle='-', linewidth='0.5', color="#FFAFAF", alpha=0.2)

    for lead in range(len(leads)):
        offset = -lead*3
        ax.text(0.25, offset, lead_labels[lead], fontsize=8)
        ax.plot(leads[lead][0] ,leads[lead][1] + offset, linewidth=1, color="black")
    
    temp = StringIO()

    plt.savefig("./plot.svg", bbox_inches='tight', format='svg', dpi=1200, pad_inches=0, facecolor="None", edgecolor="red", transparent=False)

    plt.close()

    return save_svg(temp, "./plot.svg")