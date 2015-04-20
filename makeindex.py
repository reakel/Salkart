#-*- coding:utf-8 -*-
#Lager html-skjelett for salkart fra xhtml-regneark.
#Erik Roede, 2014

import sys
import sqlite3 as lite
from bs4 import BeautifulSoup

def makeSal(sal):
    html=[]
    html.append("<table class=\"kart\" id=\"%s\">\n<caption class=\"salcaption\">%s</caption>" %(sal,sal))
    innfil=open("input/%s.html" %sal)
    innsoup=BeautifulSoup(innfil.read())
    table=innsoup.find("table")
    rows=table.findChildren("tr")
    for row in rows:
        html.append("<tr>\n")
        cells=row.findChildren("td")
        for cell in cells:
            data=cell.string
            if data.isdigit():
                #cellen er maskin
                mnr=data
                html.append("<td class =\"maskin\" id=\"%s\"></td>" %mnr)
            elif data =="doer":
                #cellen er dør
                html.append("<td class=\"doer\"></td>")
            elif data=="printer":
                #cellen er printer
                html.append("<td class=\"printer\" id=\"%sprinter\"><td>" %sal)
            else:
                #cellen er tom
                html.append("<td class=\"tom\"></td>")
        html.append("</tr>\n")
    html.append("</table>\n")
    html=''.join(html)
    return html
def makeToc(saler):
    html=[]
    for sal in saler:
        html.append("<a class=\"toclink\" id=\"toc%s\" href=\"#%s\">%s</a><span id=\"%stocspan\"></span><br>" %(sal,sal,sal,sal))
    html=''.join(html)
    return html
def makeHtml(saler):
    html=[]
    html.append("<!doctype html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<title>Salkart</title>\n<link rel=\"stylesheet\" href=\"kartStyle2.css\">")
    html.append("<script type=\"text/javascript\" src=\"jquery.js\"></script>\n<script type=\"text/javascript\" src=\"jquery.simpletip-1.3.1.js\"></script>")
    #alt annet i header her
    html.append("</head>\n<body>\n")
    #her begynner body
    html.append("<h1>Salkart</h1>\n")
    html.append("<button type='button'>Ping (kommer)</button>")
    #ToC:
    html.append("<div id=\"testing\"></div>\n")
    tocHtml=makeToc(saler)
    html.append(tocHtml)
    
    html.append("Forklaring: <table class='kart'><tr><td class='maskin'>Ok</td><td>Maskinen pinger</td></tr> <tr><td class='maskin' feil='av'>Av</td><td>Maskinen pinger ikke</td></tr> <tr><td class='maskin' feil='ureg'>Uregistrert</td><td>Maskinen er ikke registrert</td></tr><tr><td class='maskin' feil = 'annet'>Annet</td><td>Maskinen er merket med kommentarer, trykk for aa lese</td></tr></table>")
    for sal in saler:
        salHtml=makeSal(sal)
        html.append(salHtml)
    
    html.append("<script type=\"text/javascript\" src=\"kartScript.js\"></script>\n")
    html.append("<div class=\"pop\"></div>")
    html.append("</body>\n</html>")
    return html

def findSaler():
    dbcon=lite.connect('/usr/local/share/innloggingslogging/innlogging.db')
    dbcon.text_factory=str
    cur = dbcon.cursor()
    cmd = "SELECT * FROM datasaler"
    cur.execute(cmd)
    a=cur.fetchall()
    saler = []
    for line in a:
        saler.append(line[0])
        #print line[0]
    return saler
    
fil=open("www/index.php","w")
saler=findSaler();
html=makeHtml(saler)
fil.write("".join(html).encode("utf-8","strip"))
fil.close()
fil2=open("/var/www/salstat2/kart.php","w")
fil2.write("".join(html).encode("utf-8","strip"))
fil2.close()
